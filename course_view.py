"""Vue de gestion des cours par classe."""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from models import Utilisateur
from services import CoursService, EtudiantService

WINDOW_COURSE_SIZE: str = "1000x600"


class CourseView:
    """Interface graphique pour gérer les cours par classe."""

    def __init__(self, root: tk.Tk, utilisateur: Utilisateur) -> None:
        """Initialise la vue des cours."""
        self.root = root
        self.utilisateur = utilisateur
        self.cours_service = CoursService()
        self.etudiant_service = EtudiantService()

        self.root.title("EduManager - Gestion des cours")
        self.root.geometry(WINDOW_COURSE_SIZE)
        self.root.resizable(False, False)

        self.create_widgets()
        self.load_classes()
        self.refresh_courses()

    def create_widgets(self) -> None:
        """Crée les composants graphiques."""
        title = tk.Label(
            self.root,
            text="Gestion des cours par classe",
            font=("Arial", 18, "bold"),
        )
        title.pack(pady=10)

        form_frame = tk.LabelFrame(
            self.root,
            text="Ajouter / modifier un cours",
        )
        form_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(form_frame, text="Classe").grid(row=0, column=0, padx=5)
        self.classe_combo = ttk.Combobox(form_frame, state="readonly")
        self.classe_combo.grid(row=0, column=1, padx=5)
        self.classe_combo.bind("<<ComboboxSelected>>", self.load_students)

        tk.Label(form_frame, text="Nom du cours").grid(row=0, column=2, padx=5)
        self.cours_entry = tk.Entry(form_frame)
        self.cours_entry.grid(row=0, column=3, padx=5)

        tk.Label(form_frame, text="Catégorie").grid(row=1, column=0, padx=5)
        self.categorie_combo = ttk.Combobox(
            form_frame,
            values=["Cours général", "Cours d'option"],
            state="readonly",
        )
        self.categorie_combo.grid(row=1, column=1, padx=5)
        self.categorie_combo.set("Cours général")

        tk.Button(
            form_frame,
            text="Ajouter cours",
            command=self.add_course,
        ).grid(row=1, column=2, padx=5, pady=8)

        tk.Button(
            form_frame,
            text="Modifier cours",
            command=self.update_course,
        ).grid(row=1, column=3, padx=5, pady=8)

        info = tk.Label(
            self.root,
            text=(
                "Le professeur ajoute, modifie ou supprime uniquement "
                "les cours ici. Les cotes sont enregistrées dans Bulletins."
            ),
            fg="red",
            font=("Arial", 10, "bold"),
        )
        info.pack(pady=5)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Supprimer",
            width=15,
            command=self.delete_course,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Actualiser",
            width=15,
            command=self.refresh_all,
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Retour",
            width=15,
            command=self.back,
        ).grid(row=0, column=2, padx=5)

        tables_frame = tk.Frame(self.root)
        tables_frame.pack(fill="both", expand=True, padx=10, pady=10)

        student_frame = tk.LabelFrame(
            tables_frame,
            text="Élèves inscrits dans la classe",
        )
        student_frame.pack(side="left", fill="both", expand=True, padx=5)

        self.student_table = ttk.Treeview(
            student_frame,
            columns=("matricule", "nom_complet"),
            show="headings",
        )
        self.student_table.heading("matricule", text="Matricule")
        self.student_table.heading("nom_complet", text="Nom complet")
        self.student_table.pack(fill="both", expand=True, padx=5, pady=5)

        course_frame = tk.LabelFrame(
            tables_frame,
            text="Cours enregistrés",
        )
        course_frame.pack(side="right", fill="both", expand=True, padx=5)

        self.course_table = ttk.Treeview(
            course_frame,
            columns=("classe", "cours", "categorie"),
            show="headings",
        )
        self.course_table.heading("classe", text="Classe")
        self.course_table.heading("cours", text="Cours")
        self.course_table.heading("categorie", text="Catégorie")
        self.course_table.pack(fill="both", expand=True, padx=5, pady=5)
        self.course_table.bind("<<TreeviewSelect>>", self.fill_selected_course)

    def load_classes(self) -> None:
        """Charge les classes à partir des élèves inscrits."""
        statistiques = self.etudiant_service.statistiques_par_classe()
        classes = [classe for classe, _ in statistiques]

        self.classe_combo["values"] = classes

        if classes:
            self.classe_combo.set(classes[0])
            self.load_students()

    def load_students(self, event: object | None = None) -> None:
        """Affiche les élèves de la classe sélectionnée."""
        classe = self.classe_combo.get()

        for row in self.student_table.get_children():
            self.student_table.delete(row)

        for etudiant in self.etudiant_service.lister():
            matricule, nom, postnom, student_classe = etudiant

            if student_classe == classe:
                nom_complet = f"{nom} {postnom}"
                self.student_table.insert(
                    "",
                    "end",
                    values=(matricule, nom_complet),
                )

    def add_course(self) -> None:
        """Ajoute un cours."""
        classe = self.classe_combo.get().strip()
        nom_cours = self.cours_entry.get().strip()
        categorie = self.categorie_combo.get().strip()

        if classe == "":
            messagebox.showwarning(
                "Classe obligatoire",
                "Veuillez sélectionner une classe.",
            )
            return

        if nom_cours == "":
            messagebox.showwarning(
                "Cours obligatoire",
                "Veuillez saisir le nom du cours.",
            )
            self.cours_entry.focus()
            return

        try:
            self.cours_service.ajouter(
                nom_cours,
                classe,
                categorie,
            )
        except Exception as error:
            messagebox.showerror("Erreur", str(error))
        else:
            messagebox.showinfo("Succès", "Cours ajouté avec succès.")
            self.cours_entry.delete(0, tk.END)
            self.refresh_courses()

    def fill_selected_course(self, event: object | None = None) -> None:
        """Remplit le formulaire avec le cours sélectionné."""
        selected = self.course_table.selection()

        if not selected:
            return

        values = self.course_table.item(selected[0])["values"]

        self.classe_combo.set(values[0])
        self.cours_entry.delete(0, tk.END)
        self.cours_entry.insert(0, values[1])
        self.categorie_combo.set(values[2])

    def update_course(self) -> None:
        """Modifie le nom et la catégorie du cours sélectionné."""
        selected = self.course_table.selection()

        if not selected:
            messagebox.showwarning(
                "Sélection obligatoire",
                "Veuillez sélectionner un cours à modifier.",
            )
            return

        old_values = self.course_table.item(selected[0])["values"]
        old_classe = old_values[0]
        old_nom = old_values[1]

        new_nom = self.cours_entry.get().strip()
        new_categorie = self.categorie_combo.get().strip()

        if new_nom == "":
            messagebox.showwarning(
                "Cours obligatoire",
                "Veuillez saisir le nouveau nom du cours.",
            )
            return

        try:
            self.cours_service.modifier(
                old_nom,
                old_classe,
                new_nom,
                new_categorie,
            )
        except Exception as error:
            messagebox.showerror("Erreur", str(error))
        else:
            messagebox.showinfo("Succès", "Cours modifié avec succès.")
            self.cours_entry.delete(0, tk.END)
            self.refresh_courses()

    def delete_course(self) -> None:
        """Supprime le cours sélectionné."""
        selected = self.course_table.selection()

        if not selected:
            messagebox.showwarning(
                "Sélection obligatoire",
                "Veuillez sélectionner un cours à supprimer.",
            )
            return

        values = self.course_table.item(selected[0])["values"]
        classe = values[0]
        nom_cours = values[1]

        confirmation = messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous vraiment supprimer le cours {nom_cours} ?",
        )

        if not confirmation:
            return

        try:
            self.cours_service.supprimer(nom_cours, classe)
        except Exception as error:
            messagebox.showerror("Erreur", str(error))
        else:
            messagebox.showinfo("Succès", "Cours supprimé avec succès.")
            self.refresh_courses()

    def refresh_courses(self) -> None:
        """Recharge la liste des cours enregistrés."""
        for row in self.course_table.get_children():
            self.course_table.delete(row)

        for cours in self.cours_service.lister():
            nom, classe, categorie = cours
            self.course_table.insert(
                "",
                "end",
                values=(classe, nom, categorie),
            )

    def refresh_all(self) -> None:
        """Actualise les classes, élèves et cours."""
        self.load_classes()
        self.load_students()
        self.refresh_courses()

    def back(self) -> None:
        """Retourne au tableau de bord."""
        from dashboard_view import DashboardView

        for widget in self.root.winfo_children():
            widget.destroy()

        DashboardView(self.root, self.utilisateur)