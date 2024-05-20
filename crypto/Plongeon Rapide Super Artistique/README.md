# Write-Up 404-CTF : Plongeon Rapide Super Artistique

__Catégorie :__ Cryptanalyse - Moyen

**Enoncé :**

![Enoncé](images/enonce.png)

**Résolution :**

Dans ce challenge, on nous propose de déchiffrer un message chiffré à l'aide d'une variante de RSA, utilisant les polynômes.

Ici, nous avons deux polynômes P et Q, de degré 7, généré aléatoirement mais premier entre eux. A partir de ces deux polynômes, on génère deux nombres premiers p et q, à partir d'un nombre aléatoire r. On a `p = P(r)` et `q = Q(r)`. Enfin, on nous donne N, le produit des polynômes et n, le produit de p et q.

Le but d'un challenge sur RSA est très souvent de réussir à factoriser n pour retrouver l'exposant de déchiffrement. Malheureusement, nous ne pouvons pas utiliser la fonction `factor()` de sagemath car les nombres p et q sont trop grands et la factorisation prendrait trop de temps. Par contre, on peut remarquer que `n = p * q = P(r) * Q(r) = N(r)`. Du coup, connaissant N et n, on peut retrouver r en calculant les racines du polynôme (N - n). De plus, même si la factorisation de n n'est pas possible, la factorisation de N quant à elle est quasi immédiate. On peut alors facilement retrouver p et q et déchiffrer le message donné.

```python
from Crypto.Util.number import long_to_bytes, isPrime

F = PolynomialRing(ZZ, "x")
x = F.gen()

N = 9621137267597279445*x^14 + 18586175928444648302*x^13 + 32676401831531099971*x^12 + 42027592883389639924*x^11 + 51798494845427766041*x^10 + 63869556820398134000*x^9 + 74077517072964271516*x^8 + 79648012933926385783*x^7 + 69354747135812903055*x^6 + 59839859116273822972*x^5 + 48120985784611588945*x^4 + 36521316280908315838*x^3 + 26262107762070282460*x^2 + 16005081865177344119*x + 5810204145325142255 
n = 60130547801168751450983574194169752606596547774564695794919298973251203587128237799602582911050022571941793197314565314876508860461087209144687558341117955877761335067848122512358149929745084363835027292307961660634453113069168408298081720503728087287329906197832876696742245078666352861209105027134133927
c = 15129303695051503318505193172155921684909431243538868778377472653134183034984012506799855760917107279844275732327557949646134247015031503441468669978820652020054856908495646419146697920950182671202962511480958513703999302195279666734261744679837757391212026023983284529606062512100507387854428089714836938
e = 65537

r = (N - n).roots()[0][0]
P, Q = N.factor()

p, q = int(P[0](r)), int(Q[0](r))

d = pow(e, -1, (p-1) * (q-1))
m = pow(c, d, n)

print(long_to_bytes(int(m)))
```

**Flag :** `404CTF{8rAv0_v0U5_r3u55I5532_av3c_8Ri0_c3773_p3RF0RMaNC3_0daCI3u23}`