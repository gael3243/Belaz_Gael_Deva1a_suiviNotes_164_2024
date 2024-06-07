# Module 164 2024.06.07

# Important :
Concernant le delete des apprentis, s'ils sont liés à une note, l'apprenti ne peut pas être effacer.
Pour que le test fonctione correctement, les apprentis ayant un ID de 3 à 7 ne peuvent pas être effacer.
Cependant ceux ayant un ID de 22 à 26 peuvent être effacer.

## Installation requise

### 1. Pycharm
Pour que le proket fonctionne correctement vous aurez besoin de PyCharm.
https://www.jetbrains.com/fr-fr/community/education/#students

Lors de l'installation, il faut cocher toutes options ASSOCIATIONS, ADD PATH, etc...
Lors de la première ouverture de PyCharm, il faut choisir "New project" changer le répertoire pour ce nouveau projet
, il faut crée un répertoire "vide" sur votre disque local.

Il est important d'avoir sélectionné le répertoire que vous venez de crée car PyCharm va automatiquement créer un environnement
virtuel (.venv) dans ce répertoire.

Menu : File->Settings->Editor->General->Auto Import cocher "Show auto-import tooltip"

---

### 1.1 Gestionnaire de base de données
Vous aurez besoin d'un système de gestion de base de données, vous trouverez différent système au choix :

- Laragon : https://laragon.org/download/ 
- MAC : MAMP ou : https://www.codeur.com/tuto/creation-de-site-internet/version-mysql/

---

### 1.2 Python
La dernière installation requise est celle de python, vous trouvez toute les informations dont vous avez besoin :

- https://www.python.org/downloads/
- ATTENTION : Cocher la case pour que le “PATH” intègre le programme Python

- Une fois la case à cocher du PATH cochée, il faut choisir d’installer.

- Un peu avant la fin du processus d’installation, cliquer sur disabled length limit et cliquer sur CLOSE.

- Le test de Python se fait après avec le programme PyCharm.


--- 


### 2. Téléchargement
Afin d'obtenir le projet vous avez 2 possibilités, la première est de télécharger directement le fichier ZIP
depuis GIT.

La seconde est d'exécuter es commandes ci-dessous dans un terminal de commande :

cd C:\
git clone https://github.com/gael3243/Belaz_Gael_Deva1a_suiviNotes_164_2024 164_suiviNotes_GB
cd 164_suiviNotes_GB
rmdir /S/Q .git
python -m venv .venv
cd "C:\164_suiviNotes_GB\.venv\Scripts"
activate
cd C:\164_suiviNotes_GB
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Vos commandes ont été exécutées.
REM -- Pause jusqu'à ce qu'une touche soit pressée, puis ferme la fenêtre --
pause
exit

---

### 2.1 Ouverture du projet
Une fois le projet télécharger, il faut vous rendre dans PyCharm et cliqué dans le coin supérieur gauche sur "File"
et "Open project". Ensuite naviguer jusqu'à l'emplacement du fichier et doublie cliquer dessus.

---

### 2.2 Démarage
Premièrement il va falloir démarrer le serveur SQL. Ensuite se rendre sur PyCharm et ouvrir le fichier 
"APP_FILMS_164/database/1ImportationDumpSql.py" et l'éxecuter, en cas de problème il faut vous rendre dans le fichier
.env et contrôler les indications de connexion pour la base de données.

Ensuite ouvrir le fichier "APP_FILMS_164/database/2_test_connection_bd.py" et l'exécuter.

Une fois ceci fait, se rendre dans le fichier "run_mon_app.py" et l'exécuter.

Cliquer sur le lien bleu s'affichant dans le terminal de commande, vous aurez accès au proket et pourrez y naviguer librement





