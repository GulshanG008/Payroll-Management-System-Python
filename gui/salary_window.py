# gui/salary_window.py

import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal

from database.salary_dao import SalaryDAO
from models.salary_structure import SalaryStructure


class SalaryWindow:
    """
    GUI window to manage Salary Structures (Pay Grades).
    """

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Salary Structure Management")
        self.window.geometry("900x550")
        self.window.resizable(False, False)

        self.salary_dao = SalaryDAO()

        self._create_widgets()
        self.load_structures()

    # --------------------------------------------------
    def _create_widgets(self):
        tk.Label(
            self.window,
            text="Salary Structure Management",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        main = tk.Frame(self.window)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # ---------------- FORM ----------------
        form = tk.LabelFrame(main, text="Add / Update Structure", font=("Arial", 12))
        form.pack(side="left", fill="y", padx=10)

        labels = [
            "Name",
            "Base Salary Min",
            "Base Salary Max",
            "HRA (%)",
            "Transport Allowance",
            "Tax (%)"
        ]

        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(form, text=label).grid(row=i, column=0, pady=6, sticky="w")
            entry = tk.Entry(form, width=25)
            entry.grid(row=i, column=1, pady=6)
            self.entries[label] = entry

        btn_frame = tk.Frame(form)
        btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=15)

        tk.Button(
            btn_frame,
            text="Add",
            width=12,
            command=self.add_structure
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Update",
            width=12,
            command=self.update_structure
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Clear",
            width=12,
            command=self.clear_form
        ).pack(side="left", padx=5)

        # ---------------- TABLE ----------------
        table_frame = tk.Frame(main)
        table_frame.pack(side="right", fill="both", expand=True)

        columns = (
            "ID",
            "Name",
            "Min",
            "Max",
            "HRA",
            "Transport",
            "Tax"
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

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    # --------------------------------------------------
    def load_structures(self):
        self.tree.delete(*self.tree.get_children())

        structures = self.salary_dao.get_all()
        for s in structures:
            self.tree.insert(
                "",
                "end",
                values=(
                    s.structure_id,
                    s.name,
                    s.base_salary_min,
                    s.base_salary_max,
                    float(s.housing_allowance_pct * 100),
                    s.transport_allowance,
                    float(s.tax_rate_pct * 100)
                )
            )

    # --------------------------------------------------
    def add_structure(self):
        try:
            structure = self._read_form(structure_id=None)
            self.salary_dao.create_salary_structure(structure)
            self.load_structures()
            self.clear_form()
            messagebox.showinfo("Success", "Salary structure added")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --------------------------------------------------
    def update_structure(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a structure to update")
            return

        structure_id = self.tree.item(selected)["values"][0]

        try:
            structure = self._read_form(structure_id=structure_id)
            self.salary_dao.update_salary_structure(structure)
            self.load_structures()
            messagebox.showinfo("Success", "Salary structure updated")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --------------------------------------------------
    def on_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected)["values"]

        self.clear_form()
        keys = list(self.entries.keys())

        self.entries[keys[0]].insert(0, values[1])
        self.entries[keys[1]].insert(0, values[2])
        self.entries[keys[2]].insert(0, values[3])
        self.entries[keys[3]].insert(0, values[4])
        self.entries[keys[4]].insert(0, values[5])
        self.entries[keys[5]].insert(0, values[6])

    # --------------------------------------------------
    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    # --------------------------------------------------
    def _read_form(self, structure_id):
        name = self.entries["Name"].get().strip()
        min_salary = Decimal(self.entries["Base Salary Min"].get())
        max_salary = Decimal(self.entries["Base Salary Max"].get())
        hra_pct = Decimal(self.entries["HRA (%)"].get()) / Decimal("100")
        transport = Decimal(self.entries["Transport Allowance"].get())
        tax_pct = Decimal(self.entries["Tax (%)"].get()) / Decimal("100")

        return SalaryStructure(
            structure_id=structure_id,
            name=name,
            base_salary_min=min_salary,
            base_salary_max=max_salary,
            housing_allowance_pct=hra_pct,
            transport_allowance=transport,
            tax_rate_pct=tax_pct
        )
