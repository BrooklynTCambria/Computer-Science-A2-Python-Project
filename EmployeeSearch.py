# EmployeeSearch.py
import tkinter as tk
from tkinter import ttk, messagebox

def center_window(window, width=650, height=500):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def EmployeeSearch(parent_window, tree, load_callback):
    """Employee Search window"""
    
    def setup_hover_effects():
        """Setup hover effects for buttons"""
        def on_enter(e):
            if hasattr(e.widget, 'hover_color'):
                e.widget.config(bg=e.widget.hover_color)
        
        def on_leave(e):
            if hasattr(e.widget, 'normal_color'):
                e.widget.config(bg=e.widget.normal_color)
        
        buttons = [search_btn, clear_btn, back_btn]
        for btn in buttons:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def perform_search():
        """Perform search based on criteria"""
        firstname = firstname_entry.get().strip().lower()
        surname = surname_entry.get().strip().lower()
        username = username_entry.get().strip().lower()
        
        # Clear current selection
        tree.selection_remove(tree.selection())
        
        # Show all items first
        for child in tree.get_children():
            tree.item(child, tags=())
        
        # If no search criteria, show all
        if not firstname and not surname and not username:
            load_callback()
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
        firstname_entry.delete(0, tk.END)
        surname_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        load_callback()
    
    def go_back():
        """Go back to Employee View window"""
        root.destroy()
        if parent_window:
            parent_window.deiconify()
    
    # Create the window
    root = tk.Toplevel(parent_window)
    root.title("SPOTLIGHT AGENCY - Employee Search")
    root.geometry("650x500")
    root.resizable(False, False)
    center_window(root, 650, 500)
    
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
    title_label = tk.Label(main_frame, text="EMPLOYEE SEARCH", 
                          font=("Helvetica", 20, "bold"),
                          fg="black",
                          bg="#f0f0f0")
    title_label.pack(pady=(0, 20))
    
    # Search criteria frame
    criteria_frame = tk.Frame(main_frame, bg="#f0f0f0")
    criteria_frame.pack(pady=10)
    
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
    
    # First Name
    firstname_label = tk.Label(criteria_frame, text="First Name:", **label_style)
    firstname_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    firstname_entry = tk.Entry(criteria_frame, **entry_style)
    firstname_entry.grid(row=1, column=0, pady=(0, 15), ipady=5)
    
    # Surname
    surname_label = tk.Label(criteria_frame, text="Surname:", **label_style)
    surname_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
    
    surname_entry = tk.Entry(criteria_frame, **entry_style)
    surname_entry.grid(row=3, column=0, pady=(0, 15), ipady=5)
    
    # Username
    username_label = tk.Label(criteria_frame, text="Username:", **label_style)
    username_label.grid(row=4, column=0, sticky="w", pady=(0, 5))
    
    username_entry = tk.Entry(criteria_frame, **entry_style)
    username_entry.grid(row=5, column=0, pady=(0, 20), ipady=5)
    
    # Button frame
    button_frame = tk.Frame(main_frame, bg="#f0f0f0")
    button_frame.pack(pady=20)
    
    search_btn = tk.Button(button_frame, text="SEARCH",
                          font=("Helvetica", 12, "bold"),
                          bg="#8A8A8A",
                          fg="white",
                          width=12,
                          command=perform_search)
    search_btn.pack(side="left", padx=5)
    
    clear_btn = tk.Button(button_frame, text="CLEAR",
                         font=("Helvetica", 12, "bold"),
                         bg="#8A8A8A",
                         fg="white",
                         width=12,
                         command=clear_search)
    clear_btn.pack(side="left", padx=5)
    
    # Set hover colors
    search_btn.normal_color = "#8A8A8A"
    search_btn.hover_color = "#A3A3A3"
    
    clear_btn.normal_color = "#8A8A8A"
    clear_btn.hover_color = "#A3A3A3"
    
    back_btn.normal_color = "#757575"
    back_btn.hover_color = "#616161"
    
    # Setup hover effects
    setup_hover_effects()
    
    # Bind Enter key to search
    firstname_entry.bind('<Return>', lambda e: perform_search())
    surname_entry.bind('<Return>', lambda e: perform_search())
    username_entry.bind('<Return>', lambda e: perform_search())
    
    # Focus on first entry
    firstname_entry.focus_set()