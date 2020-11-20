from collections import defaultdict
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
        
        .. code-block:: python
            from LL1Parser import LL1Parser            
            g = [r"E \to T E'", 
                r"E' \to + T E | \epsilon ", 
                r"T \to F T", 
                r"T' \to *F T' | \epsilon ",
                r"F \to ( E ) | \textbf{id}"]     
            grammer = LL1Parser(g)

        :type rules: List[str]


    """

    def __init__(self,rules:List[str]) -> None:
        """init the LL(1) grammer
        """


        self.rules = defaultdict(list)
        for rule in rules:
            alternatives = re.split('\|',rule) # find rules connect by |          
            first_part = alternatives[0].split()
            left = first_part[0] # the nonterminal can find in the first part
            self.rules[left].append(first_part[2:]) # add elements except left symbol and ->

            for alternative in alternatives[1:]:
                self.rules[left].append([alternative])
    
    def display(self,raw=False):
        """display  the latex code of the gammer

        :param raw: show the raw code, defaults to False
        :type raw: bool, optional
        """
        begin = r"\begin{array}{l}" + "\n"
        end = r"\end{array}"
        
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
        

