import tkinter as tk
from tkinter import messagebox
import random
import pickle
import hashlib
import os

# User data file
PASS_HASHED = "passHash.pkl"

# List of random nouns for password generation
RANDOM_NOUNS = [
    "apple", "river", "mountain", "ocean", "forest", "desert", "valley",
    "sun", "moon", "star", "planet", "galaxy", "comet", "meteor",
    "tiger", "eagle", "dolphin", "panther", "falcon", "wolf", "bear",
    "crystal", "diamond", "emerald", "ruby", "sapphire", "amber", "opal",
    "thunder", "lightning", "storm", "rainbow", "cloud", "breeze", "hurricane",
    "phoenix", "dragon", "unicorn", "griffin", "pegasus", "mermaid", "centaur"
]

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

def generate_username():
    """Generate username in format 'USER' + 4 random digits"""
    random_num = random.randint(1000, 9999)
    return f"USER{random_num}"

def generate_password():
    """Generate password as random noun + 3 random numbers"""
    random_noun = random.choice(RANDOM_NOUNS)
    random_nums = random.randint(100, 999)
    return f"{random_noun}{random_nums}"

def EmployeeAdd(parent_window=None):
    """Function to open Employee Add window"""
    
    def setup_hover_effects():
        """Setup hover effects for buttons"""
        def on_enter(e):
            if hasattr(e.widget, 'hover_color'):
                e.widget.config(bg=e.widget.hover_color)
        
        def on_leave(e):
            if hasattr(e.widget, 'normal_color'):
                e.widget.config(bg=e.widget.normal_color)
        
        # Set hover colors for ADD button
        add_button.normal_color = "#8A8A8A"
        add_button.hover_color = "#A3A3A3"
        
        # Bind events for ADD button
        add_button.bind("<Enter>", on_enter)
        add_button.bind("<Leave>", on_leave)
        
        # Set hover colors for BACK button
        back_btn.normal_color = "#757575"
        back_btn.hover_color = "#616161"
        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)
    
    def add_employee():
        """Add employee to the system"""
        # Get values
        firstname = firstname_entry.get().strip()
        surname = surname_entry.get().strip()
        
        # Validation
        if not firstname:
            messagebox.showerror("Error", "First name is required!")
            firstname_entry.focus_set()
            return
        
        if not surname:
            messagebox.showerror("Error", "Surname is required!")
            surname_entry.focus_set()
            return
        
        # Generate credentials
        username = generate_username()
        password = generate_password()
        
        # Check if username already exists
        users = load_users()
        
        # Ensure username is unique (should be rare but just in case)
        while username in users:
            username = generate_username()
        
        # Create credentials popup
        show_credentials_popup(firstname, surname, username, password, users)
    
    def show_credentials_popup(firstname, surname, username, password, users):
        """Show popup with generated credentials"""
        # Create popup window
        popup = tk.Toplevel(root)
        popup.title("Employee Credentials")
        popup.geometry("300x400")
        popup.resizable(False, False)
        popup.configure(bg="#152e41")
        
        # Center the popup
        popup.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() // 2) - (300 // 2)
        y = root.winfo_y() + (root.winfo_height() // 2) - (400 // 2)
        popup.geometry(f"300x400+{x}+{y}")
        
        # Set icon
        try:
            popup.iconphoto(False, tk.PhotoImage(file="icon.png"))
        except:
            pass
        
        # Title
        title_label = tk.Label(popup, text="EMPLOYEE CREDENTIALS", 
                              font=("Helvetica", 16, "bold"),
                              fg="white",
                              bg="#152e41")
        title_label.pack(pady=20)
        
        # Employee info
        info_frame = tk.Frame(popup, bg="#152e41")
        info_frame.pack(pady=10, padx=20, fill="both")
        
        # Employee name
        name_label = tk.Label(info_frame, 
                             text=f"{firstname} {surname}",
                             font=("Helvetica", 14, "bold"),
                             bg="#152e41")
        name_label.pack(pady=5)
        
        # Generated credentials
        cred_frame = tk.Frame(info_frame, bg="#152e41", highlightbackground="#8A8A8A", 
                             highlightthickness=2, highlightcolor="#8A8A8A")
        cred_frame.pack(pady=20, padx=10, fill="both")
        
        # Username
        username_label = tk.Label(cred_frame, text="Username:", 
                                 font=("Helvetica", 12),
                                 bg="#152e41", fg="#333333")
        username_label.pack(pady=(15, 5))
        
        username_value = tk.Label(cred_frame, text=username,
                                 font=("Helvetica", 12, "bold"),
                                 bg="#152e41", fg="white")
        username_value.pack(pady=(0, 10))
        
        # Password
        password_label = tk.Label(cred_frame, text="Password:", 
                                 font=("Helvetica", 12),
                                 bg="#152e41", fg="#333333")
        password_label.pack(pady=(5, 5))
        
        password_value = tk.Label(cred_frame, text=password,
                                 font=("Helvetica", 12, "bold"),
                                 bg="#152e41", fg="white")
        password_value.pack(pady=(0, 15))
        
        # OK Button
        def save_and_close():
            # Save employee to database
            users[username] = {
                "password_hash": hash_password(password),
                "role": "employee",
                "firstname": firstname,
                "surname": surname
            }
            
            save_users(users)
            
            # Close popup
            popup.destroy()
            
            # Clear form and focus on first name for next entry
            firstname_entry.delete(0, tk.END)
            surname_entry.delete(0, tk.END)
            firstname_entry.focus_set()
        
        ok_button = tk.Button(popup, text="OK", 
                             font=("Helvetica", 12, "bold"),
                             bg="#8A8A8A",
                             fg="white",
                             width=10,
                             height=1,
                             command=save_and_close)
        ok_button.pack(pady=20)
        
        # Make popup modal
        popup.transient(root)
        popup.grab_set()
        popup.focus_set()
        
        # Bind Enter key to OK button
        popup.bind('<Return>', lambda e: save_and_close())
        
        # Set hover for OK button
        ok_button.normal_color = "#8A8A8A"
        ok_button.hover_color = "#A3A3A3"
        ok_button.bind("<Enter>", lambda e: e.widget.config(bg="#A3A3A3"))
        ok_button.bind("<Leave>", lambda e: e.widget.config(bg="#8A8A8A"))
    
    def go_back():
        """Go back to previous window"""
        root.destroy()
        if parent_window:
            # Bring focus back to parent window
            parent_window.deiconify()
    
    # Create the window
    root = tk.Toplevel() if parent_window else tk.Tk()
    root.title("SPOTLIGHT AGENCY - Add Employee")
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
    
    # TOP FRAME for BACK button (top right) - ALWAYS show
    top_frame = tk.Frame(main_frame, bg="#152e41")
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
    
    # Title - SPOTLIGHT AGENCY
    agency_label = tk.Label(main_frame, text="EMPLOYEE ADD", 
                           font=("Helvetica", 18, "bold"),
                           fg="white",
                           bg="#152e41")
    agency_label.pack(pady=(0, 30))
    
    # Input fields frame
    input_frame = tk.Frame(main_frame, bg="#152e41")
    input_frame.pack(pady=10)
    
    # Style for labels
    label_style = {
        "font": ("Helvetica", 11),
        "bg": "#152e41",
        "fg": "white",
        "anchor": "w"
    }
    
    # Style for entries
    entry_style = {
        "font": ("Helvetica", 12),
        "width": 30,
        "bd": 1,
        "relief": "solid",
        "highlightthickness": 1
    }
    
    # First Name
    firstname_label = tk.Label(input_frame, text="FIRST NAME", **label_style)
    firstname_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    firstname_entry = tk.Entry(input_frame, **entry_style)
    firstname_entry.grid(row=1, column=0, pady=(0, 15), ipady=5)
    
    # Surname
    surname_label = tk.Label(input_frame, text="SURNAME", **label_style)
    surname_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
    
    surname_entry = tk.Entry(input_frame, **entry_style)
    surname_entry.grid(row=3, column=0, pady=(0, 30), ipady=5)
    
    # Button frame for ADD button
    button_frame = tk.Frame(main_frame, bg="#152e41")
    button_frame.pack(pady=20)
    
    # Add Button
    add_button = tk.Button(button_frame, text="ADD", 
                          font=("Helvetica", 14, "bold"),
                          bg="#8A8A8A",
                          fg="white",
                          activebackground="#A3A3A3",
                          width=15,
                          height=2,
                          command=add_employee)
    add_button.pack()
    
    # Set up hover effects
    setup_hover_effects()
    
    # Bind Enter key to add employee
    root.bind('<Return>', lambda e: add_employee())
    
    # Focus on first entry
    firstname_entry.focus_set()
    
    if not parent_window:
        root.mainloop()

# For testing the EmployeeAdd directly
if __name__ == "__main__":
    EmployeeAdd()