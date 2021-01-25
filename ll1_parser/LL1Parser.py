from collections import defaultdict, deque
from typing import *
from IPython.display import display, Math
import itertools
# import sys
# sys.path.insert(0,"../")
from grammar import Grammar


class LL1Parser(Grammar):
    r"""a set of algorithms to analyse the LL(1) grammer

        :param rules: the LL(1) grammer,you need input using latex gammer and
            sparated by spaces.

            for instance, in you want to input:

            :math:`E \to T E`

            :math:`E' \to + T E | \epsilon`

            :math:`T \to F T`

            :math:`T' \to *F T' | \epsilon`

            :math:`F \to ( E ) | \textbf{id}`

            then run:

            .. jupyter-execute::

                from LL1Parser import LL1Parser
                g = [r"E \to T E'",
                    r"E' \to + T E' | \epsilon ",
                    r"T \to F T'",
                    r"T' \to * F T' | \epsilon ",
                    r"F \to ( E ) | \textbf{id}"
                    ]
                grammer = LL1Parser(g)

        :type rules: List[str]
        :param start_symbol: the start symbol
        :type start_symbol: str, optional

        then you can display the rules using `display_rules()`, for example:

        .. jupyter-execute::

            grammer.display_rules()

        You can see the first sets and follow sets
        using `display_first_sets()`, for examples:

        .. jupyter-execute::

            grammer.display_first_sets()

        Similarly, you can see the follow set using:

        .. jupyter-execute::

            grammer.display_follow_sets()

        The :meth:`LL1Parser.display_parsing_table`
        can show the parsing table

        .. jupyter-execute::

            grammer.display_parsing_table()

    """

    def __init__(self, rules: List[str], start_symbol: str = None) -> None:
        """init the LL(1) grammer
        """
        super().__init__(rules,start_symbol)
        # create first
        self.first: Dict[str, set] = defaultdict(set)
        """the first symbol dicts
        """
        self.create_first()

        # create follow set
        self.follow = defaultdict(set)
        """the follow set of every nonterminal
        """
        self.create_follow()

        self.parsing_table: Dict[str, Dict[str, List[str]]] \
            = defaultdict(dict)
        """ the parsing table
        self.parsing_table[A][a] = (rule)
        where A is the nonterminal at the left of rule,
        a is the nonterminal
        """

        # create parsing table
        self.create_table()



    def create_first(self):
        """create the first sets

        :ivar nonterminals: the queue to save the first nonterminal of
            a rule
        :vartype nonterminals: collections.deque
        :ivar can_emptystring: the set of nonterminals can be empty
        :vartype can_emptystring: set
        """
        nonterminals = deque()

        for left, rule in self.iter_rules():
            if rule[0] in self.terminals:  # symbol rule[0] is terminal
                self.first[left].add(rule[0])
            elif rule[0] == r'\epsilon':
                self.contains_empty.add(left)
            else: # rule[0] is nonterminal
                nonterminals.append((left, rule))

        while nonterminals:
            left, rule = nonterminals.popleft()
            if rule[0] in self.first:  # first symbol is nonterminal
                self.first[left].update(self.first[rule[0]])
            else:  # pending
                nonterminals.append((left, rule))

            if rule[0] in self.contains_empty:  # first symbol can empty string
                if rule[1:]:
                    nonterminals.append((left, rule[1:]))

    def display_sets(self, name, raw=False):
        """display the sets

        :param names: the set names(first,follow)
        :type name: str
        :param raw: show the raw latex code, defaults to False
        :type raw: bool, optional
        """
        begin = r"\begin{array}{ll}" + "\n"
        end = r"\end{array}" + "\n"
        contents = begin
        for left, first_set in self.__dict__[name].items():
            s = "\t" + r"\mathrm{" + name + r"}(" + left + r") &= \{"
            s += ", ".join(list(first_set))
            s += r"\} \\" + "\n"
            contents += s
        contents += end
        if raw:
            print(contents)

        display(Math(contents))

    def display_first_sets(self, raw=False):
        """render the first(i) in jupyter notebook

        :param raw: the raw code of latex, defaults to False
        :type raw: bool, optional
        """
        self.display_sets(raw=raw, name='first')

    def display_follow_sets(self, raw=False):
        """render the follow(i) in jupyter notebook

        :param raw: the raw code of LaTeX, defaults to False
        :type raw: bool, optional
        """
        self.display_sets(raw=raw, name='follow')

    def create_follow(self):
        r"""create the follow sets of all nonterminals

            1. place the $ symbol in follow(S),
            where S is the start symbol,
            and $ is the input right endmarker

            2. if there is a production :math:`A \to \alpha B \beta`,
            then everything in `first(B)` except :math:`\epsilon`
            is in `follow(B)`

            3. if there is a production :math:`A \to \alpha B`,
            or a production :math:`A \to aB\beta`,
            where first(:math:`\beta`) contains `\epsilon`,
            then everything in `follow(A)` is in `follow(B)`
        """

        self.follow[self.start_symbol].add(r'\$')  # add end symbol
        to_union = deque()  # (A,B) such that set B is the subset of set A
        empty_symbol = set([r'\epsilon'])
        for left, rule in self.iter_rules():
            for cur, post in \
                itertools.zip_longest(rule, rule[1:],
                                      fillvalue=r'\epsilon'):
                if cur in self.rules:  # cur is nonterminal
                    if post in self.rules:  # post is nonterminal
                        self.follow[cur].update(self.first[post]-empty_symbol)
                    if post in self.contains_empty:
                        # follow(cur) contains follow(left)
                        to_union.append((cur, left))
                    elif post in self.terminals:
                        self.follow[cur].add(post)
        to_union.append((None, None))  # add the terminal symbol
        has_enlarged = False
        while to_union:
            tail, left = to_union.popleft()
            if left is None:
                if not has_enlarged:
                    break
                else:
                    has_enlarged = False
                    to_union.append((None, None))
            else:
                set_, subset = self.follow[tail], self.follow[left]
                new_set = set_.union(subset)
                if set_ != new_set:
                    has_enlarged = True
                    self.follow[tail] = new_set
                to_union.append((tail, left))

    def add_to_table(self, left: str, terminal: str,
                     rule: List[str]):
        r"""add the rule to the predictive parsing table

        :param left: the left of the production
        :type left: str
        :param terminal: the related terminal
        :type terminal: str
        :param rule: the rule of the right
        :type rule: List[str]
        :raises RuntimeError: conflict in add items,
            that means the grammer isn't LL(1) grammer.
            for example, if you have the grammer

            .. jupyter-execute::

                from IPython.display import display, Math, Latex
                w = [r"S \to i E t S S' | a",
                    r"S' \to e S | \epsilon",
                    r"E \to b"]
                for g in w:
                    display(Math(g))

            then you create the instance,
            you will see the information

            .. jupyter-execute::
                :raises:

                wrong = LL1Parser(w)
        """

        if terminal in self.parsing_table[left] and rule != self.parsing_table[left][terminal]:
            raise RuntimeError(f"""It isn't a LL(1) grammar,
            new added M[{left}][{terminal}] = {rule}
            conflict with existing M[{left}][{terminal}] = {self.parsing_table[left][terminal]}
            parsing table.
            """)
        self.parsing_table[left][terminal] = rule

    def create_table(self):
        r"""create a predictive parsing table
        For each production :math:`A \to \alpha` of the grammar,
        do the following:

        1. For each terminal :math:`a`, add :math:`A \to \alpha`
        to `M[A,a]`.

        2. If :math:`\epsilon` in first(:math:`\alpha`),
        then for each terminal b in follow(A),
        add :math:`A \to \alpha` to `M[A,b]`.
        If :math:`\epsilon` in first(:math:`\alpha`)
        and $ in follow(A),
        add :math:`A \to \alpha` to M[A,$] as well.
        """
        for left, rule in self.iter_rules():
            first = self.get_first(rule)
            for terminal in first:
                self.add_to_table(left=left, terminal=terminal, rule=rule)
            if r'\epsilon' in first:  # epsilon is in first symbol
                for i in self.follow[left]:  # every symbol should add to table
                    self.add_to_table(left=left,
                                      terminal=i, rule=rule)
                if r'\$' in self.follow[left]:
                    self.add_to_table(left=left,
                                      terminal=r'\$', rule=rule)

    # TODO calculate the first of production, and store them
    # Then calculate tht first of nonterminal
    def get_first(self, rule: List[str]) -> set:
        r"""return the first symbol of a expression(calculate first(:math:`\alpha`))

        :param rule: the list of rule symbols
        :type rule: List[str]
        :return: the set of the first set
        :rtype: set
        """
        if rule[0] in self.terminals or rule[0] == r'\epsilon':
            return set([rule[0]])
        first_set = self.first[rule[0]]
        first_part = self.first[rule[0]]
        while r'\epsilon' in first_part:
            first_part = self.get_first(rule[1:])
            first_set.update(first_part)

        return first_set

    def display_parsing_table(self, raw=False):
        begin = r"\begin{array}{|"
        begin += r"|".join(["c"]*(len(self.terminals)+1))
        begin += r"|}" + '\n'
        end = r"\end{array}"

        # create the header
        header = "\t\hline \n" + "\t" +r"\text{terminal}"
        for terminal in self.terminals:
            header += "\t&"
            header += terminal
        header += r'\\ \hline' + "\n"
        cells = ""
        for nonterminal in self.rules.keys():
            line = "\t" + nonterminal
            for terminal in self.terminals:
                line += " \t&"
                if terminal in self.parsing_table[nonterminal]:
                    line += self.display_rule(left=nonterminal,
                                              rule=self.parsing_table[nonterminal][terminal],
                                              new_line=False,
                                              array_environment=False)
            # line += r"\\ \hline" + '\n'
            line += r"\\ " + '\n'
            cells += line

        cells += r"\hline" + "\n"
        content = begin+header + cells + end
        display(Math(content))
        if raw:
            print(content)
