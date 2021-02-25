from regex_parser.Automata import Automata
from typing import *

class DFA(Automata):
    """DFA have,
    for each state,
    and for each symbols of its input alphabet exactly 
    one edge with that symbol leaving that state

    """
    def __init__(self,nfa:Automata):
        """generate from Automata

        :param nfa: a NFA
        :type nfa: Automata

        :ivar self.NFA_map: the map from NFA to DFA
        :type self.NFA_map: Dict[Frozenset[int],int]
        """
        super().__init__(nfa.input_alphabet)
        self.NFA_map = {}
        initial = nfa.e_closure(nfa.start_state)
        self.set_start_state(1)
        for i in nfa.input_alphabet:
            self._get_new_state(nfa=nfa,
                cur=initial,
                input_=i)

    def _get_states_id(self,states_set:Set[int]) -> int:
        """get the DFA state id of the NFA states set

        :param states_set: a set of the states fromNFA
        :type states_set: Set[int]
        :return: the number of the state id
        :rtype: int

        :ivar key: the key of self.NFA_map
        :vartype key: frozenset[int]
        """
        key = frozenset(states_set)
        if key not in self.NFA_map:
            state_id = len(self.NFA_map) + 1
            self.NFA_map[key] = state_id
            self.states.add(state_id)
        return self.NFA_map[key]

    def _get_new_state(self,
        nfa: Automata,
        cur:Set[int],
        input_:str) -> None:
        """a recursion method to get the new set from 
        state `cur` to new states with the input `input_`

        :param nfa: the nfa automata
        :type nfa: Automata
        :param cur: the sets of current states
        :type cur: Set[int]
        :param input_: the input character
        :type input_: str
        """
        cur_id = self._get_states_id(cur)
        to_state = nfa.move(cur,input_)
        to_id = self._get_states_id(to_state)
        if cur_id in self.transitions and to_id in self.transitions[cur_id]:
            return None
        self.add_transition(cur_id,to_id,set([input_]))

        for i in self.input_alphabet:
            self._get_new_state(
                nfa=nfa,
                cur=to_state,
                input_=i)
