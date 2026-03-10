import tkinter as tk
from datetime import date
from decimal import Decimal
from tkinter import messagebox, ttk

from database.employee_dao import EmployeeDAO


class EmployeeManagerWindow:
    def __init__(self, parent_root, dashboard_root):

        self.dashboard_root = dashboard_root

        self.root = tk.Toplevel(parent_root)
        self.root.title("Employee Management")

        # Full screen but keep minimum size
        self.root.state("zoomed")
        self.root.minsize(1000, 700)

        # Modal behavior so dashboard stays intact
        self.root.transient(parent_root)
        self.root.grab_set()

        self.dao = EmployeeDAO()

        self._setup_style()
        self._create_widgets()
        self.load_employees()

        self.root.protocol("WM_DELETE_WINDOW", self.go_back)

    def _setup_style(self):

        style = ttk.Style()
        style.theme_use("clam")

        # Title
        style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"))

        # Section frames
        style.configure("Section.TLabelframe", padding=20)

        style.configure("Section.TLabelframe.Label", font=("Segoe UI", 13, "bold"))

        # Entry widgets
        style.configure("TEntry", font=("Segoe UI", 11), padding=4)

        style.configure("TCombobox", font=("Segoe UI", 11))

        # Buttons
        style.configure("Action.TButton", font=("Segoe UI", 11, "bold"), padding=8)

        style.configure(
            "Danger.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=8,
            foreground="white",
            background="#d9534f",
        )

        style.map("Danger.TButton", background=[("active", "#c9302c")])

        # Table
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=32)

        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"))

    def _create_widgets(self):

        header = ttk.Frame(self.root, padding=12)
        header.pack(fill="x")

        ttk.Button(
            header,
            text="⬅ Back to Dashboard",
            style="Action.TButton",
            command=self.go_back,
        ).pack(anchor="w")

        ttk.Label(
            self.root, text="Employee Management", style="Title.TLabel", anchor="center"
        ).pack(pady=(5, 15))

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=15, pady=10)

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
            ttk.Label(form, text=label, font=("Segoe UI", 11)).grid(
                row=i, column=0, sticky="w", pady=10
            )

            if label == "Gender":
                entry = ttk.Combobox(
                    form, values=["Male", "Female", "Other"], state="readonly", width=28
                )

            else:
                entry = ttk.Entry(form, width=30)

            entry.grid(row=i, column=1, sticky="ew", pady=10)

            self.entries[label] = entry

        form.columnconfigure(1, weight=1)

        ttk.Button(
            form,
            text="Add Employee",
            style="Action.TButton",
            command=self.add_employee,
        ).grid(row=len(labels), column=0, columnspan=2, pady=(20, 0))

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

            self.tree.column(col, anchor="center", width=120, stretch=True)

        self.tree.column("Name", width=220)
        self.tree.column("Code", width=150)

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

    def load_employees(self):

        self.tree.delete(*self.tree.get_children())

        for emp in self.dao.get_all_active():
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
                    emp["status"],
                ),
            )

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
                structure_id=None,
            )

            self.load_employees()

            messagebox.showinfo("Success", "Employee added successfully")

            for entry in self.entries.values():
                entry.delete(0, tk.END)

            self.entries["Employee Code"].focus()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def deactivate_employee(self):

        selected = self.tree.focus()

        if not selected:
            messagebox.showerror("Error", "Please select an employee")
            return

        emp_id = self.tree.item(selected)["values"][0]

        if messagebox.askyesno(
            "Confirm Deactivation",
            "Deactivate this employee?\n\nThey will no longer appear in payroll.",
        ):
            self.dao.deactivate_employee(emp_id)
            self.load_employees()

    def delete_employee(self):

        selected = self.tree.focus()

        if not selected:
            messagebox.showerror("Error", "Please select an employee")
            return

        emp_id = self.tree.item(selected)["values"][0]

        if not messagebox.askyesno(
            "Confirm Permanent Deletion",
            "This will permanently delete the employee record.\n\n"
            "This action cannot be undone.\n\n"
            "Do you want to continue?",
        ):
            return

        self.dao.delete_employee(emp_id)

        self.load_employees()

    def go_back(self):

        self.root.destroy()

        # restore dashboard properly
        self.dashboard_root.deiconify()
        self.dashboard_root.state("zoomed")
        self.dashboard_root.lift()
        self.dashboard_root.focus_force()
