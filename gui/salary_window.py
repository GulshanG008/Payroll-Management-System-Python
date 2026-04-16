# gui/salary_window.py

import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation

from database.salary_dao import SalaryDAO
from models.salary_structure import SalaryStructure


class SalaryWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Salary Structure")
        self.window.geometry("920x560")
        self.window.resizable(False, False)

        self.salary_dao = SalaryDAO()

        self._create_widgets()
        self.load_structures()

    # ================= UI =================
    def _create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Title
        ttk.Label(
            self.window,
            text="Salary Structure",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=10)

        container = ttk.Frame(self.window, padding=10)
        container.pack(fill="both", expand=True)

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=2)

        # -------- FORM --------
        form_frame = ttk.LabelFrame(container, text="Details", padding=10)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        labels = [
            "Name",
            "Base Salary Min",
            "Base Salary Max",
            "HRA (%)",
            "Transport Allowance",
            "Tax (%)",
        ]

        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky="w", pady=5)

            entry = ttk.Entry(form_frame, width=25)
            entry.grid(row=i, column=1, pady=5, padx=5, sticky="ew")

            self.entries[label] = entry

        form_frame.columnconfigure(1, weight=1)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=15)

        ttk.Button(btn_frame, text="Add", command=self.add_structure).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_structure).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form).grid(row=0, column=2, padx=5)

        # -------- TABLE --------
        table_frame = ttk.Frame(container)
        table_frame.grid(row=0, column=1, sticky="nsew")

        columns = ("ID", "Name", "Min", "Max", "HRA %", "Transport", "Tax %")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        widths = [50, 130, 100, 100, 80, 120, 80]

        for col, w in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=w)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    # ================= DATA =================
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
                    float(s.tax_rate_pct * 100),
                ),
            )

    # ================= ACTIONS =================
    def add_structure(self):
        try:
            structure = self._read_form(None)
            self.salary_dao.create_salary_structure(structure)

            self.load_structures()
            self.clear_form()

            messagebox.showinfo("Success", "Added successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_structure(self):
        selected = self.tree.focus()

        if not selected:
            messagebox.showerror("Error", "Select a row first")
            return

        structure_id = self.tree.item(selected)["values"][0]

        try:
            structure = self._read_form(structure_id)
            self.salary_dao.update_salary_structure(structure)

            self.load_structures()
            messagebox.showinfo("Success", "Updated successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_select(self, event):
        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(selected)["values"]
        self.clear_form()

        keys = list(self.entries.keys())

        for i in range(len(keys)):
            self.entries[keys[i]].insert(0, values[i + 1])

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    # ================= VALIDATION =================
    def _read_form(self, structure_id):
        try:
            name = self.entries["Name"].get().strip()

            if not name:
                raise ValueError("Name cannot be empty")

            min_salary = Decimal(self.entries["Base Salary Min"].get())
            max_salary = Decimal(self.entries["Base Salary Max"].get())

            if min_salary > max_salary:
                raise ValueError("Min salary cannot be greater than max salary")

            hra_pct = Decimal(self.entries["HRA (%)"].get()) / Decimal("100")
            transport = Decimal(self.entries["Transport Allowance"].get())
            tax_pct = Decimal(self.entries["Tax (%)"].get()) / Decimal("100")

        except InvalidOperation:
            raise ValueError("Invalid numeric input")

        return SalaryStructure(
            structure_id=structure_id,
            name=name,
            base_salary_min=min_salary,
            base_salary_max=max_salary,
            housing_allowance_pct=hra_pct,
            transport_allowance=transport,
            tax_rate_pct=tax_pct,
        )