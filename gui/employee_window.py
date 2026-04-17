import tkinter as tk
from datetime import date
from decimal import Decimal
from tkinter import messagebox, ttk

from database.employee_dao import EmployeeDAO


class EmployeeManagerWindow:
    def __init__(self, parent_root, dashboard_root):
        self.parent_root = parent_root
        self.dashboard_root = dashboard_root

        self.window = tk.Toplevel(parent_root)
        self.window.title("Employee Management")

        self.window.state("zoomed")
        self.window.minsize(1000, 700)

        self.dao = EmployeeDAO()

        self._setup_style()
        self._create_widgets()
        self.load_employees()

        # ✅ FIXED
        self.window.protocol("WM_DELETE_WINDOW", self.go_back)

    # ---------------- STYLE ---------------- #

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure(".", background="#f5f5f5", foreground="#333")

        style.configure("Title.TLabel",
                        font=("Segoe UI", 20, "bold"))

        style.configure("Section.TLabelframe",
                        padding=18)

        style.configure("Section.TLabelframe.Label",
                        font=("Segoe UI", 12, "bold"))

        style.configure("TEntry", fieldbackground="#ffffff")
        style.configure("TCombobox", fieldbackground="#ffffff")

        style.configure("Success.TButton",
                        font=("Segoe UI", 11, "bold"),
                        padding=8,
                        foreground="white",
                        background="#28a745")

        style.map("Success.TButton",
                  background=[("active", "#218838")])

        style.configure("Danger.TButton",
                        font=("Segoe UI", 11, "bold"),
                        padding=8,
                        foreground="white",
                        background="#d9534f")

        style.map("Danger.TButton",
                  background=[("active", "#c9302c")])

        style.configure("Treeview",
                        background="#ffffff",
                        fieldbackground="#ffffff",
                        rowheight=30)

        style.map("Treeview",
                  background=[("selected", "#d6d6d6")],
                  foreground=[("selected", "#000")])

    # ---------------- UI ---------------- #

    def _create_widgets(self):

        header = ttk.Frame(self.window, padding=12)
        header.pack(fill="x")

        ttk.Button(
            header,
            text="⬅ Back to Dashboard",
            command=self.go_back,
        ).pack(anchor="w")

        ttk.Label(
            self.window,
            text="Employee Management",
            style="Title.TLabel",
        ).pack(pady=(5, 15))

        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # -------- FORM --------
        form = ttk.Labelframe(
            main_frame, text="Add Employee", style="Section.TLabelframe"
        )
        form.pack(side="left", fill="y", padx=(10, 25))

        labels = [
            "Employee Code",
            "Full Name",
            "Gender",
            "Contact No",
            "Email",
            "Basic Salary",
        ]

        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", pady=10)

            if label == "Gender":
                entry = ttk.Combobox(
                    form,
                    values=["Male", "Female", "Other"],
                    state="readonly",
                    width=28
                )
            else:
                entry = ttk.Entry(form, width=30)

            entry.grid(row=i, column=1, sticky="ew", pady=10)
            self.entries[label] = entry

        form.columnconfigure(1, weight=1)

        ttk.Button(
            form,
            text="Add Employee",
            style="Success.TButton",
            command=self.add_employee,
        ).grid(row=len(labels), column=0, columnspan=2, pady=(20, 0))

        # -------- TABLE --------
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(side="right", fill="both", expand=True)

        tree_container = ttk.Frame(table_frame)
        tree_container.pack(fill="both", expand=True)

        columns = ("ID", "Code", "Name", "Gender", "Contact", "Salary", "Status")

        self.tree = ttk.Treeview(tree_container, columns=columns, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")

        self.tree.configure(yscrollcommand=vsb.set)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        # Buttons
        button_bar = ttk.Frame(table_frame)
        button_bar.pack(fill="x", pady=10)

        ttk.Button(
            button_bar,
            text="Deactivate Employee",
            style="Danger.TButton",
            command=self.deactivate_employee,
        ).pack(side="left", padx=5)

        ttk.Button(
            button_bar,
            text="Delete Employee",
            style="Danger.TButton",
            command=self.delete_employee,
        ).pack(side="left", padx=5)

    # ---------------- DATA ---------------- #

    def load_employees(self):
        self.tree.delete(*self.tree.get_children())

        for emp in self.dao.get_all_active():
            self.tree.insert("", "end", values=(
                emp["emp_id"],
                emp["emp_code"],
                emp["full_name"],
                emp["gender"],
                emp["contact_no"],
                emp["basic_salary"],
                emp["status"],
            ))

    # ---------------- ACTIONS ---------------- #

    def add_employee(self):
        try:
            emp_code = self.entries["Employee Code"].get().strip()
            full_name = self.entries["Full Name"].get().strip()

            if not emp_code or not full_name:
                raise ValueError("Employee Code and Full Name are required")

            self.dao.create_employee(
                emp_code=emp_code,
                full_name=full_name,
                gender=self.entries["Gender"].get(),
                contact_no=self.entries["Contact No"].get(),
                email=self.entries["Email"].get(),
                date_of_joining=date.today(),
                basic_salary=Decimal(self.entries["Basic Salary"].get()),
                structure_id=None,
            )

            self.load_employees()
            messagebox.showinfo("Success", "Employee added successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def deactivate_employee(self):
        selected = self.tree.focus()
        if not selected:
            return

        emp_id = self.tree.item(selected)["values"][0]
        self.dao.deactivate_employee(emp_id)
        self.load_employees()

    def delete_employee(self):
        selected = self.tree.focus()
        if not selected:
            return

        emp_id = self.tree.item(selected)["values"][0]
        self.dao.delete_employee(emp_id)
        self.load_employees()

    # ---------------- NAVIGATION ---------------- #

    def go_back(self):
        self.window.destroy()