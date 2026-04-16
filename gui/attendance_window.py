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
        self.window.minsize(900, 600)

        self.window.transient(parent)
        self.window.grab_set()

        self.employee_dao = EmployeeDAO()
        self.attendance_service = AttendanceService()

        self._create_widgets()
        self.load_employees()
        self.load_attendance()

    def _create_widgets(self):

        tk.Label(
            self.window, text="Employee Attendance", font=("Arial", 16, "bold")
        ).pack(pady=15)

        # 🔙 Back Button
        tk.Button(
            self.window,
            text="Back to Dashboard",
            width=20,
            command=self.go_back
        ).pack(pady=5)

        form = tk.Frame(self.window)
        form.pack(pady=10)

        # Employee
        tk.Label(form, text="Employee").grid(row=0, column=0, pady=8, sticky="e")

        self.employee_combo = ttk.Combobox(form, width=30, state="readonly")
        self.employee_combo.grid(row=0, column=1, pady=8)

        # Month-Year (YYYY-MM)
        tk.Label(form, text="Month (YYYY-MM)").grid(row=1, column=0, pady=8, sticky="e")

        self.month_entry = tk.Entry(form, width=33)
        self.month_entry.grid(row=1, column=1, pady=8)
        self.month_entry.insert(0, "2025-03")

        # Days Worked
        tk.Label(form, text="Days Worked").grid(row=2, column=0, pady=8, sticky="e")

        self.days_worked_entry = tk.Entry(form, width=33)
        self.days_worked_entry.grid(row=2, column=1, pady=8)

        # Days Absent (AUTO)
        tk.Label(form, text="Days Absent (Auto)").grid(row=3, column=0, pady=8, sticky="e")

        self.days_absent_entry = tk.Entry(form, width=33, state="readonly")
        self.days_absent_entry.grid(row=3, column=1, pady=8)

        # Bind auto calculation
        self.days_worked_entry.bind("<KeyRelease>", lambda e: self.calculate_absent_days())
        self.month_entry.bind("<KeyRelease>", lambda e: self.calculate_absent_days())

        # Buttons
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="Save Attendance",
            width=18,
            command=self.save_attendance
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Delete Attendance",
            width=18,
            command=self.delete_attendance
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Clear",
            width=18,
            command=self.clear_form
        ).pack(side="left", padx=10)

        # Table
        table_frame = tk.Frame(self.window)
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

    # ---------------- DATA LOAD ---------------- #

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

    def go_back(self):
        self.window.destroy()