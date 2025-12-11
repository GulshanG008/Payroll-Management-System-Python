# gui/dashboard_window.py

import tkinter as tk
from tkinter import messagebox

#from gui.employee_window import EmployeeManagerWindow

class DashboardWindow:
    def __init__(self, root, login_window_class):
        self.root = root
        self.login_window_class = login_window_class 
        
        self.root.title("Payroll Management System - Dashboard")
        self.root.configure(bg="#e8f0fe")
        
        window_width = 800
        window_height = 600
        self._center_window(window_width, window_height)
        
        self._create_widgets()

    def _center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def _create_widgets(self):
        tk.Label(self.root, 
                 text="Welcome to the Payroll Management Dashboard", 
                 font=("Arial", 20, "bold"),
                 bg="#e8f0fe",
                 fg="#003366").pack(pady=40)

        content_frame = tk.Frame(self.root, bg="#e8f0fe")
        content_frame.pack(pady=20)
        
        button_font = ("Arial", 12)
        
        tk.Button(content_frame, text="Manage Employees", width=20, height=2, font=button_font,
                  command=self.open_employee_manager).grid(row=0, column=0, padx=20, pady=10)
                  
        tk.Button(content_frame, text="Generate Payroll", width=20, height=2, font=button_font,
                  state=tk.DISABLED).grid(row=0, column=1, padx=20, pady=10) 
                  
        # Row 1: Reporting and Tools
        tk.Button(content_frame, text="View Reports", width=20, height=2, font=button_font,
                  state=tk.DISABLED).grid(row=1, column=0, padx=20, pady=10)
                  
        tk.Button(content_frame, text="Employee Attendance", width=20, height=2, font=button_font,
                  state=tk.DISABLED).grid(row=1, column=1, padx=20, pady=10) 
        
        # --- LOGOUT BUTTON ---
        tk.Button(self.root, text="Logout", width=15, font=("Arial", 11, "bold"),
                  bg="#ff6666", fg="white", command=self.logout).pack(pady=40)

    """def open_employee_manager(self):
        manager_root = tk.Toplevel(self.root)
        EmployeeManagerWindow(manager_root)
        manager_root.grab_set() 
        self.root.wait_window(manager_root)""" 
    
    def logout(self):        
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            self.root.destroy()
            login_root = tk.Tk()
            self.login_window_class(login_root)