# gui/employee_window.py

import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal
from datetime import date

from database.employee_dao import EmployeeDAO


class EmployeeManagerWindow:
    """
    GUI window to manage employees (Add / View / Deactivate).
    """

    def __init__(self, root):
        self.root = tk.Toplevel(root)
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

        # ---------------- FORM ----------------
        form = tk.LabelFrame(main_frame, text="Add Employee", font=("Arial", 12))
        form.pack(side="left", fill="y", padx=10)

        labels = [
            "Employee Code",
            "Full Name",
            "Gender",
            "Contact No",
            "Email",
            "Basic Salary"
        ]

        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(form, text=label).grid(row=i, column=0, pady=6, sticky="w")
            entry = tk.Entry(form, width=25)
            entry.grid(row=i, column=1, pady=6)
            self.entries[label] = entry

        tk.Button(
            form,
            text="Add Employee",
            width=20,
            command=self.add_employee
        ).grid(row=len(labels), column=0, columnspan=2, pady=15)

        # ---------------- TABLE ----------------
        table_frame = tk.Frame(main_frame)
        table_frame.pack(side="right", fill="both", expand=True)

        columns = (
            "ID",
            "Code",
            "Name",
            "Gender",
            "Contact",
            "Salary",
            "Status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )
        self.tree.pack(fill="both", expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        tk.Button(
            self.root,
            text="Deactivate Selected Employee",
            bg="#ff6666",
            fg="white",
            command=self.deactivate_employee
        ).pack(pady=10)

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
                    emp["gender"],
                    emp["contact_no"],
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
            contact = self.entries["Contact No"].get().strip()
            email = self.entries["Email"].get().strip()
            salary = Decimal(self.entries["Basic Salary"].get().strip())

            if not emp_code or not full_name:
                raise ValueError("Employee Code and Full Name are required")

            self.dao.create_employee(
                emp_code=emp_code,
                full_name=full_name,
                gender=gender,
                contact_no=contact,
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
            messagebox.showerror("Error", "Please select an employee")
            return

        emp_id = self.tree.item(selected)["values"][0]

        if messagebox.askyesno(
            "Confirm",
            "Are you sure you want to deactivate this employee?"
        ):
            self.dao.deactivate_employee(emp_id)
            self.load_employees()