# gui/dashboard_window.py

import tkinter as tk
from tkinter import messagebox

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
        self.root.geometry("900x600")
        self.root.configure(bg="#e8f0fe")

        self._center_window(900, 600)
        self._create_widgets()

    def _center_window(self, width, height):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw // 2) - (width // 2)
        y = (sh // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _create_widgets(self):
        admin = self.auth_service.current_user

        # Header
        header = tk.Frame(self.root, bg="#003366", height=60)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Payroll Management System",
            font=("Arial", 18, "bold"),
            bg="#003366",
            fg="white",
        ).pack(side="left", padx=20)

        tk.Label(
            header,
            text=f"Logged in as: {admin['username']}",
            font=("Arial", 11),
            bg="#003366",
            fg="white",
        ).pack(side="right", padx=20)

        # Main content
        content = tk.Frame(self.root, bg="#e8f0fe")
        content.pack(pady=70)

        button_font = ("Arial", 12)

        # Row 0
        tk.Button(
            content,
            text="Manage Employees",
            width=22,
            height=2,
            font=button_font,
            command=self.open_employee_window,
        ).grid(row=0, column=0, padx=30, pady=20)

        tk.Button(
            content,
            text="Generate Payroll",
            width=22,
            height=2,
            font=button_font,
            command=self.generate_payroll,
        ).grid(row=0, column=1, padx=30, pady=20)

        # Row 1
        tk.Button(
            content,
            text="Attendance",
            width=22,
            height=2,
            font=button_font,
            command=self.open_attendance_window,
        ).grid(row=1, column=0, padx=30, pady=20)

        tk.Button(
            content,
            text="Salary Structure",
            width=22,
            height=2,
            font=button_font,
            command=self.open_salary_window,
        ).grid(row=1, column=1, padx=30, pady=20)

        # Logout
        tk.Button(
            self.root,
            text="Logout",
            width=15,
            font=("Arial", 11, "bold"),
            bg="#ff6666",
            fg="white",
            command=self.logout,
        ).pack(pady=30)

    def open_employee_window(self):
        EmployeeManagerWindow(self.root)

    def open_attendance_window(self):
        AttendanceWindow(self.root)

    def open_salary_window(self):
        SalaryWindow(self.root)

    def generate_payroll(self):
        PayrollWindow(self.root)

    def logout(self):
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
            self.auth_service.logout_admin()
            self.on_logout()
