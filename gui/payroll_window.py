import tkinter as tk
from tkinter import messagebox, ttk

from database.employee_dao import EmployeeDAO
from services.payroll_service import PayrollService


class PayrollWindow:
    def __init__(self, parent, dashboard_root):
        self.parent = parent
        self.dashboard_root = dashboard_root

        self.window = tk.Toplevel(parent)
        self.window.title("Payroll Generation")

        self.window.state("zoomed")
        self.window.minsize(1000, 700)

        self.employee_dao = EmployeeDAO()
        self.payroll_service = PayrollService()

        self._setup_style()
        self._create_widgets()

        self.load_employees()

        self.window.protocol("WM_DELETE_WINDOW", self.go_back)

    # ---------------- STYLE ---------------- #

    def _setup_style(self):
        style = ttk.Style()

        # ✅ REMOVE BLUE THEME
        style.theme_use("default")

        # Base colors
        style.configure(".",
            background="#f5f5f5",
            foreground="#333333"
        )

        # Title
        style.configure("Title.TLabel",
            font=("Segoe UI", 20, "bold"),
            background="#f5f5f5"
        )

        # Section
        style.configure("Section.TLabelframe",
            background="#f5f5f5",
            padding=18
        )

        style.configure("Section.TLabelframe.Label",
            font=("Segoe UI", 12, "bold"),
            background="#f5f5f5"
        )

        # Inputs
        style.configure("TEntry", fieldbackground="#ffffff")
        style.configure("TCombobox", fieldbackground="#ffffff")

        style.map("TEntry",
            bordercolor=[("focus", "#999999")]
        )

        style.map("TCombobox",
            bordercolor=[("focus", "#999999")]
        )

        # Buttons
        style.configure("Success.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=8,
            foreground="white",
            background="#28a745"   
        )

        style.map("Success.TButton",
            background=[("active", "#218838")]  
        )

        style.configure("Danger.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=8,
            foreground="white",
            background="#d9534f"
        )

        style.map("Danger.TButton",
            background=[("active", "#c9302c")]
        )

    # ---------------- UI ---------------- #

    def _create_widgets(self):

        header = ttk.Frame(self.window, padding=12)
        header.pack(fill="x")

        ttk.Button(
            header,
            text="⬅ Back to Dashboard",
            style="Action.TButton",
            command=self.go_back,
        ).pack(anchor="w")

        ttk.Label(
            self.window,
            text="Payroll Generation",
            style="Title.TLabel",
        ).pack(pady=(5, 15))

        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=15, pady=10)

        form = ttk.Labelframe(
            main_frame,
            text="Generate Payroll",
            style="Section.TLabelframe"
        )
        form.pack(pady=20)

        ttk.Label(form, text="Employee").grid(row=0, column=0, sticky="w", pady=10)

        self.employee_combo = ttk.Combobox(
            form,
            width=30,
            state="readonly"
        )
        self.employee_combo.grid(row=0, column=1, pady=10)

        ttk.Label(form, text="Month-Year").grid(row=1, column=0, sticky="w", pady=10)

        self.month_entry = ttk.Entry(form, width=30)
        self.month_entry.grid(row=1, column=1, pady=10)
        self.month_entry.insert(0, "2025-03")

        form.columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

        ttk.Button(
            btn_frame,
            text="Generate Payslip",
            style="Success.TButton",
            command=self.generate_payroll
        ).pack(side="left", padx=10)

        ttk.Button(
            btn_frame,
            text="Back",
            style="Danger.TButton",
            command=self.go_back
        ).pack(side="left", padx=10)

    # ---------------- DATA ---------------- #

    def load_employees(self):
        self.employees = self.employee_dao.get_all_active()

        display_list = [
            f"{e['emp_id']} - {e['full_name']}" for e in self.employees
        ]

        self.employee_combo["values"] = display_list

        if display_list:
            self.employee_combo.current(0)

    # ---------------- ACTIONS ---------------- #

    def generate_payroll(self):

        if not self.employee_combo.get():
            messagebox.showerror("Error", "Select an employee first")
            return

        month_year = self.month_entry.get().strip()

        if not month_year:
            messagebox.showerror("Error", "Enter Month-Year")
            return

        try:
            emp_id = int(self.employee_combo.get().split("-")[0].strip())

            payroll_id = self.payroll_service.generate_payroll(
                emp_id=emp_id,
                month_year=month_year
            )

            messagebox.showinfo(
                "Success",
                f"Payroll generated successfully\nID: {payroll_id}"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- NAVIGATION ---------------- #

    def go_back(self):
        self.window.destroy()