# gui/login_window.py
from tkinter import messagebox, ttk


class LoginWindow:
    ENTRY_WIDTH = 28

    title_font = ("Segoe UI", 20, "bold")
    label_font = ("Segoe UI", 11, "bold")
    entry_font = ("Segoe UI", 11)
    button_font = ("Segoe UI", 11, "bold")

    def __init__(self, root, auth_service, on_login_success):
        self.root = root
        self.auth_service = auth_service
        self.on_login_success = on_login_success

        self.root.title("Payroll Management System - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self._center_window(400, 300)
        self._configure_styles()
        self._create_widgets()

    def _center_window(self, width, height):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw // 2) - (width // 2)
        y = (sh // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#f4f6f8")

        style.configure(
            "Title.TLabel",
            font=self.title_font,
            background="#f4f6f8",
            foreground="#2c3e50",
        )

        style.configure(
            "Form.TLabel",
            font=self.label_font,
            background="#f4f6f8",
            foreground="#2c3e50",
        )

        style.configure("TEntry", font=self.entry_font)

        style.configure("Login.TButton", font=self.button_font, padding=6)

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(expand=True, fill="both")

        ttk.label(
            main_frame, text="Payroll Management System", style="Title.TLabel"
        ).pack(pady=(10, 5))

        ttk.Label(main_frame, text="Admin Login", style="Title.TLabel").pack(
            pady=(10, 25)
        )

        form_frame = ttk.Frame(main_frame)
        form_frame.pack()

        # Username
        ttk.Label(form_frame, text="Username:", style="Form.TLabel").grid(
            row=0, column=0, padx=10, pady=10, sticky="e"
        )

        self.username_entry = ttk.Entry(form_frame, width=self.ENTRY_WIDTH)
        self.username_entry.grid(row=0, column=1, pady=10)

        # Password
        ttk.Label(form_frame, text="Password:", style="Form.TLabel").grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )

        self.password_entry = ttk.Entry(form_frame, width=self.ENTRY_WIDTH, show="*")
        self.password_entry.grid(row=1, column=1, pady=10)

        # Login Button
        ttk.Button(
            main_frame, text="Login", style="Login.TButton", command=self.login
        ).pack(pady=25)

        # Focus username field
        self.username_entry.focus()

        # Press Enter to login
        self.root.bind("<Return>", lambda event: self.login())

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
