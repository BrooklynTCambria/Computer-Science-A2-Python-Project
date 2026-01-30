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

def EmployeeMenu():
    root = tk.Tk()
    root.title("SPOTLIGHT AGENCY - Employee Menu")
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
    
    # Title
    title_label = tk.Label(main_frame, text="EMPLOYEE MENU", 
                          font=("Helvetica", 28, "bold"),
                          fg="black",
                          bg="#f0f0f0")
    title_label.pack(pady=(0, 40))
    
    # Main frame for buttons
    button_frame = tk.Frame(main_frame, bg="#f0f0f0")
    button_frame.pack(pady=20)
    
    # Rental View Button
    rental_view_btn = tk.Button(button_frame, text="VIEW RENTALS", 
                               font=("Helvetica", 16, "bold"),
                               bg="#8A8A8A",
                               fg="white",
                               activebackground="#A3A3A3",
                               width=25,
                               height=2,
                               command=lambda: print("Opening Rental View"))
    rental_view_btn.pack(pady=10)
    
    # Rental Create Button
    rental_create_btn = tk.Button(button_frame, text="CREATE RENTAL", 
                                 font=("Helvetica", 16, "bold"),
                                 bg="#8A8A8A",
                                 fg="white",
                                 activebackground="#A3A3A3",
                                 width=25,
                                 height=2,
                                 command=lambda: print("Opening Rental Create"))
    rental_create_btn.pack(pady=10)
    
    # Hover effects
    def on_enter(e):
        if hasattr(e.widget, 'hover_color'):
            e.widget.config(bg=e.widget.hover_color)
    
    def on_leave(e):
        if hasattr(e.widget, 'normal_color'):
            e.widget.config(bg=e.widget.normal_color)
    
    # Set hover colors for buttons
    rental_view_btn.normal_color = "#8A8A8A"
    rental_view_btn.hover_color = "#A3A3A3"
    
    rental_create_btn.normal_color = "#8A8A8A"
    rental_create_btn.hover_color = "#A3A3A3"
    
    back_btn.normal_color = "#757575"
    back_btn.hover_color = "#616161"
    
    # Bind hover events
    rental_view_btn.bind("<Enter>", on_enter)
    rental_view_btn.bind("<Leave>", on_leave)
    
    rental_create_btn.bind("<Enter>", on_enter)
    rental_create_btn.bind("<Leave>", on_leave)
    
    back_btn.bind("<Enter>", on_enter)
    back_btn.bind("<Leave>", on_leave)
    
    # Make sure window is fully visible
    root.update_idletasks()
    
    root.mainloop()

# If you want to test the EmployeeMenu directly
if __name__ == "__main__":
    EmployeeMenu()