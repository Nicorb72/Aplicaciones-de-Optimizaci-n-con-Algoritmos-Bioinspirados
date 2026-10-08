"""Tablas y discusión trazables a los resultados guardados."""
import csv
from importlib.metadata import distributions
import json
import os
from pathlib import Path
import sys

from .html_report import write_html_report


def write_comparison(rows, output_dir, artifacts_dir, include_figures=True):
    output_dir, artifacts_dir = Path(output_dir), Path(artifacts_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "comparison.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    environment = {"python": sys.version, "packages": {d.metadata["Name"]: d.version for d in distributions()}}
    (output_dir / "environment.json").write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8")
    fields = ["function", "method", "dimension", "runs", "mean_value", "std_value", "best_value", "worst_value",
              "success_rate", "excluded_runs", "mean_function_evaluations", "mean_gradient_evaluations", "mean_equivalent_evaluations"]
    with (output_dir / "comparison.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            data = dict(row["config"], **row["summary"])
            writer.writerow({key: data[key] for key in fields})
    def number(value):
        return "N/D" if value is None else f"{value:.6g}"
    lines = ["# Parte 1: comparación de costos y resultados", "",
             "Fuente de las tablas y figuras: elaboración propia. Este informe se genera desde las corridas, no desde números escritos a mano.", "",
             "## Metodología y alcance", "",
             "Cada configuración y su umbral están conservados en `comparison.json`; las versiones ejecutadas, en `environment.json`. "
             "Las semillas son `seed + i`, para i desde 0 hasta runs−1. El éxito exige terminar con valor finito y f ≤ umbral. "
             "La desviación estándar es muestral (ddof=1). Media, desviación, mejor y peor excluyen divergencias; "
             "la tasa de éxito y los promedios de costos incluyen TODAS las corridas. Una divergencia nunca cuenta como éxito.", "",
             "GD entrega el valor de su último punto; los heurísticos entregan el mejor conocido. "
             "Los intervalos del YAML definen el muestreo inicial. Los heurísticos recortan posiciones a esos intervalos; "
             "GD no aplica proyección. Es una diferencia de tratamiento de límites que debe considerarse al interpretar resultados.", "",
             "## Tabla 1. Valores finales y éxito", "",
             "| Función | Dim. | Método | Corridas | Media | Desv. muestral | Mejor | Peor | Éxito | Excluidas |",
             "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|"]
    thresholds = ", ".join(str(v) for v in sorted({r['config']['success_threshold'] for r in rows}))
    seeds = ", ".join(sorted({f"{r['config']['seed']}–{r['config']['seed'] + r['config']['runs'] - 1}" for r in rows}))
    lines[4:4] = [f"Umbral(es) de éxito: **{thresholds}**. Intervalo(s) de semillas: **{seeds}**.", ""]
    for row in rows:
        c, s = row["config"], row["summary"]
        lines.append(f"| {c['function']} | {c['dimension']} | {c['method']} | {s['runs']} | "
                     f"{number(s['mean_value'])} | {number(s['std_value'])} | {number(s['best_value'])} | {number(s['worst_value'])} | "
                     f"{s['success_rate']:.1%} | {s['excluded_runs']} |")
    lines += ["", "## Tabla 2. Costo medio por corrida", "",
              "Se cuentan las llamadas de optimización a f y al gradiente por separado. Las evaluaciones para dibujar quedan fuera. "
              "Definimos C = N_f + 2d N_grad: diferencias centrales necesitarían 2d llamadas a f por gradiente. "
              "Es una convención de equivalencia, NO el tiempo real ni el costo medido del gradiente analítico implementado. "
              "Los presupuestos dependen de los parámetros guardados en comparison.json. "
              "GD cuenta una llamada final a f además de sus gradientes. "
              "Los resultados 3D se analizan por separado y no se usan para ordenar métodos 2D.", "",
              "| Función | Dim. | Método | N_f medio | N_grad medio | C medio |",
              "|---|---:|---|---:|---:|---:|"]
    for row in rows:
        c, s = row["config"], row["summary"]
        lines.append(f"| {c['function']} | {c['dimension']} | {c['method']} | {number(s['mean_function_evaluations'])} | "
                     f"{number(s['mean_gradient_evaluations'])} | {number(s['mean_equivalent_evaluations'])} |")
    lines += ["", "Las divergencias pueden reducir el costo medio de GD porque detienen la corrida: ese menor costo no representa una mejora. "
              "La demostración usa un presupuesto menor que el experimento principal; "
              "la Tabla 2 siempre muestra los costos realmente contados bajo la convención elegida.", "", "## Discusión", ""]
    for name in sorted({r["config"]["function"] for r in rows}):
        group = [r for r in rows if r["config"]["function"] == name and r["config"]["dimension"] == 2]
        if not group:
            continue
        lines.append(f"**{name.capitalize()} 2D.** " + "; ".join(
            f"{r['config']['method'].upper()}: {r['summary']['successful_runs']}/{r['summary']['runs']} éxitos, media {number(r['summary']['mean_value'])}"
            for r in group) + ".")
        finite = [r for r in group if r["summary"]["mean_value"] is not None]
        if finite:
            best_value = min(r["summary"]["mean_value"] for r in finite)
            best_names = ", ".join(r["config"]["method"].upper() for r in finite if r["summary"]["mean_value"] == best_value)
            lines.append(f"El menor promedio observado entre las configuraciones mostradas corresponde a {best_names}. "
                         "Es una descripción de esta muestra y estos parámetros, no una garantía de superioridad general.")
        lines.append("Rosenbrock tiene un valle curvo y estrecho: GD aprovecha el gradiente, pero un paso fijo puede avanzar lentamente por el valle "
                     "o divergir desde algunos inicios. PSO, DE y el evolutivo exploran mediante poblaciones sin calcular derivadas; "
                     "su precisión final depende de sus actualizaciones y parámetros." if name == "rosenbrock" else
                     "Rastrigin tiene muchos mínimos locales. GD es un método local: una corrida puede estabilizarse lejos del mínimo global. "
                     "La exploración poblacional permite comparar distintas regiones, aunque no garantiza llegar siempre al óptimo. "
                     "La dispersión y la tasa de éxito de la Tabla 1 permiten valorar esa diferencia.")
        lines.append("")
    lines += ["El evolutivo conserva la mejor mitad, cruza padres por combinación aritmética y muta con ruido gaussiano de desviación fija. "
              "Ese ruido mantiene exploración, pero puede dificultar ajustes muy finos. PSO combina memoria individual y colectiva. "
              "DE usa diferencias entre individuos para proponer candidatos y conserva las mejoras. "
              "Igualar el costo proxy no iguala los mecanismos de búsqueda ni prueba que el tiempo de ejecución sea igual.", "",
              "No se realizaron pruebas de significancia ni un barrido de hiperparámetros. Las conclusiones se limitan a estas funciones, "
              "dimensiones, semillas, umbral y presupuestos. Los experimentos GD 3D de la configuración principal son adicionales, "
              "no una comparación contra heurísticos 3D. Un valor calculado como cero refleja precisión finita; no demuestra "
              "que todas las coordenadas sean exactamente el óptimo en aritmética real.", "",
              "## Figuras y animaciones", "",
              "Las curvas muestran corridas completadas y finitas. La trayectoria ilustrada es la primera exitosa o, si no hay éxitos, "
              "la primera completada. Es una selección explícita para ilustrar, no una corrida representativa de toda la distribución. "
              "En heurísticos, la línea une mejores puntos conocidos: no es la trayectoria de una partícula individual. "
              "En PSO, los puntos lavanda animan las posiciones guardadas de todas las partículas. "
              "En modo movement se interpola entre estados consecutivos y se reparte el tiempo por desplazamiento; "
              "el pie del GIF lo indica. Los puntos intermedios son visuales, no nuevas iteraciones ni resultados del optimizador.", ""]
    index = 1
    for row in rows if include_figures else []:
        c = row["config"]
        relative = Path(c["function"]) / c["method"] / f"{c['dimension']}d"
        for filename, label in [("convergence.png", "Convergencia"), ("trajectory.png", "Trayectoria")]:
            path = artifacts_dir / "figures" / relative / filename
            if path.exists():
                link = Path(os.path.relpath(path, output_dir)).as_posix()
                lines.append(f"La [Figura {index}]({link}) muestra {label.lower()} de {c['function']} {c['dimension']}D con {c['method'].upper()}. Fuente: elaboración propia.")
                lines.append("")
                index += 1
        with (artifacts_dir / "raw" / relative / "runs.csv").open(newline="", encoding="utf-8") as file:
            completed = [r for r in csv.DictReader(file) if r['status'] == 'completed']
        selected = next((r for r in completed if r['success'] == 'True'), completed[0] if completed else None)
        if selected and c['method'] in ('gd', 'pso'):
            path = artifacts_dir / "animations" / relative / f"trajectory_{selected['run_id']}.gif"
            if path.exists():
                lines.append(f"[Animación de {relative}]({Path(os.path.relpath(path, output_dir)).as_posix()}). Fuente: elaboración propia.\n")
    theory = Path(__file__).resolve().parents[2] / "docs/parte1_metodologia.md"
    lines += ["", f"[Fundamentación matemática, ecuaciones y referencias]({Path(os.path.relpath(theory, output_dir)).as_posix()})."]
    (output_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_html_report("\n".join(lines), rows, output_dir / "report.html", artifacts_dir.name)
