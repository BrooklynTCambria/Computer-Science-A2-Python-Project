import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pickle
import hashlib
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

def create_default_admin():
    users = load_users()
    if not users:
        users = {
            "admin": {
                "password_hash": hash_password("admin123"),  # Default admin password
                "role": "admin"
            }
        }
        with open(PASS_HASHED, 'wb') as f:
            pickle.dump(users, f)
        print("Default admin account created. Username: admin, Password: admin123")

def authenticate_user(username, password):
    users = load_users()
    
    if username not in users:
        return False, "Invalid username or password"
    
    stored_hash = users[username]["password_hash"]
    input_hash = hash_password(password)
    
    if stored_hash == input_hash:
        return True, users[username]["role"]
    else:
        return False, "Invalid username or password"

def center_window(window, width=650, height=500):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def Login():
    root = tk.Tk()
    root.title("SPOTLIGHT AGENCY")
    root.geometry("650x500")
    root.resizable(False, False)
    center_window(root, 650, 500)
    
    # Set icon
    try:
        root.iconphoto(False, tk.PhotoImage(file="icon.png"))
    except:
        pass
    
    # Create default admin account if needed
    create_default_admin()
    
    # Main container frame
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Create a frame for the image
    image_frame = tk.Frame(main_frame, bg="white")
    image_frame.pack(pady=(20, 10))
    
    # Load and display image
    try:
        # Try to load the image
        img = Image.open("logo.png")  # Replace with your image file
        img = img.resize((180, 180), Image.Resampling.LANCZOS)  # Resize for 650x500
        photo = ImageTk.PhotoImage(img)
        
        image_label = tk.Label(image_frame, image=photo, bg="white")
        image_label.image = photo  # Keep a reference
        image_label.pack()
        
    except Exception as e:
        # If image not found, show text only
        print(f"Image not found: {e}")
        label = tk.Label(image_frame, text="SPOTLIGHT AGENCY", font=("Helvetica", 24, "bold"), bg="white")
        label.pack()
    
    # Login frame
    login_frame = tk.Frame(main_frame, bg="white")
    login_frame.pack(pady=10, padx=50, fill=tk.BOTH, expand=True)
    
    # Username entry with initial placeholder
    userInput = tk.Entry(login_frame, font=("Helvetica", 14), fg="grey", width=30)
    userInput.insert(0, "USERNAME")
    
    # Password entry with initial placeholder
    passInput = tk.Entry(login_frame, font=("Helvetica", 14), fg="grey", width=30)
    passInput.insert(0, "PASSWORD")
    
    def on_focus_in(event):
        widget = event.widget
        if widget == userInput and widget.get() == "USERNAME":
            widget.delete(0, tk.END)
            widget.config(fg="black")
        elif widget == passInput and widget.get() == "PASSWORD":
            widget.delete(0, tk.END)
            widget.config(fg="black", show="*")
    
    def on_focus_out(event):
        widget = event.widget
        if widget == userInput and not widget.get():
            widget.insert(0, "USERNAME")
            widget.config(fg="grey")
        elif widget == passInput and not widget.get():
            widget.insert(0, "PASSWORD")
            widget.config(fg="grey", show="")
    
    # Bind events
    userInput.bind("<FocusIn>", on_focus_in)
    userInput.bind("<FocusOut>", on_focus_out)
    passInput.bind("<FocusIn>", on_focus_in)
    passInput.bind("<FocusOut>", on_focus_out)
    
    userInput.pack(pady=15)
    passInput.pack(pady=15)
    
    # Error label (initially empty)
    error_label = tk.Label(login_frame, text="", fg="red", font=("Helvetica", 10), bg="white")
    error_label.pack(pady=5)
    
    # Login button
    def submit_login():
        username = userInput.get().strip()
        password = passInput.get().strip()
        
        # Clear previous error
        error_label.config(text="")
        
        # Check for placeholder values
        if username == "USERNAME" or not username:
            error_label.config(text="Please enter username")
            return
        
        if password == "PASSWORD" or not password:
            error_label.config(text="Please enter password")
            return
        
        # Authenticate user
        success, result = authenticate_user(username, password)
        
        if success:
            print(f"Login successful - Username: {username}, Role: {result}")
            root.destroy()  # Close login window
            
            # Import AdminMenu here to avoid circular import
            from AdminMenu import AdminMenu
            
            # Open appropriate menu based on role
            if result == "admin":
                AdminMenu()
            else:
                # For regular users, you can create a different menu
                AdminMenu()
        else:
            error_label.config(text=result)
    
    login_button = tk.Button(login_frame, text="LOGIN", font=("Helvetica", 14, "bold"), command=submit_login, bg="#8A8A8A", fg="white", width=25, height=2)
    login_button.pack(pady=20)
    
    # Instructions for default login
    info_label = tk.Label(main_frame, text="Default login: admin / admin123", font=("Helvetica", 10), fg="gray", bg="white")
    info_label.pack(pady=5)
    
    root.mainloop()

# Start the login screen
if __name__ == "__main__":
    Login()