import tkinter as tk
from tkinter import messagebox, ttk
import calendar

from database.employee_dao import EmployeeDAO
from services.attendance_service import AttendanceService


class AttendanceWindow:
    def __init__(self, parent, dashboard_root):
        self.parent = parent
        self.dashboard_root = dashboard_root

        self.window = tk.Toplevel(parent)
        self.window.title("Employee Attendance")

        self.window.state("zoomed")
        self.window.minsize(900, 600)

        self.employee_dao = EmployeeDAO()
        self.attendance_service = AttendanceService()

        self._setup_style()
        self._create_widgets()

        self.load_employees()
        self.load_attendance()

        self.window.protocol("WM_DELETE_WINDOW", self.go_back)

    # ---------------- STYLE ---------------- #

    def _setup_style(self):
        style = ttk.Style()

        # Remove bluish theme
        style.theme_use("default")

        # Base UI
        style.configure(".",
            background="#f5f5f5",
            foreground="#333333"
        )

        # Title
        style.configure("Title.TLabel",
            font=("Segoe UI", 20, "bold"),
            background="#f5f5f5"
        )

        # Buttons
        style.configure("Success.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=8,
            foreground="white",
            background="#28a745"
            )

        style.map("Success.TButton",
            background=[("active", "#218838")]
        )

        style.configure("Danger.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=8,
            foreground="white",
            background="#d9534f"
        )

        style.map("Danger.TButton",
            background=[("active", "#c9302c")]
        )

        # Inputs
        style.configure("TEntry", fieldbackground="#ffffff")
        style.configure("TCombobox", fieldbackground="#ffffff")

        style.map("TEntry",
            bordercolor=[("focus", "#999999")]
        )

        style.map("TCombobox",
            bordercolor=[("focus", "#999999")]
        )

        # Table
        style.configure("Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            rowheight=30
        )

        style.configure("Treeview.Heading",
            font=("Segoe UI", 12, "bold")
        )

        style.map("Treeview",
            background=[("selected", "#d6d6d6")],
            foreground=[("selected", "#000000")]
        )

    # ---------------- UI ---------------- #

    def _create_widgets(self):

        header = ttk.Frame(self.window, padding=12)
        header.pack(fill="x")

        ttk.Button(
            header,
            text="⬅ Back to Dashboard",
            style="Action.TButton",
            command=self.go_back,
        ).pack(anchor="w")

        ttk.Label(
            self.window,
            text="Employee Attendance",
            style="Title.TLabel",
        ).pack(pady=(5, 15))

        form = ttk.Frame(self.window)
        form.pack(pady=10)

        ttk.Label(form, text="Employee").grid(row=0, column=0, pady=8, sticky="e")

        self.employee_combo = ttk.Combobox(form, width=30, state="readonly")
        self.employee_combo.grid(row=0, column=1, pady=8)

        ttk.Label(form, text="Month (YYYY-MM)").grid(row=1, column=0, pady=8, sticky="e")

        self.month_entry = ttk.Entry(form, width=33)
        self.month_entry.grid(row=1, column=1, pady=8)
        self.month_entry.insert(0, "2025-03")

        ttk.Label(form, text="Days Worked").grid(row=2, column=0, pady=8, sticky="e")

        self.days_worked_entry = ttk.Entry(form, width=33)
        self.days_worked_entry.grid(row=2, column=1, pady=8)

        ttk.Label(form, text="Days Absent (Auto)").grid(row=3, column=0, pady=8, sticky="e")

        self.days_absent_entry = ttk.Entry(form, width=33, state="readonly")
        self.days_absent_entry.grid(row=3, column=1, pady=8)

        self.days_worked_entry.bind("<KeyRelease>", lambda e: self.calculate_absent_days())
        self.month_entry.bind("<KeyRelease>", lambda e: self.calculate_absent_days())

        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, text="Save Attendance", style="Success.TButton",
                   command=self.save_attendance).pack(side="left", padx=10)

        ttk.Button(btn_frame, text="Delete Attendance", style="Danger.TButton",
                   command=self.delete_attendance).pack(side="left", padx=10)

        ttk.Button(btn_frame, text="Clear", style="Action.TButton",
                   command=self.clear_form).pack(side="left", padx=10)

        table_frame = ttk.Frame(self.window)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("ID", "Employee", "Month", "Worked", "Absent")

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

    # ---------------- LOGIC ---------------- #

    def calculate_absent_days(self):
        try:
            month_year = self.month_entry.get().strip()
            days_worked = int(self.days_worked_entry.get())

            year, month = map(int, month_year.split("-"))
            total_days = calendar.monthrange(year, month)[1]

            if days_worked > total_days:
                raise ValueError("Days worked exceeds total days")

            days_absent = total_days - days_worked

            self.days_absent_entry.config(state="normal")
            self.days_absent_entry.delete(0, tk.END)
            self.days_absent_entry.insert(0, str(days_absent))
            self.days_absent_entry.config(state="readonly")

        except:
            self.days_absent_entry.config(state="normal")
            self.days_absent_entry.delete(0, tk.END)
            self.days_absent_entry.config(state="readonly")

    # ---------------- DATA ---------------- #

    def load_employees(self):
        self.employees = self.employee_dao.get_all_active()

        self.employee_combo["values"] = [
            f"{e['emp_id']} - {e['full_name']}" for e in self.employees
        ]

    def load_attendance(self):
        records = self.attendance_service.get_all_attendance()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for r in records:
            self.tree.insert(
                "",
                "end",
                values=(
                    r["attendance_id"],
                    f"{r['emp_id']} - {r['full_name']}",
                    r["month_year"],
                    r["days_worked"],
                    r["days_absent"],
                ),
            )

    # ---------------- ACTIONS ---------------- #

    def save_attendance(self):
        if not self.employee_combo.get():
            messagebox.showerror("Error", "Select employee")
            return

        try:
            emp_id = int(self.employee_combo.get().split("-")[0].strip())
            month_year = self.month_entry.get().strip()

            days_worked = int(self.days_worked_entry.get())
            days_absent = int(self.days_absent_entry.get())

            self.attendance_service.record_attendance(
                emp_id, month_year, days_worked, days_absent
            )

            messagebox.showinfo("Success", "Saved successfully")

            self.load_attendance()
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_attendance(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showerror("Error", "Select a record")
            return

        item = self.tree.item(selected[0])
        attendance_id = item["values"][0]

        try:
            self.attendance_service.delete_attendance(attendance_id)
            self.tree.delete(selected[0])
            messagebox.showinfo("Success", "Deleted")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):
        self.month_entry.delete(0, tk.END)
        self.days_worked_entry.delete(0, tk.END)

        self.days_absent_entry.config(state="normal")
        self.days_absent_entry.delete(0, tk.END)
        self.days_absent_entry.config(state="readonly")

    # ---------------- NAVIGATION ---------------- #

    def go_back(self):
        self.window.destroy()