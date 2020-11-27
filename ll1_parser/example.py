# ---
# jupyter:
#   jupytext:
#     formats: ipynb,md,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: ~ython3
# ---

# # test a LL(1) grammar

# ## input a ll(1) grammar

from IPython.display import display, Math, Latex 

g = [r"E \to T E'", 
     r"E' \to + T E' | \epsilon ", 
     r"T \to F T'", 
     r"T' \to * F T' | \epsilon ",
     r"F \to ( E ) | \textbf{id}"]

for item in g:
    display(Math(item)) 

from LL1Parser import LL1Parser
import importlib
import sys
importlib.reload(sys.modules['LL1Parser'])
from LL1Parser import LL1Parser

grammer = LL1Parser(g)

# ## store and display the rules

grammer.rules

grammer.display_rules(raw=True)

# ## calculate and see the first,follow sets

grammer.display_first_sets()

grammer.display_follow_sets()

# ## create and display the parsing table

grammer.parsing_table

grammer.display_parsing_table(raw=True)

# # test a wrong grammer

w = [r"S \to i E t S S' | a",
    r"S' \to e S | \epsilon",
    r"E \to b"]
for g in w:
    display(Math(g))

wrong = LL1Parser(w)
