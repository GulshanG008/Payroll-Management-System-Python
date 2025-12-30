# gui/attendance_window.py

import tkinter as tk
from tkinter import messagebox, ttk

from database.employee_dao import EmployeeDAO
from services.attendance_service import AttendanceService


class AttendanceWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Employee Attendance")
        self.window.geometry("700x500")
        self.window.resizable(False, False)

        self.employee_dao = EmployeeDAO()
        self.attendance_service = AttendanceService()

        self._create_widgets()
        self.load_employees()

    def _create_widgets(self):
        tk.Label(
            self.window, text="Employee Attendance", font=("Arial", 16, "bold")
        ).pack(pady=15)

        form = tk.Frame(self.window)
        form.pack(pady=10)

        # Employee
        tk.Label(form, text="Employee").grid(row=0, column=0, pady=8, sticky="e")
        self.employee_combo = ttk.Combobox(form, width=30, state="readonly")
        self.employee_combo.grid(row=0, column=1, pady=8)

        # Month-Year
        tk.Label(form, text="Month-Year").grid(row=1, column=0, pady=8, sticky="e")
        self.month_entry = tk.Entry(form, width=33)
        self.month_entry.grid(row=1, column=1, pady=8)
        self.month_entry.insert(0, "March-2025")

        # Days Worked
        tk.Label(form, text="Days Worked").grid(row=2, column=0, pady=8, sticky="e")
        self.days_worked_entry = tk.Entry(form, width=33)
        self.days_worked_entry.grid(row=2, column=1, pady=8)

        # Days Absent
        tk.Label(form, text="Days Absent").grid(row=3, column=0, pady=8, sticky="e")
        self.days_absent_entry = tk.Entry(form, width=33)
        self.days_absent_entry.grid(row=3, column=1, pady=8)

        # Buttons
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame, text="Save Attendance", width=18, command=self.save_attendance
        ).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Clear", width=18, command=self.clear_form).pack(
            side="left", padx=10
        )

        table_frame = tk.Frame(self.window)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("Employee", "Month", "Worked", "Absent")

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

    def load_employees(self):
        self.employees = self.employee_dao.get_all_active()
        self.employee_combo["values"] = [
            f"{e['emp_id']} - {e['full_name']}" for e in self.employees
        ]

    def save_attendance(self):
        if not self.employee_combo.get():
            messagebox.showerror("Error", "Please select an employee")
            return

        try:
            emp_id = int(self.employee_combo.get().split("-")[0].strip())
            month_year = self.month_entry.get().strip()
            days_worked = int(self.days_worked_entry.get())
            days_absent = int(self.days_absent_entry.get())

            self.attendance_service.record_attendance(
                emp_id=emp_id,
                month_year=month_year,
                days_worked=days_worked,
                days_absent=days_absent,
            )

            self.tree.insert(
                "",
                "end",
                values=(
                    self.employee_combo.get(),
                    month_year,
                    days_worked,
                    days_absent,
                ),
            )

            messagebox.showinfo("Success", "Attendance saved successfully")
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):
        self.month_entry.delete(0, tk.END)
        self.days_worked_entry.delete(0, tk.END)
        self.days_absent_entry.delete(0, tk.END)
