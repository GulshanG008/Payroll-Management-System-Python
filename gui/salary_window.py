import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation

from database.salary_dao import SalaryDAO
from models.salary_structure import SalaryStructure


class SalaryWindow:
    def __init__(self, parent, dashboard_root):
        self.parent = parent
        self.dashboard_root = dashboard_root

        self.window = tk.Toplevel(parent)
        self.window.title("Salary Structure")

        self.window.state("zoomed")
        self.window.minsize(1000, 700)

        self.window.transient(parent)
        self.window.grab_set()

        self.salary_dao = SalaryDAO()

        self._setup_style()
        self._create_widgets()
        self.load_structures()

        self.window.protocol("WM_DELETE_WINDOW", self.go_back)

    # ---------------- STYLE ---------------- #

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))

        style.configure("Section.TLabelframe", padding=18)
        style.configure("Section.TLabelframe.Label", font=("Segoe UI", 12, "bold"))

        style.configure("TEntry", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 11), padding=6)

        style.configure("Action.TButton", font=("Segoe UI", 11, "bold"), padding=8)

        style.configure(
            "Danger.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=8,
            foreground="white",
            background="#d9534f",
        )

        style.map("Danger.TButton", background=[("active", "#c9302c")])

        style.configure("Treeview", font=("Segoe UI", 11), rowheight=30)
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"))

    # ---------------- UI ---------------- #

    def _create_widgets(self):

        # Header
        header = ttk.Frame(self.window, padding=12)
        header.pack(fill="x")

        ttk.Button(
            header,
            text="⬅ Back to Dashboard",
            style="Action.TButton",
            command=self.go_back
        ).pack(anchor="w")

        ttk.Label(
            self.window,
            text="Salary Structure",
            style="Title.TLabel"
        ).pack(pady=(5, 15))

        # Main layout
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=15, pady=10)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)

        # -------- FORM --------
        form_frame = ttk.Labelframe(
            main_frame,
            text="Salary Details",
            style="Section.TLabelframe"
        )
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

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
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky="w", pady=10)

            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=10)

            self.entries[label] = entry

        form_frame.columnconfigure(1, weight=1)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=20)

        ttk.Button(
            btn_frame,
            text="Add",
            style="Action.TButton",
            command=self.add_structure
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="Update",
            style="Action.TButton",
            command=self.update_structure
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="Clear",
            style="Danger.TButton",
            command=self.clear_form
        ).pack(side="left", padx=5)

        # -------- TABLE --------
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=0, column=1, sticky="nsew")

        columns = ("ID", "Name", "Min", "Max", "HRA %", "Transport", "Tax %")

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")

        self.tree.configure(yscrollcommand=scrollbar.set)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    # ---------------- DATA ---------------- #

    def load_structures(self):
        self.tree.delete(*self.tree.get_children())

        for s in self.salary_dao.get_all():
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

    # ---------------- ACTIONS ---------------- #

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

    # ---------------- VALIDATION ---------------- #

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

    # ---------------- NAVIGATION ---------------- #

    def go_back(self):
        self.window.grab_release()
        self.window.destroy()
        self.dashboard_root.deiconify()