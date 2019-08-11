**Cette documentation est en cours de rédaction, elle ne permet pas l'installation du site django_education à ce jour.**

Le projet django_education est un site internet réalisé à partir de [Django](https://www.djangoproject.com/). 

Il permet à un professeur de:
 - partager ses ressources,
 - travailler par compétences,
 - proposer à ses élèves des QCM.

Il est construit à partir des applications suivantes:
 - [django-jchart](https://github.com/matthisk/django-jchart) une application pour configurer et générer des graphiques [Chart.js](http://www.chartjs.org/),
 - [django_quiz](https://github.com/tomwalker/django_quiz) une application pour créer et gérer des quizzes,


# Installation


## Présentation

Cette présentation s'adresse au utilisateur n'ayant de connaissances particulières quant à la conception, la mise en oeuvre et l'hébergement d'un site web.
Pour mettre en oeuvre ce site en utilisant la démarche suivante, il suffit:
 - d'une carte [Rapsberry Pi](https://www.raspberrypi.org/),
 - d'une box internet classique équipée d'un port RJ45 ou du Wifi,

Bien sûr, ces explications peuvent être détournées pour ceux qui veulent adapter l'installation à leur convenance.

**Il faudra au préalable avoir installé [Raspbian](https://www.raspberrypi.org/downloads/) sur la carte Rapsberry Pi et avoir un accès SSH, des tutoriels sont disponibles sur internet à cet effet, en cas de besoin, me contacter.**

Se connecter en SSH sur la carte Raspberry Pi à l'adresse IP qui lui a été attribuée, (dans l'exemple suivant, ce sera 192.168.0.7, une adresse d'une réseau local).

```
ssh pi@192.168.0.7
```

Par défaut, le mot de passe est raspberry, il est conseillé de le changer.

```
sudo raspi-config
```

## Installation de python, pip et virtualenv

Normalement `python3` est déjà installé par défaut sur Raspbian, pour le tester tapper `python3` dans un terminal. Pour l'installer, la commande est:

```
sudo apt-get install python3
```

De même, normalent `pip` est déjà installé par défaut sur Raspbian, pour le tester tapper `pip` dans un terminal. Pour l'installer, la commande est:

```
sudo apt-get install python3-pip
```

`virtualenv` est un paquet qui permet d'associer une configuration et des librairies python à un projet. Pour installer `virtualenv` tapper:

```
pip install virtualenv
```

## Préparation de l'installation

Créer un dossier `\django` à la racine de votre Raspberry Pi, changer l'utilisateur associé au dossier et accéder au dossier.

```
sudo mkdir \django
sudo chown pi:pi \django
cd \django
```

Créer l'environnement `virtualenv` et l'activer.

```
virtualenv myenv
source myenv/bin/activate
```

Si tout s'est bien passé, `(myenv)` apparaît en début de ligne de commande, cela signifie que toutes les bibliothèques python que vous allez installer à partir de maintenant le seront dans cet environnement.

## Installation de l'applicaiton django-education et django_quiz

Tapper les commandes suivantes.

```
git clone https://github.com/tomwalker/django_quiz.git
git clone https://github.com/costadoat/django_education.git
```

```
cd django_quiz
pip install -r requirements.txt
python setup.py install
```
