# gui/login_window.py

import tkinter as tk
from tkinter import messagebox


class LoginWindow:
    def __init__(self, root, auth_service, on_login_success):
        self.root = root
        self.auth_service = auth_service
        self.on_login_success = on_login_success

        self.root.title("Payroll Management System - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self._center_window(400, 300)
        self._create_widgets()

    def _center_window(self, width, height):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw // 2) - (width // 2)
        y = (sh // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    title_font = ("Segoe UI", 20, "bold")
    label_font = ("Segoe UI", 11, "bold")
    entry_font = ("Segoe UI", 11, "bold")
    button_font = ("Segoe UI", 11, "bold")

    def _create_widgets(self):
        tk.Label(self.root, text="Admin Login", font=self.title_font).pack(pady=20)

        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        # Username
        tk.Label(form_frame, text="Username:", font=self.label_font).grid(
            row=0, column=0, padx=10, pady=10, sticky="e"
        )

        self.username_entry = tk.Entry(form_frame, width=25, font=self.entry_font)
        self.username_entry.grid(row=0, column=1, pady=10)

        # Password
        tk.Label(form_frame, text="Password:", font=self.label_font).grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )

        self.password_entry = tk.Entry(form_frame, width=25, show="*")
        self.password_entry.grid(row=1, column=1, pady=10)

        # Login Button
        tk.Button(
            self.root,
            text="Login",
            width=15,
            font=self.button_font,
            command=self.login,
        ).pack(pady=20)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror(
                "Login Error", "Please enter both username and password."
            )
            return

        if self.auth_service.login_admin(username, password):
            messagebox.showinfo("Login Successful", "Welcome to the system!")
            self.on_login_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
