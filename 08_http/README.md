# Vérificateur de sécurité HTTP

Ce dossier contient un outil qui analyse une URL et vérifie ses
protections web : headers de sécurité, cookies, redirections, certificat TLS.

---

## `url_checker.py` — Analyse une URL

**À quoi ça sert ?**
Quand on veut savoir si un site web est bien configuré côté sécurité,
on vérifie plusieurs choses. Cet outil le fait en une seule commande.

**Comment l'utiliser ?**
python3 url_checker.py <url>


**Exemple :**
$ python3 url_checker.py https://github.com
URL: https://github.com
Status: 200
Final URL: https://github.com/
Server: github.com
Elapsed: 1.127s

=== Security Headers ===
[✓] Strict-Transport-Security: max-age=31536000; includeSubdomains; preload
[✓] Content-Security-Policy: default-src 'none'; ...
[✓] X-Frame-Options: deny
[✓] X-Content-Type-Options: nosniff
[✓] Referrer-Policy: origin-when-cross-origin
[✗] Permissions-Policy: MISSING

=== Cookies ===
[✓] _gh_sess
[✗] _octo (missing HttpOnly)
[✓] logged_in

=== Redirects ===
1 redirect(s):

1. 301 → http://github.com/
Final: https://github.com/

=== TLS Certificate ===
Subject: {'commonName': 'github.com'}
Issuer: {'organizationName': 'Sectigo Limited', ...}
Valid until: Jan 27 23:59:59 2027 GMT
Days left: 75


**Ce qu'il fait :**

1. **Headers de sécurité** — vérifie 6 headers standards :
   - `Strict-Transport-Security` (force HTTPS)
   - `Content-Security-Policy` (anti-XSS)
   - `X-Frame-Options` (anti-clickjacking)
   - `X-Content-Type-Options` (anti-MIME-sniffing)
   - `Referrer-Policy` (contrôle des référents)
   - `Permissions-Policy` (contrôle des APIs navigateur)

2. **Cookies** — vérifie que chaque cookie a :
   - `Secure` (envoyé uniquement en HTTPS)
   - `HttpOnly` (inaccessible au JavaScript)
   - `SameSite` (protection contre CSRF)

3. **Version serveur** — regarde le header `Server` pour voir la version

4. **Redirections** — liste la chaîne de redirections suivie

5. **Certificat TLS** — affiche sujet, émetteur, dates de validité,
   jours restants avant expiration

**Limitations :**
- Un header manquant n'est pas toujours une faille (dépend du contexte)
- Les cookies sans `HttpOnly` peuvent être normaux (accès JS intentionnel)
- Les CDN masquent les vrais serveurs

**Bibliothèques utilisées :**
- `requests` — pour faire la requête HTTP (à installer avec `pip install requests`)
- `ssl` — pour le certificat TLS
- `socket` — pour la connexion TLS
