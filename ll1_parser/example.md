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

## input a ll(1) grammar

```python
from IPython.display import display, Math, Latex 
```

```python
g = [r"E \to T E'", 
     r"E' \to + T E | \epsilon ", 
     r"T \to F T", 
     r"T' \to *F T' | \epsilon ",
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

```python
grammer.rules
```

```python
grammer.display()
```

```python

```
