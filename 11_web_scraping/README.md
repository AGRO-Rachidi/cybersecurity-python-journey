# Extracteur de liens web

`web_scraper.py` récupère une page web puis extrait les liens contenus dans ses balises HTML. Il affiche les URLs trouvées avec leur texte visible.

J’ai fait ce petit outil pour essayer `requests` et `BeautifulSoup` ensemble.

## Pré-requis

```bash
pip install beautifulsoup4 requests
```

## Utilisation

```bash
python3 web_scraper.py <url>
```

Par exemple :

```bash
python3 web_scraper.py https://example.com
```

Le script doit recevoir une URL complète, avec `http://` ou `https://`.

## Exemple de sortie

```text
Liens trouvés sur https://example.com :

https://example.com/docs
    Texte : Documentation
https://example.com/about
    Texte : À propos
mailto:contact@example.com
    Texte : Contact
```

Les liens affichés peuvent être absolus ou relatifs selon le contenu de la page. S’il n’y a pas de texte dans le lien, le script affiche seulement l’URL.

## Ce que j’ai appris

J’ai commencé par récupérer le contenu HTTP avec `requests`, puis je l’ai donné à `BeautifulSoup` pour chercher les balises `<a>`.

Au début, je vérifiais chaque lien avec `if link.startswith("http")`, mais cela excluait des adresses comme `mailto:`. J’ai gardé tous les liens contenant un attribut `href`, plutôt que de deviner leur type.
