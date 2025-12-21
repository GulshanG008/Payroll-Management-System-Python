# gui/payroll_window.py

import tkinter as tk
from tkinter import ttk, messagebox

from database.employee_dao import EmployeeDAO
from services.payroll_service import PayrollService


class PayrollWindow:
    """
    GUI window to generate payroll and payslip PDF.
    """

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Generate Payroll")
        self.window.geometry("500x400")
        self.window.resizable(False, False)

        self.employee_dao = EmployeeDAO()
        self.payroll_service = PayrollService()

        self._create_widgets()
        self.load_employees()

    # --------------------------------------------------
    def _create_widgets(self):
        tk.Label(
            self.window,
            text="Generate Payroll",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        form = tk.Frame(self.window)
        form.pack(pady=20)

        # Employee
        tk.Label(form, text="Employee").grid(row=0, column=0, pady=10, sticky="e")
        self.employee_combo = ttk.Combobox(form, width=30, state="readonly")
        self.employee_combo.grid(row=0, column=1, pady=10)

        # Month-Year
        tk.Label(form, text="Month-Year").grid(row=1, column=0, pady=10, sticky="e")
        self.month_entry = tk.Entry(form, width=33)
        self.month_entry.grid(row=1, column=1, pady=10)
        self.month_entry.insert(0, "March-2025")

        tk.Button(
            self.window,
            text="Generate Payslip",
            width=20,
            command=self.generate_payroll
        ).pack(pady=25)

    # --------------------------------------------------
    def load_employees(self):
        self.employees = self.employee_dao.get_all_active()
        display_list = [
            f"{e['emp_id']} - {e['full_name']}"
            for e in self.employees
        ]
        self.employee_combo["values"] = display_list

    # --------------------------------------------------
    def generate_payroll(self):
        if not self.employee_combo.get():
            messagebox.showerror("Error", "Please select an employee")
            return

        try:
            emp_id = int(self.employee_combo.get().split("-")[0].strip())
            month_year = self.month_entry.get().strip()

            payroll_id = self.payroll_service.generate_payroll(
                emp_id=emp_id,
                month_year=month_year
            )

            messagebox.showinfo(
                "Success",
                f"Payroll generated successfully (ID: {payroll_id})"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))