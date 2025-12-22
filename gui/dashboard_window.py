import tkinter as tk
from tkinter import messagebox

from gui.attendance_window import AttendanceWindow
from gui.employee_window import EmployeeManagerWindow
from gui.payroll_window import PayrollWindow
from gui.salary_window import SalaryWindow


class DashboardWindow:
    TITLE_FONT = ("Segoe UI", 18, "bold")
    HEADER_FONT = ("Segoe UI", 11)
    BUTTON_FONT = ("Segoe UI", 12)
    LOGOUT_FONT = ("Segoe UI", 11, "bold")

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

        header = tk.Frame(self.root, bg="#003366", height=60)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Payroll Management System",
            font=self.TITLE_FONT,
            bg="#003366",
            fg="white",
        ).pack(side="left", padx=20)

        tk.Label(
            header,
            text=f"Logged in as: {admin['username']}",
            font=self.HEADER_FONT,
            bg="#003366",
            fg="white",
        ).pack(side="right", padx=20)

        card = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        card.pack(pady=60, padx=80)

        button_font = self.BUTTON_FONT

        # Row 0
        tk.Button(
            card,
            text="Manage Employees",
            width=22,
            height=2,
            font=button_font,
            relief="raised",
            bd=2,
            command=self.open_employee_window,
        ).grid(row=0, column=0, padx=40, pady=25)

        tk.Button(
            card,
            text="Generate Payroll",
            width=22,
            height=2,
            font=button_font,
            relief="raised",
            bd=2,
            command=self.generate_payroll,
        ).grid(row=0, column=1, padx=40, pady=25)

        # Row 1
        tk.Button(
            card,
            text="Attendance",
            width=22,
            height=2,
            font=button_font,
            relief="raised",
            bd=2,
            command=self.open_attendance_window,
        ).grid(row=1, column=0, padx=40, pady=25)

        tk.Button(
            card,
            text="Salary Structure",
            width=22,
            height=2,
            font=button_font,
            relief="raised",
            bd=2,
            command=self.open_salary_window,
        ).grid(row=1, column=1, padx=40, pady=25)

        tk.Button(
            self.root,
            text="Logout",
            width=15,
            font=self.LOGOUT_FONT,
            bg="#ff6666",
            fg="white",
            relief="flat",
            command=self.logout,
        ).pack(pady=(10, 30))

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
