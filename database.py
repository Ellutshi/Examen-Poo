"""Gestion de la base de données SQLite avec Singleton."""

import sqlite3
from sqlite3 import Connection

from exceptions import ConnexionBDDException

DB_NAME: str = "edumanager.db"


class DatabaseConnection:
    """Connexion unique à SQLite grâce au Design Pattern Singleton."""

    _instance: "DatabaseConnection | None" = None
    connection: Connection

    def __new__(cls) -> "DatabaseConnection":
        """Crée une seule instance de connexion."""

        if cls._instance is None:
            cls._instance = super().__new__(cls)

            try:
                cls._instance.connection = sqlite3.connect(DB_NAME)
            except sqlite3.Error as error:
                raise ConnexionBDDException(
                    f"Erreur de connexion : {error}"
                ) from error

        return cls._instance

    def create_tables(self) -> None:
        """Crée toutes les tables de la base de données."""

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS etudiants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricule TEXT UNIQUE NOT NULL,
                nom TEXT NOT NULL,
                postnom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                sexe TEXT NOT NULL,
                date_naissance TEXT,
                lieu_naissance TEXT,
                nationalite TEXT,
                etat_civil TEXT,
                photo TEXT,
                classe TEXT NOT NULL,
                option_etude TEXT,
                section TEXT,
                annee_scolaire TEXT,
                numero_inscription TEXT,
                date_inscription TEXT,
                statut TEXT,
                adresse TEXT,
                ville TEXT,
                commune TEXT,
                quartier TEXT,
                telephone TEXT,
                email TEXT,
                nom_pere TEXT,
                telephone_pere TEXT,
                nom_mere TEXT,
                telephone_mere TEXT,
                nom_tuteur TEXT,
                telephone_tuteur TEXT,
                profession_tuteur TEXT,
                adresse_tuteur TEXT,
                montant_total REAL DEFAULT 0,
                montant_paye REAL DEFAULT 0,
                mode_paiement TEXT,
                date_dernier_paiement TEXT,
                groupe_sanguin TEXT,
                allergies TEXT,
                maladies TEXT,
                personne_urgence TEXT,
                telephone_urgence TEXT,
                acte_naissance TEXT,
                bulletin_precedent TEXT,
                certificat_medical TEXT,
                attestation TEXT,
                presences INTEGER DEFAULT 0,
                absences_justifiees INTEGER DEFAULT 0,
                absences_non_justifiees INTEGER DEFAULT 0,
                retards INTEGER DEFAULT 0,
                avertissements INTEGER DEFAULT 0,
                sanctions TEXT,
                recompenses TEXT,
                observation TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                classe TEXT NOT NULL,
                section TEXT,
                categorie TEXT NOT NULL,
                credit INTEGER DEFAULT 1,
                UNIQUE(nom, classe)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricule TEXT NOT NULL,
                cours TEXT NOT NULL,
                note REAL NOT NULL,
                pourcentage REAL,
                mention TEXT,
                decision TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricule TEXT NOT NULL,
                nom_complet TEXT NOT NULL,
                classe TEXT NOT NULL,
                cours TEXT NOT NULL,
                type_evaluation TEXT NOT NULL,
                cote REAL NOT NULL,
                date_evaluation TEXT NOT NULL
            )
            """
        )

        self.connection.commit()
        cursor.close()

        self.insert_default_admin()

    def insert_default_admin(self) -> None:
        """Crée le compte administrateur s'il n'existe pas."""

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM utilisateurs
            WHERE username = ?
            """,
            ("admin",),
        )

        admin = cursor.fetchone()

        if admin is None:
            cursor.execute(
                """
                INSERT INTO utilisateurs (
                    nom,
                    username,
                    password,
                    role
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    "Administrateur",
                    "admin",
                    "admin1234",
                    "admin",
                ),
            )

        self.connection.commit()
        cursor.close()

    def close(self) -> None:
        """Ferme la connexion SQLite."""

        self.connection.close()


if __name__ == "__main__":
    database = DatabaseConnection()
    database.create_tables()
    print("Base de données créée avec succès.")