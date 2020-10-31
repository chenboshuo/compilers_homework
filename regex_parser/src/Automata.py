"""
filename src/Automata.py
reference https://github.com/sdht0/automata-from-regex/blob/master/AutomataTheory.py
"""
from __future__ import annotations  # type hint within a class
from typing import *
# see https://stackoverflow.com/questions/41135033/type-hinting-within-a-class
from matplotlib import pyplot as plt
import networkx as nx
import matplotlib as mpl
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})
# for Palatino and other serif fonts use:
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Palatino"],
})


class Automata:
    """
    class to represent a automata

    :param input_alphabet: a set of input symbols
    :type input_alphabet: set,optional

    :ivar empty_string: empty string, denoted by :math:`\epsilon`
    :ivar self.states: a finite states of S
    :ivar self.transitions: 11
    :ivar self.input_alphabet:  a set of input symbols
    :ivar self.final_states: the set of final state
    :ivar self.transitions: the transitions functions,
        `translations[f][t] = d` where f is from state,t in to state,
        d is the dict of states where d[state] = set of input symbols
    """
    empty_string = set([r'\epsilon'])

    def __init__(self, input_alphabet: set):
        self.states = set()  # a finite states of S
        self.input_alphabet = input_alphabet  # a set of input symbols
        self.start_state = None
        self.final_states = set()
        self.transitions = dict()

    # @staticmethod
    # def empty_string() -> str:
    #     r"""get the symbol of empty_string symbol :math:`\epsilon`

    #     :return: r'\epsilon'
    #     :rtype: str
    #     """
    #     return r'\epsilon'

    def set_start_state(self, state: int):
        """set the start state

        :param state: the label of start state
        :type state: int
        """
        self.start_state = state
        self.states.add(state)

    def add_final_states(self, *states):
        """add the final states

        :param states: the list of states
        """
        for state in states:
            self.final_states.add(state)

    def add_transition(self, from_state: int, to_state: int, input_symbols: set):
        """add the transition to transfer functions
        (`self.transitions` in the program)

        :param from_state: the begin state
        :type from_state: int
        :param to_state: the next state
        :type to_state: int
        :param input_symbols: the transfer symbols to the next states
        :type input_symbols: set
        """

        self.states.add(from_state)
        self.states.add(to_state)
        if from_state in self.transitions:
            if to_state in self.transitions[from_state]:
                self.transitions[from_state][to_state].update(input_symbols)
            else:
                self.transitions[from_state][to_state] = input_symbols
        else:
            self.transitions[from_state] = {to_state: input_symbols}

    def add_transition_from_dict(self, translations: Dict[int, Dict[int, set]]):
        """
        :param translations: translations[f][t] = d where f is from state,t in to state,
                                    d is the dict of states where d[state] = set of input symbols
        :type translations: dict
        """
        for from_state, to_states in translations.items():
            for to_state, input_symbols in to_states.items():
                self.add_transition(from_state, to_state, input_symbols)

    def __repr__(self):
        """
        display the information of the automata
        """
        trans = ""
        for from_state, to_states in self.transitions.items():
            for to_state, symbols in to_states.items():
                for char in symbols:
                    trans += f"\t{from_state}->{to_state} on '{char}'\n"
            trans += '\n'

        return f"states:\t{self.states}\n" \
            f"start state:\t{self.start_state}\n" \
            f"final state:\t{self.final_states}\n" \
            f"transitions:\n{trans}"

    def rename(self, offset: int) -> None:
        """change the state name to prevent the conflict

        :param offset: offset the number
        :type offset: int
        """
        self.states = set(i+offset for i in self.states)
        self.start_state += offset
        self.final_states = set(i+offset for i in self.final_states)

        # change the transition
        new_transitions = dict()
        for from_state, to_states in self.transitions.items():
            new_transitions[from_state+offset] = dict()
            for to_state in to_states.keys():
                new_transitions[from_state+offset][to_state+offset] = \
                    self.transitions[from_state][to_state]

        self.transitions = new_transitions

    def draw(self, save='temp.pdf',seed:int=None) -> None:
        """
        draw the graph

        :param save: save the save path (`reference <https://stackoverflow.com/a/20382152>`_)
        :type save: str
        :param seed: the node location random seed
        :type seed: int

        if you haven't installed network2tikz,
        you need install it by 

        .. code-block:: bash

            pip install -U network2tikz

        """
        from network2tikz import plot
        nodes = list(self.states)
        node_colors = [
            'green!20' if node not in self.final_states else 'blue!20' for node in self.states]
        node_colors[nodes.index(self.start_state)] = "red!20"
        edges = []
        edge_labels = []
        for from_state, to_states in self.transitions.items():
            for to_state, symbols in to_states.items():
                edges.append((from_state, to_state))
                labels = []
                for symbol in symbols:
                    labels.append(symbol)
                edge_labels.append("| ".join(labels))

        plot((nodes, edges), save,
             seed=seed, 
             node_label_as_id=True,
             node_color=node_colors,
             edge_label=edge_labels,
             edge_math_mode=True, edge_directed=True, edge_curved=0.2,
             edge_label_position='left')

    @classmethod
    def empty_construct(cls):
        """construct a empty construct of a automata

        :return: the empty automata
        :rtype: Automata
        """
        return cls.basic_construct(set([r'\epsilon']))

    @classmethod
    def basic_construct(cls, symbol: set):
        """construct NFA with a single symbol

        :param symbol: the symbol
        :type symbol: str
        :return: a NFA
        :rtype: Automata
        """
        basic = Automata(symbol)
        basic.set_start_state(1)
        basic.add_final_states(2)
        basic.add_transition(1, 2, set(symbol))
        return basic

    @staticmethod
    def star_operation(nfa):
        """process the star operation

        .. note::

            the nfa is changed after call the method

        :param nfa: the previous NFA
        :type nfa: Automata
        :return: the new NFA after processing star operation
            that means add two string in the begin state and end state
        :rtype: Automata
        """
        for final_state in nfa.final_states:
            nfa.add_transition(nfa.start_state, final_state,
                               set([r"\epsilon"]))
            nfa.add_transition(final_state, nfa.start_state,
                               set([r"\epsilon"]))

        return nfa

    @staticmethod
    def concatenation(basic: Automata, addition: Automata) -> Automata:
        """union two Automata

        :param basic: this Automata will be changed after union
        :type basic: Automata
        :param addition: This Automata will be deleted after  union
        :type addition: Automata
        :return: [description]
        :rtype: Automata
        """
        # to manage the state name conflict
        offset = max(basic.states)
        addition.rename(offset)

        basic.add_transition_from_dict(addition.transitions)
        for pre_final in basic.final_states:
            basic.add_transition(pre_final, addition.start_state,
                                 Automata.empty_string)

        basic.final_states = addition.final_states
        del addition
        return basic

    @staticmethod
    def union(basic: Automata, parallel: Automata) -> Automata:
        """handle the regex s|t by union these NFA

        :param basic: the NFA will change after union
        :type basic: Automata
        :param parallel: the NFA will be deleted after union
        :type parallel: Automata
        :return: The new NFA based on `basic`
        :rtype: Automata
        """
        # rename the two graph
        basic.rename(1)
        offset = max(basic.states)
        parallel.rename(offset)

        # update edges
        basic.add_transition_from_dict(parallel.transitions)

        # update the start
        new_start_state = min(basic.states) - 1
        basic.add_transition(new_start_state,
                             basic.start_state, Automata.empty_string)
        basic.add_transition(new_start_state, parallel.start_state,
                             Automata.empty_string)
        basic.set_start_state(new_start_state)

        # handle the final states
        new_final_state = max(parallel.states)+1
        pre_finals = basic.final_states.union(parallel.final_states)
        for pre_final in pre_finals:
            basic.add_transition(
                pre_final, new_final_state, Automata.empty_string)
        basic.final_states = set([new_final_state])

        del parallel
        return basic


if __name__ == "__main__":
    # basic test
    test = Automata(set('ab'))
    test.set_start_state(1)
    test.add_final_states(2)
    test.add_final_states(2)
    test.add_transition(1, 2, set(['a', 'b']))
    test.add_transition(1, 1, set('b'))
    print(test.transitions)
    print(test)
    test.draw('../docs/figures/test_automata.pdf',seed=2) # 2
    """ output
    {1: {2: {'a', 'b'}, 1: {'b'}}}
    states: {1, 2}
    start state:    1
    final state:    {2}
    transitions:
            1->2 on 'a'
            1->2 on 'b'
            1->1 on 'b'
    """
    print(test.transitions)
    test.rename(3)
    print(test)
    """output
        {1: {2: {'a', 'b'}, 1: {'b'}}}
        states: {4, 5}
        start state:    4
        final state:    {5}
        transitions:
                4->5 on 'a'
                4->5 on 'b'
                4->4 on 'b'    
        """

    # test basic construct
    test1 = Automata.basic_construct(set(['a']))
    print(test1)
    """
    states: {1, 2}
    start state:    1
    final state:    {2}
    transitions:
            1->2 on 'a'    
    """

    # test star operation
    test1 = Automata.star_operation(test1)
    print(test1)
    test1.draw('../docs/figures/test_star.pdf')
    # TODO debug

    # test link operation
    test2 = Automata.basic_construct('c')
    print(Automata.concatenation(test, test2))
    r"""output
        states: {4, 5, 6, 7}
        start state:    4
        final state:    {7}
        transitions:
                4->5 on 'a'
                4->5 on 'b'
                4->4 on 'b'

                6->7 on 'c'

                5->6 on '\epsilon'
    """

    # test parallel union
    test3 = Automata.basic_construct(set('d'))
    test4 = Automata.basic_construct(set('e'))
    test3 = Automata.union(test3, test4)
    print(test3)
    r"""output
        states: {1, 2, 3, 4, 5, 6}
        start state:    1
        final state:    {6}
        transitions:
                2->3 on 'd'

                4->5 on 'e'

                1->2 on '\epsilon'
                1->4 on '\epsilon'

                3->6 on '\epsilon'

                5->6 on '\epsilon'
    """
