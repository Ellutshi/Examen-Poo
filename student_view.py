"""Vue complète de gestion des étudiants."""

from datetime import datetime
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from models import Utilisateur
from services import EtudiantService

WINDOW_STUDENT_SIZE: str = "1000x600"
DATE_FORMAT: str = "%d/%m/%Y"
DATE_PLACEHOLDER: str = "JJ/MM/AAAA"

CLASSES_BASE: tuple[str, ...] = (
    "1e",
    "2e",
    "3e",
    "4e",
    "5e",
    "6e",
)

LETTRES_CLASSES: tuple[str, ...] = (
    "A",
    "B",
    "C",
    "D",
)

SECTIONS: tuple[str, ...] = (
    "Maternelle",
    "Primaire",
    "Secondaire",
    "Technique",
    "Scientifique",
    "Commerciale",
    "Pédagogique",
    "Littéraire",
)

OPTIONS: tuple[str, ...] = (
    "Générale",
    "Scientifique",
    "Commerciale",
    "Pédagogique",
    "Informatique",
    "Électricité",
    "Mécanique",
    "Coupe et Couture",
)


class StudentView:
    """Interface graphique complète pour gérer les étudiants."""

    def __init__(self, root: tk.Tk, utilisateur: Utilisateur) -> None:
        """Initialise la vue étudiant."""
        self.root = root
        self.utilisateur = utilisateur
        self.service = EtudiantService()
        self.entries: dict[str, object] = {}
        self.selected_student_id: int | None = None

        self.root.title("EduManager - Gestion complète des étudiants")
        self.root.geometry(WINDOW_STUDENT_SIZE)
        self.root.resizable(False, False)

        self.create_widgets()
        self.refresh_table()
        self.refresh_statistics()

    def create_widgets(self) -> None:
        """Crée l'interface principale."""
        title = tk.Label(
            self.root,
            text="Gestion complète des étudiants",
            font=("Arial", 18, "bold"),
        )
        title.pack(pady=8)

        self.stats_label = tk.Label(
            self.root,
            text="Total général des élèves : 0",
            font=("Arial", 12, "bold"),
        )
        self.stats_label.pack(pady=4)

        self.create_search_zone()
        self.create_notebook()
        self.create_buttons()
        self.create_table()

    def create_search_zone(self) -> None:
        """Crée la zone de recherche."""
        search_frame = tk.LabelFrame(self.root, text="Recherche et filtres")
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Recherche").grid(row=0, column=0)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=5)

        tk.Label(search_frame, text="Classe").grid(row=0, column=2)
        self.filter_classe = tk.Entry(search_frame, width=15)
        self.filter_classe.grid(row=0, column=3, padx=5)

        tk.Button(
            search_frame,
            text="Rechercher",
            command=self.search_students,
        ).grid(row=0, column=4, padx=5)

        tk.Button(
            search_frame,
            text="Réinitialiser",
            command=self.refresh_table,
        ).grid(row=0, column=5, padx=5)

    def create_notebook(self) -> None:
        """Crée les onglets de la fiche étudiant."""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="x", padx=10, pady=5)

        tabs = {
            "Informations personnelles": [
                "matricule",
                "nom",
                "postnom",
                "prenom",
                "sexe",
                "date_naissance",
                "lieu_naissance",
                "nationalite",
                "etat_civil",
                "photo",
            ],
            "Informations scolaires": [
                "classe",
                "lettre_classe",
                "classe_complete",
                "section",
                "option_etude",
                "annee_scolaire",
                "numero_inscription",
                "date_inscription",
                "statut",
            ],
            "Coordonnées": [
                "adresse",
                "ville",
                "commune",
                "quartier",
                "telephone",
                "email",
            ],
            "Parents / Tuteur": [
                "nom_pere",
                "telephone_pere",
                "nom_mere",
                "telephone_mere",
                "nom_tuteur",
                "telephone_tuteur",
                "profession_tuteur",
                "adresse_tuteur",
            ],
            "Finances": [
                "montant_total",
                "montant_paye",
                "mode_paiement",
                "date_dernier_paiement",
            ],
            "Médical": [
                "groupe_sanguin",
                "allergies",
                "maladies",
                "personne_urgence",
                "telephone_urgence",
            ],
            "Documents": [
                "acte_naissance",
                "bulletin_precedent",
                "certificat_medical",
                "attestation",
            ],
            "Présence / Discipline": [
                "presences",
                "absences_non_justifiees",
                "retards",
                "absences_justifiees",
                "avertissements",
                "sanctions",
                "recompenses",
                "observation",
            ],
        }

        for tab_name, fields in tabs.items():
            frame = tk.Frame(notebook)
            notebook.add(frame, text=tab_name)
            self.create_fields(frame, fields)

    def create_fields(self, frame: tk.Frame, fields: list[str]) -> None:
        """Crée les champs d'un onglet."""
        file_fields = [
            "photo",
            "acte_naissance",
            "bulletin_precedent",
            "certificat_medical",
            "attestation",
        ]

        date_fields = [
            "date_naissance",
            "date_inscription",
            "date_dernier_paiement",
        ]

        for index, field in enumerate(fields):
            row = index // 2
            column = (index % 2) * 2
            label_text = field.replace("_", " ").capitalize()

            tk.Label(frame, text=label_text).grid(
                row=row,
                column=column,
                sticky="w",
                padx=5,
                pady=4,
            )

            if field == "sexe":
                entry = ttk.Combobox(
                    frame,
                    values=["Homme", "Femme"],
                    state="readonly",
                    width=25,
                )
                entry.set("Homme")

            elif field == "classe":
                entry = ttk.Combobox(
                    frame,
                    values=CLASSES_BASE,
                    state="readonly",
                    width=25,
                )
                entry.bind("<<ComboboxSelected>>", self.update_full_class)

            elif field == "lettre_classe":
                entry = ttk.Combobox(
                    frame,
                    values=LETTRES_CLASSES,
                    state="readonly",
                    width=25,
                )
                entry.bind("<<ComboboxSelected>>", self.update_full_class)

            elif field == "classe_complete":
                entry = tk.Entry(frame, width=28)
                entry.configure(state="readonly")

            elif field == "section":
                entry = ttk.Combobox(
                    frame,
                    values=SECTIONS,
                    state="readonly",
                    width=25,
                )

            elif field == "option_etude":
                entry = ttk.Combobox(
                    frame,
                    values=OPTIONS,
                    state="readonly",
                    width=25,
                )

            elif field == "statut":
                entry = ttk.Combobox(
                    frame,
                    values=[
                        "Actif",
                        "Suspendu",
                        "Diplômé",
                        "Abandonné",
                        "Transféré",
                    ],
                    state="readonly",
                    width=25,
                )
                entry.set("Actif")

            elif field in date_fields:
                entry = tk.Entry(frame, width=28)
                entry.insert(0, DATE_PLACEHOLDER)
                entry.bind(
                    "<FocusIn>",
                    lambda event, e=entry: self.clear_date(e),
                )
                entry.bind(
                    "<FocusOut>",
                    lambda event, e=entry: self.restore_date(e),
                )

            elif field in file_fields:
                file_frame = tk.Frame(frame)

                entry = tk.Entry(file_frame, width=22)
                entry.pack(side="left")

                tk.Button(
                    file_frame,
                    text="Choisir",
                    command=lambda e=entry: self.choose_file(e),
                ).pack(side="left", padx=3)

                file_frame.grid(
                    row=row,
                    column=column + 1,
                    sticky="w",
                    padx=5,
                    pady=4,
                )

                self.entries[field] = entry
                continue

            elif field in [
                "presences",
                "absences_non_justifiees",
                "retards",
            ]:
                entry = tk.BooleanVar()

                labels = {
                    "presences": "Présent",
                    "absences_non_justifiees": "Absent",
                    "retards": "Retard",
                }

                tk.Checkbutton(
                    frame,
                    text=labels[field],
                    variable=entry,
                ).grid(
                    row=row,
                    column=column + 1,
                    sticky="w",
                    padx=5,
                    pady=4,
                )

                self.entries[field] = entry
                continue

            else:
                entry = tk.Entry(frame, width=28)

            entry.grid(
                row=row,
                column=column + 1,
                sticky="w",
                padx=5,
                pady=4,
            )

            self.entries[field] = entry

    def create_buttons(self) -> None:
        """Crée les boutons d'action."""
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=8)

        tk.Button(
            button_frame,
            text="Ajouter",
            width=14,
            command=self.add_student,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Modifier",
            width=14,
            command=self.update_student,
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Supprimer",
            width=14,
            command=self.delete_student,
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Voir détails",
            width=14,
            command=self.show_details,
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            button_frame,
            text="Retour",
            width=14,
            command=self.back,
        ).grid(row=0, column=4, padx=5)

    def create_table(self) -> None:
        """Crée le tableau des étudiants."""
        self.table = ttk.Treeview(
            self.root,
            columns=(
                "matricule",
                "nom_complet",
                "sexe",
                "classe",
                "option",
                "section",
                "statut",
            ),
            show="headings",
        )

        headings = {
            "matricule": "Matricule",
            "nom_complet": "Nom complet",
            "sexe": "Sexe",
            "classe": "Classe",
            "option": "Option",
            "section": "Section",
            "statut": "Statut",
        }

        widths = {
            "matricule": 110,
            "nom_complet": 260,
            "sexe": 100,
            "classe": 110,
            "option": 180,
            "section": 180,
            "statut": 110,
        }

        for column, text in headings.items():
            self.table.heading(column, text=text)
            self.table.column(
                column,
                width=widths[column],
                anchor="center",
            )

        self.table.pack(fill="both", expand=True, padx=10, pady=10)
        self.table.bind("<<TreeviewSelect>>", self.fill_selected_student)

    def fill_selected_student(self, event: object | None = None) -> None:
        """Remplit le formulaire avec l'étudiant sélectionné."""
        selected = self.table.selection()

        if not selected:
            return

        values = self.table.item(selected[0])["values"]
        matricule = str(values[0])
        etudiant = self.service.get_by_matricule(matricule)

        if etudiant is None:
            return

        fields = [
            "id",
            "matricule",
            "nom",
            "postnom",
            "prenom",
            "sexe",
            "date_naissance",
            "lieu_naissance",
            "nationalite",
            "etat_civil",
            "photo",
            "classe",
            "option_etude",
            "section",
            "annee_scolaire",
            "numero_inscription",
            "date_inscription",
            "statut",
            "adresse",
            "ville",
            "commune",
            "quartier",
            "telephone",
            "email",
            "nom_pere",
            "telephone_pere",
            "nom_mere",
            "telephone_mere",
            "nom_tuteur",
            "telephone_tuteur",
            "profession_tuteur",
            "adresse_tuteur",
            "montant_total",
            "montant_paye",
            "mode_paiement",
            "date_dernier_paiement",
            "groupe_sanguin",
            "allergies",
            "maladies",
            "personne_urgence",
            "telephone_urgence",
            "acte_naissance",
            "bulletin_precedent",
            "certificat_medical",
            "attestation",
            "presences",
            "absences_justifiees",
            "absences_non_justifiees",
            "retards",
            "avertissements",
            "sanctions",
            "recompenses",
            "observation",
        ]

        data = dict(zip(fields, etudiant))
        self.selected_student_id = int(data["id"])
        classe_complete = str(data.get("classe") or "")

        self.clear_fields()

        for field, value in data.items():
            if field == "id" or field == "classe":
                continue

            widget = self.entries.get(field)

            if widget is None:
                continue

            value_text = "" if value is None else str(value)

            if isinstance(widget, ttk.Combobox):
                widget.set(value_text)
                continue

            if isinstance(widget, tk.BooleanVar):
                widget.set(value_text in ["1", "True", "true"])
                continue

            if isinstance(widget, tk.Entry):
                widget.configure(state="normal")
                widget.delete(0, tk.END)
                widget.insert(0, value_text)

        # Remplir l'affichage de la classe complète
        complete_widget = self.entries.get("classe_complete")
        if isinstance(complete_widget, tk.Entry):
            complete_widget.configure(state="normal")
            complete_widget.delete(0, tk.END)
            complete_widget.insert(0, classe_complete)
            complete_widget.configure(state="readonly")

        self.fill_class_parts(classe_complete)

    def fill_class_parts(self, classe_complete: str) -> None:
        """Remplit la classe et la lettre à partir de la classe complète."""
        classe_widget = self.entries.get("classe")
        lettre_widget = self.entries.get("lettre_classe")

        if not classe_complete:
            return

        parts = classe_complete.split()

        if len(parts) < 2:
            return

        classe = parts[0]
        lettre = " ".join(parts[1:])

        if isinstance(classe_widget, ttk.Combobox):
            classe_widget.set(classe)

        if isinstance(lettre_widget, ttk.Combobox):
            lettre_widget.set(lettre)

    def update_full_class(self, event: object | None = None) -> None:
        """Construit la classe complète, par exemple 6e A."""
        classe_widget = self.entries.get("classe")
        lettre_widget = self.entries.get("lettre_classe")
        complete_widget = self.entries.get("classe_complete")

        if not isinstance(classe_widget, ttk.Combobox):
            return

        if not isinstance(lettre_widget, ttk.Combobox):
            return

        if not isinstance(complete_widget, tk.Entry):
            return

        classe = classe_widget.get().strip()
        lettre = lettre_widget.get().strip()
        classe_complete = ""

        if classe and lettre:
            classe_complete = f"{classe} {lettre}"

        complete_widget.configure(state="normal")
        complete_widget.delete(0, tk.END)
        complete_widget.insert(0, classe_complete)
        complete_widget.configure(state="readonly")

    def clear_date(self, entry: tk.Entry) -> None:
        """Efface le texte indicatif du format de date."""
        if entry.get() == DATE_PLACEHOLDER:
            entry.delete(0, tk.END)

    def restore_date(self, entry: tk.Entry) -> None:
        """Remet le format de date si le champ est vide."""
        if entry.get().strip() == "":
            entry.insert(0, DATE_PLACEHOLDER)

    def choose_file(self, entry: tk.Entry) -> None:
        """Permet de choisir une photo ou un document."""
        file_path = filedialog.askopenfilename(
            title="Choisir un fichier",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg"),
                ("PDF", "*.pdf"),
                ("Tous les fichiers", "*.*"),
            ],
        )

        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    def validate_date(self, date_value: str) -> bool:
        """Vérifie que la date est au format JJ/MM/AAAA."""
        if date_value in ["", DATE_PLACEHOLDER]:
            return True

        try:
            datetime.strptime(date_value, DATE_FORMAT)
            return True
        except ValueError:
            return False

    def validate_class(self, classe: str) -> bool:
        """Vérifie que la classe contient un niveau et une précision."""
        if classe == "":
            return False

        pattern = r"^[1-6]e\s+[A-Za-zÀ-ÿ0-9 -]+$"
        return re.match(pattern, classe) is not None

    def get_form_data(self) -> dict[str, str]:
        """Récupère toutes les données du formulaire."""
        self.update_full_class()
        data = {}

        for field, entry in self.entries.items():
            if isinstance(entry, tk.BooleanVar):
                data[field] = "1" if entry.get() else "0"
            else:
                value = entry.get().strip()

                if value == DATE_PLACEHOLDER:
                    value = ""

                data[field] = value

        return data

    def add_student(self) -> None:
        """Ajoute un étudiant en transmettant via **extra_data."""
        data = self.get_form_data()

        if data.get("matricule", "").strip() == "":
            messagebox.showwarning(
                "Champ obligatoire",
                "Veuillez saisir le matricule.",
            )
            return

        if data.get("nom", "").strip() == "":
            messagebox.showwarning(
                "Champ obligatoire",
                "Veuillez saisir le nom de l'étudiant.",
            )
            return

        if data.get("postnom", "").strip() == "":
            messagebox.showwarning(
                "Champ obligatoire",
                "Veuillez saisir le postnom de l'étudiant.",
            )
            return

        classe_complete = data.get("classe_complete", "").strip()
        if not self.validate_class(classe_complete):
            messagebox.showwarning(
                "Classe invalide",
                "Veuillez choisir une classe complète.",
            )
            return

        # Extraction des paramètres obligatoires attendus par la méthode ajouter
        matricule = data.pop("matricule")
        nom = data.pop("nom")
        postnom = data.pop("postnom")
        prenom = data.pop("prenom", "Non défini")
        sexe = data.pop("sexe", "Homme")

        # Le champ attendu par le service s'appelle 'classe'
        data.pop("classe", None)
        data.pop("classe_complete", None)

        try:
            self.service.ajouter(
                matricule,
                nom,
                postnom,
                classe_complete,
                prenom,
                sexe,
                **data,
            )
        except Exception as error:
            messagebox.showerror("Erreur", str(error))
        else:
            messagebox.showinfo("Succès", "Étudiant ajouté.")
            self.clear_fields()
            self.refresh_table()
            self.refresh_statistics()

    def update_student(self) -> None:
        """Modifie l'étudiant sélectionné."""
        selected = self.table.selection()

        if not selected or self.selected_student_id is None:
            messagebox.showwarning(
                "Attention",
                "Veuillez sélectionner un étudiant à modifier.",
            )
            return

        data = self.get_form_data()

        if data.get("matricule", "").strip() == "":
            messagebox.showwarning(
                "Champ obligatoire",
                "Veuillez saisir le matricule.",
            )
            return

        if data.get("nom", "").strip() == "":
            messagebox.showwarning(
                "Champ obligatoire",
                "Veuillez saisir le nom de l'étudiant.",
            )
            return

        if data.get("postnom", "").strip() == "":
            messagebox.showwarning(
                "Champ obligatoire",
                "Veuillez saisir le postnom de l'étudiant.",
            )
            return

        classe_complete = data.get("classe_complete", "").strip()

        if not self.validate_class(classe_complete):
            messagebox.showwarning(
                "Classe invalide",
                "Veuillez choisir une classe complète.",
            )
            return

        matricule = data.pop("matricule")
        nom = data.pop("nom")
        postnom = data.pop("postnom")
        prenom = data.pop("prenom", "Non défini")
        sexe = data.pop("sexe", "Homme")
        option_etude = data.pop("option_etude", "")
        section = data.pop("section", "")

        data.pop("classe", None)
        data.pop("lettre_classe", None)
        data.pop("classe_complete", None)

        try:
            self.service.modifier(
                student_id=self.selected_student_id,
                matricule=matricule,
                nom=nom,
                postnom=postnom,
                prenom=prenom,
                sexe=sexe,
                classe=classe_complete,
                option_etude=option_etude,
                section=section,
                **data,
            )
        except Exception as error:
            messagebox.showerror("Erreur", str(error))
        else:
            messagebox.showinfo("Succès", "Étudiant modifié.")
            self.selected_student_id = None
            self.refresh_table()
            self.refresh_statistics()

    def delete_student(self) -> None:
        """Supprime un étudiant."""
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Attention",
                "Veuillez sélectionner un étudiant.",
            )
            return

        matricule = self.table.item(selected[0])["values"][0]

        try:
            self.service.supprimer(str(matricule))
        except Exception as error:
            messagebox.showerror("Erreur", str(error))
        else:
            messagebox.showinfo("Succès", "Étudiant supprimé.")
            self.selected_student_id = None
            self.refresh_table()
            self.refresh_statistics()

    def refresh_table(self) -> None:
        """Recharge le tableau complète."""
        for row in self.table.get_children():
            self.table.delete(row)

        for etudiant in self.service.lister_complet():
            (
                matricule,
                nom,
                postnom,
                prenom,
                sexe,
                classe,
                option_etude,
                section,
                _telephone,
                _montant_total,
                _montant_paye,
                statut,
            ) = etudiant

            nom_complet = f"{nom} {postnom} {prenom}".strip()

            self.table.insert(
                "",
                "end",
                values=(
                    matricule,
                    nom_complet,
                    sexe,
                    classe,
                    option_etude or "",
                    section or "",
                    statut,
                ),
            )

    def refresh_statistics(self) -> None:
        """Affiche le total général et le total par classe."""
        total = self.service.total_etudiants()
        stats = self.service.statistiques_par_classe()

        text = f"Total général des élèves : {total}"

        if stats:
            details = " | ".join(
                f"{classe} : {nombre}" for classe, nombre in stats
            )
            text = f"{text}    ({details})"

        self.stats_label.config(text=text)

    def search_students(self) -> None:
        """Recherche localement dans le tableau."""
        keyword = self.search_entry.get().lower().strip()
        classe_filter = self.filter_classe.get().lower().strip()

        self.refresh_table()

        for row in self.table.get_children():
            values = self.table.item(row)["values"]
            row_text = " ".join(str(value).lower() for value in values)

            match_keyword = keyword in row_text
            match_classe = classe_filter == "" or classe_filter in row_text

            if not match_keyword or not match_classe:
                self.table.delete(row)

    def show_details(self) -> None:
        """Affiche les détails de l'étudiant sélectionné."""
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Attention",
                "Veuillez sélectionner un étudiant.",
            )
            return

        values = self.table.item(selected[0])["values"]

        detail_window = tk.Toplevel(self.root)
        detail_window.title("Détails de l'étudiant")
        detail_window.geometry("500x400")

        tk.Label(
            detail_window,
            text="Fiche détaillée de l'étudiant",
            font=("Arial", 16, "bold"),
        ).pack(pady=10)

        labels = [
            "Matricule",
            "Nom complet",
            "Sexe",
            "Classe",
            "Option",
            "Section",
            "Statut",
        ]

        for label, value in zip(labels, values):
            tk.Label(
                detail_window,
                text=f"{label} : {value}",
                anchor="w",
                font=("Arial", 11),
            ).pack(fill="x", padx=30, pady=4)

    def clear_fields(self) -> None:
        """Vide tous les champs."""
        for field, entry in self.entries.items():
            if isinstance(entry, ttk.Combobox):
                entry.set("")
                continue

            if isinstance(entry, tk.BooleanVar):
                entry.set(False)
                continue

            if isinstance(entry, tk.Entry):
                entry.configure(state="normal")
                entry.delete(0, tk.END)

                if field in [
                    "date_naissance",
                    "date_inscription",
                    "date_dernier_paiement",
                ]:
                    entry.insert(0, DATE_PLACEHOLDER)

                if field == "classe_complete":
                    entry.configure(state="readonly")

        if isinstance(self.entries.get("sexe"), ttk.Combobox):
            self.entries["sexe"].set("Homme")

        if isinstance(self.entries.get("statut"), ttk.Combobox):
            self.entries["statut"].set("Actif")

    def back(self) -> None:
        """Retourne au tableau de bord."""
        from dashboard_view import DashboardView

        for widget in self.root.winfo_children():
            widget.destroy()

        DashboardView(self.root, self.utilisateur)
