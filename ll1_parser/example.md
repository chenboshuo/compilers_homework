---
jupyter:
  jupytext:
    formats: ipynb,md,py:light
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.3.3
  kernelspec:
    display_name: Python 3
    language: python
    name: ~ython3
---

# test a LL(1) grammar


## input a ll(1) grammar

```python
from IPython.display import display, Math, Latex 
```

```python
g = [r"E \to T E'", 
     r"E' \to + T E' | \epsilon ", 
     r"T \to F T'", 
     r"T' \to * F T' | \epsilon ",
     r"F \to ( E ) | \textbf{id}"]
```

```python
for item in g:
    display(Math(item)) 
```

```python
from LL1Parser import LL1Parser
import importlib
import sys
importlib.reload(sys.modules['LL1Parser'])
from LL1Parser import LL1Parser
```

```python
grammer = LL1Parser(g)
```

## store and display the rules

```python
grammer.rules
```

```python
grammer.display_rules(raw=True)
```

## calculate and see the first,follow sets

```python
grammer.display_first_sets(raw=True)
```

```python
grammer.display_follow_sets(raw=True)
```

## create and display the parsing table

```python
grammer.parsing_table
```

```python
grammer.display_parsing_table()
```

# test a wrong grammer

```python
w = [r"S \to i E t S S' | a",
    r"S' \to e S | \epsilon",
    r"E \to b"]
for g in w:
    display(Math(g))
```

```python
wrong = LL1Parser(w)
```

```python
wrong.display_rules(raw=True)
```

```python

```
