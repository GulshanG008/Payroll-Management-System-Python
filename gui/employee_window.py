# gui/employee_window.py

import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal
from datetime import date

from database.employee_dao import EmployeeDAO


class EmployeeManagerWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        self.dao = EmployeeDAO()

        self._create_widgets()
        self.load_employees()

    # --------------------------------------------------
    def _create_widgets(self):
        tk.Label(
            self.root,
            text="Employee Management",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # -------- Form --------
        form_frame = tk.LabelFrame(
            main_frame,
            text="Employee Details",
            font=("Arial", 12)
        )
        form_frame.pack(side="left", fill="y", padx=10)

        labels = ["Employee Code", "Full Name", "Gender", "Email", "Basic Salary"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label).grid(row=i, column=0, pady=5, sticky="w")
            entry = tk.Entry(form_frame, width=25)
            entry.grid(row=i, column=1, pady=5)
            self.entries[label] = entry

        tk.Button(
            form_frame,
            text="Add Employee",
            width=20,
            command=self.add_employee
        ).grid(row=len(labels), column=0, columnspan=2, pady=10)

        tk.Button(
            form_frame,
            text="Deactivate Selected",
            width=20,
            command=self.deactivate_employee
        ).grid(row=len(labels) + 1, column=0, columnspan=2, pady=5)

        # -------- Table --------
        table_frame = tk.Frame(main_frame)
        table_frame.pack(side="right", fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Code", "Name", "Salary", "Status"),
            show="headings"
        )
        self.tree.pack(fill="both", expand=True)

        for col in ("ID", "Code", "Name", "Salary", "Status"):
            self.tree.heading(col, text=col)

    # --------------------------------------------------
    def load_employees(self):
        self.tree.delete(*self.tree.get_children())

        employees = self.dao.get_all_active()

        for emp in employees:
            self.tree.insert(
                "",
                "end",
                values=(
                    emp["emp_id"],
                    emp["emp_code"],
                    emp["full_name"],
                    emp["basic_salary"],
                    emp["status"]
                )
            )

    # --------------------------------------------------
    def add_employee(self):
        try:
            emp_code = self.entries["Employee Code"].get().strip()
            full_name = self.entries["Full Name"].get().strip()
            gender = self.entries["Gender"].get().strip()
            email = self.entries["Email"].get().strip()
            salary = Decimal(self.entries["Basic Salary"].get().strip())

            if not emp_code or not full_name:
                raise ValueError("Required fields missing")

            self.dao.create_employee(
                emp_code=emp_code,
                full_name=full_name,
                gender=gender,
                contact_no="",
                email=email,
                date_of_joining=date.today(),
                basic_salary=salary,
                structure_id=None
            )

            self.load_employees()
            messagebox.showinfo("Success", "Employee added successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --------------------------------------------------
    def deactivate_employee(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select an employee")
            return

        emp_id = self.tree.item(selected)["values"][0]

        if messagebox.askyesno("Confirm", "Deactivate selected employee?"):
            self.dao.deactivate_employee(emp_id)
            self.load_employees()
