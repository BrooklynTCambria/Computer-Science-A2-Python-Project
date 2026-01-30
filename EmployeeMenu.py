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
    main_frame.pack(fill="both", expand=True)
    
    # Title
    title_label = tk.Label(main_frame, text="EMPLOYEE MENU", 
                          font=("Helvetica", 28, "bold"),
                          fg="black",
                          bg="#f0f0f0")
    title_label.pack(pady=40)
    
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
    
    # Bottom frame for back button
    bottom_frame = tk.Frame(main_frame, bg="#f0f0f0")
    bottom_frame.pack(side="bottom", pady=20)
    
    # Back Button
    back_btn = tk.Button(bottom_frame, text="BACK", 
                        font=("Helvetica", 14),
                        bg="#757575",
                        fg="white",
                        activebackground="#616161",
                        width=15,
                        height=1,
                        command=lambda: [root.destroy(), open_login_window()])
    back_btn.pack()
    
    # Hover effects
    def on_enter(e):
        e.widget.config(bg=e.widget.hover_color)
    
    def on_leave(e):
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