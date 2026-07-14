"""Services métier de l'application EduManager."""

import sqlite3
from datetime import datetime

from database import DatabaseConnection
from exceptions import EtudiantIntrouvableException
from factory import UtilisateurFactory
from models import Cours, Note, Utilisateur


DATE_FORMAT: str = "%d/%m/%Y"


class AuthService:
    """Service responsable de l'authentification."""

    def __init__(self) -> None:
        """Initialise le service."""
        self.db = DatabaseConnection()

    def login(self, username: str, password: str) -> Utilisateur | None:
        """Connecte un utilisateur."""
        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            SELECT nom, username, password, role
            FROM utilisateurs
            WHERE username = ?
            AND password = ?
            """,
            (username.strip(), password.strip()),
        )

        result = cursor.fetchone()
        cursor.close()

        if result is None:
            return None

        nom, db_username, db_password, role = result

        return UtilisateurFactory.creer_utilisateur(
            role,
            nom,
            db_username,
            db_password,
        )


class EtudiantService:
    """Service de gestion des étudiants."""

    def __init__(self) -> None:
        """Initialise le service."""
        self.db = DatabaseConnection()

    def ajouter(
        self,
        matricule: str,
        nom: str,
        postnom: str,
        classe: str,
        prenom: str = "Non défini",
        sexe: str = "Homme",
        **extra_data: str,
    ) -> None:
        """Ajoute un étudiant."""
        matricule = matricule.strip()

        if not matricule.isdigit():
            raise ValueError(
                "Le matricule doit contenir uniquement des chiffres."
            )

        cursor = self.db.connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO etudiants (
                    matricule,
                    nom,
                    postnom,
                    prenom,
                    sexe,
                    date_naissance,
                    lieu_naissance,
                    nationalite,
                    etat_civil,
                    photo,
                    classe,
                    option_etude,
                    section,
                    annee_scolaire,
                    numero_inscription,
                    date_inscription,
                    statut,
                    adresse,
                    ville,
                    commune,
                    quartier,
                    telephone,
                    email,
                    nom_pere,
                    telephone_pere,
                    nom_mere,
                    telephone_mere,
                    nom_tuteur,
                    telephone_tuteur,
                    profession_tuteur,
                    adresse_tuteur,
                    montant_total,
                    montant_paye,
                    mode_paiement,
                    date_dernier_paiement,
                    groupe_sanguin,
                    allergies,
                    maladies,
                    personne_urgence,
                    telephone_urgence,
                    acte_naissance,
                    bulletin_precedent,
                    certificat_medical,
                    attestation,
                    presences,
                    absences_justifiees,
                    absences_non_justifiees,
                    retards,
                    avertissements,
                    sanctions,
                    recompenses,
                    observation
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?
                )
                """,
                (
                    matricule,
                    nom.strip(),
                    postnom.strip(),
                    prenom.strip(),
                    sexe.strip(),
                    extra_data.get("date_naissance", ""),
                    extra_data.get("lieu_naissance", ""),
                    extra_data.get("nationalite", ""),
                    extra_data.get("etat_civil", ""),
                    extra_data.get("photo", ""),
                    classe.strip(),
                    extra_data.get("option_etude", ""),
                    extra_data.get("section", ""),
                    extra_data.get("annee_scolaire", ""),
                    extra_data.get("numero_inscription", ""),
                    extra_data.get("date_inscription", ""),
                    extra_data.get("statut", "Actif"),
                    extra_data.get("adresse", ""),
                    extra_data.get("ville", ""),
                    extra_data.get("commune", ""),
                    extra_data.get("quartier", ""),
                    extra_data.get("telephone", ""),
                    extra_data.get("email", ""),
                    extra_data.get("nom_pere", ""),
                    extra_data.get("telephone_pere", ""),
                    extra_data.get("nom_mere", ""),
                    extra_data.get("telephone_mere", ""),
                    extra_data.get("nom_tuteur", ""),
                    extra_data.get("telephone_tuteur", ""),
                    extra_data.get("profession_tuteur", ""),
                    extra_data.get("adresse_tuteur", ""),
                    float(extra_data.get("montant_total", 0) or 0),
                    float(extra_data.get("montant_paye", 0) or 0),
                    extra_data.get("mode_paiement", ""),
                    extra_data.get("date_dernier_paiement", ""),
                    extra_data.get("groupe_sanguin", ""),
                    extra_data.get("allergies", ""),
                    extra_data.get("maladies", ""),
                    extra_data.get("personne_urgence", ""),
                    extra_data.get("telephone_urgence", ""),
                    extra_data.get("acte_naissance", ""),
                    extra_data.get("bulletin_precedent", ""),
                    extra_data.get("certificat_medical", ""),
                    extra_data.get("attestation", ""),
                    int(extra_data.get("presences", 0) or 0),
                    int(extra_data.get("absences_justifiees", 0) or 0),
                    int(extra_data.get("absences_non_justifiees", 0) or 0),
                    int(extra_data.get("retards", 0) or 0),
                    int(extra_data.get("avertissements", 0) or 0),
                    extra_data.get("sanctions", ""),
                    extra_data.get("recompenses", ""),
                    extra_data.get("observation", ""),
                ),
            )
        except sqlite3.IntegrityError as error:
            raise ValueError("Ce matricule existe déjà.") from error
        else:
            self.db.connection.commit()
        finally:
            cursor.close()

    def modifier(
        self,
        student_id: int,
        matricule: str,
        nom: str,
        postnom: str,
        prenom: str,
        sexe: str,
        classe: str,
        option_etude: str,
        section: str,
        **extra_data: str,
    ) -> None:
        """Modifie toutes les informations d'un étudiant."""
        matricule = matricule.strip()

        if not matricule.isdigit():
            raise ValueError(
                "Le matricule doit contenir uniquement des chiffres."
            )

        cursor = self.db.connection.cursor()

        cursor.execute(
            "SELECT id FROM etudiants WHERE id = ?",
            (student_id,),
        )

        if cursor.fetchone() is None:
            cursor.close()
            raise EtudiantIntrouvableException("Étudiant introuvable.")

        try:
            cursor.execute(
                """
                UPDATE etudiants
                SET matricule = ?,
                    nom = ?,
                    postnom = ?,
                    prenom = ?,
                    sexe = ?,
                    classe = ?,
                    option_etude = ?,
                    section = ?
                WHERE id = ?
                """,
                (
                    matricule,
                    nom.strip(),
                    postnom.strip(),
                    prenom.strip(),
                    sexe.strip(),
                    classe.strip(),
                    option_etude.strip(),
                    section.strip(),
                    student_id,
                ),
            )
        except sqlite3.IntegrityError as error:
            cursor.close()
            raise ValueError("Ce matricule existe déjà.") from error

        self.db.connection.commit()
        cursor.close()

    def lister(self) -> list[tuple[str, str, str, str]]:
        """Retourne les étudiants pour les anciennes vues."""
        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            SELECT matricule, nom, postnom, classe
            FROM etudiants
            ORDER BY classe ASC, nom ASC
            """
        )

        data = cursor.fetchall()
        cursor.close()

        return data

    def lister_complet(self) -> list[tuple]:
        """Retourne les étudiants pour le tableau complet."""
        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            SELECT
                matricule,
                nom,
                postnom,
                prenom,
                sexe,
                classe,
                option_etude,
                section,
                telephone,
                montant_total,
                montant_paye,
                statut
            FROM etudiants
            ORDER BY classe ASC, nom ASC
            """
        )

        data = cursor.fetchall()
        cursor.close()

        return data

    def get_by_matricule(self, matricule: str) -> tuple | None:
        """Retourne toutes les informations d'un étudiant."""
        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM etudiants
            WHERE matricule = ?
            """,
            (matricule,),
        )

        data = cursor.fetchone()
        cursor.close()

        return data

    def statistiques_par_classe(self) -> list[tuple[str, int]]:
        """Retourne le nombre d'étudiants par classe."""
        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            SELECT classe, COUNT(*) AS total
            FROM etudiants
            GROUP BY classe
            ORDER BY classe ASC
            """
        )

        data = cursor.fetchall()
        cursor.close()

        return data

    def total_etudiants(self) -> int:
        """Retourne le total des étudiants."""
        cursor = self.db.connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM etudiants")

        total = cursor.fetchone()[0]
        cursor.close()

        return int(total)

    def supprimer(self, matricule: str) -> None:
        """Supprime un étudiant."""
        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            DELETE FROM etudiants
            WHERE matricule = ?
            """,
            (matricule,),
        )

        if cursor.rowcount == 0:
            cursor.close()
            raise EtudiantIntrouvableException("Étudiant introuvable.")

        self.db.connection.commit()
        cursor.close()


class CoursService:
    """Service de gestion des cours."""

    def __init__(self) -> None:
        """Initialise le service."""
        self.db = DatabaseConnection()

    def ajouter(
        self,
        nom: str,
        classe: str,
        categorie: str,
        credit: int = 1,
    ) -> None:
        """Ajoute un cours."""
        nom = nom.strip()
        classe = classe.strip()
        categorie = categorie.strip()

        if nom == "":
            raise ValueError("Le nom du cours est obligatoire.")

        if classe == "":
            raise ValueError("La classe est obligatoire.")

        if categorie == "":
            raise ValueError("La catégorie est obligatoire.")

        cours = Cours(nom, credit)
        cursor = self.db.connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO cours (
                    nom,
                    classe,
                    categorie,
                    credit
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    cours.nom,
                    classe,
                    categorie,
                    cours.credit,
                ),
            )
        except sqlite3.IntegrityError as error:
            raise ValueError(
                "Ce cours existe déjà pour cette classe."
            ) from error
        else:
            self.db.connection.commit()
        finally:
            cursor.close()

    def lister(self) -> list[tuple[str, str, str]]:
        """Retourne tous les cours."""
        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            SELECT nom, classe, categorie
            FROM cours
            ORDER BY classe ASC, categorie ASC, nom ASC
            """
        )

        data = cursor.fetchall()
        cursor.close()

        return data

    def modifier(
        self,
        ancien_nom: str,
        classe: str,
        nouveau_nom: str,
        categorie: str,
    ) -> None:
        """Modifie un cours."""
        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            UPDATE cours
            SET nom = ?, categorie = ?
            WHERE nom = ?
            AND classe = ?
            """,
            (
                nouveau_nom.strip(),
                categorie.strip(),
                ancien_nom.strip(),
                classe.strip(),
            ),
        )

        if cursor.rowcount == 0:
            cursor.close()
            raise ValueError("Cours introuvable.")

        self.db.connection.commit()
        cursor.close()

    def supprimer(
        self,
        nom: str,
        classe: str,
    ) -> None:
        """Supprime un cours."""
        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            DELETE FROM cours
            WHERE nom = ?
            AND classe = ?
            """,
            (
                nom.strip(),
                classe.strip(),
            ),
        )

        if cursor.rowcount == 0:
            cursor.close()
            raise ValueError("Cours introuvable.")

        self.db.connection.commit()
        cursor.close()


class NoteService:
    """Service de gestion des notes."""

    def __init__(self) -> None:
        """Initialise le service."""
        self.db = DatabaseConnection()

    def ajouter(self, matricule: str, cours: str, note_value: float) -> None:
        """Ajoute une note."""
        note = Note(matricule, cours, note_value)
        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            INSERT INTO notes (
                matricule,
                cours,
                note
            )
            VALUES (?, ?, ?)
            """,
            (
                note.matricule,
                note.cours,
                note.note,
            ),
        )

        self.db.connection.commit()
        cursor.close()

    def lister(self) -> list[tuple[str, str, float]]:
        """Retourne les notes."""
        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            SELECT matricule, cours, note
            FROM notes
            ORDER BY matricule ASC
            """
        )

        data = cursor.fetchall()
        cursor.close()

        return data


class EvaluationService:
    """Service de gestion des évaluations et bulletins."""

    def __init__(self) -> None:
        """Initialise le service."""
        self.db = DatabaseConnection()

    def lister_classes(self) -> list[str]:
        """Retourne les classes inscrites."""
        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            SELECT DISTINCT classe
            FROM etudiants
            ORDER BY classe ASC
            """
        )

        data = [row[0] for row in cursor.fetchall()]
        cursor.close()

        return data

    def lister_eleves_par_classe(
        self,
        classe: str,
    ) -> list[tuple[str, str]]:
        """Retourne les élèves d'une classe."""
        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            SELECT matricule, nom || ' ' || postnom || ' ' || prenom
            FROM etudiants
            WHERE classe = ?
            ORDER BY nom ASC
            """,
            (classe,),
        )

        data = cursor.fetchall()
        cursor.close()

        return data

    def lister_cours_details_par_classe(
        self,
        classe: str,
    ) -> list[tuple[str, str]]:
        """Retourne les cours et catégories d'une classe."""
        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            SELECT DISTINCT nom, categorie
            FROM cours
            WHERE TRIM(classe) = TRIM(?)
            ORDER BY categorie ASC, nom ASC
            """,
            (classe,),
        )

        data = cursor.fetchall()
        cursor.close()

        return data

    def ajouter_evaluation(
        self,
        matricule: str,
        nom_complet: str,
        classe: str,
        cours: str,
        type_evaluation: str,
        cote: float,
        date_evaluation: str,
    ) -> None:
        """Ajoute une évaluation."""
        self.validate_date(date_evaluation)

        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            INSERT INTO evaluations (
                matricule,
                nom_complet,
                classe,
                cours,
                type_evaluation,
                cote,
                date_evaluation
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                matricule,
                nom_complet,
                classe,
                cours,
                type_evaluation,
                cote,
                date_evaluation,
            ),
        )

        self.db.connection.commit()
        cursor.close()

    def lister_evaluations_par_classe(
        self,
        classe: str,
    ) -> list[tuple[str, str, str, str, float, str]]:
        """Retourne les évaluations d'une classe."""
        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            SELECT
                matricule,
                nom_complet,
                cours,
                type_evaluation,
                cote,
                date_evaluation
            FROM evaluations
            WHERE classe = ?
            ORDER BY nom_complet ASC, date_evaluation ASC, cours ASC
            """,
            (classe,),
        )

        data = cursor.fetchall()
        cursor.close()

        return data

    def modifier_evaluation(
        self,
        matricule: str,
        ancien_cours: str,
        ancien_type: str,
        ancienne_date: str,
        nouveau_cours: str,
        nouveau_type: str,
        nouvelle_cote: float,
        nouvelle_date: str,
    ) -> None:
        """Modifie une évaluation existante."""
        self.validate_date(nouvelle_date)

        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            UPDATE evaluations
            SET cours = ?,
                type_evaluation = ?,
                cote = ?,
                date_evaluation = ?
            WHERE matricule = ?
            AND cours = ?
            AND type_evaluation = ?
            AND date_evaluation = ?
            """,
            (
                nouveau_cours.strip(),
                nouveau_type.strip(),
                nouvelle_cote,
                nouvelle_date.strip(),
                matricule.strip(),
                ancien_cours.strip(),
                ancien_type.strip(),
                ancienne_date.strip(),
            ),
        )

        if cursor.rowcount == 0:
            cursor.close()
            raise ValueError("Évaluation introuvable.")

        self.db.connection.commit()
        cursor.close()

    def bulletin_eleve(
        self,
        matricule: str,
        type_evaluation: str,
        date_debut: str,
        date_fin: str,
    ) -> list[tuple[str, float, str]]:
        """Retourne le bulletin d'un élève."""
        self.validate_period(date_debut, date_fin)

        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            SELECT cours, cote, date_evaluation
            FROM evaluations
            WHERE matricule = ?
            AND type_evaluation = ?
            ORDER BY date_evaluation ASC, cours ASC
            """,
            (
                matricule,
                type_evaluation,
            ),
        )

        rows = cursor.fetchall()
        cursor.close()

        debut = self.convert_date(date_debut)
        fin = self.convert_date(date_fin)

        bulletin = []

        for cours, cote, date_evaluation in rows:
            date_value = self.convert_date(date_evaluation)

            if debut <= date_value <= fin:
                bulletin.append((cours, cote, date_evaluation))

        return bulletin

    def convert_date(self, date_value: str) -> datetime:
        """Convertit une date texte en datetime."""
        try:
            return datetime.strptime(date_value, DATE_FORMAT)
        except ValueError as error:
            raise ValueError(
                "La date doit être au format JJ/MM/AAAA."

                "Exemple : 11/01/2026"
            ) from error

    def validate_date(self, date_value: str) -> None:
        """Valide une date."""
        self.convert_date(date_value)

    def validate_period(self, date_debut: str, date_fin: str) -> None:
        """Valide une période."""
        debut = self.convert_date(date_debut)
        fin = self.convert_date(date_fin)

        if debut > fin:
            raise ValueError(
                "La date de début ne peut pas être supérieure "
                "à la date de fin."
            )
