import tkinter as tk
from tkinter import ttk

def center_window(window, width=650, height=500):
    """Center the window on screen"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def open_login_window():
    """Function to open login window"""
    from Login import Login
    Login()

def create_button(parent, text, command, row, col, width=20):
    """Helper function to create styled buttons"""
    btn = tk.Button(parent, text=text, 
                   font=("Helvetica", 12),
                   command=command,
                   bg="#8A8A8A",
                   fg="white",
                   activebackground="#A3A3A3",
                   width=width,
                   height=2,
                   relief=tk.RAISED,
                   borderwidth=2)
    btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    return btn

def AdminMenu():
    root = tk.Tk()
    root.title("SPOTLIGHT AGENCY - Admin Menu")
    root.geometry("650x500")
    root.resizable(False, False)
    center_window(root, 650, 500)
    
    # Configure grid weights
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=1)
    
    # Try to set icon
    try:
        root.iconphoto(False, tk.PhotoImage(file="icon.png"))
    except:
        pass
    
    # Title frame
    title_frame = tk.Frame(root, height=80)
    title_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
    title_frame.grid_propagate(False)
    
    title_label = tk.Label(title_frame, text="ADMIN MENU", 
                          font=("Helvetica", 24, "bold"),
                          fg="Black",)
    title_label.pack(expand=True)
    
    # Main content frame
    main_frame = tk.Frame(root, bg="#ECF0F1")
    main_frame.grid(row=1, column=0, columnspan=2, rowspan=4, sticky="nsew", padx=20, pady=20)
    
    # Configure main frame grid
    for i in range(4):
        main_frame.grid_rowconfigure(i, weight=1)
    for i in range(2):
        main_frame.grid_columnconfigure(i, weight=1)
    
    # Create buttons in grid layout (4 rows x 2 columns)
    buttons = [
        ("RENTAL VIEW", lambda: print("Opening Rental View"), 0, 0),
        ("RENTAL CREATE", lambda: print("Opening Rental Create"), 0, 1),
        ("EMPLOYEE VIEW", lambda: print("Opening Employee View"), 1, 0),
        ("EMPLOYEE ADD", lambda: print("Opening Employee Add"), 1, 1),
        ("STOCK VIEW", lambda: print("Opening Stock View"), 2, 0),
        ("STOCK ADD", lambda: print("Opening Stock Add"), 2, 1),
        ("CUSTOMER VIEW", lambda: print("Opening Customer View"), 3, 0),
        ("REVENUE", lambda: print("Opening Revenue"), 3, 1),
    ]
    
    for text, command, row, col in buttons:
        create_button(main_frame, text, command, row, col, width=22)
    
    # Bottom frame for back button
    bottom_frame = tk.Frame(root, bg="#ECF0F1", height=60)
    bottom_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
    bottom_frame.grid_propagate(False)
    
    # Back button
    back_btn = tk.Button(bottom_frame, text="BACK", 
                        command=lambda: [root.destroy(), open_login_window()], 
                        font=("Helvetica", 12, "bold"),
                        height=2,
                        width=20,
                        bg="#A3A3A3",
                        fg="white",
                        activebackground="#8A8A8A",
                        relief=tk.RAISED,
                        borderwidth=2)
    back_btn.pack(pady=10)
    
    # Hover effect function
    def on_enter(e):
        e.widget.config(bg="#8A8A8A")
    
    def on_leave(e):
        if e.widget.cget("text") != "BACK":
            e.widget.config(bg="#8A8A8A")
        else:
            e.widget.config(bg="#A3A3A3")
    
    # Apply hover effects to all buttons
    for child in main_frame.winfo_children():
        if isinstance(child, tk.Button):
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)
    
    back_btn.bind("<Enter>", on_enter)
    back_btn.bind("<Leave>", on_leave)
    
    root.mainloop()

# If you want to test the AdminMenu directly
if __name__ == "__main__":
    AdminMenu()