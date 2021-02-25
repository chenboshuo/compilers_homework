from regex_parser.RegexParser import RegexParser
from regex_parser.dfa import DFA
import pytest

def figure_path(s):
    # return f"reports/regex_parser/figures/{s}.pdf"
    return f"tests/__pycache__/{s}.tex"
    # return f"tests/__pycache__/{s}.pdf"

@pytest.fixture
def dfa():
    nfa = RegexParser('(a|b)*abb').parse_regex()
    nfa.draw(figure_path('source_nfa'),seed=56)
    dfa = DFA(nfa)
    dfa.draw(figure_path('test_dfa'),seed=56)
    print('dfa.NFA_map')
    print(dfa.NFA_map)
    print()
    print('nfa.transitions:')
    print(nfa.transitions)
    print()
    print('dfa.transitions:')
    print(dfa.transitions)
    print()
    print('nfa.input_alphabet')
    print(nfa.input_alphabet)

def test_dfa(dfa):
    # assert False
    pass