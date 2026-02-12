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

def center_window(window, width=650, height=500):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def EmployeeView(parent_window=None):
    
    # Variables for sorting
    sort_by_options = ["First Name", "Surname", "Username"]
    current_sort = tk.StringVar(value="First Name")
    sort_order = tk.BooleanVar(value=False)  # False = ascending, True = descending
    
    def setup_hover_effects():

        def on_enter(e):
            if hasattr(e.widget, 'hover_color'):
                e.widget.config(bg=e.widget.hover_color)
        
        def on_leave(e):
            if hasattr(e.widget, 'normal_color'):
                e.widget.config(bg=e.widget.normal_color)
        
        buttons = [search_btn, delete_btn, credentials_btn, back_btn]
        for btn in buttons:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def load_employee_data():

        users = load_users()
        
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)
        
        # Collect employee data
        employees = []
        for username, data in users.items():
            if data.get("role") == "employee":
                employees.append({
                    "firstname": data.get("firstname", ""),
                    "surname": data.get("surname", ""),
                    "username": username,
                    "password": "••••••••"  # Hide password for security
                })
        
        # Sort employees
        sort_key = current_sort.get()
        reverse_order = sort_order.get()
        
        if sort_key == "First Name":
            employees.sort(key=lambda x: x["firstname"].lower(), reverse=reverse_order)
        elif sort_key == "Surname":
            employees.sort(key=lambda x: x["surname"].lower(), reverse=reverse_order)
        elif sort_key == "Username":
            employees.sort(key=lambda x: x["username"].lower(), reverse=reverse_order)
        elif sort_key == "Password":
            employees.sort(key=lambda x: x["password"], reverse=reverse_order)
        
        # Add sorted data to treeview
        for emp in employees:
            tree.insert("", "end", values=(emp["firstname"], emp["surname"], emp["username"], emp["password"]))
    
    def on_item_select(event):

        selected = tree.selection()
        if selected:
            delete_btn.config(state="normal")
            credentials_btn.config(state="normal")
        else:
            delete_btn.config(state="disabled")
            credentials_btn.config(state="disabled")
    
    def delete_selected():

        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an employee to delete.")
            return
        
        # Get selected employee data
        item = tree.item(selected[0])
        username = item['values'][2]
        firstname = item['values'][0]
        surname = item['values'][1]
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete employee:\n\n{firstname} {surname}\nUsername: {username}"
        )
        
        if confirm:
            users = load_users()
            if username in users:
                del users[username]
                save_users(users)
                messagebox.showinfo("Success", f"Employee {firstname} {surname} deleted successfully.")
                load_employee_data()
                delete_btn.config(state="disabled")
                credentials_btn.config(state="disabled")
    
    def open_search_window():
        SearchWindow(root, apply_search_filter)
    
    def open_change_credentials():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an employee to change credentials.")
            return
        
        # Get selected employee data
        item = tree.item(selected[0])
        username = item['values'][2]
        firstname = item['values'][0]
        surname = item['values'][1]
        
        ChangeCredentialsWindow(root, username, firstname, surname, load_employee_data)
    
    def apply_search_filter(firstname_filter, surname_filter, username_filter):
        # Clear current selection
        tree.selection_remove(tree.selection())
        
        # CRITICAL: RELOAD ALL DATA FIRST
        load_employee_data()
        
        # If no search criteria, show ALL items
        if not firstname_filter and not surname_filter and not username_filter:
            return
        
        # Hide non-matching items
        for child in tree.get_children():
            item_values = tree.item(child)['values']
            item_firstname = str(item_values[0]).lower()
            item_surname = str(item_values[1]).lower()
            item_username = str(item_values[2]).lower()
            
            match = True
            
            if firstname_filter and firstname_filter.lower() not in item_firstname:
                match = False
            if surname_filter and surname_filter.lower() not in item_surname:
                match = False
            if username_filter and username_filter.lower() not in item_username:
                match = False
            
            if not match:
                tree.detach(child)
    
    def go_back():
        root.destroy()
        if parent_window:
            parent_window.deiconify()
    
    def sort_changed(*args):
        load_employee_data()
    
    def toggle_sort_order():
        sort_order.set(not sort_order.get())
        load_employee_data()
        # Update button text
        if sort_order.get():
            sort_order_btn.config(text="▲")
        else:
            sort_order_btn.config(text="▼")
    
    # Create the main window
    root = tk.Toplevel() if parent_window else tk.Tk()
    root.title("SPOTLIGHT AGENCY - Employee View")
    root.geometry("650x500")
    root.resizable(False, False)
    center_window(root, 650, 500)
    
    # Set icon
    try:
        root.iconphoto(False, tk.PhotoImage(file="icon.png"))
    except:
        pass
    
    # Set background color
    root.configure(bg="#152e41")
    
    # Main container frame
    main_frame = tk.Frame(root, bg="#152e41")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # TOP FRAME for BACK button (top right)
    top_frame = tk.Frame(main_frame, bg="#152e41")
    top_frame.pack(fill="x", pady=(0, 10))
    
    # BACK Button in top right corner
    back_btn = tk.Button(top_frame, text="BACK", 
                        font=("Helvetica", 12, "bold"),
                        bg="#8acbcb",
                        fg="white",
                        activebackground="#7db6b6",
                        width=10,
                        height=1,
                        command=go_back)
    back_btn.pack(side="right", padx=5, pady=5)
    
    # Title
    title_label = tk.Label(main_frame, text="EMPLOYEE SEARCH", 
                          font=("Helvetica", 24, "bold"),
                          fg="white",
                          bg="#152e41")
    title_label.pack(pady=(0, 20))
    
    # Top button frame (Search, Delete, Change Credentials)
    top_button_frame = tk.Frame(main_frame, bg="#152e41")
    top_button_frame.pack(pady=(0, 15))
    
    # Search button
    search_btn = tk.Button(top_button_frame, text="SEARCH",
                          font=("Helvetica", 12, "bold"),
                          bg="#8acbcb",
                          fg="white",
                          activebackground="#7db6b6",
                          width=15,
                          height=2,
                          command=open_search_window)
    search_btn.pack(side="left", padx=5)
    
    # Delete Selected button
    delete_btn = tk.Button(top_button_frame, text="DELETE SELECTED",
                          font=("Helvetica", 12, "bold"),
                          bg="#8acbcb",
                          fg="white",
                          activebackground="#7db6b6",
                          width=16,
                          height=2,
                          
                          command=delete_selected)
    delete_btn.pack(side="left", padx=5)
    
    # Change Credentials button
    credentials_btn = tk.Button(top_button_frame, text="CHANGE CREDENTIALS",
                               font=("Helvetica", 12, "bold"),
                               bg="#8acbcb",
                               fg="white",
                               activebackground="#7db6b6",
                               width=20,
                               height=2,
                               
                               command=open_change_credentials)
    credentials_btn.pack(side="left", padx=5)
    
    # Sort frame (below buttons)
    sort_frame = tk.Frame(main_frame, bg="#152e41")
    sort_frame.pack(pady=(0, 15))
    
    sort_label = tk.Label(sort_frame, text="Sort by:",
                         font=("Helvetica", 12),
                         bg="#152e41"
                         , fg="white")
    sort_label.pack(side="left", padx=(0, 10))
    
    sort_dropdown = ttk.Combobox(sort_frame, 
                                textvariable=current_sort,
                                values=sort_by_options,
                                state="readonly",
                                width=15,
                                font=("Helvetica", 11))
    sort_dropdown.pack(side="left", padx=(0, 10))
    sort_dropdown.bind("<<ComboboxSelected>>", sort_changed)
    
    # Sort order toggle button
    sort_order_btn = tk.Button(sort_frame, text="▼",
                              font=("Helvetica", 10, "bold"),
                              bg="#8acbcb",
                              fg="white",
                              width=3,
                              command=toggle_sort_order)
    sort_order_btn.pack(side="left")
    
    # Treeview frame with scrollbar
    tree_frame = tk.Frame(main_frame, bg="#152e41")
    tree_frame.pack(fill="both", expand=True, pady=(0, 10))
    
    # Create Treeview
    columns = ("First Name", "Surname", "Username", "Password")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    
    # Define headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Set hover colors
    search_btn.normal_color = "#8acbcb"
    search_btn.hover_color = "#7db6b6"
    
    delete_btn.normal_color = "#8acbcb"
    delete_btn.hover_color = "#7db6b6"
    
    credentials_btn.normal_color = "#8acbcb"
    credentials_btn.hover_color = "#7db6b6"
    
    back_btn.normal_color = "#8acbcb"
    back_btn.hover_color = "#7db6b6"
    
    sort_order_btn.normal_color = "#8acbcb"
    sort_order_btn.hover_color = "#7db6b6"
    
    # Setup hover effects
    setup_hover_effects()
    sort_order_btn.bind("<Enter>", lambda e: sort_order_btn.config(bg="#7db6b6"))
    sort_order_btn.bind("<Leave>", lambda e: sort_order_btn.config(bg="#8acbcb"))
    
    # Bind selection event
    tree.bind("<<TreeviewSelect>>", on_item_select)
    
    # Load initial data
    load_employee_data()
    
    if not parent_window:
        root.mainloop()
   
def SearchWindow(parent_window, apply_callback):
    
    def perform_search(event=None):  # Add event parameter for Enter key
        firstname = firstname_entry.get().strip()
        surname = surname_entry.get().strip()
        username = username_entry.get().strip()
        
        # Apply search to main window - empty strings will show all results
        apply_callback(firstname, surname, username)
        
        # Close search window
        search_root.destroy()
    
    def go_back():
        search_root.destroy()
    
    # Create search window
    search_root = tk.Toplevel(parent_window)
    search_root.title("SPOTLIGHT AGENCY - Employee Search")
    search_root.geometry("650x500")
    search_root.resizable(False, False)
    center_window(search_root, 650, 500)
    
    # Set icon
    try:
        search_root.iconphoto(False, tk.PhotoImage(file="icon.png"))
    except:
        pass
    
    # Set background color
    search_root.configure(bg="#152e41")
    
    # Main container frame - use grid for better control
    main_frame = tk.Frame(search_root, bg="#152e41")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # TOP FRAME for BACK button (top right)
    top_frame = tk.Frame(main_frame, bg="#152e41", height=40)
    top_frame.pack(fill="x", pady=(0, 10))
    top_frame.pack_propagate(False)  # Prevent frame from shrinking
    
    # BACK Button in top right corner
    back_btn = tk.Button(top_frame, text="BACK", 
                        font=("Helvetica", 12, "bold"),
                        bg="#8acbcb",
                        fg="white",
                        activebackground="#7db6b6",
                        width=10,
                        height=1,
                        command=go_back)
    back_btn.pack(side="right", padx=5, pady=5)
    
    # Title
    title_label = tk.Label(main_frame, text="EMPLOYEE SEARCH", 
                          font=("Helvetica", 24, "bold"),
                          fg="white",
                          bg="#152e41")
    title_label.pack(pady=(0, 20))
    
    # Search criteria frame
    criteria_frame = tk.Frame(main_frame, bg="#152e41")
    criteria_frame.pack(pady=20)
    
    # Style for labels
    label_style = {
        "font": ("Helvetica", 12),
        "bg": "#152e41",
        "fg": "white",
        "anchor": "w"
    }
    
    # Style for entries
    entry_style = {
        "font": ("Helvetica", 12),
        "width": 30,
        "bg": "#dcffff",
        "relief": "solid",
        "highlightthickness": 0
    }

    # First Name
    firstname_label = tk.Label(criteria_frame, text="FIRST NAME", **label_style)
    firstname_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    firstname_entry = tk.Entry(criteria_frame, **entry_style)
    firstname_entry.grid(row=1, column=0, pady=(0, 20), ipady=5)
    
    # Surname
    surname_label = tk.Label(criteria_frame, text="SURNAME", **label_style)
    surname_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
    
    surname_entry = tk.Entry(criteria_frame, **entry_style)
    surname_entry.grid(row=3, column=0, pady=(0, 20), ipady=5)
    
    # Username
    username_label = tk.Label(criteria_frame, text="USERNAME", **label_style)
    username_label.grid(row=4, column=0, sticky="w", pady=(0, 5))
    
    username_entry = tk.Entry(criteria_frame, **entry_style)
    username_entry.grid(row=5, column=0, pady=(0, 30), ipady=5)
    
    # Button frame at BOTTOM - separate frame that stays at bottom
    button_frame = tk.Frame(main_frame, bg="#152e41", height=80)
    button_frame.pack(fill="x", side="bottom", pady=10)
    button_frame.pack_propagate(False)  # Prevent frame from shrinking
    
    # SEARCH button
    search_btn = tk.Button(button_frame, text="SEARCH",
                          font=("Helvetica", 14, "bold"),
                          bg="#8acbcb",
                          fg="white",
                          activebackground="#7db6b6",
                          width=20,
                          height=2,
                          command=perform_search)
    search_btn.pack(expand=True)  # Center the button
    
    # Set hover colors
    back_btn.normal_color = "#8acbcb"
    back_btn.hover_color = "#7db6b6"
    search_btn.normal_color = "#8acbcb"
    search_btn.hover_color = "#7db6b6"
    
    # Setup hover effects
    back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#7db6b6"))
    back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#8acbcb"))
    search_btn.bind("<Enter>", lambda e: search_btn.config(bg="#7db6b6"))
    search_btn.bind("<Leave>", lambda e: search_btn.config(bg="#8acbcb"))
    
    # Bind Enter key to search
    firstname_entry.bind('<Return>', perform_search)
    surname_entry.bind('<Return>', perform_search)
    username_entry.bind('<Return>', perform_search)
    
    # Make window modal
    search_root.transient(parent_window)
    search_root.grab_set()
    search_root.focus_set()
    
    # Focus on first entry
    firstname_entry.focus_set()

def ChangeCredentialsWindow(parent_window, username, firstname, surname, reload_callback):
    
    # Use a mutable container for username
    username_container = {"value": username}
    
    def setup_hover_effects():

        def on_enter(e):
            if hasattr(e.widget, 'hover_color'):
                e.widget.config(bg=e.widget.hover_color)
        
        def on_leave(e):
            if hasattr(e.widget, 'normal_color'):
                e.widget.config(bg=e.widget.normal_color)
        
        buttons = [change_user_btn, change_pass_btn]
        for btn in buttons:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def change_username():

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
        
        if new_user1 == username_container["value"]:
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
            f"Are you sure you want to change username from '{username_container['value']}' to '{new_user1}'?"
        )
        
        if confirm:
            # Get employee data
            employee_data = users[username_container["value"]]
            
            # Create new entry with new username
            users[new_user1] = employee_data
            
            # Delete old entry
            del users[username_container["value"]]
            
            save_users(users)
            
            messagebox.showinfo("Success", f"Username changed successfully to '{new_user1}'.")
            
            # Update username in container
            username_container["value"] = new_user1
            
            # Update displayed username
            info_label.config(text=f"Employee: {firstname} {surname}\nUsername: {username_container['value']}")
            
            # Clear fields
            new_user_entry1.delete(0, tk.END)
            new_user_entry2.delete(0, tk.END)
            
            # Reload data in main window
            reload_callback()
    
    def change_password():

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
            f"Are you sure you want to change password for '{username_container['value']}'?"
        )
        
        if confirm:
            users = load_users()
            
            if username_container["value"] in users:
                users[username_container["value"]]["password_hash"] = hash_password(new_pass1)
                save_users(users)
                
                messagebox.showinfo("Success", f"Password changed successfully for '{username_container['value']}'.")
                
                # Clear fields
                new_pass_entry1.delete(0, tk.END)
                new_pass_entry2.delete(0, tk.END)
                
                # Reload data in main window
                reload_callback()
            else:
                messagebox.showerror("Error", "Employee not found in database.")
    
    # Create credentials window
    cred_root = tk.Toplevel(parent_window)
    cred_root.title("SPOTLIGHT AGENCY - Change Credentials")
    cred_root.geometry("650x500")
    cred_root.resizable(False, False)
    center_window(cred_root, 650, 500)
    
    # Set icon
    try:
        cred_root.iconphoto(False, tk.PhotoImage(file="icon.png"))
    except:
        pass
    
    # Set background color
    cred_root.configure(bg="#152e41")
    
    # Main container frame
    main_frame = tk.Frame(cred_root, bg="#152e41")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Title
    title_label = tk.Label(main_frame, text="CHANGE CREDENTIALS", 
                          font=("Helvetica", 24, "bold"),
                          fg="white",
                          bg="#152e41")
    title_label.pack(pady=(0, 20))
    
    # Current employee info
    info_label = tk.Label(main_frame, 
                         text=f"Employee: {firstname} {surname}\nUsername: {username_container['value']}",
                         font=("Helvetica", 14, "bold"),
                         bg="#152e41",
                         fg="white")
    info_label.pack(pady=(0, 30))
    
    # Two-column layout for username and password changes
    columns_frame = tk.Frame(main_frame, bg="#152e41")
    columns_frame.pack(fill="both", expand=True, pady=10)
    
    # Style for labels
    label_style = {
        "font": ("Helvetica", 12),
        "bg": "#152e41",
        "fg": "white",
        "anchor": "w"
    }
    
    # Style for entries
    entry_style = {
        "font": ("Helvetica", 12),
        "width": 22,
        "bg": "#dcffff",
        "relief": "solid",
        "highlightthickness": 0
    }
    
    # Left column - Username change
    left_frame = tk.Frame(columns_frame, bg="#152e41")
    left_frame.pack(side="left", fill="both", expand=True, padx=20)
    
    user_title = tk.Label(left_frame, text="Change Username",
                         font=("Helvetica", 14, "bold"),
                         bg="#152e41",
                         fg="white")
    user_title.pack(pady=(0, 20))
    
    user_label1 = tk.Label(left_frame, text="New Username:", **label_style)
    user_label1.pack(anchor="w", pady=(0, 5))
    
    new_user_entry1 = tk.Entry(left_frame, **entry_style)
    new_user_entry1.pack(pady=(0, 15), ipady=5)
    
    user_label2 = tk.Label(left_frame, text="Re-enter Username:", **label_style)
    user_label2.pack(anchor="w", pady=(0, 5))
    
    new_user_entry2 = tk.Entry(left_frame, **entry_style)
    new_user_entry2.pack(pady=(0, 20), ipady=5)
    
    change_user_btn = tk.Button(left_frame, text="CHANGE USERNAME",
                               font=("Helvetica", 12, "bold"),
                               bg="#8acbcb",
                               fg="white",
                               activebackground="#7db6b6",
                               width=20,
                               height=2,
                               command=change_username)
    change_user_btn.pack(pady=10)
    
    # Right column - Password change
    right_frame = tk.Frame(columns_frame, bg="#152e41")
    right_frame.pack(side="right", fill="both", expand=True, padx=20)
    
    pass_title = tk.Label(right_frame, text="Change Password",
                         font=("Helvetica", 14, "bold"),
                         bg="#152e41",
                         fg="white")
    pass_title.pack(pady=(0, 20))
    
    pass_label1 = tk.Label(right_frame, text="New Password:", **label_style)
    pass_label1.pack(anchor="w", pady=(0, 5))
    
    new_pass_entry1 = tk.Entry(right_frame, show="•", **entry_style)
    new_pass_entry1.pack(pady=(0, 15), ipady=5)
    
    pass_label2 = tk.Label(right_frame, text="Re-enter Password:", **label_style)
    pass_label2.pack(anchor="w", pady=(0, 5))
    
    new_pass_entry2 = tk.Entry(right_frame, show="•", **entry_style)
    new_pass_entry2.pack(pady=(0, 20), ipady=5)
    
    change_pass_btn = tk.Button(right_frame, text="CHANGE PASSWORD",
                               font=("Helvetica", 12, "bold"),
                               bg="#8acbcb",
                               fg="white",
                               activebackground="#7db6b6",
                               width=20,
                               height=2,
                               command=change_password)
    change_pass_btn.pack(pady=10)
    
    # Set hover colors
    change_user_btn.normal_color = "#8acbcb"
    change_user_btn.hover_color = "#7db6b6"
    
    change_pass_btn.normal_color = "#8acbcb"
    change_pass_btn.hover_color = "#7db6b6"
    
    # Setup hover effects
    setup_hover_effects()
    
    # Make window modal
    cred_root.transient(parent_window)
    cred_root.grab_set()
    cred_root.focus_set()
    
    # Bind Enter key to change username/password
    new_user_entry1.bind('<Return>', lambda e: change_username())
    new_user_entry2.bind('<Return>', lambda e: change_username())
    new_pass_entry1.bind('<Return>', lambda e: change_password())
    new_pass_entry2.bind('<Return>', lambda e: change_password())
    
    # Focus on first entry
    new_user_entry1.focus_set()

if __name__ == "__main__":
    EmployeeView()