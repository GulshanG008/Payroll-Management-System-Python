# gui/login_window.py

import tkinter as tk
from tkinter import messagebox

#from services.auth_service import AuthService
from dashboard_window import DashboardWindow 

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Payroll Management - Admin Login")
        self.root.configure(bg="#f0f0f0")
        
       # self.auth_service = AuthService()

        window_width = 350
        window_height = 260
        self._center_window(window_width, window_height) 
        self.root.resizable(False, False) 

        self._create_widgets()
        
    def _create_widgets(self):
        tk.Label(self.root, text="LOGIN", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

        form = tk.Frame(self.root, bg="#f0f0f0")
        form.pack(pady=5)

        tk.Label(form, text="User ID:", font=("Arial", 11), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.user_id_entry = tk.Entry(form, width=25)
        self.user_id_entry.grid(row=0, column=1)

        # USERNAME
        tk.Label(form, text="Username:", font=("Arial", 11), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.username_entry = tk.Entry(form, width=25)
        self.username_entry.grid(row=1, column=1)

        # PASSWORD
        tk.Label(form, text="Password:", font=("Arial", 11), bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.password_entry = tk.Entry(form, width=25, show="*")
        self.password_entry.grid(row=2, column=1)

        # LOGIN BUTTON
        tk.Button(self.root, text="Login", width=12, font=("Arial", 11, "bold"),
                  command=self.login).pack(pady=15)
        
    def _center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def open_dashboard(self):
        self.root.destroy()
        dashboard_root = tk.Tk()
        DashboardWindow(dashboard_root, LoginWindow)

    def login(self):
        uid = self.user_id_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not uid or not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        is_valid = self.auth_service.login_admin(uid, username, password)
        
        if is_valid:
            messagebox.showinfo("Success", "Login Successful!")
            self.open_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials. Please check User ID, Username, and Password.")


if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()