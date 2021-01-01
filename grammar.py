from typing import * # List
from collections import defaultdict
from IPython.display import display, Math


class Grammar:
    """the class represent a grammer
    """
    def __init__(self,rules: List[str], start_symbol: str = None):
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

        self.terminals: set = set()
        """
        The list of terminals in table parsing table
        (include $, not include :math:`\epsilon`)
        """

        for rule in rules:
            alternatives = rule.split('|')  # find rules connect by |
            first_part = alternatives[0].split()
            left = first_part[0]  # the nonterminal can find in the first part
            # add elements except left symbol and ->
            self.rules[left].append(first_part[2:])
            self.terminals.update(first_part[2:])

            for alternative in alternatives[1:]:
                alternative_symbols = alternative.split()
                self.rules[left].append(alternative_symbols)
                self.terminals.update(alternative_symbols)

            self.terminals = self.terminals - \
                set(self.rules.keys()) - set([r'\epsilon'])
            self.terminals.update([r'\$'])

        self.contains_empty: set = set([r'\epsilon'])
        """the set of terminals that contains empty strings
        """

    def display_rules(self, raw=False):
        """display  the latex code of the gammer

        :param raw: show the raw code, defaults to False
        :type raw: bool, optional
        """
        begin = r"\begin{array}{ll}" + "\n"
        end = r"\end{array}"+"\n"

        for left, rules in self.rules.items():
            s = self.display_rule(left, rules[0])
            for r in rules[1:]:
                s += self.display_rule(left, rule=r, is_alternative=True)
            begin += s

        if raw:
            print(begin+end)

        display(Math(begin+end))

    def display_rule(self, left: str,
                     rule: List[str], new_line=True,
                     array_environment=True,
                     is_alternative=False) -> str:
        """display a rule

        :param left: left symbol
        :type left: str
        :param rule: the list of the rule
        :type rule: List[str]
        :param new_line: whether need a new line at the end, defaults to True
        :type new_line: bool, optional
        :param array_environment: whether the expression in array environment
        :type array_environment: bool
        :param is_alternative: whether the rule is the alternative, defaults to False
        :type is_alternative: bool, optional
        :return: the latex string of the rule
        :rtype: str
        """
        if not is_alternative:  # need left symbol
            s = "\t"+left
            if array_environment:
                s += r" & "  # TODO handle the & symbol
            s += r" \to "
        else:
            s = "\t\t"
            if array_environment:
                s += r"&"
            s += r"\;\, |\;\,"

        s += " ".join(rule)
        if new_line:
            s += r" \\" + "\n"

        return s

    def iter_rules(self) -> tuple:
        """iter all the rules

        :yield: the iterator of (left,rule)
        :rtype: Iterator[tuple]
        """

        for left, rules in self.rules.items():
            for rule in rules:
                yield (left, rule)