from optimization.rastrigin import rastrigin


def test_rastrigin_minimum_at_zero():
    assert rastrigin([0.0, 0.0]) == 0.0
