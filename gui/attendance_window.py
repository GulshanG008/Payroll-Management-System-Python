import tkinter as tk
from tkinter import messagebox, ttk
import calendar

from database.employee_dao import EmployeeDAO
from services.attendance_service import AttendanceService


class AttendanceWindow:
    def __init__(self, parent):
        self.parent = parent

        self.window = tk.Toplevel(parent)
        self.window.title("Employee Attendance")
        self.window.state("zoomed")

        self.employee_dao = EmployeeDAO()
        self.attendance_service = AttendanceService()

        self._setup_style()
        self._create_widgets()

        self.load_employees()
        self.load_attendance()

    # ---------------- STYLE ---------------- #

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure(".", background="#f5f5f5", foreground="#333")

        style.configure("Title.TLabel",
                        font=("Segoe UI", 20, "bold"))

        style.configure("Success.TButton",
                        font=("Segoe UI", 11, "bold"),
                        padding=8)

        style.configure("Danger.TButton",
                        font=("Segoe UI", 11, "bold"),
                        padding=8)

    # ---------------- UI ---------------- #

    def _create_widgets(self):

        ttk.Label(self.window, text="Employee Attendance",
                  style="Title.TLabel").pack(pady=10)

        form = ttk.Frame(self.window)
        form.pack(pady=10)

        ttk.Label(form, text="Employee").grid(row=0, column=0)
        self.employee_combo = ttk.Combobox(form, width=30, state="readonly")
        self.employee_combo.grid(row=0, column=1)

        ttk.Label(form, text="Month").grid(row=1, column=0)
        self.month_entry = ttk.Entry(form)
        self.month_entry.grid(row=1, column=1)

        ttk.Label(form, text="Days Worked").grid(row=2, column=0)
        self.days_worked_entry = ttk.Entry(form)
        self.days_worked_entry.grid(row=2, column=1)

        ttk.Label(form, text="Days Absent").grid(row=3, column=0)
        self.days_absent_entry = ttk.Entry(form, state="readonly")
        self.days_absent_entry.grid(row=3, column=1)

        self.days_worked_entry.bind("<KeyRelease>", lambda e: self.calculate_absent())

        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Save",
                   command=self.save_attendance).pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Delete",
                   command=self.delete_attendance).pack(side="left", padx=5)

        # Table
        self.tree = ttk.Treeview(self.window,
                                 columns=("ID", "Emp", "Month", "Worked", "Absent"),
                                 show="headings")

        for col in ("ID", "Emp", "Month", "Worked", "Absent"):
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True)

    # ---------------- LOGIC ---------------- #

    def calculate_absent(self):
        try:
            month = self.month_entry.get()
            days_worked = int(self.days_worked_entry.get())

            year, month = map(int, month.split("-"))
            total = calendar.monthrange(year, month)[1]

            absent = total - days_worked

            self.days_absent_entry.config(state="normal")
            self.days_absent_entry.delete(0, tk.END)
            self.days_absent_entry.insert(0, str(absent))
            self.days_absent_entry.config(state="readonly")

        except:
            pass

    # ---------------- DATA ---------------- #

    def load_employees(self):
        employees = self.employee_dao.get_all_active()
        self.employee_combo["values"] = [
            f"{e['emp_id']} - {e['full_name']}" for e in employees
        ]

    def load_attendance(self):
        records = self.attendance_service.get_all_attendance()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for r in records:
            self.tree.insert("", "end", values=(
                r["attendance_id"],
                r["emp_id"],
                r["month_year"],
                r["days_worked"],
                r["days_absent"]
            ))

    # ---------------- ACTIONS ---------------- #

    def save_attendance(self):
        try:
            emp_id = int(self.employee_combo.get().split("-")[0])
            month = self.month_entry.get()
            worked = int(self.days_worked_entry.get())
            absent = int(self.days_absent_entry.get())

            self.attendance_service.record_attendance(emp_id, month, worked, absent)

            messagebox.showinfo("Success", "Saved")

            self.load_attendance()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_attendance(self):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        att_id = item["values"][0]

        self.attendance_service.delete_attendance(att_id)

        self.tree.delete(selected[0])