# employee_manager.py (MODIFIED)

import tkinter as tk
from tkinter import ttk, messagebox
from database.employee_dao import EmployeeDAO 

class EmployeeManagerWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Employees - CRUD Operations (MySQL)")
        self.root.geometry("850x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        self.dao = EmployeeDAO() 
        if not self.dao.connection or not self.dao.connection.is_connected():
             messagebox.showerror("Database Error", "Failed to connect to MySQL database. Check credentials and server status.")
             self.root.destroy()
             return

        self._create_widgets()
        self.load_employees()

    def _create_widgets(self):
        tk.Label(self.root, text="Employee Management (MySQL)", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333333").pack(pady=10)
        
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(padx=10, pady=5, fill="both", expand=True)

        form_frame = tk.LabelFrame(main_frame, text="Employee Details", font=("Arial", 12), padx=10, pady=10, bg="#ffffff")
        form_frame.pack(side="left", fill="y", padx=10)

        fields = ["Name:", "Role:", "Salary:"]
        self.entries = {}

        for i, field in enumerate(fields):
            tk.Label(form_frame, text=field, font=("Arial", 10), bg="#ffffff").grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[field.replace(":", "")] = entry

        button_frame = tk.Frame(form_frame, bg="#ffffff")
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=15)
        
        tk.Button(button_frame, text="Add Employee", command=self.add_employee, width=15, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Button(button_frame, text="Update Selected", command=self.update_employee, width=15, bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete Selected", command=self.delete_employee, width=15, bg="#F44336", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Button(button_frame, text="Clear Form", command=self.clear_form, width=15, font=("Arial", 10)).pack(side="left", padx=5)


        table_frame = tk.Frame(main_frame)
        table_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        yscrollbar = ttk.Scrollbar(table_frame)
        yscrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Role", "Salary"), show="headings", yscrollcommand=yscrollbar.set)
        self.tree.pack(fill="both", expand=True)
        yscrollbar.config(command=self.tree.yview)

        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Name", text="Employee Name", anchor="w")
        self.tree.heading("Role", text="Role", anchor="w")
        self.tree.heading("Salary", text="Salary", anchor="e")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=150)
        self.tree.column("Role", width=120)
        self.tree.column("Salary", width=100, anchor="e")

        self.tree.bind("<<TreeviewSelect>>", self.on_employee_select)

    def load_employees(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        employees = self.dao.get_all_employees()
            
        for emp in employees:
            formatted_salary = f"${emp['salary']:,.2f}"
            self.tree.insert("", "end", values=(emp["id"], emp["name"], emp["role"], formatted_salary))

    def add_employee(self):
        name = self.entries["Name"].get().strip()
        role = self.entries["Role"].get().strip()
        salary_str = self.entries["Salary"].get().strip()

        if not name or not role or not salary_str:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        try:
            salary = float(salary_str)
            if salary <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Salary must be a valid positive number.")
            return

        new_id = self.dao.add_employee(name, role, salary)
        
        if new_id:
            self.load_employees()
            self.clear_form()
            messagebox.showinfo("Success", f"Employee {name} (ID: {new_id}) added successfully to database.")
        else:
            messagebox.showerror("DB Error", "Failed to add employee to the database.")

    def update_employee(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select an employee to update.")
            return

        selected_id = self.tree.item(selected_item)['values'][0]
        
        name = self.entries["Name"].get().strip()
        role = self.entries["Role"].get().strip()
        salary_str = self.entries["Salary"].get().strip()

        if not name or not role or not salary_str:
            messagebox.showerror("Error", "All fields must be filled out for update.")
            return
            
        try:
            salary = float(salary_str)
            if salary <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Salary must be a valid positive number.")
            return

        success = self.dao.update_employee(selected_id, name, role, salary)
        
        if success:
            self.load_employees()
            self.clear_form()
            messagebox.showinfo("Success", f"Employee ID {selected_id} updated in database.")
        else:
            messagebox.showerror("DB Error", "Failed to update employee.")


    def delete_employee(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select an employee to delete.")
            return

        selected_id = self.tree.item(selected_item)['values'][0]
        selected_name = self.tree.item(selected_item)['values'][1]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete employee: {selected_name} (ID: {selected_id})?"):
            
            success = self.dao.delete_employee(selected_id)
            
            if success:
                self.load_employees()
                self.clear_form()
                messagebox.showinfo("Success", f"Employee ID {selected_id} deleted from database.")
            else:
                messagebox.showerror("DB Error", "Failed to delete employee.")
    
    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def on_employee_select(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return

        values = self.tree.item(selected_item)['values']
        
        salary_value = values[3].replace('$', '').replace(',', '')

        self.clear_form()

        self.entries["Name"].insert(0, values[1])
        self.entries["Role"].insert(0, values[2])
        self.entries["Salary"].insert(0, salary_value)

if __name__ == "__main__":
    root = tk.Tk()
    EmployeeManagerWindow(root)
    root.mainloop()