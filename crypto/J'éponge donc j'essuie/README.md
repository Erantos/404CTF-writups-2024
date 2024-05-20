# Write-Up 404-CTF : J'éponge donc j'essuie

__Catégorie :__ Cryptanalyse - Moyen

**Enoncé :**

![Enoncé](images/enonce.png)

**Résolution :**

Dans ce challenge, nous devons nous connecter à un serveur afin que celui-ci nous envoie un hash et nous devons lui répondre avec une entrée en hexadécimal pour provoquer une collision de hash, c'est à dire, trouver une entrée différente de celle du serveur mais qui produira le même hash en sortie.

La première étape est d'analyser et de comprendre le code. Le classe Bob prend en argument la donnée à hasher. Cette donnée est convertie en liste de bits avec la fonction `bytes2binArray()` puis la fonction `hexdigest()` permet de créer le hash puis de le convertir chaîne hexadécimal. Le hash provient de la variable `state` qui est initialisé à 0 puis mise à jour en fonction de la donnée, dans les fonctions `_f()` et `_absorb()`

En s'intéressant de plus près à la fonction `_absorb()`, on voit que la donnée est traitée par bloc de 32 bits, qu'un XOR est appliqué entre le début de `state` et le bloc de données, puis l'état est complètement mélangé dans la fonction `_f()` grâce à un tableau de permutation. Malheureusement, le tableau de permutation est bien pensé et ne laisse apparaitre aucun pattern que nous pourrions utiliser lors d'un exploit. Il va donc falloir trouver une entrée qui soit différente de la donnée initiale, mais dont l'état initial de la classe Bob soit le même. PLus formellement, on veut trouver `data2` tel que `data != data2` mais `self.data == self.data2`.

Notre analyse se tourne donc sur la fonction `bytes2binArray()`. Cette fonction transforme les octets en bits et ajoute un petit padding à gauche pour compléter l'octet initial (101 => 00000101) et ajoute aussi un padding à droite afin d'atteindre une bonne taille de bloc. La faille vient de la première ligne `b = bin(bytes_to_long(b))[2:]`. En effet, l'utilisation de la fonction `bytes_to_long()` ignore complètement les octets `00` placé à gauche. Nous allons donc pouvoir exploiter cette faille en ajoutant un padding à gauche rempli de `00`.

Cependant, il reste un dernier problème : l'ajout des longueurs en début et fin de donnée dans le constructeur, juste avant l'appel à `bytes2binArray()`, soit la ligne `data = long_to_bytes(len(data)%256)+data+long_to_bytes(len(data)%256)`. Si on modifie la longueur de la donnée en entrée, cela modifiera le `self.data`, sauf si on choisit un hash de longueur multiple de 256. Le modulo passera fera 0 et notre modification passera inaperçu.

Il ne reste plus qu'à écrire un script python permettant de forger la bonne entrée et l'envoyer au serveur.

```python
from pwn import *

context.log_level = "debug"

r = remote("challenges.404ctf.fr", 31952)

r.recvuntil(b"of hash : ")
hash = r.recvline().decode()[:-1]
r.recvuntil(b"> ")

hash = "10" + hash + "10" # Add length as Bob() do
hash = "0" * (512 - len(hash)) + hash # Add padding (512 hex char = 256 bytes)

r.sendline(hash.encode())

r.recvall(timeout=2)
r.close()
```

**Flag :** `404CTF{p4dD1nG_1s_A_tRIckY_0p3r@TiOn_bUt_g0od_cHeckS_aR3_aN_H4rd3r_0n3}`