# Semaine 1 — Fondamentaux Python

Notebook : `week1.ipynb`

Tout ce que j'ai fait pour poser les bases. Les cellules contiennent
l'énoncé, mon code, et parfois mes commentaires sur ce que je n'avais pas
compris au début.

## Ce que j'ai couvert

- types de base et conversions (`int()`, `str()`, `type()`)
- listes (indexation, `append`, `remove`, `len`, `in`)
- tuples (immutabilité, unpacking)
- dictionnaires (accès par clé, `items()`, `get()`)
- conditions `if / elif / else` et opérateurs logiques
- boucles `for` et `while`, avec `break` et `continue`
- fonctions avec `return`, paramètres, et le piège des fonctions qui
  modifient en place (`.append()` renvoie `None`)
- manipulation de chaînes (`strip`, `split`, slicing)
- lecture / écriture de fichiers avec `with open(...)`
- premières regex avec `re.findall` et `re.search`

## Difficultés rencontrées

- `x = x.append(...)` qui renvoie `None`
- `line.split()` sans stocker le résultat
- la variable `list` qui écrase le built-in Python
- l'ordre des arguments dans `sorted(..., key=lambda x: x[1], reverse=True)`

Le notebook garde la trace de ces erreurs et des corrections.
