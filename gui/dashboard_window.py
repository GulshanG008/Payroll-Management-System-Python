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
        self.root.geometry("900x600")

        self._center_window(900, 600)
        self._setup_style()
        self._create_widgets()

    def _center_window(self, width, height):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw // 2) - (width // 2)
        y = (sh // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _setup_style(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("Header.TFrame", background="#003366")

        self.style.configure(
            "Header.TLabel",
            background="#003366",
            foreground="white",
            font=("Segoe UI", 18, "bold"),
        )

        self.style.configure(
            "SubHeader.TLabel",
            background="#003366",
            foreground="white",
            font=("Segoe UI", 11),
        )

        self.style.configure("Dashboard.TButton", font=("Segoe UI", 12), padding=10)

        self.style.configure(
            "Logout.TButton",
            font=("Segoe UI", 11, "bold"),
            foreground="white",
            background="#ff6666",
        )

        self.style.map("Logout.TButton", background=[("active", "#ff4d4d")])

    def _create_widgets(self):
        admin = self.auth_service.current_user

        header = ttk.Frame(self.root, style="Header.TFrame", height=60)
        header.pack(fill="x")

        ttk.Label(header, text="Payroll Management System", style="Header.TLabel").pack(
            side="left", padx=20
        )

        ttk.Label(
            header, text=f"Logged in as: {admin['username']}", style="SubHeader.TLabel"
        ).pack(side="right", padx=20)

        card = ttk.Frame(self.root, padding=40, relief="solid")
        card.pack(pady=60)

        ttk.Button(
            card,
            text="Manage Employees",
            style="Dashboard.TButton",
            command=self.open_employee_window,
        ).grid(row=0, column=0, padx=40, pady=25)

        ttk.Button(
            card,
            text="Generate Payroll",
            style="Dashboard.TButton",
            command=self.generate_payroll,
        ).grid(row=0, column=1, padx=40, pady=25)

        ttk.Button(
            card,
            text="Attendance",
            style="Dashboard.TButton",
            command=self.open_attendance_window,
        ).grid(row=1, column=0, padx=40, pady=25)

        ttk.Button(
            card,
            text="Salary Structure",
            style="Dashboard.TButton",
            command=self.open_salary_window,
        ).grid(row=1, column=1, padx=40, pady=25)

        ttk.Button(
            self.root, text="Logout", style="Logout.TButton", command=self.logout
        ).pack(pady=(10, 30))

    def open_employee_window(self):
        self.root.withdraw()
        EmployeeManagerWindow(self.root, self.root)

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
