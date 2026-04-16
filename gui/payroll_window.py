import tkinter as tk
from tkinter import messagebox, ttk

from database.employee_dao import EmployeeDAO
from services.payroll_service import PayrollService


class PayrollWindow:
    def __init__(self, parent):
        self.parent = parent

        self.window = tk.Toplevel(parent)
        self.window.title("Payroll Generation")
        self.window.state("zoomed")
        self.window.configure(bg="#eef2f7")

        self.employee_dao = EmployeeDAO()
        self.payroll_service = PayrollService()

        self._setup_style()
        self._create_widgets()
        self.load_employees()

    def _setup_style(self):
        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "TCombobox",
            padding=6,
            font=("Segoe UI", 11)
        )

        style.configure(
            "TEntry",
            padding=6,
            font=("Segoe UI", 11)
        )

    def _create_widgets(self):

        # Main container
        container = tk.Frame(self.window, bg="#eef2f7")
        container.pack(expand=True)

        # Card
        card = tk.Frame(
            container,
            bg="white",
            padx=50,
            pady=40,
            bd=0,
            highlightthickness=1,
            highlightbackground="#dcdde1"
        )
        card.pack()

        # Title
        title = tk.Label(
            card,
            text="Payroll Generation",
            font=("Segoe UI", 22, "bold"),
            bg="white",
            fg="#2f3640"
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        label_font = ("Segoe UI", 12)
        entry_font = ("Segoe UI", 11)

        # Employee
        tk.Label(card, text="Employee", font=label_font, bg="white").grid(
            row=1, column=0, sticky="e", pady=10, padx=10
        )

        self.employee_combo = ttk.Combobox(
            card,
            width=35,
            font=entry_font,
            state="readonly"
        )
        self.employee_combo.grid(row=1, column=1, pady=10, ipady=3)

        # Month-Year
        tk.Label(card, text="Month-Year", font=label_font, bg="white").grid(
            row=2, column=0, sticky="e", pady=10, padx=10
        )

        self.month_entry = ttk.Entry(card, width=37)
        self.month_entry.grid(row=2, column=1, pady=10, ipady=3)
        self.month_entry.insert(0, "March-2025")

        # Buttons
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=30)

        generate_btn = tk.Button(
            btn_frame,
            text="Generate Payslip",
            font=("Segoe UI", 12, "bold"),
            bg="#4cd137",
            fg="white",
            activebackground="#44bd32",
            activeforeground="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.generate_payroll
        )
        generate_btn.pack(side="left", padx=10)

        back_btn = tk.Button(
            btn_frame,
            text="Back",
            font=("Segoe UI", 12, "bold"),
            bg="#e84118",
            fg="white",
            activebackground="#c23616",
            activeforeground="white",
            width=14,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.go_back
        )
        back_btn.pack(side="left", padx=10)

    def load_employees(self):
        self.employees = self.employee_dao.get_all_active()

        display_list = [
            f"{e['emp_id']} - {e['full_name']}" for e in self.employees
        ]

        self.employee_combo["values"] = display_list

        if display_list:
            self.employee_combo.current(0)

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

    def go_back(self):
        self.window.destroy()