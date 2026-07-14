"""Vue de connexion moderne de l'application EduManager."""

import tkinter as tk
from tkinter import messagebox

from dashboard_view import DashboardView
from services import AuthService

BG_COLOR = "#f3f5ff"
PRIMARY_COLOR = "#5b4df5"
SECONDARY_COLOR = "#7b61ff"
TEXT_COLOR = "#111b3d"
MUTED_COLOR = "#6f7895"
WHITE = "#ffffff"
INPUT_BG = "#ffffff"
INPUT_BORDER = "#5b4df5"

WINDOW_SIZE = "1000x600"
MIN_WINDOW_SIZE = (900, 560)
MIN_PASSWORD_LENGTH = 8


class LoginView:
    """Interface graphique moderne de connexion."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.auth_service = AuthService()
        self.password_visible = False

        self.root.title("EduManager - Connexion")
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(*MIN_WINDOW_SIZE)
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(True, True)

        self.create_widgets()

    def create_widgets(self) -> None:
        """Crée l'interface de connexion."""
        container = tk.Frame(self.root, bg=BG_COLOR)
        container.pack(fill="both", expand=True, padx=50, pady=40)

        left_frame = tk.Frame(container, bg=BG_COLOR)
        left_frame.pack(side="left", fill="both", expand=True)

        right_frame = tk.Frame(container, bg=BG_COLOR)
        right_frame.pack(side="right", fill="both", expand=True)

        tk.Label(
            left_frame,
            text="🎓 EduManager",
            font=("Segoe UI", 24, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        ).pack(anchor="w", pady=(20, 5))

        tk.Label(
            left_frame,
            text="Gestion Scolaire Intelligente",
            font=("Segoe UI", 12),
            bg=BG_COLOR,
            fg=MUTED_COLOR,
        ).pack(anchor="w")

        tk.Label(
            left_frame,
            text="Bienvenue ! 👋",
            font=("Segoe UI", 30, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        ).pack(anchor="w", pady=(90, 20))

        tk.Label(
            left_frame,
            text=(
                "Connectez-vous à votre espace EduManager\n"
                "et gérez vos étudiants, cours et notes\n"
                "en toute simplicité."
            ),
            font=("Segoe UI", 14),
            bg=BG_COLOR,
            fg=MUTED_COLOR,
            justify="left",
        ).pack(anchor="w")

        tk.Label(
            left_frame,
            text="📚  📝  💻",
            font=("Segoe UI Emoji", 60),
            bg=BG_COLOR,
            fg=PRIMARY_COLOR,
        ).pack(anchor="w", pady=(80, 0))

        card = tk.Frame(
            right_frame,
            bg=WHITE,
            highlightbackground="#d7dcf3",
            highlightthickness=2,
        )
        card.pack(padx=40, pady=30, fill="both", expand=True)

        tk.Label(
            card,
            text="🎓",
            font=("Segoe UI Emoji", 45),
            bg=WHITE,
            fg=PRIMARY_COLOR,
        ).pack(pady=(35, 10))

        tk.Label(
            card,
            text="Connexion EduManager",
            font=("Segoe UI", 22, "bold"),
            bg=WHITE,
            fg=TEXT_COLOR,
        ).pack(pady=(5, 5))

        tk.Frame(card, bg=PRIMARY_COLOR, height=4, width=70).pack(
            pady=(5, 20)
        )

        tk.Label(
            card,
            text="Veuillez entrer vos identifiants pour accéder à votre compte",
            font=("Segoe UI", 11),
            bg=WHITE,
            fg=MUTED_COLOR,
        ).pack(pady=(0, 25))

        tk.Label(
            card,
            text="👤  Nom d'utilisateur",
            font=("Segoe UI", 11, "bold"),
            bg=WHITE,
            fg=TEXT_COLOR,
        ).pack(anchor="w", padx=70)

        username_frame = tk.Frame(
            card,
            bg=INPUT_BG,
            highlightbackground=INPUT_BORDER,
            highlightthickness=2,
        )
        username_frame.pack(fill="x", padx=70, pady=(8, 18), ipady=3)

        self.username_entry = tk.Entry(
            username_frame,
            font=("Segoe UI", 13),
            bd=0,
            bg=INPUT_BG,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
        )
        self.username_entry.pack(fill="x", padx=12, pady=10)

        tk.Label(
            card,
            text="🔒  Mot de passe",
            font=("Segoe UI", 11, "bold"),
            bg=WHITE,
            fg=TEXT_COLOR,
        ).pack(anchor="w", padx=70)

        password_frame = tk.Frame(
            card,
            bg=INPUT_BG,
            highlightbackground=INPUT_BORDER,
            highlightthickness=2,
        )
        password_frame.pack(fill="x", padx=70, pady=(8, 5), ipady=3)

        self.password_entry = tk.Entry(
            password_frame,
            font=("Segoe UI", 13),
            bd=0,
            bg=INPUT_BG,
            fg=TEXT_COLOR,
            show="*",
            insertbackground=TEXT_COLOR,
        )
        self.password_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(12, 5),
            pady=10,
        )

        self.show_password_button = tk.Button(
            password_frame,
            text="👁",
            command=self.toggle_password,
            font=("Segoe UI", 11),
            bg=INPUT_BG,
            fg=MUTED_COLOR,
            bd=0,
            cursor="hand2",
        )
        self.show_password_button.pack(side="right", padx=(5, 12))

        tk.Label(
            card,
            text="🔑 Le mot de passe doit contenir au moins 8 caractères.",
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=MUTED_COLOR,
        ).pack(anchor="w", padx=70, pady=(0, 15))

        options_frame = tk.Frame(card, bg=WHITE)
        options_frame.pack(fill="x", padx=70, pady=(0, 20))

        tk.Checkbutton(
            options_frame,
            text="Se souvenir de moi",
            bg=WHITE,
            fg=MUTED_COLOR,
            activebackground=WHITE,
            font=("Segoe UI", 10),
        ).pack(side="left")

        tk.Label(
            options_frame,
            text="Mot de passe oublié ?",
            bg=WHITE,
            fg=PRIMARY_COLOR,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="right")

        tk.Button(
            card,
            text="↪  Se connecter",
            command=self.login,
            font=("Segoe UI", 13, "bold"),
            bg=PRIMARY_COLOR,
            fg=WHITE,
            activebackground=SECONDARY_COLOR,
            activeforeground=WHITE,
            bd=0,
            cursor="hand2",
        ).pack(fill="x", padx=70, pady=(0, 25), ipady=12)

        tk.Label(
            card,
            text="🛡  Compte test : admin / admin1234",
            font=("Segoe UI", 11, "bold"),
            bg="#f8f9ff",
            fg=TEXT_COLOR,
            padx=20,
            pady=12,
        ).pack(fill="x", padx=70)

        footer = tk.Label(
            self.root,
            text="© 2026 EduManager - Tous droits réservés 💜",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=MUTED_COLOR,
        )
        footer.place(relx=0.5, rely=0.96, anchor="center")

        self.root.bind("<Return>", lambda event: self.login())

    def toggle_password(self) -> None:
        """Affiche ou masque le mot de passe."""
        if self.password_visible:
            self.password_entry.config(show="*")
            self.show_password_button.config(text="👁")
            self.password_visible = False
        else:
            self.password_entry.config(show="")
            self.show_password_button.config(text="🙈")
            self.password_visible = True

    def login(self) -> None:
        """Vérifie les identifiants et ouvre le tableau de bord."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == "":
            messagebox.showwarning(
                "Champ obligatoire",
                "Veuillez saisir votre nom d'utilisateur.",
            )
            self.username_entry.focus()
            return

        if password == "":
            messagebox.showwarning(
                "Champ obligatoire",
                "Veuillez saisir votre mot de passe.",
            )
            self.password_entry.focus()
            return

        if len(password) < MIN_PASSWORD_LENGTH:
            messagebox.showwarning(
                "Mot de passe invalide",
                "Le mot de passe doit contenir au moins 8 caractères.",
            )
            self.password_entry.focus()
            return

        utilisateur = self.auth_service.login(username, password)

        if utilisateur:
            self.clear_window()
            DashboardView(self.root, utilisateur)
        else:
            messagebox.showerror(
                "Connexion échouée",
                "Nom d'utilisateur ou mot de passe incorrect.\n"
                "Veuillez réessayer.",
            )
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()

    def clear_window(self) -> None:
        """Vide la fenêtre actuelle."""
        for widget in self.root.winfo_children():
            widget.destroy()