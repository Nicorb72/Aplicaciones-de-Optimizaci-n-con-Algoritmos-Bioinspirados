"""Vista HTML sin dependencias del formato Markdown que genera comparison.py.

No es un conversor Markdown general: reconoce títulos, tablas y párrafos del
informe y muestra sus enlaces PNG/GIF como figuras. Conserva los datos originales.
"""
from html import escape
from pathlib import Path
import re
from urllib.parse import quote


STYLE = """
:root { color-scheme: light; --ink:#493444; --rose:#a63866; --line:#ead6df; }
* { box-sizing:border-box; }
body { margin:0; color:var(--ink); background:#fff8f3; font:16px/1.7 system-ui,sans-serif; }
header,main,footer { max-width:1250px; margin:auto; padding:28px 5%; }
header { padding-top:55px; }
.eyebrow { text-transform:uppercase; letter-spacing:.17em; font-size:12px; color:var(--rose); }
h1 { font:italic 46px/1.2 Georgia,serif; color:var(--rose); margin:16px 0; }
h2 { font:28px/1.3 Georgia,serif; margin-top:48px; color:var(--rose); }
a { color:#873f69; text-underline-offset:3px; }
nav { display:flex; flex-wrap:wrap; gap:16px; margin:20px 0; }
.cards { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
.card { background:#f4e9f5; border:1px solid var(--line); border-radius:18px; padding:20px; }
.card strong { display:block; font:32px Georgia,serif; }
.notice { padding:18px 22px; border-left:4px solid var(--rose); background:#fce9ef; border-radius:0 12px 12px 0; }
.table-wrap { overflow-x:auto; border:1px solid var(--line); border-radius:14px; }
table { width:100%; border-collapse:collapse; font-size:14px; background:white; white-space:nowrap; font-variant-numeric:tabular-nums; }
th { background:#f3dce8; text-align:left; }
th,td { padding:12px 14px; border-bottom:1px solid var(--line); }
tr:nth-child(even) { background:#fcf7fa; }
figure { background:white; margin:24px 0; padding:18px; border:1px solid var(--line); border-radius:18px; break-inside:avoid; }
figure img { display:block; max-width:100%; height:auto; max-height:680px; margin:auto; }
figcaption { font-size:14px; margin-top:12px; }
code { background:#f3e8ee; border-radius:4px; padding:2px 5px; overflow-wrap:anywhere; }
footer { border-top:1px solid var(--line); font-size:14px; }
@media(max-width:650px) { h1 {font-size:34px} .cards {grid-template-columns:1fr} }
@media print { body {background:white;font-size:11px} nav {display:none} header,main,footer {padding:8px} h2 {break-after:avoid} .table-wrap {overflow:visible} th,td {padding:5px;font-size:9px} }
"""


def inline(text):
    """Escapa primero el texto; convierte únicamente el formato usado aquí."""
    text = escape(text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)


def write_html_report(markdown, rows, path, dataset):
    path = Path(path)
    blocks = []
    lines = markdown.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line or line.startswith('# '):
            continue
        if line.startswith('## '):
            title = line[3:]
            anchor = 'figuras' if title == 'Figuras y animaciones' else f'section-{i}'
            blocks.append(f'<h2 id="{anchor}">{inline(title)}</h2>')
        elif line.startswith('|'):
            table = [line]
            while i < len(lines) and lines[i].strip().startswith('|'):
                table.append(lines[i].strip())
                i += 1
            header = ''.join(f'<th scope="col">{inline(v.strip())}</th>' for v in table[0].strip('|').split('|'))
            body = ''.join('<tr>' + ''.join(f'<td>{inline(v.strip())}</td>' for v in row.strip('|').split('|')) + '</tr>' for row in table[2:])
            blocks.append(f'<div class="table-wrap"><table><thead><tr>{header}</tr></thead><tbody>{body}</tbody></table></div>')
        else:
            picture = re.search(r'\[([^\]]+)\]\(([^)]+\.(?:png|gif))\)', line)
            if picture:
                label, url = picture.groups()
                source = escape(quote(url, safe='/._-'), quote=True)
                blocks.append(f'<figure><a href="{source}"><img loading="lazy" src="{source}" alt="{escape(label)}"></a><figcaption>{inline(line)}</figcaption></figure>')
            else:
                blocks.append(f'<p>{inline(line)}</p>')
    runs = sum(row['summary']['runs'] for row in rows)
    thresholds = ', '.join(f"{v:g}" for v in sorted({r['config']['success_threshold'] for r in rows}))
    budgets = '; '.join(f"{r['config']['function']} {r['config']['dimension']}D: {r['config']['parameters']['iterations']} iteraciones" for r in rows if r['config']['method'] == 'gd')
    demo = 'demo' in dataset.lower()
    note = ('Demostración con presupuesto reducido. Sirve para mostrar el funcionamiento; las conclusiones de la entrega deben usar el experimento principal.' if demo else 'Resultados de la configuración guardada. Consulta los parámetros y límites de esta comparación antes de interpretar las tasas de éxito.')
    content = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Parte 1 · {escape(dataset)} · Resultados</title><style>{STYLE}</style></head>
<body><header><div class="eyebrow">Cuaderno de optimización · {escape(dataset)}</div>
<h1>Pequeños pasos, grandes paisajes</h1><p>Parte 1 · Rosenbrock y Rastrigin · GD, PSO, evolutivo y DE</p>
<nav aria-label="Informe"><a href="#resultados">Leer resultados</a><a href="#figuras">Ver gráficas y GIF</a><a href="comparison.csv">Tabla CSV</a><a href="comparison.json">Parámetros y datos</a><a href="environment.json">Entorno</a><a href="report.md">Markdown</a></nav>
<div class="cards"><div class="card"><strong>{runs}</strong>corridas guardadas</div><div class="card"><strong>{len(rows)}</strong>configuraciones</div><div class="card"><strong>{escape(thresholds)}</strong>umbral(es) de éxito</div></div>
<p class="notice">{note}</p><p><strong>Presupuesto GD:</strong> {escape(budgets) or 'No incluido en esta selección'}.</p></header>
<main id="resultados">{''.join(blocks)}</main>
<footer>Fuente: elaboración propia a partir de las corridas guardadas. Abre este archivo en el navegador sin conexión. Para PDF: Ctrl+P; los GIF quedan estáticos al imprimir. Conserva la carpeta de resultados para mantener las imágenes.</footer></body></html>
'''
    path.write_text(content, encoding='utf-8')
