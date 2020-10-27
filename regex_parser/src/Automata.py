"""
filename src/Automata.py
reference https://github.com/sdht0/automata-from-regex/blob/master/AutomataTheory.py
"""
# from collections import defaultdict


class Automata:
    """
    class to represent a automata
    """
    pass

    def __init__(self, input_alphabet: set):
        """
        @param input_alphabet a set of input symbols
        """
        self.states = set()  # a finite states of S
        self.input_alphabet = input_alphabet  # a set of input symbols
        self.start_state = None
        self.final_states = set()
        self.transitions = dict()

    @staticmethod
    def epsilon():
        return r'\epsilon'

    def set_start_state(self, state: int):
        self.start_state = state
        self.states.add(state)

    def add_final_states(self, *states):
        for state in states:
                self.final_states.add(state) 
                
    def add_transition(self, from_state, to_state, input_symbols: set):
        self.states.add(from_state)
        self.states.add(to_state)
        if from_state in self.transitions:
            if to_state in self.transitions[from_state]:
                self.transitions[from_state][to_state].update(input_symbols)
            else:
                self.transitions[from_state][to_state] = input_symbols
        else:
            self.transitions[from_state] = {to_state: input_symbols}

    def add_transition_from_dict(self, translations: dict):
        """
        @param translations translations[f][t] = d where f is from state,t in to state,
                                    d is the dict of states where d[state] = set of input symbols
        """
        for from_state, to_states in translations.items():
            for to_state, input_symbols in to_states.items():
                self.add_transition(from_state, to_state, input_symbols)

    def __repr__(self):
        """
        display the information of the automata
        """
        trans = ""
        for from_state,to_states in self.transitions.items():
            for to_state,symbols in to_states.items():
                for char in symbols:
                    trans += f"\t{from_state}->{to_state} on '{char}'\n" 
            trans += '\n'

        return f"states:\t{self.states}\n" \
            f"start state:\t{self.start_state}\n" \
            f"final state:\t{self.final_states}\n" \
            f"transitions:\n{trans}" 

if __name__ == "__main__":
    test = Automata('ab')
    test.set_start_state(1)
    test.add_final_states(2)
    test.add_final_states(2)
    test.add_transition(1,2,set('a'))
    test.add_transition(1,3,set('b'))
    print(test.transitions)
    print(test)
""" output
{1: {2: {'a'}, 3: {'b'}}}
states: {1, 2, 3}
start state:    1
final state:    [2]
transitions:
    1->2 on 'a'
    1->3 on 'b'
"""