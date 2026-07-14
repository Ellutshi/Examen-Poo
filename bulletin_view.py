"""Vue de gestion des évaluations et bulletins."""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from models import Utilisateur
from services import EvaluationService

WINDOW_BULLETIN_SIZE: str = "1000x600"
DATE_PLACEHOLDER: str = "JJ/MM/AAAA"


class BulletinView:
    """Interface pour gérer les évaluations et bulletins."""

    def __init__(self, root: tk.Tk, utilisateur: Utilisateur) -> None:
        """Initialise la vue bulletin."""
        self.root = root
        self.utilisateur = utilisateur
        self.service = EvaluationService()
        self.eleves: list[tuple[str, str]] = []
        self.cours_data: dict[str, str] = {}

        self.root.title("EduManager - Bulletins")
        self.root.geometry(WINDOW_BULLETIN_SIZE)
        self.root.resizable(False, False)

        self.create_widgets()
        self.load_classes()

    def create_widgets(self) -> None:
        """Crée les composants graphiques."""
        title = tk.Label(
            self.root,
            text="Gestion des évaluations et bulletins",
            font=("Arial", 18, "bold"),
        )
        title.pack(pady=10)

        form_frame = tk.LabelFrame(self.root, text="Évaluation")
        form_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(form_frame, text="Classe").grid(
            row=0,
            column=0,
            padx=5,
            pady=3,
            sticky="w",
        )
        self.classe_combo = ttk.Combobox(form_frame, state="readonly")
        self.classe_combo.grid(row=0, column=1, padx=5, pady=3)
        self.classe_combo.bind("<<ComboboxSelected>>", self.load_eleves)

        tk.Label(form_frame, text="Élève").grid(
            row=0,
            column=2,
            padx=5,
            pady=3,
            sticky="w",
        )
        self.eleve_combo = ttk.Combobox(form_frame, state="readonly", width=30)
        self.eleve_combo.grid(row=0, column=3, padx=5, pady=3)

        tk.Label(form_frame, text="Cours").grid(
            row=1,
            column=0,
            padx=5,
            pady=3,
            sticky="w",
        )
        self.cours_combo = ttk.Combobox(form_frame, state="readonly")
        self.cours_combo.grid(row=1, column=1, padx=5, pady=3)

        tk.Label(form_frame, text="Type").grid(
            row=1,
            column=2,
            padx=5,
            pady=3,
            sticky="w",
        )
        self.type_combo = ttk.Combobox(
            form_frame,
            values=["Devoir", "Interrogation", "Examen", "Exercice"],
            state="readonly",
        )
        self.type_combo.grid(row=1, column=3, padx=5, pady=3)
        self.type_combo.set("Devoir")

        tk.Label(form_frame, text="Cote /20").grid(
            row=2,
            column=0,
            padx=5,
            pady=3,
            sticky="w",
        )
        self.cote_entry = tk.Entry(form_frame)
        self.cote_entry.grid(row=2, column=1, padx=5, pady=3)

        tk.Label(form_frame, text="Date cote").grid(
            row=2,
            column=2,
            padx=5,
            pady=3,
            sticky="w",
        )
        self.date_cote_entry = tk.Entry(form_frame)
        self.date_cote_entry.insert(0, DATE_PLACEHOLDER)
        self.date_cote_entry.grid(row=2, column=3, padx=5, pady=3)

        tk.Label(form_frame, text="Début période").grid(
            row=3,
            column=0,
            padx=5,
            pady=3,
            sticky="w",
        )
        self.date_debut_entry = tk.Entry(form_frame)
        self.date_debut_entry.insert(0, DATE_PLACEHOLDER)
        self.date_debut_entry.grid(row=3, column=1, padx=5, pady=3)

        tk.Label(form_frame, text="Fin période").grid(
            row=3,
            column=2,
            padx=5,
            pady=3,
            sticky="w",
        )
        self.date_fin_entry = tk.Entry(form_frame)
        self.date_fin_entry.insert(0, DATE_PLACEHOLDER)
        self.date_fin_entry.grid(row=3, column=3, padx=5, pady=3)

        info = tk.Label(
            form_frame,
            text=(
                "Le professeur choisit lui-même la période. "
                "La date de la cote doit être dans la période définie."
            ),
            fg="red",
            font=("Arial", 10, "bold"),
        )
        info.grid(row=4, column=0, columnspan=4, pady=8, sticky="w")

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Ajouter cote",
            command=self.add_evaluation,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Modifier cote",
            command=self.update_evaluation,
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Générer bulletin",
            command=self.generate_bulletin,
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Retour",
            command=self.back,
        ).grid(row=0, column=3, padx=5)

        self.evaluation_table = ttk.Treeview(
            self.root,
            columns=(
                "matricule",
                "nom",
                "cours",
                "categorie",
                "type",
                "date",
                "cote",
            ),
            show="headings",
        )

        headings = {
            "matricule": "Matricule",
            "nom": "Nom de l'élève",
            "cours": "Cours",
            "categorie": "Catégorie",
            "type": "Type",
            "date": "Date",
            "cote": "Cote /20",
        }

        for column, text in headings.items():
            self.evaluation_table.heading(column, text=text)

        self.evaluation_table.column(
            "matricule",
            width=90,
            anchor="center",
            stretch=False,
        )
        self.evaluation_table.column(
            "nom",
            width=210,
            anchor="w",
            stretch=False,
        )
        self.evaluation_table.column(
            "cours",
            width=160,
            anchor="center",
            stretch=False,
        )
        self.evaluation_table.column(
            "categorie",
            width=120,
            anchor="center",
            stretch=False,
        )
        self.evaluation_table.column(
            "type",
            width=130,
            anchor="center",
            stretch=False,
        )
        self.evaluation_table.column(
            "date",
            width=120,
            anchor="center",
            stretch=False,
        )
        self.evaluation_table.column(
            "cote",
            width=110,
            anchor="center",
            stretch=False,
        )

        self.evaluation_table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10,
        )
        self.evaluation_table.bind(
            "<<TreeviewSelect>>",
            self.fill_selected_evaluation,
        )

    def load_classes(self) -> None:
        """Charge les classes des élèves inscrits."""
        classes = self.service.lister_classes()
        self.classe_combo["values"] = classes

        if classes:
            self.classe_combo.set(classes[0])
            self.load_eleves()

    def load_eleves(self, event: object | None = None) -> None:
        """Charge les élèves et les cours selon la classe."""
        classe = self.classe_combo.get()

        self.eleves = self.service.lister_eleves_par_classe(classe)
        self.eleve_combo["values"] = [
            f"{matricule} - {nom}" for matricule, nom in self.eleves
        ]

        if self.eleves:
            self.eleve_combo.set(f"{self.eleves[0][0]} - {self.eleves[0][1]}")
        else:
            self.eleve_combo.set("")

        self.load_courses(classe)
        self.refresh_evaluation_table()

    def load_courses(self, classe: str) -> None:
        """Charge les cours avec catégories."""
        cours = self.service.lister_cours_details_par_classe(classe)

        self.cours_data = {nom: categorie for nom, categorie in cours}
        noms_cours = list(self.cours_data.keys())

        self.cours_combo["values"] = noms_cours

        if noms_cours:
            self.cours_combo.set(noms_cours[0])
        else:
            self.cours_combo.set("")

    def get_selected_student(self) -> tuple[str, str]:
        """Retourne l'élève sélectionné."""
        selected = self.eleve_combo.get()

        if selected == "":
            raise ValueError("Veuillez sélectionner un élève.")

        matricule = selected.split(" - ")[0]

        for student_matricule, nom in self.eleves:
            if student_matricule == matricule:
                return student_matricule, nom

        raise ValueError("Élève introuvable.")

    def get_course_category(self, cours: str) -> str:
        """Retourne la catégorie simplifiée du cours."""
        categorie = self.cours_data.get(cours, "")

        if categorie.lower() == "cours d'option":
            return "Option"

        return "Général"

    def add_evaluation(self) -> None:
        """Ajoute une cote uniquement si sa date est dans la période."""
        try:
            matricule, nom_complet = self.get_selected_student()

            classe = self.classe_combo.get().strip()
            cours = self.cours_combo.get().strip()
            type_evaluation = self.type_combo.get().strip()
            date_cote = self.date_cote_entry.get().strip()
            date_debut = self.date_debut_entry.get().strip()
            date_fin = self.date_fin_entry.get().strip()

            if classe == "":
                raise ValueError("Veuillez sélectionner une classe précise.")

            if cours == "":
                raise ValueError("Veuillez sélectionner un cours.")

            if type_evaluation == "":
                raise ValueError("Veuillez sélectionner le type d'évaluation.")

            if date_cote == "" or date_debut == "" or date_fin == "":
                raise ValueError("Veuillez remplir toutes les dates.")

            if DATE_PLACEHOLDER in [date_cote, date_debut, date_fin]:
                raise ValueError(
                    "Veuillez remplacer JJ/MM/AAAA par une vraie date."
                )

            self.service.validate_period(date_debut, date_fin)

            date_cote_value = self.service.convert_date(date_cote)
            date_debut_value = self.service.convert_date(date_debut)
            date_fin_value = self.service.convert_date(date_fin)

            if date_cote_value < date_debut_value:
                raise ValueError(
                    "La date de la cote est avant la période définie.\n\n"
                    f"Période : {date_debut} au {date_fin}\n"
                    f"Date de la cote : {date_cote}"
                )

            if date_cote_value > date_fin_value:
                raise ValueError(
                    "La date de la cote dépasse la période définie.\n\n"
                    f"Période : {date_debut} au {date_fin}\n"
                    f"Date de la cote : {date_cote}"
                )

            cote = float(self.cote_entry.get())

            if cote < 0 or cote > 20:
                raise ValueError("La cote doit être entre 0 et 20.")

            self.service.ajouter_evaluation(
                matricule,
                nom_complet,
                classe,
                cours,
                type_evaluation,
                cote,
                date_cote,
            )

        except Exception as error:
            messagebox.showerror("Erreur", str(error))
        else:
            messagebox.showinfo("Succès", "Cote ajoutée.")
            self.cote_entry.delete(0, tk.END)
            self.refresh_evaluation_table()

    def refresh_evaluation_table(self) -> None:
        """Recharge les cotes affichées."""
        for row in self.evaluation_table.get_children():
            self.evaluation_table.delete(row)

        classe = self.classe_combo.get()
        evaluations = self.service.lister_evaluations_par_classe(classe)

        for evaluation in evaluations:
            matricule, nom, cours, type_eval, cote, date_eval = evaluation

            self.evaluation_table.insert(
                "",
                "end",
                values=(
                    matricule,
                    nom,
                    cours,
                    self.get_course_category(cours),
                    type_eval,
                    date_eval,
                    f"{cote:.2f}",
                ),
            )

    def fill_selected_evaluation(self, event: object | None = None) -> None:
        """Remplit les champs avec l'évaluation sélectionnée."""
        selected = self.evaluation_table.selection()

        if not selected:
            return

        values = self.evaluation_table.item(selected[0])["values"]

        self.cours_combo.set(values[2])
        self.type_combo.set(values[4])

        self.date_cote_entry.delete(0, tk.END)
        self.date_cote_entry.insert(0, values[5])

        self.cote_entry.delete(0, tk.END)
        self.cote_entry.insert(0, values[6])

    def update_evaluation(self) -> None:
        """Modifie la cote sélectionnée."""
        selected = self.evaluation_table.selection()

        if not selected:
            messagebox.showwarning(
                "Attention",
                "Veuillez sélectionner une cote à modifier.",
            )
            return

        values = self.evaluation_table.item(selected[0])["values"]

        matricule = str(values[0])
        ancien_cours = str(values[2])
        ancien_type = str(values[4])
        ancienne_date = str(values[5])

        cours = self.cours_combo.get().strip()
        type_evaluation = self.type_combo.get().strip()
        date_cote = self.date_cote_entry.get().strip()
        cote_text = self.cote_entry.get().strip()

        if cours == "":
            messagebox.showwarning(
                "Cours obligatoire",
                "Veuillez sélectionner un cours.",
            )
            return

        if type_evaluation == "":
            messagebox.showwarning(
                "Type obligatoire",
                "Veuillez sélectionner le type d'évaluation.",
            )
            return

        if cote_text == "":
            messagebox.showwarning(
                "Cote obligatoire",
                "Veuillez saisir la cote.",
            )
            return

        if date_cote == "" or date_cote == DATE_PLACEHOLDER:
            messagebox.showwarning(
                "Date obligatoire",
                "Veuillez saisir la date de la cote.",
            )
            return

        try:
            cote = float(cote_text)

            if cote < 0 or cote > 20:
                raise ValueError("La cote doit être entre 0 et 20.")

            self.service.modifier_evaluation(
                matricule=matricule,
                ancien_cours=ancien_cours,
                ancien_type=ancien_type,
                ancienne_date=ancienne_date,
                nouveau_cours=cours,
                nouveau_type=type_evaluation,
                nouvelle_cote=cote,
                nouvelle_date=date_cote,
            )
        except Exception as error:
            messagebox.showerror("Erreur", str(error))
        else:
            messagebox.showinfo("Succès", "Cote modifiée.")
            self.cote_entry.delete(0, tk.END)
            self.refresh_evaluation_table()

    def generate_bulletin(self) -> None:
        """Génère un bulletin selon le type et la période."""
        try:
            matricule, nom_complet = self.get_selected_student()
            type_evaluation = self.type_combo.get().strip()
            date_debut = self.date_debut_entry.get().strip()
            date_fin = self.date_fin_entry.get().strip()

            if DATE_PLACEHOLDER in [date_debut, date_fin]:
                raise ValueError(
                    "Veuillez saisir une vraie période au format JJ/MM/AAAA."
                )

            bulletin = self.service.bulletin_eleve(
                matricule,
                type_evaluation,
                date_debut,
                date_fin,
            )

            if not bulletin:
                raise ValueError("Aucune cote trouvée pour cette période.")

        except Exception as error:
            messagebox.showerror("Erreur", str(error))
            return

        self.show_bulletin_window(
            matricule,
            nom_complet,
            type_evaluation,
            date_debut,
            date_fin,
            bulletin,
        )

    def show_bulletin_window(
        self,
        matricule: str,
        nom_complet: str,
        type_evaluation: str,
        date_debut: str,
        date_fin: str,
        bulletin: list[tuple[str, float, str]],
    ) -> None:
        """Affiche la fenêtre du bulletin."""
        window = tk.Toplevel(self.root)
        window.title("Bulletin")
        window.geometry("700x520")

        tk.Label(
            window,
            text=f"BULLETIN - {type_evaluation.upper()}",
            font=("Arial", 16, "bold"),
        ).pack(pady=10)

        tk.Label(window, text=f"Nom : {nom_complet}").pack()
        tk.Label(window, text=f"Matricule : {matricule}").pack()
        tk.Label(window, text=f"Classe : {self.classe_combo.get()}").pack()
        tk.Label(
            window,
            text=f"Période : {date_debut} au {date_fin}",
        ).pack(pady=5)

        table = ttk.Treeview(
            window,
            columns=("cours", "categorie", "date", "cote"),
            show="headings",
        )
        table.heading("cours", text="Cours")
        table.heading("categorie", text="Catégorie")
        table.heading("date", text="Date")
        table.heading("cote", text="Cote /20")
        table.pack(fill="both", expand=True, padx=10, pady=10)

        somme = 0.0

        for cours, cote, date_eval in bulletin:
            table.insert(
                "",
                "end",
                values=(
                    cours,
                    self.get_course_category(cours),
                    date_eval,
                    f"{cote:.2f}",
                ),
            )
            somme += cote

        moyenne = somme / len(bulletin)

        tk.Label(
            window,
            text=f"Moyenne : {moyenne:.2f} / 20",
            font=("Arial", 12, "bold"),
        ).pack(pady=5)

        tk.Label(window, text=f"Mention : {self.get_mention(moyenne)}").pack()
        tk.Label(window, text=f"Décision : {self.get_decision(moyenne)}").pack()

    def get_mention(self, moyenne: float) -> str:
        """Retourne la mention."""
        if moyenne >= 16:
            return "Très Bien"

        if moyenne >= 14:
            return "Bien"

        if moyenne >= 12:
            return "Assez Bien"

        if moyenne >= 10:
            return "Passable"

        return "Insuffisant"

    def get_decision(self, moyenne: float) -> str:
        """Retourne la décision."""
        if moyenne >= 10:
            return "Travail satisfaisant"

        return "Travail insuffisant"

    def back(self) -> None:
        """Retourne au tableau de bord."""
        from dashboard_view import DashboardView

        for widget in self.root.winfo_children():
            widget.destroy()

        DashboardView(self.root, self.utilisateur)