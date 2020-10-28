"""
filename src/Automata.py
reference https://github.com/sdht0/automata-from-regex/blob/master/AutomataTheory.py
"""
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
    """
    pass

    def __init__(self, input_alphabet: set):
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

    def draw(self, save=None):
        """
        draw the graph

        :param save: save the save path
        reference_

        .. _reference: https://stackoverflow.com/a/20382152
        """
        # create graph
        G = nx.DiGraph()
        for from_state, to_states in self.transitions.items():
            for to_state, symbols in to_states.items():
                G.add_edge(from_state, to_state, trans=symbols)

        # get attributes
        node_labels = {node: str(node) for node in G.nodes()}
        pos = nx.spring_layout(G)
        edge_labels = nx.get_edge_attributes(G, 'trans')
        for edge, label in edge_labels.items():
            string = []
            for char in label:
                string.append(str(char))
            edge_labels[edge] = '$' + "| ".join(string)+'$'

        # draw
        nx.draw(G, pos, node_color='#dcfc7c')  # base graph

        nx.draw_networkx_nodes(G, pos,
                               nodelist=list(self.final_states))  # final states
        nx.draw_networkx_nodes(
            G, pos, nodelist=[self.start_state], node_color='#fc7c7c')  # start state
        nx.draw_networkx_labels(G, pos, labels=node_labels)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                     #  horizontalalignment='left',
                                     verticalalignment='top')

        if save:
            plt.savefig(save)


if __name__ == "__main__":
    test = Automata('ab')
    test.set_start_state(1)
    test.add_final_states(2)
    test.add_final_states(2)
    test.add_transition(1, 2, set(['a', 'b']))
    test.add_transition(1, 3, set('b'))
    print(test.transitions)
    print(test)
    test.draw('../docs/figures/test_automata.pdf')
""" output
{1: {2: {'a', 'b'}, 3: {'b'}}}
states: {1, 2, 3}
start state:    1
final state:    {2}
transitions:
        1->2 on 'a'
        1->2 on 'b'
        1->3 on 'b'
"""
