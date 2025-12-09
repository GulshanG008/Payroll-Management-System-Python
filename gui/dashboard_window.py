# gui/dashboard_window.py

import tkinter as tk
from tkinter import messagebox

# 💡 Import components for the feature pages
from gui.employee_window import EmployeeManagerWindow
# from gui.payroll_window import PayrollWindow # Placeholder for future implementation
# from gui.attendance_window import AttendanceWindow # Placeholder

class DashboardWindow:
    # 💡 The login_window_class parameter is crucial for the Logout function 
    # to be able to restart the LoginWindow.
    def __init__(self, root, login_window_class):
        self.root = root
        self.login_window_class = login_window_class # Store the class reference
        
        self.root.title("Payroll Management System - Dashboard")
        self.root.configure(bg="#e8f0fe")
        
        # Define the desired window size and center it
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
        # Title Label
        tk.Label(self.root, 
                 text="Welcome to the Payroll Management Dashboard", 
                 font=("Arial", 20, "bold"),
                 bg="#e8f0fe",
                 fg="#003366").pack(pady=40)

        # Dashboard content (Feature Buttons)
        content_frame = tk.Frame(self.root, bg="#e8f0fe")
        content_frame.pack(pady=20)
        
        button_font = ("Arial", 12)
        
        # Row 0: Core Management
        tk.Button(content_frame, text="Manage Employees", width=20, height=2, font=button_font,
                  command=self.open_employee_manager).grid(row=0, column=0, padx=20, pady=10)
                  
        tk.Button(content_frame, text="Generate Payroll", width=20, height=2, font=button_font,
                  state=tk.DISABLED).grid(row=0, column=1, padx=20, pady=10) # Placeholder
                  
        # Row 1: Reporting and Tools
        tk.Button(content_frame, text="View Reports", width=20, height=2, font=button_font,
                  state=tk.DISABLED).grid(row=1, column=0, padx=20, pady=10) # Placeholder
                  
        tk.Button(content_frame, text="Employee Attendance", width=20, height=2, font=button_font,
                  state=tk.DISABLED).grid(row=1, column=1, padx=20, pady=10) # Placeholder
        
        # --- LOGOUT BUTTON ---
        tk.Button(self.root, text="Logout", width=15, font=("Arial", 11, "bold"),
                  bg="#ff6666", fg="white", command=self.logout).pack(pady=40)

    # --- Feature Navigation Methods ---
    
    def open_employee_manager(self):
        """Opens the Employee Manager in a Toplevel window."""
        # 1. Create a new independent window linked to the dashboard root
        manager_root = tk.Toplevel(self.root)
        
        # 2. Instantiate the EmployeeManager GUI
        EmployeeManagerWindow(manager_root)
        
        # 3. Optional: Make the manager window modal (blocks interaction with the dashboard)
        manager_root.grab_set() 
        # Wait until the manager window is closed before allowing dashboard interaction
        self.root.wait_window(manager_root) 

    # --- Authentication Handling ---
    
    def logout(self):
        """Destroys the dashboard and reinstantiates the LoginWindow."""
        
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            
            # 1. Destroy the current dashboard window
            self.root.destroy()
            
            # 2. Create a new Tkinter root for the login window
            login_root = tk.Tk()
            
            # 3. Instantiate the stored LoginWindow class
            self.login_window_class(login_root)

# NOTE: The execution block for the dashboard is usually handled by the 
# LoginWindow.open_dashboard method, so no 'if __name__ == "__main__":' block is needed here.