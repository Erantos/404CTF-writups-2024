# Write-Up 404-CTF : Bébé nageur

__Catégorie :__ Cryptanalyse - Intro

**Enoncé :**

![Enoncé](images/enonce.png)

**Résolution :**

Dans ce challenge, nous devons déchiffrer un message qui a été chiffré grâce au script `challenge.py`.

En analysant le script, on voit la fonction `encrypt()` appliquer la fonction `f()` sur chacun des caractères du flag. La fonction `f()` est une simple transformation affine modulo n qui transforme un caractère en un autre. On connait n mais malheureusement, a et b sont inconnus.

Heureusement, on sait que le flag doit commencer par `404CTF`. Donc le 4 devient - et le 0 devient 4. Nous avons donc deux points et une équation de droite affine, c'est donc suffisant pour retrouver a et b comme nous le ferions pour une droite classique. Le fait que nous appliquons un modulo n ne rajoute pas de complexité, il suffira de se placer dans un anneau d'entier plutôt que dans l'ensemble des enties naturels.

Pour résoudre ce problème, j'utilise la librarie Python Sagemath qui dispose de tout un tas de fontions et de classes utiles pour faire des maths en python.

```python
cipher = "-4-c57T5fUq9UdO0lOqiMqS4Hy0lqM4ekq-0vqwiNoqzUq5O9tyYoUq2_"
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-!"

n = len(charset)
R = IntegerModRing(n) # Sagemath handle n moduli automatically in this structure

x0 = R(charset.index('4'))
x1 = R(charset.index('0'))
y0 = R(charset.index(cipher[0]))
y1 = R(charset.index(cipher[1]))

# Finding a and b
a = (y1 - y0) / (x1 - x0)
b = y0 - a * x0

# Decoding flag
flag = ""
for c in cipher:
    y = charset.index(c)
    x = (y - b) / a
    flag += charset[x]

print(flag)
```

Et voilà ! Le tour est joué ! On a plus qu'à lancer le script avec `sage script.sage`.

**Flag :** `404CTF{Th3_r3vEnGE_1S_c0minG_S0oN_4nD_w1Ll_b3_TErRiBl3_!}`