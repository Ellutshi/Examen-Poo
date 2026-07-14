"""Point d'entrée principal de l'application EduManager."""

import tkinter as tk

from database import DatabaseConnection
from login_view import LoginView


def main() -> None:
    """Lance l'application EduManager."""
    db = DatabaseConnection()
    db.create_tables()

    root = tk.Tk()
    LoginView(root)
    root.mainloop()


if __name__ == "__main__":
    main()