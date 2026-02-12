import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import database_schema as db
import RentalCreate

def center_window(window, width=650, height=500):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def RentalView(parent_window=None):
    
    def setup_hover_effects():
        def on_enter(e):
            if hasattr(e.widget, 'hover_color'):
                e.widget.config(bg=e.widget.hover_color)
        
        def on_leave(e):
            if hasattr(e.widget, 'normal_color'):
                e.widget.config(bg=e.widget.normal_color)
        
        buttons = [search_btn, delete_btn, view_btn, edit_btn, back_btn]
        for btn in buttons:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def load_rental_data():
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)
        
        # Load rentals
        rentals = db.load_rentals()
        customers = db.load_customers()
        
        # Create customer lookup dictionary
        customer_dict = {c.customer_id: c for c in customers}
        
        # Add rental data with tags
        for rental in rentals:
            customer = customer_dict.get(rental.customer_id)
            if customer:
                customer_name = f"{customer.surname}, {customer.firstname}"
            else:
                customer_name = f"Customer ID: {rental.customer_id}"
            
            date_range = f"{rental.start_date.strftime('%d/%m/%y')} - {rental.end_date.strftime('%d/%m/%y')}"
            
            # Insert with rental ID as tag
            tree.insert("", "end", 
                       values=(date_range, customer_name, f"£{rental.total_price:.2f}", rental.employee),
                       tags=(str(rental.rental_id),))
    
    def on_item_select(event):
        selected = tree.selection()
        if selected:
            delete_btn.config(state="normal")
            view_btn.config(state="normal")
            edit_btn.config(state="normal")
            # Update selected count
            count_label.config(text=f"{len(selected)} SELECTED")
        else:
            delete_btn.config(state="disabled")
            view_btn.config(state="disabled")
            edit_btn.config(state="disabled")
            count_label.config(text="0 SELECTED")
    
    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a rental to delete.")
            return
        
        item = tree.item(selected[0])
        
        # Check if item has tags
        if not item['tags']:
            messagebox.showerror("Error", "Cannot delete this item - missing rental ID.")
            return
            
        rental_id = int(item['tags'][0])
        rental_info = item['values'][0]
        customer_name = item['values'][1]
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete rental:\n\n{customer_name}\n{rental_info}"
        )
        
        if confirm:
            # Delete from database
            rentals = db.load_rentals()
            rentals = [r for r in rentals if r.rental_id != rental_id]
            db.save_rentals(rentals)
            
            # Update treeview
            tree.delete(selected[0])
            messagebox.showinfo("Success", "rental deleted successfully.")
            delete_btn.config(state="disabled")
            view_btn.config(state="disabled")
            edit_btn.config(state="disabled")
            count_label.config(text="0 SELECTED")
    
    def edit_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a rental to edit.")
            return
        
        item = tree.item(selected[0])
        
        # Check if item has tags
        if not item['tags']:
            messagebox.showerror("Error", "Cannot edit this item - missing rental ID.")
            return
            
        rental_id = int(item['tags'][0])
        
        # Find rental details
        rentals = db.load_rentals()
        customers = db.load_customers()
        items_db = db.load_items()
        
        rental = None
        for r in rentals:
            if r.rental_id == rental_id:
                rental = r
                break
        
        if not rental:
            messagebox.showerror("Error", "rental not found!")
            return
        
        # Find customer
        customer = None
        for c in customers:
            if c.customer_id == rental.customer_id:
                customer = c
                break
        
        if not customer:
            messagebox.showerror("Error", "Customer not found!")
            return
        
        # Create edit window (using RentalCreate but with pre-filled data)
        # We need to pass the rental data to a modified version of RentalCreate
        edit_window = EditRentalWindow(root, rental, customer, items_db)
    
    def open_search_window():
        SearchWindow(root, apply_search_filter)
    
    def view_selected_list():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a rental to view.")
            return
        
        item = tree.item(selected[0])
        
        # Check if item has tags
        if not item['tags']:
            messagebox.showerror("Error", "Cannot view this item - missing rental ID.")
            return
            
        rental_id = int(item['tags'][0])
        
        # Find rental details
        rentals = db.load_rentals()
        customers = db.load_customers()
        items_db = db.load_items()
        
        rental = None
        for r in rentals:
            if r.rental_id == rental_id:
                rental = r
                break
        
        if not rental:
            messagebox.showerror("Error", "rental not found!")
            return
        
        # Find customer
        customer = None
        for c in customers:
            if c.customer_id == rental.customer_id:
                customer = c
                break
        
        # Build details string
        details = f"RENTAL DETAILS\n\n"
        details += f"rental ID: {rental.rental_id}\n"
        if customer:
            details += f"Customer: {customer.firstname} {customer.surname}\n"
            details += f"Phone: {customer.phone}\n"
        details += f"Employee: {rental.employee}\n"
        
        # Handle both datetime and date objects
        start_date = rental.start_date
        end_date = rental.end_date
        
        # Format dates
        if hasattr(start_date, 'strftime'):
            details += f"Start Date: {start_date.strftime('%d/%m/%Y')}\n"
        else:
            details += f"Start Date: {start_date}\n"
            
        if hasattr(end_date, 'strftime'):
            details += f"End Date: {end_date.strftime('%d/%m/%Y')}\n"
        else:
            details += f"End Date: {end_date}\n"
            
        details += f"Total: £{rental.total_price:.2f}\n"
        details += f"\nItems:\n"
        
        # Add items
        if hasattr(rental, 'items') and rental.items:
            for item_id, quantity in rental.items.items():
                for item in items_db:
                    if item.item_id == item_id:
                        item_total = item.price * quantity
                        details += f"- {item.name} x{quantity}: £{item_total:.2f} (£{item.price:.2f} each)\n"
                        break
        else:
            details += "- No items found for this rental\n"
        
        messagebox.showinfo("rental Details", details)
    
    def apply_search_filter(firstname_filter, lastname_filter, date_filter, employee_filter):
        # Clear current selection
        tree.selection_remove(tree.selection())
        
        # Show all items first by reattaching all
        for child in tree.get_children():
            tree.reattach(child, '', 'end')
        
        # If no search criteria, show all
        if not firstname_filter and not lastname_filter and not date_filter and not employee_filter:
            return
        
        # Hide non-matching items
        for child in tree.get_children():
            item = tree.item(child)
            item_values = item['values']
            
            # Skip items without proper values
            if len(item_values) < 2:
                tree.detach(child)
                continue
            
            customer_info = str(item_values[1]).lower()
            date_range = str(item_values[0]).lower()
            employee_info = str(item_values[3]).lower() if len(item_values) > 3 else ""
            
            match = True
            
            # Check customer name (format: "Last, First")
            if firstname_filter:
                # Extract first name from "Last, First" format
                parts = customer_info.split(',')
                if len(parts) > 1:
                    customer_firstname = parts[1].strip()
                    if firstname_filter.lower() not in customer_firstname:
                        match = False
                else:
                    match = False
            
            if lastname_filter:
                # Extract last name from "Last, First" format
                parts = customer_info.split(',')
                if len(parts) > 0:
                    customer_lastname = parts[0].strip()
                    if lastname_filter.lower() not in customer_lastname:
                        match = False
                else:
                    match = False
            
            if date_filter:
                date_str = date_filter.strip().lower()
                if date_str and date_str not in date_range:
                    match = False
            
            if employee_filter and employee_filter.lower() not in employee_info:
                match = False
            
            if not match:
                tree.detach(child)
    
    def go_back():
        root.destroy()
        if parent_window:
            parent_window.deiconify()
    
    # Create the main window
    root = tk.Toplevel() if parent_window else tk.Tk()
    root.title("SPOTLIGHT AGENCY - Rental Search")
    root.geometry("800x500")  # Wider for more columns
    root.resizable(False, False)
    center_window(root, 800, 550)  # Slightly taller for additional button
    
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
    title_label = tk.Label(main_frame, text="RENTAL SEARCH", 
                          font=("Helvetica", 20, "bold"),
                          fg="white",
                          bg="#152e41")
    title_label.pack(pady=(0, 20))
    
    # Top button frame (Search, View Selected, Edit, Delete Selected)
    top_button_frame = tk.Frame(main_frame, bg="#152e41")
    top_button_frame.pack(pady=(0, 15))
    
    # Search button
    search_btn = tk.Button(top_button_frame, text="SEARCH",
                          font=("Helvetica", 11, "bold"),
                          bg="#8acbcb",
                          fg="white",
                          activebackground="#7db6b6",
                          width=8,
                          height=2,
                          command=open_search_window)
    search_btn.pack(side="left", padx=5)
    
    # View Selected List button
    view_btn = tk.Button(top_button_frame, text="VIEW SELECTED LIST",
                        font=("Helvetica", 11, "bold"),
                        bg="#8acbcb",
                        fg="white",
                        activebackground="#7db6b6",
                        width=18,
                        height=2,
                        
                        command=view_selected_list)
    view_btn.pack(side="left", padx=5)
    
    # Edit Selected button
    edit_btn = tk.Button(top_button_frame, text="EDIT SELECTED",
                        font=("Helvetica", 11, "bold"),
                        bg="#8acbcb",
                        fg="white",
                        activebackground="#7db6b6",
                        width=14,
                        height=2,
                        
                        command=edit_selected)
    edit_btn.pack(side="left", padx=5)
    
    # Delete Selected button
    delete_btn = tk.Button(top_button_frame, text="DELETE SELECTED",
                          font=("Helvetica", 11, "bold"),
                          bg="#8acbcb",
                          fg="white",
                          activebackground="#7db6b6",
                          width=16,
                          height=2,
                          
                          command=delete_selected)
    delete_btn.pack(side="left", padx=5)
    
    # Selected count label
    count_label = tk.Label(top_button_frame, text="0 SELECTED",
                          font=("Helvetica", 12, "bold"),
                          bg="#152e41",
                          fg="white")
    count_label.pack(side="right", padx=20)
    
    # Treeview frame with scrollbar
    tree_frame = tk.Frame(main_frame, bg="#152e41")
    tree_frame.pack(fill="both", expand=True, pady=(0, 10))
    
    # Create Treeview
    columns = ("Date Range", "Customer", "Total", "Employee")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    
    # Define headings
    tree.heading("Date Range", text="Date Range")
    tree.heading("Customer", text="Customer")
    tree.heading("Total", text="Total")
    tree.heading("Employee", text="Employee")
    
    # Define columns
    tree.column("Date Range", width=150, anchor="w")
    tree.column("Customer", width=200, anchor="w")
    tree.column("Total", width=100, anchor="w")
    tree.column("Employee", width=100, anchor="w")
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Set hover colors
    search_btn.normal_color = "#8acbcb"
    search_btn.hover_color = "#7db6b6"
    
    view_btn.normal_color = "#8acbcb"
    view_btn.hover_color = "#7db6b6"
    
    edit_btn.normal_color = "#8acbcb"
    edit_btn.hover_color = "#7db6b6"
    
    delete_btn.normal_color = "#8acbcb"
    delete_btn.hover_color = "#7db6b6"
    
    back_btn.normal_color = "#8acbcb"
    back_btn.hover_color = "#7db6b6"
    
    # Setup hover effects
    setup_hover_effects()
    
    # Bind selection event
    tree.bind("<<TreeviewSelect>>", on_item_select)
    
    # Load initial data
    load_rental_data()
    
    if not parent_window:
        root.mainloop()

def SearchWindow(parent_window, apply_callback):
    
    def perform_search():
        firstname = firstname_entry.get().strip()
        lastname = lastname_entry.get().strip()
        date = date_entry.get().strip()
        employee = employee_entry.get().strip()
        
        # Apply search to main window
        apply_callback(firstname, lastname, date, employee)
        
        # Close search window
        search_root.destroy()
    
    def clear_and_close():
        apply_callback("", "", "", "")  # Clear filter
        search_root.destroy()
    
    def go_back():
        search_root.destroy()
    
    # Create search window
    search_root = tk.Toplevel(parent_window)
    search_root.title("SPOTLIGHT AGENCY - Search")
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
    
    # Main container frame
    main_frame = tk.Frame(search_root, bg="#152e41")
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
    title_label = tk.Label(main_frame, text="SEARCH", 
                          font=("Helvetica", 24, "bold"),
                          fg="white",
                          bg="#152e41")
    title_label.pack(pady=(0, 8))
    
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
        "bd": 0,
        "bg": "#dcffff",
        "relief": "solid",
        "highlightthickness": 0
    }
    
    # First Name
    firstname_label = tk.Label(criteria_frame, text="FIRST NAME", **label_style)
    firstname_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    firstname_entry = tk.Entry(criteria_frame, **entry_style)
    firstname_entry.grid(row=1, column=0, pady=(0, 20), ipady=5)
    
    # Last Name
    lastname_label = tk.Label(criteria_frame, text="LAST NAME", **label_style)
    lastname_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
    
    lastname_entry = tk.Entry(criteria_frame, **entry_style)
    lastname_entry.grid(row=3, column=0, pady=(0, 20), ipady=5)
    
    # Date (format hint)
    date_label = tk.Label(criteria_frame, text="DATE (dd/mm/yy)", **label_style)
    date_label.grid(row=4, column=0, sticky="w", pady=(0, 5))
    
    date_entry = tk.Entry(criteria_frame, **entry_style)
    date_entry.grid(row=5, column=0, pady=(0, 20), ipady=5)
    
    # Employee
    employee_label = tk.Label(criteria_frame, text="EMPLOYEE", **label_style)
    employee_label.grid(row=6, column=0, sticky="w", pady=(0, 5))
    
    employee_entry = tk.Entry(criteria_frame, **entry_style)
    employee_entry.grid(row=7, column=0, pady=(0, 30), ipady=5)
    
    # Button frame
    button_frame = tk.Frame(main_frame, bg="#152e41")
    button_frame.pack(pady=20)
    
    search_btn = tk.Button(button_frame, text="SEARCH",
                          font=("Helvetica", 14, "bold"),
                          bg="#8acbcb",
                          fg="white",
                          activebackground="#7db6b6",
                          width=20,
                          height=2,
                          command=perform_search)
    search_btn.pack(pady=10)
    
    clear_btn = tk.Button(button_frame, text="CLEAR",
                         font=("Helvetica", 14, "bold"),
                         bg="#8acbcb",
                         fg="white",
                         activebackground="#7db6b6",
                         width=20,
                         height=2,
                         command=clear_and_close)
    clear_btn.pack(pady=10)
    
    # Set hover colors
    search_btn.normal_color = "#8acbcb"
    search_btn.hover_color = "#7db6b6"
    
    clear_btn.normal_color = "#8acbcb"
    clear_btn.hover_color = "#7db6b6"
    
    back_btn.normal_color = "#8acbcb"
    back_btn.hover_color = "#7db6b6"
    
    # Setup hover effects
    search_btn.bind("<Enter>", lambda e: search_btn.config(bg="#7db6b6"))
    search_btn.bind("<Leave>", lambda e: search_btn.config(bg="#8acbcb"))
    clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg="#7db6b6"))
    clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg="#8acbcb"))
    back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#7db6b6"))
    back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#8acbcb"))
    
    # Bind Enter key to search
    firstname_entry.bind('<Return>', lambda e: perform_search())
    lastname_entry.bind('<Return>', lambda e: perform_search())
    date_entry.bind('<Return>', lambda e: perform_search())
    employee_entry.bind('<Return>', lambda e: perform_search())
    
    # Make window modal
    search_root.transient(parent_window)
    search_root.grab_set()
    search_root.focus_set()
    
    # Focus on first entry
    firstname_entry.focus_set()

class EditRentalWindow:
    def __init__(self, parent_window, rental, customer, all_items):
        self.parent_window = parent_window
        self.rental = rental
        self.customer = customer
        self.all_items = all_items
        self.original_rental = rental  # Keep original for reference
        self.selected_items = rental.items.copy() if hasattr(rental, 'items') else {}
        self.root = None
        self.create_window()
    
    def create_window(self):
        # Create the window
        self.root = tk.Toplevel(self.parent_window)
        self.root.title("SPOTLIGHT AGENCY - Edit rental")
        self.root.geometry("650x500")
        self.root.resizable(False, False)
        center_window(self.root, 650, 500)
        
        # Set icon
        try:
            self.root.iconphoto(False, tk.PhotoImage(file="icon.png"))
        except:
            pass
        
        # Set background color
        self.root.configure(bg="#152e41")
        
        self.setup_ui()
    
    def setup_hover_effects(self):
        def on_enter(e):
            if hasattr(e.widget, 'hover_color'):
                e.widget.config(bg=e.widget.hover_color)
        
        def on_leave(e):
            if hasattr(e.widget, 'normal_color'):
                e.widget.config(bg=e.widget.normal_color)
        
        buttons = [self.back_btn, self.add_btn, self.remove_btn, self.update_btn]
        for btn in buttons:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def setup_ui(self):
        # Main container frame
        main_frame = tk.Frame(self.root, bg="#152e41")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # TOP FRAME for BACK button (top right)
        top_frame = tk.Frame(main_frame, bg="#152e41")
        top_frame.pack(fill="x", pady=(0, 10))
        
        # BACK Button in top right corner
        self.back_btn = tk.Button(top_frame, text="BACK", 
                                font=("Helvetica", 12, "bold"),
                                bg="#8acbcb",
                                fg="white",
                                activebackground="#7db6b6",
                                width=10,
                                height=1,
                                command=self.go_back)
        self.back_btn.pack(side="right", padx=5, pady=5)
        
        # Title
        title_label = tk.Label(main_frame, text="EDIT RENTAL", 
                              font=("Helvetica", 18, "bold"),
                              fg="white",
                              bg="#152e41")
        title_label.pack(pady=(0, 15))
        
        # Create two columns for the form
        columns_frame = tk.Frame(main_frame, bg="#152e41")
        columns_frame.pack(fill="both", expand=True)
        
        # Left column - Customer details
        left_column = tk.Frame(columns_frame, bg="#152e41")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Right column - Items and dates
        right_column = tk.Frame(columns_frame, bg="#152e41")
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Setup left column (Customer details)
        self.setup_customer_column(left_column)
        
        # Setup right column (Items and dates)
        self.setup_items_column(right_column)
        
        # Bottom frame for total and update button
        bottom_frame = tk.Frame(main_frame, bg="#152e41")
        bottom_frame.pack(fill="x", pady=(10, 0))
        
        # Rental ID label
        rental_id_label = tk.Label(bottom_frame, text=f"Rental ID: {self.rental.rental_id}",
                                   font=("Helvetica", 11),
                                   bg="#152e41",
                                   fg="white")
        rental_id_label.pack(side="left", padx=10)
        
        # Total label
        self.total_label = tk.Label(bottom_frame, text="TOTAL: £0.00",
                                   font=("Helvetica", 14, "bold"),
                                   bg="#152e41",
                                   fg="white")
        self.total_label.pack(side="left", padx=10, expand=True)
        
        # Update button
        self.update_btn = tk.Button(bottom_frame, text="UPDATE",
                                   font=("Helvetica", 12, "bold"),
                                   bg="#8acbcb",
                                   fg="white",
                                   activebackground="#7db6b6",
                                   width=15,
                                   height=2,
                                   command=self.update_rental)
        self.update_btn.pack(side="right")
        
        # Set hover colors
        self.back_btn.normal_color = "#8acbcb"
        self.back_btn.hover_color = "#7db6b6"
        
        self.add_btn.normal_color = "#8acbcb"
        self.add_btn.hover_color = "#7db6b6"
        
        self.remove_btn.normal_color = "#8acbcb"
        self.remove_btn.hover_color = "#7db6b6"
        
        self.update_btn.normal_color = "#8acbcb"
        self.update_btn.hover_color = "#7db6b6"
        
        # Setup hover effects
        self.setup_hover_effects()
        
        # Bind Enter key to update rental
        self.root.bind('<Return>', lambda e: self.update_rental())
        
        # Update total initially
        self.update_total()
        
        # Focus on first entry
        self.firstname_entry.focus_set()
    
    def setup_customer_column(self, parent_frame):
        # Style for labels
        label_style = {
            "font": ("Helvetica", 12),
            "bg": "#152e41",
            "fg": "white",
            "anchor": "w"
        }
            
        # Style for entries
        entry_style = {
            "font": ("Helvetica", 11),
            "width": 25,
            "bd": 0,
            "bg": "#dcffff",
            "relief": "solid",
            "highlightthickness": 0
        }
        
        # First Name
        firstname_label = tk.Label(parent_frame, text="FIRST NAME", **label_style)
        firstname_label.pack(pady=(0, 5), anchor="w")
        
        self.firstname_entry = tk.Entry(parent_frame, **entry_style)
        self.firstname_entry.insert(0, self.customer.firstname)
        self.firstname_entry.pack(pady=(0, 15), ipady=5)
        
        # Last Name
        lastname_label = tk.Label(parent_frame, text="LAST NAME", **label_style)
        lastname_label.pack(pady=(0, 5), anchor="w")
        
        self.lastname_entry = tk.Entry(parent_frame, **entry_style)
        self.lastname_entry.insert(0, self.customer.surname)
        self.lastname_entry.pack(pady=(0, 15), ipady=5)
        
        # Phone Number
        phone_label = tk.Label(parent_frame, text="PHONE NUMBER", **label_style)
        phone_label.pack(pady=(0, 5), anchor="w")
        
        self.phone_entry = tk.Entry(parent_frame, **entry_style)
        self.phone_entry.insert(0, self.customer.phone)
        self.phone_entry.pack(pady=(0, 20), ipady=5)
        
        # Note: Auto fill button not needed for edit
    
    def setup_items_column(self, parent_frame):
        # Style for labels
        label_style = {
            "font": ("Helvetica", 12),
            "bg": "#152e41",
            "fg": "white",
            "anchor": "w"
        }
        
        # Date selection frame
        date_frame = tk.Frame(parent_frame, bg="#152e41")
        date_frame.pack(pady=(0, 20), fill="x")
        
        # Date label
        date_label = tk.Label(date_frame, text="DATE", **label_style)
        date_label.pack(pady=(0, 5), anchor="w")
        
        # Start and End date in one line
        dates_frame = tk.Frame(date_frame, bg="#152e41")
        dates_frame.pack(fill="x")
        
        # Start Date
        start_label = tk.Label(dates_frame, text="From:",
                              font=("Helvetica", 10),
                              bg="#152e41",
                              fg="white")
        start_label.pack(side="left", padx=(0, 5))
        
        # Create start date picker
        from datetime import datetime
        today = datetime.now()
        self.start_date_entry = DateEntry(dates_frame, 
                                         width=12,
                                         background='darkblue',
                                         foreground='white',
                                         borderwidth=2,
                                         date_pattern='dd/mm/yyyy',
                                         mindate=today)
        # Set to rental start date
        self.start_date_entry.set_date(self.rental.start_date)
        self.start_date_entry.pack(side="left", padx=(0, 15))
        
        # End Date
        end_label = tk.Label(dates_frame, text="To:",
                            font=("Helvetica", 10),
                            bg="#152e41",
                              fg="white")
        end_label.pack(side="left", padx=(0, 5))
        
        # Create end date picker
        self.end_date_entry = DateEntry(dates_frame,
                                       width=12,
                                       background='darkblue',
                                       foreground='white',
                                       borderwidth=2,
                                       date_pattern='dd/mm/yyyy',
                                       mindate=self.rental.start_date)
        # Set to rental end date
        self.end_date_entry.set_date(self.rental.end_date)
        self.end_date_entry.pack(side="left")
        
        # Bind date selection
        self.start_date_entry.bind("<<DateEntrySelected>>", self.on_start_date_selected)
        self.end_date_entry.bind("<<DateEntrySelected>>", self.validate_end_date)
        
        # Stock label
        stock_label = tk.Label(parent_frame, text="STOCK",
                              font=("Helvetica", 11, "bold"),
                              bg="#152e41",
                              fg="white",
                              anchor="w")
        stock_label.pack(pady=(0, 10), anchor="w")
        
        # Item selection frame
        item_frame = tk.Frame(parent_frame, bg="#152e41")
        item_frame.pack(fill="x", pady=(0, 10))
        
        # Item dropdown - include available quantities
        item_names = []
        for item in self.all_items:
            # Adjust available quantity if item is already in rental
            adjusted_qty = item.quantity
            if item.item_id in self.original_rental.items:
                adjusted_qty += self.original_rental.items[item.item_id]
            
            item_names.append(f"{item.name} - £{item.price:.2f} ({adjusted_qty} available)")
        
        self.item_var = tk.StringVar()
        self.item_dropdown = ttk.Combobox(item_frame,
                                         textvariable=self.item_var,
                                         values=item_names,
                                         state="readonly",
                                         width=30)
        self.item_dropdown.pack(side="left", padx=(0, 10))
        
        # Quantity
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_spin = tk.Spinbox(item_frame,
                                       from_=1,
                                       to=10,
                                       textvariable=self.quantity_var,
                                       width=5,
                                       font=("Helvetica", 10))
        self.quantity_spin.pack(side="left", padx=(0, 10))
        
        # Add button
        self.add_btn = tk.Button(item_frame, text="ADD",
                                font=("Helvetica", 10, "bold"),
                                bg="#8acbcb",
                                fg="white",
                                width=8,
                                command=self.add_item)
        self.add_btn.pack(side="left")
        
        # Selected items listbox
        selected_frame = tk.Frame(parent_frame, bg="#152e41")
        selected_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        selected_label = tk.Label(selected_frame, text="Selected Items:",
                                 font=("Helvetica", 10),
                                 bg="#152e41",
                                 fg="white")
        selected_label.pack(anchor="w")
        
        # Selected items listbox
        self.selected_listbox = tk.Listbox(selected_frame,
                                          height=6,
                                          width=35,
                                          selectmode="single",
                                          font=("Helvetica", 10))
        self.selected_listbox.pack(fill="both", expand=True, pady=(5, 10))
        
        # Add scrollbar for selected items
        selected_scrollbar = tk.Scrollbar(self.selected_listbox)
        selected_scrollbar.pack(side="right", fill="y")
        self.selected_listbox.config(yscrollcommand=selected_scrollbar.set)
        selected_scrollbar.config(command=self.selected_listbox.yview)
        
        # Populate with existing items
        for item_id, quantity in self.selected_items.items():
            for item in self.all_items:
                if item.item_id == item_id:
                    display_text = f"{item.name} x{quantity} - £{item.price * quantity:.2f}"
                    self.selected_listbox.insert(tk.END, display_text)
                    break
        
        # Remove button
        self.remove_btn = tk.Button(parent_frame, text="REMOVE SELECTED",
                                   font=("Helvetica", 10, "bold"),
                                   bg="#8acbcb",
                                   fg="white",
                                   width=20,
                                   command=self.remove_item)
        self.remove_btn.pack()
    
    def on_start_date_selected(self, event=None):
        try:
            start_date = self.start_date_entry.get_date()
            self.end_date_entry.config(mindate=start_date)
            self.update_total()
        except Exception as e:
            print(f"Error setting end date: {e}")
    
    def validate_end_date(self, event=None):
        try:
            start_date = self.start_date_entry.get_date()
            end_date = self.end_date_entry.get_date()
            
            if end_date < start_date:
                messagebox.showwarning("Invalid Date", "End date cannot be before start date!")
                self.end_date_entry.set_date(start_date)
            
            self.update_total()
        except Exception as e:
            print(f"Error validating end date: {e}")
    
    def add_item(self):
        selected_index = self.item_dropdown.current()
        if selected_index == -1:
            messagebox.showwarning("No Selection", "Please select an item from the dropdown.")
            return
        
        # Get selected item
        selected_item = self.all_items[selected_index]
        quantity = int(self.quantity_var.get())
        
        # Calculate available quantity (original + what was in rental)
        available_qty = selected_item.quantity
        if selected_item.item_id in self.original_rental.items:
            available_qty += self.original_rental.items[selected_item.item_id]
        
        # Check availability
        if quantity > available_qty:
            messagebox.showerror("Insufficient Stock", 
                               f"Only {available_qty} {selected_item.name} available.")
            return
        
        # Add to selected items
        if selected_item.item_id in self.selected_items:
            self.selected_items[selected_item.item_id] += quantity
            
            # Update display
            for i in range(self.selected_listbox.size()):
                item_text = self.selected_listbox.get(i)
                if selected_item.name in item_text:
                    if "x" in item_text:
                        parts = item_text.split("x")
                        current_qty = int(parts[1].split()[0])
                        new_qty = current_qty + quantity
                        new_text = f"{selected_item.name} x{new_qty} - £{selected_item.price * new_qty:.2f}"
                        self.selected_listbox.delete(i)
                        self.selected_listbox.insert(i, new_text)
                    break
        else:
            self.selected_items[selected_item.item_id] = quantity
            display_text = f"{selected_item.name} x{quantity} - £{selected_item.price * quantity:.2f}"
            self.selected_listbox.insert(tk.END, display_text)
        
        self.update_total()
        self.quantity_var.set("1")
    
    def remove_item(self):
        selection = self.selected_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item to remove.")
            return
        
        index = selection[0]
        item_text = self.selected_listbox.get(index)
        
        # Find which item this is
        for item in self.all_items:
            if item.name in item_text:
                if item.item_id in self.selected_items:
                    del self.selected_items[item.item_id]
                    break
        
        self.selected_listbox.delete(index)
        self.update_total()
    
    def update_total(self):
        total = 0.0
        
        for item_id, quantity in self.selected_items.items():
            for item in self.all_items:
                if item.item_id == item_id:
                    total += item.price * quantity
                    break
        
        # Calculate days
        try:
            start_date = self.start_date_entry.get_date()
            end_date = self.end_date_entry.get_date()
            days = (end_date - start_date).days + 1
            if days < 1:
                days = 1
            total *= days
        except:
            days = 1
        
        self.total_label.config(text=f"TOTAL: £{total:.2f}")
    
    def update_rental(self):
        # Get customer details
        firstname = self.firstname_entry.get().strip()
        lastname = self.lastname_entry.get().strip()
        phone = self.phone_entry.get().strip()
        
        # Validation
        if not firstname or not lastname or not phone:
            messagebox.showerror("Error", "All customer fields are required!")
            return
        
        if not self.selected_items:
            messagebox.showerror("Error", "Please add at least one item!")
            return
        
        # Get dates
        try:
            start_date = self.start_date_entry.get_date()
            end_date = self.end_date_entry.get_date()
            
            if end_date < start_date:
                messagebox.showerror("Error", "End date must be after start date!")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Invalid date: {str(e)}")
            return
        
        # Calculate total
        total = 0.0
        days = (end_date - start_date).days + 1
        
        # First, return original items to stock
        for item_id, quantity in self.original_rental.items.items():
            for item in self.all_items:
                if item.item_id == item_id:
                    item.quantity += quantity
                    break
        
        # Now deduct new items from stock and calculate total
        for item_id, quantity in self.selected_items.items():
            for item in self.all_items:
                if item.item_id == item_id:
                    # Check if enough stock
                    if quantity > item.quantity:
                        messagebox.showerror("Insufficient Stock", 
                                           f"Not enough {item.name} in stock!")
                        # Restore original items
                        for orig_id, orig_qty in self.original_rental.items.items():
                            for orig_item in self.all_items:
                                if orig_item.item_id == orig_id:
                                    orig_item.quantity -= orig_qty
                                    break
                        return
                    
                    item_total = item.price * quantity * days
                    total += item_total
                    item.quantity -= quantity
                    break
        
        # Update customer info if changed
        customers = db.load_customers()
        customer_updated = False
        for customer in customers:
            if customer.customer_id == self.customer.customer_id:
                if (customer.firstname != firstname or 
                    customer.surname != lastname or 
                    customer.phone != phone):
                    customer.firstname = firstname
                    customer.surname = lastname
                    customer.phone = phone
                    customer_updated = True
                break
        
        if customer_updated:
            db.save_customers(customers)
        
        # Update rental
        rentals = db.load_rentals()
        for rental in rentals:
            if rental.rental_id == self.rental.rental_id:
                rental.customer_id = self.customer.customer_id
                rental.start_date = start_date
                rental.end_date = end_date
                rental.items = self.selected_items.copy()
                rental.total_price = total
                break
        
        # Save all changes
        db.save_items(self.all_items)
        db.save_rentals(rentals)
        
        messagebox.showinfo("Success", "Rental updated successfully!")
        self.root.destroy()
        
        # Refresh the main view if needed
        if hasattr(self.parent_window, 'load_rental_data'):
            self.parent_window.load_rental_data()
    
    def go_back(self):
        self.root.destroy()

# For DateEntry import
from tkcalendar import DateEntry

# For testing directly
if __name__ == "__main__":
    RentalView()