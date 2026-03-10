import tkinter as tk
from tkinter import messagebox, ttk

from database.employee_dao import EmployeeDAO
from services.payroll_service import PayrollService


class PayrollWindow:
    def __init__(self, parent):

        self.parent = parent

        self.window = tk.Toplevel(parent)
        self.window.title("Generate Payroll")

        # open full screen
        self.window.state("zoomed")
        self.window.minsize(900, 600)

        # keep it linked to dashboard
        self.window.transient(parent)
        self.window.grab_set()

        self.employee_dao = EmployeeDAO()
        self.payroll_service = PayrollService()

        self._create_widgets()
        self.load_employees()

    def _create_widgets(self):

        title = tk.Label(
            self.window,
            text="Payroll Generation",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=20)

        form = tk.Frame(self.window)
        form.pack(pady=20)

        # Employee
        tk.Label(form, text="Employee").grid(
            row=0, column=0, pady=10, padx=10, sticky="e"
        )

        self.employee_combo = ttk.Combobox(
            form,
            width=35,
            state="readonly"
        )
        self.employee_combo.grid(row=0, column=1, pady=10)

        # Month-Year
        tk.Label(form, text="Month-Year").grid(
            row=1, column=0, pady=10, padx=10, sticky="e"
        )

        self.month_entry = tk.Entry(form, width=38)
        self.month_entry.grid(row=1, column=1, pady=10)
        self.month_entry.insert(0, "March-2025")

        # Button area
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=30)

        tk.Button(
            btn_frame,
            text="Generate Payslip",
            width=20,
            command=self.generate_payroll
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Back to Dashboard",
            width=20,
            command=self.go_back
        ).pack(side="left", padx=10)

    def load_employees(self):

        self.employees = self.employee_dao.get_all_active()

        display_list = [
            f"{e['emp_id']} - {e['full_name']}"
            for e in self.employees
        ]

        self.employee_combo["values"] = display_list

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

    def go_back(self):
        self.window.destroy()