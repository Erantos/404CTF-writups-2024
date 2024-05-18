# Write-Up 404-CTF : Discord

__Catégorie :__ Divers - Intro

**Enoncé :**

![Enoncé](images/enonce.png)

**Résolution :**

Ce challenge est un grand classique. Rejoindre le serveur Discord et retrouver le flag caché dedans. Rien de plus simple, sauf quand le café vous y est offert... ☕

Pour retrouver le flag, il suffit d'utiliser la fonction "Rechercher" de Discord et de taper le début du flag, soit "404CTF".

_Astuce_ : Dans ce genre de challenge, les créateurs cachent souvent le flag dans un channel qui ne peut pas être flood, ici dans annonces. Cela permettait de réduire les résultats, puisque Discord ne prend pas en compte les accolades dans la recherche.

![Image1](images/image1.png)

**Flag :** `404CTF{C'estparti!une!deux!une!deux}`