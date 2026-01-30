# EmployeeView.py
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import pickle
import os

# User data file
PASS_HASHED = "passHash.pkl"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(PASS_HASHED):
        try:
            with open(PASS_HASHED, 'rb') as f:
                return pickle.load(f)
        except:
            return {}
    return {}

def save_users(users):
    with open(PASS_HASHED, 'wb') as f:
        pickle.dump(users, f)

def center_window(window, width=900, height=700):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def EmployeeView(parent_window=None):
    """Integrated Employee View System - As a function"""
    
    def setup_hover_effects():
        """Setup hover effects for buttons"""
        def on_enter(e):
            if hasattr(e.widget, 'hover_color'):
                e.widget.config(bg=e.widget.hover_color)
        
        def on_leave(e):
            if hasattr(e.widget, 'normal_color'):
                e.widget.config(bg=e.widget.normal_color)
        
        # Get all buttons
        buttons = [
            back_btn,
            search_btn, clear_btn, delete_btn, change_btn,
            change_user_btn, change_pass_btn, back_to_search_btn
        ]
        
        for btn in buttons:
            if btn:  # Check if button exists
                btn.bind("<Enter>", on_enter)
                btn.bind("<Leave>", on_leave)
    
    def load_employee_data():
        """Load and display employee data (excluding admins)"""
        users = load_users()
        
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)
        
        # Add employee data (filter out admins)
        for username, data in users.items():
            if data.get("role") == "employee":
                firstname = data.get("firstname", "")
                surname = data.get("surname", "")
                password = "••••••••"  # Hide password for security
                
                tree.insert("", "end", values=(firstname, surname, username, password))
    
    def on_item_select(event):
        """Handle item selection in treeview"""
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            # Use a mutable container for selected employee
            selected_employee_container["data"] = {
                "firstname": item['values'][0],
                "surname": item['values'][1],
                "username": item['values'][2]
            }
            
            # Enable buttons
            delete_btn.config(state="normal")
            change_btn.config(state="normal")
            change_user_btn.config(state="normal")
            change_pass_btn.config(state="normal")
            
            # Update selected info in credentials tab
            selected_info.config(
                text=f"Selected Employee: {selected_employee_container['data']['firstname']} {selected_employee_container['data']['surname']}\nUsername: {selected_employee_container['data']['username']}",
                fg="black"
            )
        else:
            selected_employee_container["data"] = None
            delete_btn.config(state="disabled")
            change_btn.config(state="disabled")
            change_user_btn.config(state="disabled")
            change_pass_btn.config(state="disabled")
            selected_info.config(
                text="No employee selected. Select an employee in the Search tab.",
                fg="#333333"
            )
    
    def perform_search():
        """Perform search based on criteria"""
        firstname = search_firstname.get().strip().lower()
        surname = search_surname.get().strip().lower()
        username = search_username.get().strip().lower()
        
        # Clear current selection
        tree.selection_remove(tree.selection())
        
        # Show all items first
        for child in tree.get_children():
            tree.item(child, tags=())
        
        # If no search criteria, show all
        if not firstname and not surname and not username:
            load_employee_data()
            return
        
        # Hide non-matching items
        for child in tree.get_children():
            item_values = tree.item(child)['values']
            item_firstname = str(item_values[0]).lower()
            item_surname = str(item_values[1]).lower()
            item_username = str(item_values[2]).lower()
            
            match = True
            
            if firstname and firstname not in item_firstname:
                match = False
            if surname and surname not in item_surname:
                match = False
            if username and username not in item_username:
                match = False
            
            if not match:
                tree.detach(child)
    
    def clear_search():
        """Clear search and show all employees"""
        search_firstname.delete(0, tk.END)
        search_surname.delete(0, tk.END)
        search_username.delete(0, tk.END)
        load_employee_data()
    
    def sort_treeview(col, reverse):
        """Sort treeview column"""
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=reverse)
        
        for index, (_, child) in enumerate(data):
            tree.move(child, '', index)
        
        tree.heading(col, command=lambda: sort_treeview(col, not reverse))
    
    def delete_selected():
        """Delete selected employee"""
        if not selected_employee_container["data"]:
            messagebox.showwarning("No Selection", "Please select an employee to delete.")
            return
        
        employee = selected_employee_container["data"]
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete employee:\n\n"
            f"{employee['firstname']} {employee['surname']}\n"
            f"Username: {employee['username']}"
        )
        
        if confirm:
            users = load_users()
            if employee['username'] in users:
                del users[employee['username']]
                save_users(users)
                messagebox.showinfo("Success", 
                                  f"Employee {employee['firstname']} {employee['surname']} deleted successfully.")
                load_employee_data()
                selected_employee_container["data"] = None
                delete_btn.config(state="disabled")
                change_btn.config(state="disabled")
                change_user_btn.config(state="disabled")
                change_pass_btn.config(state="disabled")
                selected_info.config(
                    text="No employee selected. Select an employee in the Search tab.",
                    fg="#333333"
                )
    
    def change_username():
        """Change username for selected employee"""
        if not selected_employee_container["data"]:
            messagebox.showwarning("No Selection", "Please select an employee first.")
            return
        
        employee = selected_employee_container["data"]
        new_user1 = new_user_entry1.get().strip()
        new_user2 = new_user_entry2.get().strip()
        
        if not new_user1 or not new_user2:
            messagebox.showerror("Error", "Please enter new username in both fields.")
            return
        
        if new_user1 != new_user2:
            messagebox.showerror("Error", "Usernames do not match. Please re-enter.")
            new_user_entry1.delete(0, tk.END)
            new_user_entry2.delete(0, tk.END)
            new_user_entry1.focus_set()
            return
        
        if new_user1 == employee['username']:
            messagebox.showwarning("Warning", "New username is the same as current username.")
            return
        
        # Check if new username already exists
        users = load_users()
        if new_user1 in users:
            messagebox.showerror("Error", f"Username '{new_user1}' already exists. Please choose a different username.")
            new_user_entry1.delete(0, tk.END)
            new_user_entry2.delete(0, tk.END)
            new_user_entry1.focus_set()
            return
        
        # Confirm change
        confirm = messagebox.askyesno(
            "Confirm Change",
            f"Are you sure you want to change username from '{employee['username']}' to '{new_user1}'?"
        )
        
        if confirm:
            # Get employee data
            employee_data = users[employee['username']]
            
            # Create new entry with new username
            users[new_user1] = employee_data
            
            # Delete old entry
            del users[employee['username']]
            
            save_users(users)
            
            messagebox.showinfo("Success", f"Username changed successfully to '{new_user1}'.")
            
            # Update selected employee info
            selected_employee_container["data"]['username'] = new_user1
            selected_info.config(
                text=f"Selected Employee: {employee['firstname']} {employee['surname']}\nUsername: {new_user1}",
                fg="black"
            )
            
            # Clear fields and reload data
            new_user_entry1.delete(0, tk.END)
            new_user_entry2.delete(0, tk.END)
            load_employee_data()
    
    def change_password():
        """Change password for selected employee"""
        if not selected_employee_container["data"]:
            messagebox.showwarning("No Selection", "Please select an employee first.")
            return
        
        employee = selected_employee_container["data"]
        new_pass1 = new_pass_entry1.get().strip()
        new_pass2 = new_pass_entry2.get().strip()
        
        if not new_pass1 or not new_pass2:
            messagebox.showerror("Error", "Please enter new password in both fields.")
            return
        
        if new_pass1 != new_pass2:
            messagebox.showerror("Error", "Passwords do not match. Please re-enter.")
            new_pass_entry1.delete(0, tk.END)
            new_pass_entry2.delete(0, tk.END)
            new_pass_entry1.focus_set()
            return
        
        # Confirm change
        confirm = messagebox.askyesno(
            "Confirm Change",
            f"Are you sure you want to change password for '{employee['username']}'?"
        )
        
        if confirm:
            users = load_users()
            
            if employee['username'] in users:
                users[employee['username']]["password_hash"] = hash_password(new_pass1)
                save_users(users)
                
                messagebox.showinfo("Success", f"Password changed successfully for '{employee['username']}'.")
                
                # Clear fields
                new_pass_entry1.delete(0, tk.END)
                new_pass_entry2.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Employee not found in database.")
    
    def go_back():
        """Go back to previous window"""
        root.destroy()
        if parent_window:
            parent_window.deiconify()
    
    # Create the window
    root = tk.Toplevel() if parent_window else tk.Tk()
    root.title("SPOTLIGHT AGENCY - Employee Management")
    root.geometry("900x700")
    root.resizable(True, True)
    center_window(root, 900, 700)
    
    # Set icon
    try:
        root.iconphoto(False, tk.PhotoImage(file="icon.png"))
    except:
        pass
    
    # Set background color
    root.configure(bg="#f0f0f0")
    
    # Container for selected employee data
    selected_employee_container = {"data": None}
    
    # Main container frame
    main_frame = tk.Frame(root, bg="#f0f0f0")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # TOP FRAME for BACK button (top right)
    top_frame = tk.Frame(main_frame, bg="#f0f0f0")
    top_frame.pack(fill="x", pady=(0, 10))
    
    # BACK Button in top right corner
    back_btn = tk.Button(top_frame, text="BACK", 
                        font=("Helvetica", 12, "bold"),
                        bg="#757575",
                        fg="white",
                        activebackground="#616161",
                        width=10,
                        height=1,
                        command=go_back)
    back_btn.pack(side="right", padx=5, pady=5)
    
    # Title
    title_label = tk.Label(main_frame, text="EMPLOYEE MANAGEMENT", 
                          font=("Helvetica", 24, "bold"),
                          fg="black",
                          bg="#f0f0f0")
    title_label.pack(pady=(0, 20))
    
    # Create Notebook for tabs
    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill="both", expand=True, pady=10)
    
    # Create frames for each tab
    search_frame = tk.Frame(notebook, bg="#f0f0f0")
    credentials_frame = tk.Frame(notebook, bg="#f0f0f0")
    
    notebook.add(search_frame, text="Employee Search")
    notebook.add(credentials_frame, text="Change Credentials")
    
    # === SETUP SEARCH TAB ===
    # Search criteria frame (top of search tab)
    criteria_frame = tk.Frame(search_frame, bg="#f0f0f0", relief="solid", bd=1)
    criteria_frame.pack(fill="x", padx=10, pady=10)
    
    # Search criteria title
    criteria_title = tk.Label(criteria_frame, text="SEARCH CRITERIA",
                             font=("Helvetica", 14, "bold"),
                             bg="#f0f0f0",
                             fg="#333333")
    criteria_title.pack(anchor="w", pady=(5, 15))
    
    # Search fields frame
    fields_frame = tk.Frame(criteria_frame, bg="#f0f0f0")
    fields_frame.pack(fill="x", pady=(0, 10))
    
    # Style for labels
    label_style = {
        "font": ("Helvetica", 11),
        "bg": "#f0f0f0",
        "fg": "black",
        "anchor": "w"
    }
    
    # Style for entries
    entry_style = {
        "font": ("Helvetica", 11),
        "width": 20,
        "bd": 1,
        "relief": "solid",
        "highlightthickness": 1
    }
    
    # First Name
    firstname_label = tk.Label(fields_frame, text="First Name:", **label_style)
    firstname_label.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 5))
    
    search_firstname = tk.Entry(fields_frame, **entry_style)
    search_firstname.grid(row=0, column=1, pady=(0, 5), ipady=3)
    
    # Surname
    surname_label = tk.Label(fields_frame, text="Surname:", **label_style)
    surname_label.grid(row=0, column=2, sticky="w", padx=(20, 10), pady=(0, 5))
    
    search_surname = tk.Entry(fields_frame, **entry_style)
    search_surname.grid(row=0, column=3, pady=(0, 5), ipady=3)
    
    # Username
    username_label = tk.Label(fields_frame, text="Username:", **label_style)
    username_label.grid(row=0, column=4, sticky="w", padx=(20, 10), pady=(0, 5))
    
    search_username = tk.Entry(fields_frame, **entry_style)
    search_username.grid(row=0, column=5, pady=(0, 5), ipady=3)
    
    # Search buttons frame
    search_buttons_frame = tk.Frame(criteria_frame, bg="#f0f0f0")
    search_buttons_frame.pack(fill="x", pady=(5, 5))
    
    search_btn = tk.Button(search_buttons_frame, text="SEARCH",
                          font=("Helvetica", 11, "bold"),
                          bg="#8A8A8A",
                          fg="white",
                          width=12,
                          command=perform_search)
    search_btn.pack(side="left", padx=5)
    
    clear_btn = tk.Button(search_buttons_frame, text="CLEAR ALL",
                         font=("Helvetica", 11, "bold"),
                         bg="#8A8A8A",
                         fg="white",
                         width=12,
                         command=clear_search)
    clear_btn.pack(side="left", padx=5)
    
    # Treeview frame with scrollbar
    tree_frame = tk.Frame(search_frame, bg="#f0f0f0")
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Create Treeview
    columns = ("First Name", "Surname", "Username", "Password")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    
    # Define headings
    for col in columns:
        tree.heading(col, text=col, command=lambda c=col: sort_treeview(c, False))
        tree.column(col, width=150, anchor="center")
    
    # Add scrollbars
    v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    
    tree.grid(row=0, column=0, sticky="nsew")
    v_scrollbar.grid(row=0, column=1, sticky="ns")
    h_scrollbar.grid(row=1, column=0, sticky="ew")
    
    tree_frame.grid_columnconfigure(0, weight=1)
    tree_frame.grid_rowconfigure(0, weight=1)
    
    # Action buttons frame (bottom of search tab)
    action_frame = tk.Frame(search_frame, bg="#f0f0f0")
    action_frame.pack(fill="x", padx=10, pady=10)
    
    delete_btn = tk.Button(action_frame, text="DELETE SELECTED",
                          font=("Helvetica", 12, "bold"),
                          bg="#8A8A8A",
                          fg="white",
                          width=20,
                          state="disabled",
                          command=delete_selected)
    delete_btn.pack(side="left", padx=5)
    
    change_btn = tk.Button(action_frame, text="CHANGE CREDENTIALS",
                          font=("Helvetica", 12, "bold"),
                          bg="#8A8A8A",
                          fg="white",
                          width=20,
                          state="disabled",
                          command=lambda: notebook.select(1))
    change_btn.pack(side="left", padx=5)
    
    # === SETUP CREDENTIALS TAB ===
    # Title for credentials tab
    cred_title = tk.Label(credentials_frame, text="CHANGE CREDENTIALS",
                         font=("Helvetica", 20, "bold"),
                         bg="#f0f0f0",
                         fg="black")
    cred_title.pack(pady=(10, 20))
    
    # Selected employee info
    selected_info = tk.Label(credentials_frame, 
                            text="No employee selected. Select an employee in the Search tab.",
                            font=("Helvetica", 12),
                            bg="#f0f0f0",
                            fg="#333333",
                            wraplength=600)
    selected_info.pack(pady=(0, 30))
    
    # Credentials frame
    cred_main_frame = tk.Frame(credentials_frame, bg="#f0f0f0")
    cred_main_frame.pack(pady=10)
    
    # Left column - Username change
    left_frame = tk.Frame(cred_main_frame, bg="#f0f0f0")
    left_frame.grid(row=0, column=0, padx=30, pady=10)
    
    user_label = tk.Label(left_frame, text="New Username:", **label_style)
    user_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    new_user_entry1 = tk.Entry(left_frame, **entry_style)
    new_user_entry1.grid(row=1, column=0, pady=(0, 15), ipady=5)
    
    reuser_label = tk.Label(left_frame, text="Re-enter Username:", **label_style)
    reuser_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
    
    new_user_entry2 = tk.Entry(left_frame, **entry_style)
    new_user_entry2.grid(row=3, column=0, pady=(0, 20), ipady=5)
    
    change_user_btn = tk.Button(left_frame, text="CHANGE USER",
                               font=("Helvetica", 11, "bold"),
                               bg="#8A8A8A",
                               fg="white",
                               width=15,
                               state="disabled",
                               command=change_username)
    change_user_btn.grid(row=4, column=0, pady=10)
    
    # Right column - Password change
    right_frame = tk.Frame(cred_main_frame, bg="#f0f0f0")
    right_frame.grid(row=0, column=1, padx=30, pady=10)
    
    pass_label = tk.Label(right_frame, text="New Password:", **label_style)
    pass_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    new_pass_entry1 = tk.Entry(right_frame, show="•", **entry_style)
    new_pass_entry1.grid(row=1, column=0, pady=(0, 15), ipady=5)
    
    repass_label = tk.Label(right_frame, text="Re-enter Password:", **label_style)
    repass_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
    
    new_pass_entry2 = tk.Entry(right_frame, show="•", **entry_style)
    new_pass_entry2.grid(row=3, column=0, pady=(0, 20), ipady=5)
    
    change_pass_btn = tk.Button(right_frame, text="CHANGE PASS",
                               font=("Helvetica", 11, "bold"),
                               bg="#8A8A8A",
                               fg="white",
                               width=15,
                               state="disabled",
                               command=change_password)
    change_pass_btn.grid(row=4, column=0, pady=10)
    
    # Back to search button
    back_to_search_frame = tk.Frame(credentials_frame, bg="#f0f0f0")
    back_to_search_frame.pack(pady=20)
    
    back_to_search_btn = tk.Button(back_to_search_frame, text="BACK TO SEARCH",
                                  font=("Helvetica", 12, "bold"),
                                  bg="#757575",
                                  fg="white",
                                  width=20,
                                  command=lambda: notebook.select(0))
    back_to_search_btn.pack()
    
    # Set hover colors
    back_btn.normal_color = "#757575"
    back_btn.hover_color = "#616161"
    
    search_btn.normal_color = "#8A8A8A"
    search_btn.hover_color = "#A3A3A3"
    
    clear_btn.normal_color = "#8A8A8A"
    clear_btn.hover_color = "#A3A3A3"
    
    delete_btn.normal_color = "#8A8A8A"
    delete_btn.hover_color = "#A3A3A3"
    
    change_btn.normal_color = "#8A8A8A"
    change_btn.hover_color = "#A3A3A3"
    
    change_user_btn.normal_color = "#8A8A8A"
    change_user_btn.hover_color = "#A3A3A3"
    
    change_pass_btn.normal_color = "#8A8A8A"
    change_pass_btn.hover_color = "#A3A3A3"
    
    back_to_search_btn.normal_color = "#757575"
    back_to_search_btn.hover_color = "#616161"
    
    # Setup hover effects
    setup_hover_effects()
    
    # Bind selection event
    tree.bind("<<TreeviewSelect>>", on_item_select)
    
    # Bind Enter key to search
    search_firstname.bind('<Return>', lambda e: perform_search())
    search_surname.bind('<Return>', lambda e: perform_search())
    search_username.bind('<Return>', lambda e: perform_search())
    
    # Load initial data
    load_employee_data()
    
    # Focus on first entry
    search_firstname.focus_set()
    
    if not parent_window:
        root.mainloop()

# For testing directly
if __name__ == "__main__":
    EmployeeView()