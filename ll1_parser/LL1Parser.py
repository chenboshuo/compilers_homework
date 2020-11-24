from collections import defaultdict, deque
import re
from typing import *
from IPython.display import display, Math, Latex
import itertools


class LL1Parser:
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
                    r"E' \to + T E | \epsilon ", 
                    r"T \to F T", 
                    r"T' \to *F T' | \epsilon ",
                    r"F \to ( E ) | \textbf{id}"]     
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


    """

    def __init__(self, rules: List[str], start_symbol: str = None) -> None:
        """init the LL(1) grammer
        """
        # set the start symbol
        if start_symbol:
            self.start_symbol = start_symbol  # : the start symbol
        else:
            self.start_symbol = rules[0].split()[0]

        # save rules
        self.rules: Dict[str, List[str]] = defaultdict(list)
        """the rules of the gammer, 
            `self.rules[T] = L`, 
            `L[i]= items`, 
            `items[k] = symbol`,
            where `T` is a terminal, 
            `i` is the index of alternatives
            `items` is the list of the symbols of a rule
        """

        for rule in rules:
            alternatives = re.split('\|', rule)  # find rules connect by |
            first_part = alternatives[0].split()
            left = first_part[0]  # the nonterminal can find in the first part
            # add elements except left symbol and ->
            self.rules[left].append(first_part[2:])

            for alternative in alternatives[1:]:
                self.rules[left].append(alternative.split())

        # create first
        self.first: Dict[str, set] = defaultdict(set)
        """the first symbol dicts
        """
        self.contains_empty: set = set()
        """the set of terminals that contains empty strings
        """
        self.create_first()

        # create follow set
        self.follow = defaultdict(set)
        """the follow set of every nonterminal
        """
        self.create_follow()

    def display_rules(self, raw=False):
        """display  the latex code of the gammer

        :param raw: show the raw code, defaults to False
        :type raw: bool, optional
        """
        begin = r"\begin{array}{ll}" + "\n"
        end = r"\end{array}"+"\n"

        for left, rules in self.rules.items():
            s = "\t"+left + r" & \to "
            s += " ".join(rules[0])
            s += r" \\" + "\n"
            for r in rules[1:]:
                s += "\t\t" + r"&\;\, |\;\," + " ".join(r) + r"\\" + "\n"
            begin += s

        if raw:
            print(begin+end)

        display(Math(begin+end))

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
            if rule[0] not in self.rules:  # symbol rule[0] is terminal
                self.first[left].add(rule[0])
                if rule[0] == r'\epsilon':
                    self.contains_empty.add(left)
            else:
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

    def iter_rules(self) -> tuple:
        """iter all the rules

        :yield: the iterator of (left,rule)
        :rtype: Iterator[tuple]
        """

        for left, rules in self.rules.items():
            for rule in rules:
                yield (left, rule)

    def display_sets(self,name,raw=False):
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
            s = r"\mathrm{"+ name + r"}(" + left + r") &= \{"
            s += ", ".join(list(first_set))
            s += r"\} \\"
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
        self.display_sets(raw=raw,name='first')

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

        self.follow[self.start_symbol].add(r'\$')
        to_union = deque() # (A,B) such that set B is the subset of set A
        empty_symbol = set([r'\epsilon'])
        for left, rule in self.iter_rules():
            for cur, post in \
                itertools.zip_longest(rule, rule[1:],
                                      fillvalue=r'\epsilon'):
                if cur in self.rules: # cur is nonterminal
                    if post in self.rules:  # post is nonterminal
                        self.follow[cur].update(self.first[post]-empty_symbol)
                    elif post == r'\epsilon' or post in self.contains_empty:
                        to_union.append((cur,left)) # follow(cur) contains follow(left)
                    else:
                        self.follow[cur].add(post)
        to_union.append((None,None)) # add the terminal symbol
        has_enlarged = False
        while to_union:
            tail,left = to_union.popleft()
            if left is None:
                if not has_enlarged:
                    break
                else:
                    has_enlarged = False
                    to_union.append((None,None))
            else:
                set_, subset = self.follow[tail], self.follow[left] 
                new_set = set_.union(subset)
                if set_ != new_set:
                    has_enlarged = True
                    self.follow[tail] = new_set
                to_union.append((tail,left))
