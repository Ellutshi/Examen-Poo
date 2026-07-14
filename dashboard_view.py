"""Vue tableau de bord."""

import tkinter as tk

from bulletin_view import BulletinView
from course_view import CourseView
from models import Utilisateur
from student_view import StudentView

WINDOW_DASHBOARD_SIZE: str = "1000x600"


class DashboardView:
    """Interface graphique du tableau de bord."""

    def __init__(self, root: tk.Tk, utilisateur: Utilisateur) -> None:
        """Initialise le tableau de bord."""
        self.root = root
        self.utilisateur = utilisateur

        self.root.title("EduManager - Tableau de bord")
        self.root.geometry(WINDOW_DASHBOARD_SIZE)
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self) -> None:
        """Crée les boutons du tableau de bord."""
        title = tk.Label(
            self.root,
            text=f"Bienvenue {self.utilisateur.nom}",
            font=("Arial", 18, "bold"),
        )
        title.pack(pady=20)

        role = tk.Label(
            self.root,
            text=f"Rôle : {self.utilisateur.obtenir_role()}",
            font=("Arial", 12),
        )
        role.pack(pady=5)

        tk.Button(
            self.root,
            text="Gestion des étudiants",
            width=30,
            command=self.open_students,
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Gestion des cours et notes",
            width=30,
            command=self.open_courses,
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Gestion des bulletins",
            width=30,
            command=self.open_bulletins,
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Quitter",
            width=30,
            command=self.root.destroy,
        ).pack(pady=10)

    def clear_window(self) -> None:
        """Vide la fenêtre actuelle."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def open_students(self) -> None:
        """Ouvre la gestion des étudiants."""
        self.clear_window()
        StudentView(self.root, self.utilisateur)

    def open_courses(self) -> None:
        """Ouvre la gestion des cours et des notes."""
        self.clear_window()
        CourseView(self.root, self.utilisateur)

    def open_bulletins(self) -> None:
        """Ouvre la gestion des bulletins."""
        self.clear_window()
        BulletinView(self.root, self.utilisateur)