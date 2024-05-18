# Write-Up 404-CTF : Légende

__Catégorie :__ Renseignement en sources ouvertes - Intro

**Enoncé :**

![Enoncé](images/enonce.png)

**Résolution :**

Dans ce challenge d'intro, on nous propose de retrouver une légende du ski français à partir d'une photo, ainsi que le lieu dans lequel cette personne à décrocher son titre de champion.

![Photo](photo.png)

Bon... la photo n'aide pas vraiment. A moins d'un miracle, il va falloir trouver une autre piste (sans mauvais jeu de mot).

Je décide alors de m'intéresser au champions de ski français et je tombe sur la liste de tous les champions de ski alpin : https://fr.wikipedia.org/wiki/Liste_des_champions_du_monde_de_ski_alpin_par_épreuve.

On remarque que 2 français se démarquent : Émile Allais et Jean-Claude Killy. Je continue mes recherches en commençant par m'intéresser à Emile Allais (1er de la liste, et l'époque colle bien à la qualité de l'image).

Les recherches ont été fructueuses puisqu'en recherchant "emile allais arrivée ski" sur Google, je suis finalement tombé sur un hommage à Emile Allais sur Dailymotion : https://www.dailymotion.com/video/xp3chi. A la toute fin de cette vidéo, on reconnait clairement notre image, ce qui confirme la piste.

Il ne reste plus qu'à trouver la ville dans laquelle il a remporté ses 3 titres de champions du monde. Il les a gagnés en 1937 et les JO de 1937 ont eu lieu à Chamonix.

**Flag :** `404CTF{emile-allais_chamonix}`