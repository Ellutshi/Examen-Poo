"""Factory de création des utilisateurs."""

from models import Administrateur, Enseignant, EtudiantUtilisateur, Utilisateur


class UtilisateurFactory:
    """Factory pour créer les utilisateurs selon leur rôle."""

    @staticmethod
    def creer_utilisateur(
        role: str,
        nom: str,
        username: str,
        password: str,
    ) -> Utilisateur:
        """Crée un utilisateur selon son rôle.

        Args:
            role: Rôle de l'utilisateur.
            nom: Nom de l'utilisateur.
            username: Nom d'utilisateur.
            password: Mot de passe.

        Returns:
            Utilisateur: Objet utilisateur créé.

        Raises:
            ValueError: Si le rôle est inconnu.
        """
        if role == "admin":
            return Administrateur(nom, username, password)

        if role == "enseignant":
            return Enseignant(nom, username, password)

        if role == "etudiant":
            return EtudiantUtilisateur(nom, username, password)

        raise ValueError("Rôle utilisateur inconnu.")