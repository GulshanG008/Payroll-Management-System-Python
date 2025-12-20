# gui/payroll_window.py

import tkinter as tk
from tkinter import messagebox


class PayrollWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Payroll Generation")
        self.window.geometry("600x400")
        self.window.configure(bg="#f4f6f8")

        self.window.transient(parent)
        self.window.grab_set()

        self._center_window(600, 400)
        self._create_widgets()

    def _center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def _create_widgets(self):
        tk.Label(
            self.window,
            text="Payroll Generation",
            font=("Arial", 18, "bold"),
            bg="#f4f6f8",
            fg="#003366"
        ).pack(pady=30)

        form_frame = tk.Frame(self.window, bg="#f4f6f8")
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Salary Month:", font=("Arial", 12),
                 bg="#f4f6f8").grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.month_entry = tk.Entry(form_frame, width=20)
        self.month_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(
            self.window,
            text="Generate Payroll",
            width=20,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.generate_payroll
        ).pack(pady=20)

        tk.Button(
            self.window,
            text="Close",
            width=15,
            font=("Arial", 11),
            command=self.window.destroy
        ).pack(pady=10)

    def generate_payroll(self):
        month = self.month_entry.get().strip()

        if not month:
            messagebox.showerror("Input Error", "Please enter salary month.")
            return

        # Placeholder for future payroll logic
        messagebox.showinfo(
            "Payroll Generated",
            f"Payroll successfully generated for {month}."
        )
