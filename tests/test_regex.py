from regex_parser.RegexParser import RegexParser

def figure_path(s):
        # return f"reports/regex_parser/figures/{s}.pdf"
        return f"tests/__pycache__/{s}.tex"

def test_one_letter():
    test1 = RegexParser("a")
    expect = {1: {2: {'a'}}}
    parser = test1.parse_base_part()
    assert parser.transitions == expect
    assert parser.input_alphabet == set(['a']) # prevent empty string 

def test_escape_symbol():
    test2 = RegexParser("\*")
    assert test2.parse_base_part().transitions == {1: {2: {'*'}}}

def test_parse_factor():
    test3 = RegexParser('a*')
    expect = {1: {2: {"a", "\\epsilon"}}, 2: {1: {"\\epsilon"}}}
    parser = test3.parse_factor_part()
    assert parser.transitions == expect
    assert parser.input_alphabet == set(['a'])

def test_parse_term():
    test4 = RegexParser('ab')
    expect = {
        1: {2: {"\\epsilon"}},
        3: {4: {"a"}},
        2: {3: {"\\epsilon"}},
        5: {6: {"b"}},
        4: {5: {"\\epsilon"}},
    }
    parser = test4.parse_term_part()
    assert parser.transitions == expect
    assert parser.input_alphabet == set(['a','b'])

def test_simple_NFA():
    nfa1 = RegexParser('(a|b)').parse_regex()
    expect = {
        1: {2: {"\\epsilon"}},
        4: {5: {"\\epsilon"}},
        6: {7: {"a"}},
        5: {6: {"\\epsilon"}},
        8: {9: {"\\epsilon"}},
        10: {11: {"b"}},
        9: {10: {"\\epsilon"}},
        3: {4: {"\\epsilon"}, 8: {"\\epsilon"}},
        11: {12: {"\\epsilon"}},
        7: {12: {"\\epsilon"}},
        2: {3: {"\\epsilon"}},
    }
    assert nfa1.input_alphabet == set(['a','b'])
    assert nfa1.transitions == expect
    nfa1.draw(save=figure_path("a|b"),seed=79870681)

def test_complex():
    expect = {
        1: {2: {"\\epsilon"}},
        4: {5: {"\\epsilon"}},
        6: {7: {"a"}},
        5: {6: {"\\epsilon"}},
        8: {9: {"\\epsilon"}},
        10: {11: {"b"}},
        9: {10: {"\\epsilon"}},
        3: {4: {"\\epsilon"}, 8: {"\\epsilon"}, 12: {"\\epsilon"}},
        11: {12: {"\\epsilon"}},
        7: {12: {"\\epsilon"}},
        12: {3: {"\\epsilon"}, 13: {"\\epsilon"}},
        2: {3: {"\\epsilon"}},
        13: {14: {"a"}},
        15: {16: {"b"}},
        14: {15: {"\\epsilon"}},
    }
    nfa2 = RegexParser('(a|b)*ab').parse_regex()
    assert nfa2.input_alphabet == set(['a','b'])
    assert nfa2.transitions == expect
    nfa2.draw(save=figure_path('complex'),seed=53138909)

