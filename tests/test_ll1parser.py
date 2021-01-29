from ll1_parser.LL1Parser import LL1Parser
from IPython.display import display, Math
from collections import defaultdict


g = [r"E \to T E'",
     r"E' \to + T E' | \epsilon ",
     r"T \to F T'",
     r"T' \to * F T' | \epsilon ",
     r"F \to ( E ) | \textbf{id}"]

grammer = LL1Parser(g)

def test_store():

    d = {
        "E": [["T", "E'"]],
        "E'": [["+", "T", "E'"], ["\\epsilon"]],
        "T": [["F", "T'"]],
        "T'": [["*", "F", "T'"], ["\\epsilon"]],
        "F": [["(", "E", ")"], ["\\textbf{id}"]],
    }
    rules_expect = defaultdict(list, d)

    assert grammer.rules == rules_expect

def test_first():
    first = {
        "E'": {'+'},
        "T'": {'*'},
        'F': {'(', '\\textbf{id}'},
        'T': {'(', '\\textbf{id}'},
        'E': {'(', '\\textbf{id}'}
    }
    d_first = defaultdict(set,first)
    assert grammer.first == d_first

def test_follow():
    d = defaultdict(
        set,
        {
            "E": {")", "\\$"},
            "T": {")", "+", "\\$"},
            "F": {")", "*", "+", "\\$"},
            "E'": {")", "\\$"},
            "T'": {")", "+", "\\$"},
        },
    )
    assert grammer.follow == d

def test_display():
    grammer.display_rules(raw=True)
    grammer.display_first_sets(raw=True)
    grammer.display_follow_sets(raw=True)

def test_parsing_table():
    d = {
        "E": {"(": ["T", "E'"], "\\textbf{id}": ["T", "E'"]},
        "E'": {
            "+": ["+", "T", "E'"],
            "\\epsilon": ["\\epsilon"],
            ")": ["\\epsilon"],
            "\\$": ["\\epsilon"],
        },
        "T": {"(": ["F", "T'"], "\\textbf{id}": ["F", "T'"]},
        "T'": {
            "*": ["*", "F", "T'"],
            "\\epsilon": ["\\epsilon"],
            ")": ["\\epsilon"],
            "+": ["\\epsilon"],
            "\\$": ["\\epsilon"],
        },
        "F": {"(": ["(", "E", ")"], "\\textbf{id}": ["\\textbf{id}"]},
    }

    expect = defaultdict(dict, d)
    assert grammer.parsing_table == expect
    grammer.display_parsing_table(raw=True)


# Test a Wrong Grammer
def test_wrong():
    w = [r"S \to i E t S S' | a",
         r"S' \to e S | \epsilon",
         r"E \to b"]

    try:
        wrong = LL1Parser(w)
    except RuntimeError:
        pass
