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
#     display_name: venv
#     language: python
#     name: venv
# ---

# # Example

# ## Test a LL(1) Grammar

# ### Input a LL(1) Grammar

from IPython.display import display, Math

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

# ### Store and Display the Rules

grammer.rules

grammer.display_rules(raw=True)

# ### Calculate and See the First, Follow Sets

grammer.display_first_sets(raw=True)

grammer.display_follow_sets(raw=True)

# ### Create and Display the Parsing Table

grammer.parsing_table

grammer.display_parsing_table()

# ## Test a Wrong Grammer

w = [r"S \to i E t S S' | a",
    r"S' \to e S | \epsilon",
    r"E \to b"]
for g in w:
    display(Math(g))

wrong = LL1Parser(w)


