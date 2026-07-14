"""Exceptions personnalisées du projet EduManager."""


class EduManagerException(Exception):
    """Classe mère des exceptions du projet."""


class ChampVideException(EduManagerException):
    """Exception levée lorsqu'un champ obligatoire est vide."""


class ConnexionBDDException(EduManagerException):
    """Exception levée lorsqu'une erreur de base de données survient."""


class EtudiantIntrouvableException(EduManagerException):
    """Exception levée lorsqu'un étudiant est introuvable."""


class NoteInvalideException(EduManagerException):
    """Exception levée lorsqu'une note est invalide."""