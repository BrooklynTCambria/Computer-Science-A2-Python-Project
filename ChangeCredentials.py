# ChangeCredentials.py - Simplified version without class
import tkinter as tk
from tkinter import messagebox
import hashlib
import pickle
import os

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

def center_window(window, width=600, height=500):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def ChangeCredentials(parent_window, employee_username):
    """Change Credentials window"""
    
    # Use a mutable container for the username
    username_container = {"current": employee_username}
    
    def setup_hover_effects():
        """Setup hover effects for buttons"""
        def on_enter(e):
            if hasattr(e.widget, 'hover_color'):
                e.widget.config(bg=e.widget.hover_color)
        
        def on_leave(e):
            if hasattr(e.widget, 'normal_color'):
                e.widget.config(bg=e.widget.normal_color)
        
        buttons = [change_user_btn, change_pass_btn, back_btn]
        for btn in buttons:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def change_username():
        """Change username for selected employee"""
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
        
        if new_user1 == username_container["current"]:
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
            f"Are you sure you want to change username from '{username_container['current']}' to '{new_user1}'?"
        )
        
        if confirm:
            # Get employee data
            employee_data = users[username_container["current"]]
            
            # Create new entry with new username
            users[new_user1] = employee_data
            
            # Delete old entry
            del users[username_container["current"]]
            
            save_users(users)
            
            messagebox.showinfo("Success", f"Username changed successfully to '{new_user1}'.")
            
            # Update username container and info label
            username_container["current"] = new_user1
            info_label.config(text=f"Editing credentials for: {username_container['current']}")
            
            # Clear fields
            new_user_entry1.delete(0, tk.END)
            new_user_entry2.delete(0, tk.END)
    
    def change_password():
        """Change password for selected employee"""
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
            f"Are you sure you want to change password for '{username_container['current']}'?"
        )
        
        if confirm:
            users = load_users()
            
            if username_container["current"] in users:
                users[username_container["current"]]["password_hash"] = hash_password(new_pass1)
                save_users(users)
                
                messagebox.showinfo("Success", f"Password changed successfully for '{username_container['current']}'.")
                
                # Clear fields
                new_pass_entry1.delete(0, tk.END)
                new_pass_entry2.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Employee not found in database.")
    
    def go_back():
        """Go back to Employee View window"""
        root.destroy()
        if parent_window:
            parent_window.deiconify()
    
    # Create the window
    root = tk.Toplevel(parent_window)
    root.title("SPOTLIGHT AGENCY - Change Credentials")
    root.geometry("600x500")
    root.resizable(False, False)
    center_window(root, 600, 500)
    
    # Set icon
    try:
        root.iconphoto(False, tk.PhotoImage(file="icon.png"))
    except:
        pass
    
    # Set background color
    root.configure(bg="#f0f0f0")
    
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
    title_label = tk.Label(main_frame, text="CHANGE CREDENTIALS", 
                          font=("Helvetica", 24, "bold"),
                          fg="black",
                          bg="#f0f0f0")
    title_label.pack(pady=(0, 20))
    
    # Current employee info
    info_label = tk.Label(main_frame, 
                         text=f"Editing credentials for: {username_container['current']}",
                         font=("Helvetica", 12),
                         bg="#f0f0f0",
                         fg="#333333")
    info_label.pack(pady=(0, 30))
    
    # Credentials frame
    cred_frame = tk.Frame(main_frame, bg="#f0f0f0")
    cred_frame.pack(pady=10)
    
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
        "width": 25,
        "bd": 1,
        "relief": "solid",
        "highlightthickness": 1
    }
    
    # Left column - Username change
    left_frame = tk.Frame(cred_frame, bg="#f0f0f0")
    left_frame.grid(row=0, column=0, padx=20, pady=10)
    
    user_label = tk.Label(left_frame, text="New Username:", **label_style)
    user_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    new_user_entry1 = tk.Entry(left_frame, **entry_style)
    new_user_entry1.grid(row=1, column=0, pady=(0, 15), ipady=5)
    
    reuser_label = tk.Label(left_frame, text="Re-enter Username:", **label_style)
    reuser_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
    
    new_user_entry2 = tk.Entry(left_frame, **entry_style)
    new_user_entry2.grid(row=3, column=0, pady=(0, 20), ipady=5)
    
    change_user_btn = tk.Button(left_frame, text="Change User",
                               font=("Helvetica", 11, "bold"),
                               bg="#8A8A8A",
                               fg="white",
                               width=15,
                               command=change_username)
    change_user_btn.grid(row=4, column=0, pady=10)
    
    # Right column - Password change
    right_frame = tk.Frame(cred_frame, bg="#f0f0f0")
    right_frame.grid(row=0, column=1, padx=20, pady=10)
    
    pass_label = tk.Label(right_frame, text="New Password:", **label_style)
    pass_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    new_pass_entry1 = tk.Entry(right_frame, show="•", **entry_style)
    new_pass_entry1.grid(row=1, column=0, pady=(0, 15), ipady=5)
    
    repass_label = tk.Label(right_frame, text="Re-enter Password:", **label_style)
    repass_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
    
    new_pass_entry2 = tk.Entry(right_frame, show="•", **entry_style)
    new_pass_entry2.grid(row=3, column=0, pady=(0, 20), ipady=5)
    
    change_pass_btn = tk.Button(right_frame, text="Change Pass",
                               font=("Helvetica", 11, "bold"),
                               bg="#8A8A8A",
                               fg="white",
                               width=15,
                               command=change_password)
    change_pass_btn.grid(row=4, column=0, pady=10)
    
    # Set hover colors
    change_user_btn.normal_color = "#8A8A8A"
    change_user_btn.hover_color = "#A3A3A3"
    
    change_pass_btn.normal_color = "#8A8A8A"
    change_pass_btn.hover_color = "#A3A3A3"
    
    back_btn.normal_color = "#757575"
    back_btn.hover_color = "#616161"
    
    # Setup hover effects
    setup_hover_effects()
    
    # Focus on first entry
    new_user_entry1.focus_set()