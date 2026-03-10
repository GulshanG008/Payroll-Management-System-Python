import tkinter as tk
from tkinter import messagebox, ttk

from database.employee_dao import EmployeeDAO
from services.payroll_service import PayrollService


class PayrollWindow:
    def __init__(self, parent):

        self.parent = parent

        self.window = tk.Toplevel(parent)
        self.window.title("Payroll Generation")

        # full screen
        self.window.state("zoomed")

        # styling
        self.window.configure(bg="#f5f6fa")

        self.employee_dao = EmployeeDAO()
        self.payroll_service = PayrollService()

        self._create_widgets()
        self.load_employees()

    def _create_widgets(self):

        title = tk.Label(
            self.window,
            text="Payroll Generation",
            font=("Segoe UI", 22, "bold"),
            bg="#f5f6fa",
            fg="#2f3640",
        )
        title.pack(pady=30)

        # card style container
        card = tk.Frame(self.window, bg="white", padx=40, pady=40, bd=1, relief="solid")
        card.pack(pady=20)

        form = tk.Frame(card, bg="white")
        form.pack()

        label_font = ("Segoe UI", 13)
        entry_font = ("Segoe UI", 12)

        # Employee
        tk.Label(form, text="Employee", font=label_font, bg="white").grid(
            row=0, column=0, pady=15, padx=10, sticky="e"
        )

        self.employee_combo = ttk.Combobox(
            form, width=35, font=entry_font, state="readonly"
        )
        self.employee_combo.grid(row=0, column=1, pady=15)

        # Month-Year
        tk.Label(form, text="Month-Year", font=label_font, bg="white").grid(
            row=1, column=0, pady=15, padx=10, sticky="e"
        )

        self.month_entry = tk.Entry(form, width=38, font=entry_font)
        self.month_entry.grid(row=1, column=1, pady=15)
        self.month_entry.insert(0, "March-2025")

        # button section
        btn_frame = tk.Frame(self.window, bg="#f5f6fa")
        btn_frame.pack(pady=30)

        generate_btn = tk.Button(
            btn_frame,
            text="Generate Payslip",
            font=("Segoe UI", 13, "bold"),
            bg="#4cd137",
            fg="white",
            width=18,
            height=2,
            bd=0,
            command=self.generate_payroll,
        )
        generate_btn.pack(side="left", padx=15)

        back_btn = tk.Button(
            btn_frame,
            text="Back to Dashboard",
            font=("Segoe UI", 13, "bold"),
            bg="#e84118",
            fg="white",
            width=18,
            height=2,
            bd=0,
            command=self.go_back,
        )
        back_btn.pack(side="left", padx=15)

    def load_employees(self):

        self.employees = self.employee_dao.get_all_active()

        display_list = [f"{e['emp_id']} - {e['full_name']}" for e in self.employees]

        self.employee_combo["values"] = display_list

    def generate_payroll(self):

        if not self.employee_combo.get():
            messagebox.showerror("Error", "Please select an employee")
            return

        try:
            emp_id = int(self.employee_combo.get().split("-")[0].strip())
            month_year = self.month_entry.get().strip()

            payroll_id = self.payroll_service.generate_payroll(
                emp_id=emp_id, month_year=month_year
            )

            messagebox.showinfo(
                "Success", f"Payroll generated successfully (ID: {payroll_id})"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_back(self):
        self.window.destroy()
