def inc(x):
    return x + 1


def test_scenario(web_driver):
    assert inc(1) == 2


def test_answer1(web_driver):
    assert inc(1) == 2


def test_answer2(web_driver):
    assert inc(2) == 3
