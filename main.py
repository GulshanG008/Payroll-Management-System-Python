# main.py

import tkinter as tk

from services.auth_service import AuthService
from gui.login_window import LoginWindow
from gui.dashboard_window import DashboardWindow


class PayrollManagementApp:
    """
    Main application controller.
    Handles screen switching and shared services.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Payroll Management System")

        # Shared service instances
        self.auth_service = AuthService()

        self.show_login()

    # --------------------------------------------------
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --------------------------------------------------
    def show_login(self):
        self.clear_window()
        LoginWindow(
            root=self.root,
            auth_service=self.auth_service,
            on_login_success=self.show_dashboard
        )

    # --------------------------------------------------
    def show_dashboard(self):
        self.clear_window()
        DashboardWindow(
            root=self.root,
            auth_service=self.auth_service,
            on_logout=self.show_login
        )


# ------------------------------------------------------
# Application Entry Point
# ------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PayrollManagementApp(root)
    root.mainloop()
