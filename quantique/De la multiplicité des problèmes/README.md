# Write-Up 404-CTF : De la multiplicité des problèmes

__Catégorie :__ Algorithmique quantique - Moyen

**Enoncé :**

![Enoncé](images/enonce.png)

**Résolution :**

Ce troisième challenge de quantique nous propose de nous intéresser aux systèmes multiples ainsi qu'à l'intrication quantique. L'énoncé se trouve dans le notebook `chall_3.ipynb`.

**Etape 1.a**

Cette première étape est relativement simple. Elle consiste en la transformation de l'état |00> en l'état |11>. Mon idée est donc d'utiliser une porte NOT sur chacun des qubits.

```python
step_one = Circuit(4).add(0, PERM([1, 0])).add(2, PERM([1, 0]))
# raise NotImplementedError

pdisplay(step_one)
```

**Etape 1.b**

La deuxième partie est aussi simple puisqu'il s'agit de reprendre la porte CNOT dont on nous parle depuis le début du challenge. On a vu précédemment qu'une porte d'Hadamard suivi d'un CNOT provoquait l'état `1/sqrt(2) (|00> + |11>)`. Ici, nous allons réutiliser cette structure et changer la porte d'Hadamard par un Beam Splitter (vu au challenge d'intro). Un theta de pi/3 suffit à obtenir les probas désirées.

```python
step_one_more = Circuit(8).add(0, BS(theta=np.pi/3)).add(0, cnot)
# raise NotImplementedError
```

**Etape 2**

Dans cette seconde étape, nous devons créer un circuit qui permet de repasser de la base de Bell dans la base canonique, en sachant que le passage de la base canonique à la base de Bell se fait avec une porte d'Hadamard et une porte CNOT. Sous cette formulation complexe se cache un problème plus simple : faire l'inverse de ce qui est fait. De plus, la porte CNOT et la porte d'Hadamard sont leur propre inverse, c'est à dire que deux CNOT s'annule entre eux (idem pour Hadamard). On n'a plus qu'à faire le circuit inverse de celui proposé en début d'étape 2.

```python
step_two = Circuit(8, "Passage Bell -> Canonique").add(0, cnot).add(0, BS.H())
# raise NotImplementedError
```

**Etape 3**

Cette dernière étape est de loin bien plus difficile (d'après moi) que les deux autres. J'ai longtemps cherché par moi même avant de finalement trouvé une réponse similaire sur stackexchange : https://quantumcomputing.stackexchange.com/a/9533.

Cette solution propose de faire une sorte de CNOT conditionnel, piloté par des portes Ry. Ce circuit permet d'obtenir 3 états équiprobables |00>, |01> et |10>. Cependant, dans le cadre du challenge, il faudrait remplacer l'état |00> par |11>, ce qui est possible en positionnant différemment les portes NOT.

```python
step_three = Circuit(8).add(0,BS.Ry(theta=2*np.arccos(sqrt(2/3)))).add(0, PERM([1,0])).add(2,BS.Ry(theta=np.pi/4)).add(0,cnot).add(2,BS.Ry(theta=-np.pi/4)).add(2, PERM([1,0]))
# raise NotImplementedError

pdisplay(step_three)
```

Une fois toutes ces étapes terminées, il n'y a plus qu'à envoyer les réponses au serveur et récupérer le flag.

**Flag :** `404CTF{d_Un3_tR1v14l1t3_AbS0lu3}`