"""Classes métier du projet EduManager."""

from abc import ABC, abstractmethod

from exceptions import ChampVideException, NoteInvalideException


class Personne:
    """Classe mère représentant une personne."""

    def __init__(self, nom: str) -> None:
        """Initialise une personne."""
        self.nom = nom

    @property
    def nom(self) -> str:
        """Retourne le nom."""
        return self.__nom

    @nom.setter
    def nom(self, value: str) -> None:
        """Modifie le nom avec validation."""
        if not value.strip():
            raise ChampVideException("Le nom ne peut pas être vide.")

        self.__nom = value.strip()


class Utilisateur(Personne, ABC):
    """Classe abstraite représentant un utilisateur."""

    def __init__(self, nom: str, username: str, password: str) -> None:
        """Initialise un utilisateur."""
        super().__init__(nom)
        self.username = username
        self.password = password

    @property
    def username(self) -> str:
        """Retourne le username."""
        return self.__username

    @username.setter
    def username(self, value: str) -> None:
        """Modifie le username avec validation."""
        if not value.strip():
            raise ChampVideException("Le username ne peut pas être vide.")

        self.__username = value.strip()

    @property
    def password(self) -> str:
        """Retourne le mot de passe."""
        return self.__password

    @password.setter
    def password(self, value: str) -> None:
        """Modifie le mot de passe avec validation."""
        if not value.strip():
            raise ChampVideException("Le mot de passe ne peut pas être vide.")

        self.__password = value.strip()

    @abstractmethod
    def afficher_menu(self) -> str:
        """Retourne le menu de l'utilisateur."""

    @abstractmethod
    def obtenir_role(self) -> str:
        """Retourne le rôle de l'utilisateur."""


class Administrateur(Utilisateur):
    """Utilisateur administrateur."""

    def afficher_menu(self) -> str:
        """Retourne le menu administrateur."""
        return "Menu administrateur"

    def obtenir_role(self) -> str:
        """Retourne le rôle administrateur."""
        return "admin"


class Enseignant(Utilisateur):
    """Utilisateur enseignant."""

    def afficher_menu(self) -> str:
        """Retourne le menu enseignant."""
        return "Menu enseignant"

    def obtenir_role(self) -> str:
        """Retourne le rôle enseignant."""
        return "enseignant"


class EtudiantUtilisateur(Utilisateur):
    """Utilisateur étudiant."""

    def afficher_menu(self) -> str:
        """Retourne le menu étudiant."""
        return "Menu étudiant"

    def obtenir_role(self) -> str:
        """Retourne le rôle étudiant."""
        return "etudiant"


class Etudiant(Personne):
    """Classe métier représentant une fiche complète d'étudiant."""

    def __init__(
        self,
        matricule: str,
        nom: str,
        postnom: str,
        prenom: str,
        sexe: str,
        classe: str,
        option_etude: str = "",
        section: str = "",
        telephone: str = "",
        email: str = "",
        statut: str = "Actif",
    ) -> None:
        """Initialise une fiche étudiant complète."""
        super().__init__(nom)
        self.matricule = matricule
        self.postnom = postnom
        self.prenom = prenom
        self.sexe = sexe
        self.classe = classe
        self.option_etude = option_etude
        self.section = section
        self.telephone = telephone
        self.email = email
        self.statut = statut

    @property
    def matricule(self) -> str:
        """Retourne le matricule."""
        return self.__matricule

    @matricule.setter
    def matricule(self, value: str) -> None:
        """Modifie le matricule."""
        if not value.strip():
            raise ChampVideException("Le matricule est obligatoire.")

        self.__matricule = value.strip()

    @property
    def postnom(self) -> str:
        """Retourne le postnom."""
        return self.__postnom

    @postnom.setter
    def postnom(self, value: str) -> None:
        """Modifie le postnom."""
        if not value.strip():
            raise ChampVideException("Le postnom est obligatoire.")

        self.__postnom = value.strip()

    @property
    def prenom(self) -> str:
        """Retourne le prénom."""
        return self.__prenom

    @prenom.setter
    def prenom(self, value: str) -> None:
        """Modifie le prénom."""
        if not value.strip():
            raise ChampVideException("Le prénom est obligatoire.")

        self.__prenom = value.strip()

    @property
    def sexe(self) -> str:
        """Retourne le sexe."""
        return self.__sexe

    @sexe.setter
    def sexe(self, value: str) -> None:
        """Modifie le sexe."""
        if not value.strip():
            raise ChampVideException("Le sexe est obligatoire.")

        self.__sexe = value.strip()

    @property
    def classe(self) -> str:
        """Retourne la classe."""
        return self.__classe

    @classe.setter
    def classe(self, value: str) -> None:
        """Modifie la classe."""
        if not value.strip():
            raise ChampVideException("La classe est obligatoire.")

        self.__classe = value.strip()

    @property
    def option_etude(self) -> str:
        """Retourne l'option."""
        return self.__option_etude

    @option_etude.setter
    def option_etude(self, value: str) -> None:
        """Modifie l'option."""
        self.__option_etude = value.strip()

    @property
    def section(self) -> str:
        """Retourne la section."""
        return self.__section

    @section.setter
    def section(self, value: str) -> None:
        """Modifie la section."""
        self.__section = value.strip()

    @property
    def telephone(self) -> str:
        """Retourne le téléphone."""
        return self.__telephone

    @telephone.setter
    def telephone(self, value: str) -> None:
        """Modifie le téléphone."""
        self.__telephone = value.strip()

    @property
    def email(self) -> str:
        """Retourne l'email."""
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        """Modifie l'email."""
        self.__email = value.strip()

    @property
    def statut(self) -> str:
        """Retourne le statut."""
        return self.__statut

    @statut.setter
    def statut(self, value: str) -> None:
        """Modifie le statut."""
        self.__statut = value.strip() if value else "Actif"


class Cours:
    """Classe métier représentant un cours."""

    def __init__(self, nom: str, credit: int) -> None:
        """Initialise un cours."""
        self.nom = nom
        self.credit = credit

    @property
    def nom(self) -> str:
        """Retourne le nom du cours."""
        return self.__nom

    @nom.setter
    def nom(self, value: str) -> None:
        """Modifie le nom du cours."""
        if not value.strip():
            raise ChampVideException("Le nom du cours est obligatoire.")

        self.__nom = value.strip()

    @property
    def credit(self) -> int:
        """Retourne le nombre de crédits."""
        return self.__credit

    @credit.setter
    def credit(self, value: int) -> None:
        """Modifie le nombre de crédits."""
        credit = int(value)

        if credit <= 0:
            raise ValueError("Le crédit doit être supérieur à 0.")

        self.__credit = credit


class Note:
    """Classe métier représentant une note."""

    def __init__(self, matricule: str, cours: str, note: float) -> None:
        """Initialise une note."""
        self.matricule = matricule
        self.cours = cours
        self.note = note

    @property
    def matricule(self) -> str:
        """Retourne le matricule."""
        return self.__matricule

    @matricule.setter
    def matricule(self, value: str) -> None:
        """Modifie le matricule."""
        if not value.strip():
            raise ChampVideException("Le matricule est obligatoire.")

        self.__matricule = value.strip()

    @property
    def cours(self) -> str:
        """Retourne le cours."""
        return self.__cours

    @cours.setter
    def cours(self, value: str) -> None:
        """Modifie le cours."""
        if not value.strip():
            raise ChampVideException("Le cours est obligatoire.")

        self.__cours = value.strip()

    @property
    def note(self) -> float:
        """Retourne la note."""
        return self.__note

    @note.setter
    def note(self, value: float) -> None:
        """Modifie la note."""
        note = float(value)

        if note < 0 or note > 20:
            raise NoteInvalideException("La note doit être entre 0 et 20.")

        self.__note = note