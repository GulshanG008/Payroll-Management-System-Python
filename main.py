import tkinter as tk
from tkinter import messagebox

# GUI windows
from gui.components.login_window import LoginWindow
from gui.components.dashboard_window import DashboardWindow

# Database
from database.connection import DatabaseConnection

# Services
from services.auth_service import AuthService


class PayrollManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Payroll Management System")
        self.root.geometry("900x600")
        self.root.state("zoomed")

        # Initialize database
        try:
            self.db = DatabaseConnection()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            self.root.destroy()
            return

        # Initialize services
        self.auth_service = AuthService(self.db)

        # Load first screen
        self.show_login()

    # ---------------- Screen Loaders ---------------- #

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()
        LoginWindow(
            parent=self.root,
            auth_service=self.auth_service,
            on_login_success=self.show_dashboard
        )

    def show_dashboard(self, admin):
        self.clear_window()
        DashboardWindow(
            parent=self.root,
            admin=admin,
            on_logout=self.show_login
        )


def main():
    root = tk.Tk()
    app = PayrollManagementSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
