# Scanner de ports asynchrone

`async_scanner.py` teste plusieurs ports TCP en même temps sur une adresse donnée. J’utilise `asyncio` pour lancer les connexions parallèlement au lieu d’attendre la fin de chaque port avant de passer au suivant.

## Avertissement légal

Scanner uniquement `127.0.0.1` ou les machines que vous possédez. Scanner une machine sans autorisation est illégal. J’utilise cet outil uniquement sur ma machine locale.

## Utilisation

La plage par défaut va de 20 à 1000.

```bash
python3 async_scanner.py 127.0.0.1
```

Pour vérifier plusieurs ports précis :

```bash
python3 async_scanner.py 127.0.0.1 22 80 443
```

Pour vérifier une plage :

```bash
python3 async_scanner.py 127.0.0.1 20-100
```

## Exemple de sortie

```text
Scanning 127.0.0.1 (4 ports) ...

[OPEN    ] Port 22
[CLOSED  ] Port 80
[FILTERED] Port 443
[CLOSED  ] Port 500

Summary: 1 open, 2 closed, 1 filtered
Time: 1.02s
```

## Résultats possibles

- `OPEN` : le port accepte une connexion TCP.
- `CLOSED` : l’adresse répond, mais refuse la connexion sur ce port.
- `FILTERED` : aucune réponse n’est reçue avant la fin du délai d’une seconde. Un pare-feu peut avoir bloqué le trafic.

## Asynchrone ou séquentiel

Avec le mode séquentiel, le programme teste un port puis attend sa réponse avant d’essayer le suivant. Avec `asyncio`, les tentatives sont lancées ensemble et le programme reprend les résultats au fur et à mesure.

Sur localhost, le gain peut être limité avec des ports fermés, surtout si les réponses arrivent rapidement. Sur une plage plus grande ou avec un délai plus long, l’approche asynchrone évite d’attendre chaque connexion séparément.

## Ce que j’ai appris

J’ai utilisé `asyncio.gather()` pour démarrer toutes les connexions en même temps. J’ai aussi utilisé `wait_for()` pour éviter qu’une connexion reste bloquée plus d’une seconde.

J’ai dû vérifier séparément les exceptions `ConnectionRefusedError`, `TimeoutError` et `OSError`, car elles donnent des résultats différents : port fermé, filtre ou erreur de connexion.
