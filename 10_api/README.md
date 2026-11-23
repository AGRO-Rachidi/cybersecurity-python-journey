# Vérificateur VirusTotal

`vt_lookup.py` interroge VirusTotal à partir d’un hash, d’un fichier contenant des hash ou d’une URL. Il affiche le verdict de VirusTotal et, si ces informations sont disponibles, le nom du fichier, son type et sa date de première soumission.

## Pré-requis

1. Créer un compte VirusTotal : https://www.virustotal.com/gui/join-us
2. Récupérer sa clé API : https://www.virustotal.com/gui/my-apikey
3. La rendre disponible dans le terminal :

```bash
export VT_API_KEY="ta_cle_ici"
```

4. Installer `requests` :

```bash
pip install requests
```

Chaque utilisateur doit utiliser sa propre clé API. L’outil ne contient pas de clé, et chaque compte a son propre quota. Je ne mets pas de secret dans le code.

## Utilisation

### Un hash

```bash
python3 vt_lookup.py e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

### Un fichier de hash

Le fichier peut contenir un hash par ligne. Le script prend le premier élément de chaque ligne.

```text
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

```bash
python3 vt_lookup.py --file hashes.txt
```

### Une URL

```bash
python3 vt_lookup.py --url https://example.com
```

## Exemple de sortie

```text
[✓] https://example.com
    Verdict: CLEAN (0/85 detections)
    Name: example.com
    Type: URL
    First seen: 2026-11-20
```

Les informations et le nombre de détections varient selon le résultat renvoyé par VirusTotal. Si l’élément n’est pas trouvé, le script affiche `NOT FOUND`.

## Limite de requêtes

Le quota gratuit est de 4 requêtes par minute. En mode `--file`, le script attend 15 secondes entre les lignes avec `time.sleep(15)`. Les modes hash unique et URL n’ont pas cette attente.

## Ce que j’ai appris

Pour interroger une URL, je ne peux pas simplement la mettre à la fin de l’adresse de l’API : VirusTotal attend un identifiant encodé. Dans le script, je l’encode en base64 URL-safe et j’enlève les `=` à la fin.

J’ai aussi mis la clé dans `VT_API_KEY` plutôt que dans le fichier Python. Si elle n’est pas définie, le script affiche comment l’ajouter et s’arrête.
