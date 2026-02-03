import tkinter as tk

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

def open_employee_add_window():
    from EmployeeAdd import EmployeeAdd
    # Hide the admin menu window
    root.withdraw()
    # Open the Employee Add window
    EmployeeAdd(root)
    
def open_employee_view_window():
    from EmployeeView import EmployeeView
    # Hide the admin menu window
    root.withdraw()
    # Open the Employee View window
    EmployeeView(root)
    
def open_rental_view_window():
    from RentalView import RentalView
    # Hide the admin menu window
    root.withdraw()
    # Open the Rental View window
    RentalView(root)
    
def open_rental_create_window():
    from RentalCreate import RentalCreate
    # Hide the admin menu window
    root.withdraw()
    # Open the Rental Create window
    RentalCreate(root)
    
def open_stock_view_window():
    from StockView import StockView
    # Hide the admin menu window
    root.withdraw()
    # Open the Stock View window
    StockView(root)
    
def open_stock_add_window():
    from StockAdd import StockAdd
    # Hide the admin menu window
    root.withdraw()
    # Open the Stock View window
    StockAdd(root)
    
def open_customer_view_window():
    from CustomerView import CustomerView
    # Hide the admin menu window
    root.withdraw()
    # Open the Stock View window
    CustomerView(root)
    
def open_revenue_window():
    from Revenue import Revenue
    # Hide the admin menu window
    root.withdraw()
    # Open the Revenue window
    Revenue(root)
    
def AdminMenu():
    global root  # Make root accessible to other functions
    
    root = tk.Tk()
    root.title("SPOTLIGHT AGENCY - Admin Menu")
    root.geometry("650x500")
    root.resizable(False, False)
    center_window(root, 650, 500)
    
    # Set background color
    root.configure(bg="#f0f0f0")
    
    # Try to set icon
    try:
        root.iconphoto(False, tk.PhotoImage(file="icon.png"))
    except:
        pass
    
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
                        command=lambda: [root.destroy(), open_login_window()])
    back_btn.pack(side="right", padx=5, pady=5)
    
    # Title - SPOTLIGHT AGENCY
    agency_label = tk.Label(main_frame, text="SPOTLIGHT AGENCY", 
                           font=("Helvetica", 18, "bold"),
                           fg="black",
                           bg="#f0f0f0")
    agency_label.pack(pady=(0, 5))
    
    # Subtitle - ADMIN MENU
    subtitle_label = tk.Label(main_frame, text="ADMIN MENU", 
                             font=("Helvetica", 16, "bold"),
                             fg="#333333",
                             bg="#f0f0f0")
    subtitle_label.pack(pady=(0, 30))
    
    # Frame for grid of buttons (2 columns)
    grid_frame = tk.Frame(main_frame, bg="#f0f0f0")
    grid_frame.pack(pady=10, padx=10)
    
    # List of buttons in order (left column then right column)
    button_configs = [
        # (text, command, row, column)
        ("RENTAL VIEW", open_rental_view_window, 0, 0),
        ("STOCK VIEW", open_stock_view_window, 0, 1),
        ("RENTAL CREATE", open_rental_create_window, 1, 0),
        ("STOCK ADD", open_stock_add_window, 1, 1),
        ("EMPLOYEE VIEW", open_employee_view_window, 2, 0),
        ("CUSTOMER VIEW", open_customer_view_window, 2, 1),
        ("EMPLOYEE ADD", open_employee_add_window, 3, 0),
        ("REVENUE", open_revenue_window, 3, 1),
    ]
    
    # Store all buttons for hover effects
    all_buttons = []
    
    # Create buttons in grid
    for text, command, row, col in button_configs:
        btn = tk.Button(grid_frame, text=text,
                       font=("Helvetica", 13, "bold"),  # Slightly smaller font for better fit
                       bg="#8A8A8A",
                       fg="white",
                       activebackground="#A3A3A3",
                       width=18,  # Slightly smaller width
                       height=2,
                       command=command)
        btn.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        all_buttons.append(btn)
    
    # Configure grid weights for equal spacing
    grid_frame.grid_columnconfigure(0, weight=1)
    grid_frame.grid_columnconfigure(1, weight=1)
    for i in range(4):  # 4 rows
        grid_frame.grid_rowconfigure(i, weight=1)
    
    # Hover effects function
    def on_enter(e):
        if hasattr(e.widget, 'hover_color'):
            e.widget.config(bg=e.widget.hover_color)
    
    def on_leave(e):
        if hasattr(e.widget, 'normal_color'):
            e.widget.config(bg=e.widget.normal_color)
    
    # Set hover colors for all grid buttons
    for btn in all_buttons:
        btn.normal_color = "#8A8A8A"
        btn.hover_color = "#A3A3A3"
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    # Set hover colors for BACK button
    back_btn.normal_color = "#757575"
    back_btn.hover_color = "#616161"
    back_btn.bind("<Enter>", on_enter)
    back_btn.bind("<Leave>", on_leave)
    
    root.mainloop()

# If you want to test the AdminMenu directly
if __name__ == "__main__":
    AdminMenu()