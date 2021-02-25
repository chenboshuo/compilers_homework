"""
filename src/Automata.py

reference https://github.com/sdht0/automata-from-regex/blob/master/AutomataTheory.py
"""
from __future__ import annotations  # type hint within a class
from typing import *
from collections.abc import Iterable
# see https://stackoverflow.com/questions/41135033/type-hinting-within-a-class
from matplotlib import pyplot as plt
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
    r"""
    class to represent a automata

    :param input_alphabet: a set of input symbols
    :type input_alphabet: set,optional

    :ivar empty_string: empty string, denoted by :math:`\epsilon`
    :ivar self.states: a finite states of S
    :ivar self.input_alphabet:  a set of input symbols
    :ivar self.start_state: the start state
    :ivar self.final_states: the set of final state
    :ivar self.transitions: the transitions functions,
        `translations[f][t] = d` where f is from state,t in to state,
        d is the dict of states where d[state] = set of input symbols
    :vartype self.transitions: Dict[int,Dict[int,Set[str]]]
    """
    empty_string = set([r'\epsilon'])

    def __init__(self, input_alphabet: set = set()):
        self.states = set()  # a finite states of S
        self.input_alphabet = input_alphabet  # a set of input symbols
        self.start_state = None
        self.final_states = set()
        self.transitions = dict()

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
        input_symbols = input_symbols.copy() # prevent the source set changing
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

    def draw(self, save='temp.pdf', seed: int = None) -> None:
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
             #  layout="spring_layout",
             seed=seed,
             canvas=(10, 10),
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
        # return cls.basic_construct(set([r'\epsilon']))
        return cls.basic_construct()

    @classmethod
    def basic_construct(cls, symbol= None):
        """construct NFA with a single symbol

        :param symbol: the symbol
        :type symbol: Set[str] or str
        :return: a NFA
        :rtype: Automata
        """
        if isinstance(symbol, str):
            symbol = set([symbol])
        input_symbol = symbol if symbol else set([r'\epsilon'])
        basic = Automata()
        if symbol:
            basic.input_alphabet = input_symbol
        basic.set_start_state(1)
        basic.add_final_states(2)
        basic.add_transition(1, 2, input_symbol)
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
    def concatenation(base: Automata, addition: Automata) -> Automata:
        """union two Automata

        :param basic: this Automata will be changed after union
        :type basic: Automata
        :param addition: This Automata will be deleted after  union
        :type addition: Automata
        :return: [description]
        :rtype: Automata
        """
        # to manage the state name conflict
        offset = max(base.states)
        addition.rename(offset)
        print(base.input_alphabet,addition.input_alphabet)
        base.input_alphabet |= addition.input_alphabet

        base.add_transition_from_dict(addition.transitions)
        for pre_final in base.final_states:
            base.add_transition(pre_final, addition.start_state,
                                 Automata.empty_string)

        base.final_states = addition.final_states
        del addition
        return base

    @staticmethod
    def union(basic: Automata, parallel: Automata) -> Automata:
        """handle the regex `s|t` by union these NFA

        :param basic: the NFA will change after union
        :type basic: Automata
        :param parallel: the NFA will be deleted after union
        :type parallel: Automata
        :return: The new NFA based on `basic`
        :rtype: Automata
        """
        # rename the two graph
        basic.rename(offset=1)
        offset = max(basic.states)
        parallel.rename(offset)

        # update edges and input_alphabet
        basic.add_transition_from_dict(parallel.transitions)
        basic.input_alphabet = parallel.input_alphabet

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

    def e_closure(self,
                  state,
                  reachable_set: Set[int] = None) -> Set[str]:
        r"""Set of NFA states reachable from NFA state `state`
        on :math:`\epsilon`-transitions alone.

        :param state: the NFA state
        :type state: int or Iterable
        :return: the set of reachable states
        :rtype: Set[str]
        """
        if not reachable_set:
            reachable_set = set()
        if isinstance(state, Iterable):
            for s in state:
                reachable_set |= self.e_closure(s)
            return reachable_set
        if state in reachable_set:
            return reachable_set
        reachable_set.add(state)
        if state not in self.transitions:
            return reachable_set
        for target, s in self.transitions[state].items():
            if '\\epsilon' in s:
                reachable_set.add(target)
                reachable_set |= self.e_closure(target, reachable_set)

        return reachable_set

    def move(self, states: Iterable, symbol: str) -> Set[int]:
        """Set of NFA states to which there is a transition
            on a input symbol `symbol` form one state :math:`s`
            in set states

        :param states: the set of states
        :type states: Iterable
        :param symbol: input symbol
        :type symbol: str
        :return: the set of final sets
        :rtype: Set[int]
        """
        states = set(states)
        states |= self.e_closure(states)
        reachable = set()
        for state in states:
            if state not in self.transitions:
                continue
            for target, s in self.transitions[state].items():
                if symbol in s:
                    reachable.add(target)
        reachable |= self.e_closure(reachable)
        states |= reachable
        return states

    # def _get_new_state(self,
    #     states:Dict[frozenset,int],
    #     dfa: Automata,
    #     cur:Set[int],
    #     input:str):
    #     pass

    # def get_DFA(self) -> Automata:
    #     """get the DFA from the NFA

    #     :return: A DFA derivate from the current NFA
    #     :rtype: Automata
    #     """
    #     dfa = Automata(input_alphabet=self.input_alphabet)
    #     new_states = {}
    #     initial = self.e_closure(self.start_state)
    #     for i in self.input_alphabet:
    #         pass
