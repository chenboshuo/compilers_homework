from collections import defaultdict, deque
import re
from typing import *
from IPython.display import display, Math, Latex 

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
        
        .. ipython:: python

            from LL1Parser import LL1Parser            
            g = [r"E \to T E'", 
                r"E' \to + T E | \epsilon ", 
                r"T \to F T", 
                r"T' \to *F T' | \epsilon ",
                r"F \to ( E ) | \textbf{id}"]     
            grammer = LL1Parser(g)

        To show the grammer you can call :meth:`LL1Parser.display_rules`

        :type rules: List[str]
        :ivar self.rules: the rules of the gammer, 
            `self.rules[T] = L`, 
            `L[i]= items`, 
            `items[k] = symbol`,
            where `T` is a terminal, 
            `i` is the index of alternatives
            `items` is the list of the symbols of a rule 
        :vartype self.rules: Dict[str,List[str]]
    """

    def __init__(self,rules:List[str]) -> None:
        """init the LL(1) grammer
        """
        # save rules
        self.rules = defaultdict(list)
        for rule in rules:
            alternatives = re.split('\|',rule) # find rules connect by |          
            first_part = alternatives[0].split()
            left = first_part[0] # the nonterminal can find in the first part
            self.rules[left].append(first_part[2:]) # add elements except left symbol and ->

            for alternative in alternatives[1:]:
                self.rules[left].append([alternative])
        
        # create first
        self.create_first()
    
    def display_rules(self,raw=False):
        """display  the latex code of the gammer

        :param raw: show the raw code, defaults to False
        :type raw: bool, optional
        """
        begin = r"\begin{array}{ll}" + "\n"
        end = r"\end{array}"+"\n"
        
        for left,rules in self.rules.items(): 
            s = "\t"+left + r" & \to "
            s += " ".join(rules[0])
            s += r" \\" + "\n"
            for r in rules[1:]:
                s+= "\t\t" + r"&\;\, |\;\," + " ".join(r) + r"\\" + "\n"
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
        self.first = defaultdict(set)
        can_emptystring = set()
        for left,rule in self.iter_rules():
            if rule[0] not in self.rules: # symbol rule[0] is terminal 
                self.first[left].add(rule[0])
                if rule[0] == r'\epsilon':
                    can_emptystring.add(left)
            else:
                nonterminals.append((left,rule))
        
        while nonterminals:
            left,rule = nonterminals.popleft()
            if rule[0] in self.first: # first symbol is nonterminal
                self.first[left].update(self.first[rule[0]])
            else: # pending
                nonterminals.append((left,rule)) 

            if rule[0] in can_emptystring: # first symbol can empty string
                if rule[1:]:
                    nonterminals.append((left,rule[1:]))

        

    def iter_rules(self) -> tuple:
        """iter all the rules

        :yield: the iterator of (left,rule)
        :rtype: Iterator[tuple]
        """
        
        for left,rules in self.rules.items():
            for rule in rules:
                yield (left,rule)

    def display_first_sets(self,raw=False):
        begin = r"\begin{array}{ll}" + "\n"
        end = r"\end{array}" + "\n"
        contents = begin
        for left,first_set in self.first.items():
            s = r"\mathrm{first}(" + left + r") &= \{" 
            s += ", ".join(list(first_set))
            s += r"\} \\"
            contents += s
        contents += end
        if raw:
            print(contents)
        
        display(Math(contents))
        
