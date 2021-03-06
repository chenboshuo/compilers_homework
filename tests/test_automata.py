from regex_parser.Automata import Automata
from regex_parser.RegexParser import RegexParser
import pytest

@pytest.fixture
def nfa():
    test1 = Automata.basic_construct(set(['a']))
    test2 = Automata.basic_construct(set(['b']))
    test3 = Automata.union(test1, test2)
    pytest.a_union_b = test3

def figure_path(s):
    # return f"reports/regex_parser/figures/{s}.pdf"
    return f"tests/__pycache__/{s}.tex"

def test_basic():
    test = Automata(set('ab'))
    test.set_start_state(1)
    test.add_final_states(2)
    test.add_final_states(2)
    test.add_transition(1, 2, set(['a', 'b']))
    test.add_transition(1, 1, set('b'))
    print(test.transitions)
    expect1={1: {2: {'a', 'b'}, 1: {'b'}}}
    assert test.transitions == expect1
    print(test)
    test.draw(figure_path('test_automata'),seed=2) # 2

    test.rename(3)
    test.transitions == {4: {5: {'a', 'b'}, 5: {'b'}}}
    # print(test)

def test_basic_construct():
    test1 = Automata.basic_construct(set(['a']))
    test1.draw(save=figure_path("basic_a"),seed=1)
    # print(test1)
    expect1 = {
        1:{
            2:{'a'}
        }
    }
    assert test1.transitions == expect1

def test_star_operation():
    test1 = Automata.basic_construct(set(['a']))
    test1 = Automata.star_operation(test1)
    test1.draw(figure_path('test_star'),seed=1)
    # r"""output
    #     states: {1, 2}
    #     start state:    1
    #     final state:    {2}
    #     transitions:
    #             1->2 on '\epsilon'
    #             1->2 on 'a'

    #             2->1 on '\epsilon'
    # """
    expect = {
        1: {
            2: {'a', '\\epsilon'}
        },
        2: {1: {'\\epsilon'}}
    }
    assert test1.transitions == expect

def test_link_operation():
    test1 = Automata.basic_construct(set(['a']))
    test2 = Automata.basic_construct(set(['b']))
    test2.draw(figure_path('basic_b'),seed=1)
    print(Automata.concatenation(test1, test2))
    test1.draw(save=figure_path('test_concatenation'),seed=2) # 2
    expect = {
        1: {2: {'a'}},
        3: {4: {'b'}},
        2: {3: {'\\epsilon'}}
    }
    assert test1.transitions == expect

def test_parallel_union():
    test1 = Automata.basic_construct(set(['a']))
    test2 = Automata.basic_construct(set(['b']))
    test3 = Automata.union(test1, test2)
    test3.draw(save=figure_path('test_union'),seed=79744993) # 1111
    expect = {
        2: {3: {'a'}},
        4: {5: {'b'}},
        1: {
            2: {'\\epsilon'},
            4: {'\\epsilon'}
        },
        3: {6: {'\\epsilon'}},
        5: {6: {'\\epsilon'}}
    }
    assert test3.transitions == expect

def test_e_closure(nfa):
    test3 = pytest.a_union_b
    reachable_set = test3.e_closure(1)
    expect = set([1,2,4])
    assert reachable_set == expect
    expect = set([1,2,3,4,5,6])
    assert test3.e_closure([1,3,5]) == expect

def test_e_closure_circle():
    nfa = RegexParser('(a|b)*abb').parse_regex()
    print(nfa.start_state)
    nfa.e_closure(nfa.start_state)

def test_e_closure_sets_1(nfa):
    nfa = pytest.a_union_b
    expect = set([1,2,4])
    closure = nfa.e_closure([1])
    assert expect == closure


def test_e_closure_sets_2(nfa):
    nfa = pytest.a_union_b
    expect = set([1,2,3,4,6])
    closure = nfa.e_closure([1,3])
    assert expect == closure

def test_move(nfa):
    nfa = pytest.a_union_b
    moved = nfa.move([1],'a')
    expect = set([1,2,3,4,6])
    assert moved == expect
