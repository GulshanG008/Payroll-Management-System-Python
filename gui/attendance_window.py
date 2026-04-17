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

        self.employee_dao = EmployeeDAO()
        self.attendance_service = AttendanceService()

        self._setup_style()
        self._create_widgets()

        self.load_employees()
        self.load_attendance()

        # ✅ Proper close handling
        self.window.protocol("WM_DELETE_WINDOW", self.go_back)

    # ---------------- STYLE ---------------- #

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure(".", background="#f5f5f5", foreground="#333")

        style.configure("Title.TLabel",
                        font=("Segoe UI", 20, "bold"))

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
                        fieldbackground="#ffffff")

        style.map("Treeview",
                  background=[("selected", "#d6d6d6")],
                  foreground=[("selected", "#000")])

    # ---------------- UI ---------------- #

    def _create_widgets(self):

        ttk.Label(self.window, text="Employee Attendance",
                  style="Title.TLabel").pack(pady=10)

        form = ttk.Frame(self.window)
        form.pack(pady=10)

        ttk.Label(form, text="Employee").grid(row=0, column=0, padx=10, pady=5)
        self.employee_combo = ttk.Combobox(form, width=30, state="readonly")
        self.employee_combo.grid(row=0, column=1, pady=5)

        ttk.Label(form, text="Month (YYYY-MM)").grid(row=1, column=0, padx=10, pady=5)
        self.month_entry = ttk.Entry(form)
        self.month_entry.grid(row=1, column=1, pady=5)

        ttk.Label(form, text="Days Worked").grid(row=2, column=0, padx=10, pady=5)
        self.days_worked_entry = ttk.Entry(form)
        self.days_worked_entry.grid(row=2, column=1, pady=5)

        ttk.Label(form, text="Days Absent").grid(row=3, column=0, padx=10, pady=5)
        self.days_absent_entry = ttk.Entry(form, state="readonly")
        self.days_absent_entry.grid(row=3, column=1, pady=5)

        self.days_worked_entry.bind("<KeyRelease>", lambda e: self.calculate_absent())

        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Save Attendance",
                   style="Success.TButton",
                   command=self.save_attendance).pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Delete Attendance",
                   style="Danger.TButton",
                   command=self.delete_attendance).pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Back",
                   command=self.go_back).pack(side="left", padx=5)

        # Table
        self.tree = ttk.Treeview(
            self.window,
            columns=("ID", "Emp", "Month", "Worked", "Absent"),
            show="headings"
        )

        for col in ("ID", "Emp", "Month", "Worked", "Absent"):
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True)

    # ---------------- LOGIC ---------------- #

    def calculate_absent(self):
        try:
            month_val = self.month_entry.get().strip()

            if "-" not in month_val:
                return

            days_worked = int(self.days_worked_entry.get())

            year, month = map(int, month_val.split("-"))
            total = calendar.monthrange(year, month)[1]

            if days_worked > total:
                raise ValueError("Worked days exceed total days")

            absent = total - days_worked

            self.days_absent_entry.config(state="normal")
            self.days_absent_entry.delete(0, tk.END)
            self.days_absent_entry.insert(0, str(absent))
            self.days_absent_entry.config(state="readonly")

        except:
            self.days_absent_entry.config(state="normal")
            self.days_absent_entry.delete(0, tk.END)
            self.days_absent_entry.config(state="readonly")

    # ---------------- DATA ---------------- #

    def load_employees(self):
        employees = self.employee_dao.get_all_active()

        self.employee_combo["values"] = [
            f"{e['emp_id']} - {e['full_name']}" for e in employees
        ]

        if self.employee_combo["values"]:
            self.employee_combo.current(0)

    def load_attendance(self):
        records = self.attendance_service.get_all_attendance()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for r in records:
            self.tree.insert("", "end", values=(
                r["attendance_id"],
                f"{r['emp_id']} - {r['full_name']}",
                r["month_year"],
                r["days_worked"],
                r["days_absent"]
            ))

    # ---------------- ACTIONS ---------------- #

    def save_attendance(self):
        try:
            if not self.employee_combo.get():
                messagebox.showerror("Error", "Select employee")
                return

            emp_id = int(self.employee_combo.get().split("-")[0])
            month = self.month_entry.get().strip()

            if not month:
                messagebox.showerror("Error", "Enter month (YYYY-MM)")
                return

            worked = int(self.days_worked_entry.get())
            absent = int(self.days_absent_entry.get())

            self.attendance_service.record_attendance(emp_id, month, worked, absent)

            messagebox.showinfo("Success", "Saved successfully")

            self.load_attendance()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_attendance(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showerror("Error", "Select a record")
            return

        item = self.tree.item(selected[0])
        att_id = item["values"][0]

        self.attendance_service.delete_attendance(att_id)

        self.tree.delete(selected[0])

    # ---------------- NAVIGATION ---------------- #

    def go_back(self):
        self.window.destroy()