# main.py

import tkinter as tk

from services.auth_service import AuthService
from gui.login_window import LoginWindow
from gui.dashboard_window import DashboardWindow


class PayrollApp:
    def __init__(self, root):
        self.root = root
        self.auth_service = AuthService()

        self.show_login()

    def show_login(self):
        self._clear_root()
        LoginWindow(
            root=self.root,
            auth_service=self.auth_service,
            on_login_success=self.show_dashboard
        )

    def show_dashboard(self):
        self._clear_root()
        DashboardWindow(
            root=self.root,
            auth_service=self.auth_service,
            on_logout=self.show_login
        )

    def _clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# APPLICATION START
if __name__ == "__main__":
    root = tk.Tk()
    app = PayrollApp(root)
    root.mainloop()