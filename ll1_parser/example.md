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

# Example


## Test a LL(1) Grammar


### Input a LL(1) Grammar

```python
from IPython.display import display, Math
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

### Store and Display the Rules

```python
grammer.rules
```

```python
grammer.display_rules(raw=True)
```

### Calculate and See the First, Follow Sets

```python
grammer.display_first_sets(raw=True)
```

```python
grammer.display_follow_sets(raw=True)
```

### Create and Display the Parsing Table

```python
grammer.parsing_table
```

```python
grammer.display_parsing_table()
```

## Test a Wrong Grammer

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

```
