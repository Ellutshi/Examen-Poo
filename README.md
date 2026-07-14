#  EduManager

## Description

**EduManager** est une application de gestion scolaire développée en **Python** dans le cadre d'un projet de Programmation Orientée Objet (POO).

Elle permet de gérer efficacement l'ensemble des informations relatives à un établissement scolaire grâce à une interface graphique intuitive développée avec **Tkinter** et une base de données **SQLite**.

---

#  Fonctionnalités

L'application offre les fonctionnalités suivantes :

##  Gestion des étudiants

- Ajout d'un étudiant
- Modification des informations
- Suppression d'un étudiant
- Recherche multicritère
- Consultation des informations complètes
- Gestion des informations personnelles
- Gestion des informations scolaires
- Gestion financière
- Gestion des parents ou tuteurs
- Gestion médicale
- Gestion des documents
- Gestion de la présence et de la discipline

---

## Gestion des cours

- Ajout d'un cours
- Modification du nom d'un cours
- Suppression d'un cours
- Classement des cours par classe
- Catégorisation des cours
- Visualisation des élèves par classe

---

## Gestion des bulletins

- Création des évaluations
- Enregistrement des cotes
- Consultation des résultats
- Génération automatique des bulletins
- Calcul des résultats par période

---

##  Gestion des utilisateurs

- Authentification sécurisée
- Gestion des rôles

Types d'utilisateurs :

- Administrateur
- Enseignant
- Éleve

---

# Technologies utilisées

- Python 3.10+
- Tkinter
- SQLite
- Programmation Orientée Objet
- PEP 8

---

# Structure du projet

```
EduManager/
│
├── main.py
├── database.py
├── services.py
├── models.py
├── factory.py
├── exceptions.py
│
├── login_view.py
├── dashboard_view.py
├── student_view.py
├── course_view.py
├── bulletin_view.py
│
├── edumanager.db
└── README.md
```

---

# Architecture utilisée

Le projet suit une architecture en couches.

```
Interface Graphique (Views)
            │
            ▼\
Modèles (Models)
            │
            ▼
Services Métier (Services)
            │
            ▼
Base de données SQLite
```

Cette architecture permet :

- une meilleure organisation ;
- une maintenance facilitée ;
- une meilleure évolutivité du projet.

---

#  Concepts POO utilisés

## Encapsulation

Les données des objets sont protégées grâce aux attributs privés et aux méthodes d'accès.

Exemple :

```python
self.__nom
```

---

## Héritage

Les différents types d'utilisateurs héritent d'une classe commune.

```
Utilisateur
│
├── Administrateur
├── Enseignant
└── EtudiantUtilisateur
```

---

## Polymorphisme

Les utilisateurs possèdent un comportement spécifique selon leur rôle.

---

## Abstraction

Les services masquent les détails techniques de la base de données afin de simplifier leur utilisation.

---

## Composition

Les différentes vues utilisent les services métier afin d'effectuer les opérations sur les données.

---

# Design Patterns utilisés

Le projet implémente plusieurs Design Patterns.

## Singleton

Utilisé pour la connexion à la base de données.

```
DatabaseConnection
```

Une seule connexion SQLite est créée durant toute l'exécution de l'application.

---

## Factory

Utilisé pour créer automatiquement le bon type d'utilisateur.

```
UtilisateurFactory
```

---

# Persistance des données

Les données sont stockées dans une base de données **SQLite**.

Les informations sauvegardées comprennent notamment :

- étudiants ;
- utilisateurs ;
- cours ;
- évaluations ;
- bulletins ;
- informations financières ;
- informations médicales.

Toutes les données sont conservées après la fermeture de l'application.

---

# Sécurité

L'application réalise plusieurs validations :

- matricule numérique uniquement ;
- champs obligatoires ;
- unicité du matricule ;
- validation des dates ;
- validation des montants ;
- validation des rôles.

---

# Installation

## 1. Cloner le projet

```bash
git clone https://github.com/Ellutshi/EduManager.git
```

ou télécharger le projet.

---

## 2. Installer Python

Télécharger Python :

https://www.python.org

---

## 3. Lancer l'application

```bash
python main.py
```

---

# Compte administrateur

Par défaut :

**Nom d'utilisateur**

```
admin
```

**Mot de passe**

```
admin1234
```

---

# Règles de développement

Le projet respecte :

- PEP 8
- Programmation Orientée Objet
- Architecture en couches
- Séparation Interface / Métier / Données
- Code documenté avec Docstrings

---

#  Perspectives d'amélioration

Des évolutions peuvent être ajoutées :

- export PDF des bulletins ;
- export Excel ;
- statistiques graphiques ;
- impression des cartes d'élèves ;
- sauvegarde automatique ;
- tableau de bord interactif ;
- gestion multi-utilisateurs ;
- notifications.

---

# Auteur

Projet réalisé par :

**Elia Tshibangu Lubamba**

Licence Informatique

Projet de Programmation Orientée Objet

2026

---

# Licence

Projet académique réalisé dans un cadre pédagogique.

Tous droits réservés © 2026.
