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

# ## input a ll(1) grammar

from IPython.display import display, Math, Latex 

g = [r"E \to T E'", 
     r"E' \to + T E | \epsilon ", 
     r"T \to F T", 
     r"T' \to *F T' | \epsilon ",
     r"F \to ( E ) | \textbf{id}"]

for item in g:
    display(Math(item)) 

from LL1Parser import LL1Parser
import importlib
import sys
importlib.reload(sys.modules['LL1Parser'])
from LL1Parser import LL1Parser

grammer = LL1Parser(g)

grammer.rules

grammer.display(raw=True)


