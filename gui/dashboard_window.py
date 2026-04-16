import tkinter as tk
from tkinter import messagebox, ttk

from gui.attendance_window import AttendanceWindow
from gui.employee_window import EmployeeManagerWindow
from gui.payroll_window import PayrollWindow
from gui.salary_window import SalaryWindow


class DashboardWindow:
    def __init__(self, root, auth_service, on_logout):
        self.root = root
        self.auth_service = auth_service
        self.on_logout = on_logout

        self.root.title("Payroll Management System - Dashboard")

        self.root.state("zoomed")
        self.root.minsize(900, 600)

        self._setup_style()
        self._create_widgets()

    # ---------------- STYLE ---------------- #

    def _setup_style(self):

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.root.configure(bg="#eef2f7")

        self.style.configure("Header.TFrame", background="#1f3c5b")

        self.style.configure(
            "Header.TLabel",
            background="#1f3c5b",
            foreground="white",
            font=("Segoe UI", 20, "bold"),
        )

        self.style.configure(
            "SubHeader.TLabel",
            background="#1f3c5b",
            foreground="#dce6f1",
            font=("Segoe UI", 11),
        )

        self.style.configure(
            "Dashboard.TButton",
            font=("Segoe UI", 13, "bold"),
            padding=18,
        )

        self.style.configure(
            "Logout.TButton",
            font=("Segoe UI", 12, "bold"),
            foreground="white",
            background="#e74c3c",
            padding=12,
        )

        self.style.map("Logout.TButton", background=[("active", "#c0392b")])

    # ---------------- UI ---------------- #

    def _create_widgets(self):

        admin = self.auth_service.current_user

        # Header
        header = ttk.Frame(self.root, style="Header.TFrame", height=70)
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Payroll Management System",
            style="Header.TLabel"
        ).pack(side="left", padx=25)

        ttk.Label(
            header,
            text=f"Logged in as: {admin['username']}",
            style="SubHeader.TLabel"
        ).pack(side="right", padx=25)

        # Main container
        container = ttk.Frame(self.root)
        container.pack(expand=True)

        # Card
        card = ttk.Frame(container, padding=50, relief="ridge")
        card.pack()

        # Buttons
        ttk.Button(
            card,
            text="Manage Employees",
            style="Dashboard.TButton",
            command=self.open_employee_window,
            width=25,
        ).grid(row=0, column=0, padx=30, pady=30)

        ttk.Button(
            card,
            text="Generate Payroll",
            style="Dashboard.TButton",
            command=self.open_payroll_window,
            width=25,
        ).grid(row=0, column=1, padx=30, pady=30)

        ttk.Button(
            card,
            text="Attendance",
            style="Dashboard.TButton",
            command=self.open_attendance_window,
            width=25,
        ).grid(row=1, column=0, padx=30, pady=30)

        ttk.Button(
            card,
            text="Salary Structure",
            style="Dashboard.TButton",
            command=self.open_salary_window,
            width=25,
        ).grid(row=1, column=1, padx=30, pady=30)

        # Logout
        logout_frame = ttk.Frame(self.root)
        logout_frame.pack(pady=20)

        ttk.Button(
            logout_frame,
            text="Logout",
            style="Logout.TButton",
            command=self.logout,
            width=20,
        ).pack()

    def restore_window(self):
        self.root.state("zoomed")
        self.root.update_idletasks()

    # ---------------- NAVIGATION ---------------- #

    def open_employee_window(self):
        window = EmployeeManagerWindow(self.root, self.root)
        self.root.wait_window(window.window)
        self.restore_window()

    def open_attendance_window(self):
        window = AttendanceWindow(self.root, self.root)
        self.root.wait_window(window.window)
        self.restore_window()

    def open_salary_window(self):
        window = SalaryWindow(self.root, self.root)
        self.root.wait_window(window.window)
        self.restore_window()

    def open_payroll_window(self):
        window = PayrollWindow(self.root, self.root)
        self.root.wait_window(window.window)
        self.restore_window()

    # ---------------- LOGOUT ---------------- #

    def logout(self):
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
            self.auth_service.logout_admin()
            self.on_logout()