# CustomerView.py
import tkinter as tk
from tkinter import ttk, messagebox
import database_schema as db

def center_window(window, width=650, height=500):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def CustomerView(parent_window=None):
    """Main Customer View window"""
    
    def setup_hover_effects():
        """Setup hover effects for buttons"""
        def on_enter(e):
            if hasattr(e.widget, 'hover_color'):
                e.widget.config(bg=e.widget.hover_color)
        
        def on_leave(e):
            if hasattr(e.widget, 'normal_color'):
                e.widget.config(bg=e.widget.normal_color)
        
        buttons = [search_btn, delete_btn, view_btn, back_btn]
        for btn in buttons:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def load_customer_data():
        """Load customer data from database"""
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)
        
        # Load customers
        customers = db.load_customers()
        
        # Sort by last name
        customers.sort(key=lambda x: x.surname.lower())
        
        # Add customer data with tags
        for customer in customers:
            # Insert with customer ID as tag
            tree.insert("", "end", 
                       values=(customer.firstname, customer.surname, customer.phone),
                       tags=(str(customer.customer_id),))
    
    def on_item_select(event):
        """Handle item selection"""
        selected = tree.selection()
        if selected:
            delete_btn.config(state="normal")
            view_btn.config(state="normal")
            # Update selected count
            count_label.config(text=f"{len(selected)} SELECTED")
        else:
            delete_btn.config(state="disabled")
            view_btn.config(state="disabled")
            count_label.config(text="0 SELECTED")
    
    def delete_selected():
        """Delete selected customer"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a customer to delete.")
            return
        
        item = tree.item(selected[0])
        
        # Check if item has tags
        if not item['tags']:
            messagebox.showerror("Error", "Cannot delete this customer - missing customer ID.")
            return
            
        customer_id = int(item['tags'][0])
        firstname = item['values'][0]
        surname = item['values'][1]
        
        # Check if customer has any rentals
        rentals = db.load_rentals()
        customer_rentals = [r for r in rentals if r.customer_id == customer_id]
        
        if customer_rentals:
            rental_count = len(customer_rentals)
            confirm = messagebox.askyesno(
                "Customer Has Rentals",
                f"Customer {firstname} {surname} has {rental_count} rental(s) in the system.\n\n"
                f"Deleting this customer will also delete their rental history.\n"
                f"Are you sure you want to delete this customer?"
            )
            
            if not confirm:
                return
        else:
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete customer:\n\n{firstname} {surname}"
            )
            
            if not confirm:
                return
        
        # Delete from database
        customers = db.load_customers()
        customers = [c for c in customers if c.customer_id != customer_id]
        db.save_customers(customers)
        
        # Also delete customer's rentals if they exist
        if customer_rentals:
            rentals = [r for r in rentals if r.customer_id != customer_id]
            db.save_rentals(rentals)
        
        # Update treeview
        tree.delete(selected[0])
        messagebox.showinfo("Success", "Customer deleted successfully.")
        delete_btn.config(state="disabled")
        view_btn.config(state="disabled")
        count_label.config(text="0 SELECTED")
    
    def open_search_window():
        """Open Search window"""
        SearchWindow(root, apply_search_filter)
    
    def view_selected_customer():
        """View details of selected customer"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a customer to view.")
            return
        
        item = tree.item(selected[0])
        
        # Check if item has tags
        if not item['tags']:
            messagebox.showerror("Error", "Cannot view this customer - missing customer ID.")
            return
            
        customer_id = int(item['tags'][0])
        
        # Find customer details
        customers = db.load_customers()
        rentals = db.load_rentals()
        
        customer = None
        for c in customers:
            if c.customer_id == customer_id:
                customer = c
                break
        
        if not customer:
            messagebox.showerror("Error", "Customer not found!")
            return
        
        # Find customer's rentals
        customer_rentals = [r for r in rentals if r.customer_id == customer_id]
        
        # Build details string
        details = f"CUSTOMER DETAILS\n\n"
        details += f"Customer ID: {customer.customer_id}\n"
        details += f"First Name: {customer.firstname}\n"
        details += f"Last Name: {customer.surname}\n"
        details += f"Phone: {customer.phone}\n"
        details += f"\nRental History ({len(customer_rentals)}):\n"
        
        # Add rental history
        if customer_rentals:
            customer_rentals.sort(key=lambda x: x.start_date, reverse=True)
            for i, rental in enumerate(customer_rentals[:10], 1):  # Show last 10 rentals
                # Format dates
                if hasattr(rental.start_date, 'strftime'):
                    start_date = rental.start_date.strftime('%d/%m/%Y')
                    end_date = rental.end_date.strftime('%d/%m/%Y')
                else:
                    start_date = str(rental.start_date)
                    end_date = str(rental.end_date)
                
                details += f"{i}. Rental #{rental.rental_id}: {start_date} to {end_date} - £{rental.total_price:.2f}\n"
            
            if len(customer_rentals) > 10:
                details += f"... and {len(customer_rentals) - 10} more\n"
        else:
            details += "- No rental history\n"
        
        messagebox.showinfo("Customer Details", details)
    
    def apply_search_filter(firstname_filter, surname_filter, phone_filter):
        """Apply search filter to the treeview"""
        # Clear current selection
        tree.selection_remove(tree.selection())
        
        # Show all items first by reattaching all
        for child in tree.get_children():
            tree.reattach(child, '', 'end')
        
        # If no search criteria, show all
        if not firstname_filter and not surname_filter and not phone_filter:
            return
        
        # Hide non-matching items
        for child in tree.get_children():
            item = tree.item(child)
            item_values = item['values']
            
            # Skip items without proper values
            if len(item_values) < 3:
                tree.detach(child)
                continue
            
            customer_firstname = str(item_values[0]).lower()
            customer_surname = str(item_values[1]).lower()
            customer_phone = str(item_values[2]).lower()
            
            match = True
            
            # Check first name
            if firstname_filter and firstname_filter.lower() not in customer_firstname:
                match = False
            
            # Check surname
            if surname_filter and surname_filter.lower() not in customer_surname:
                match = False
            
            # Check phone (remove +41 prefix for search if provided)
            if phone_filter:
                search_phone = phone_filter.lower().replace('+41', '').replace(' ', '')
                actual_phone = customer_phone.replace('+41', '').replace(' ', '')
                if search_phone not in actual_phone:
                    match = False
            
            if not match:
                tree.detach(child)
    
    def sort_treeview(col, reverse):
        """Sort treeview by column"""
        data = [(tree.set(child, col), child) for child in tree.get_children()]
        
        # Sort alphabetically
        data.sort(reverse=reverse)
        
        for index, (_, child) in enumerate(data):
            tree.move(child, '', index)
        
        # Reverse sort direction for next time
        tree.heading(col, command=lambda: sort_treeview(col, not reverse))
    
    def go_back():
        """Go back to previous window"""
        root.destroy()
        if parent_window:
            parent_window.deiconify()
    
    # Create the main window
    root = tk.Toplevel() if parent_window else tk.Tk()
    root.title("SPOTLIGHT AGENCY - Customer Search")
    root.geometry("800x500")  # Wider for more columns
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
                        bg="#757575",
                        fg="white",
                        activebackground="#616161",
                        width=10,
                        height=1,
                        command=go_back)
    back_btn.pack(side="right", padx=5, pady=5)
    
    # Title
    title_label = tk.Label(main_frame, text="CUSTOMER SEARCH", 
                          font=("Helvetica", 20, "bold"),
                          fg="white",
                          bg="#152e41")
    title_label.pack(pady=(0, 20))
    
    # Top button frame (Search, View Selected, Delete Selected)
    top_button_frame = tk.Frame(main_frame, bg="#152e41")
    top_button_frame.pack(pady=(0, 15))
    
    # Search button
    search_btn = tk.Button(top_button_frame, text="SEARCH",
                          font=("Helvetica", 12, "bold"),
                          bg="#8A8A8A",
                          fg="white",
                          activebackground="#A3A3A3",
                          width=15,
                          height=2,
                          command=open_search_window)
    search_btn.pack(side="left", padx=5)
    
    # View Selected button
    view_btn = tk.Button(top_button_frame, text="VIEW SELECTED",
                        font=("Helvetica", 11, "bold"),
                        bg="#8A8A8A",
                        fg="white",
                        activebackground="#A3A3A3",
                        width=15,
                        height=2,
                        state="disabled",
                        command=view_selected_customer)
    view_btn.pack(side="left", padx=5)
    
    # Delete Selected button
    delete_btn = tk.Button(top_button_frame, text="DELETE SELECTED",
                          font=("Helvetica", 11, "bold"),
                          bg="#8A8A8A",
                          fg="white",
                          activebackground="#A3A3A3",
                          width=15,
                          height=2,
                          state="disabled",
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
    columns = ("First Name", "Surname", "Phone")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    
    # Define headings with clickable sorting
    tree.heading("First Name", text="First Name", 
                 command=lambda: sort_treeview(0, False))
    tree.heading("Surname", text="Surname", 
                 command=lambda: sort_treeview(1, False))
    tree.heading("Phone", text="Phone", 
                 command=lambda: sort_treeview(2, False))
    
    # Define columns
    tree.column("First Name", width=150, anchor="w")
    tree.column("Surname", width=150, anchor="w")
    tree.column("Phone", width=150, anchor="w")
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Set hover colors
    search_btn.normal_color = "#8A8A8A"
    search_btn.hover_color = "#A3A3A3"
    
    view_btn.normal_color = "#8A8A8A"
    view_btn.hover_color = "#A3A3A3"
    
    delete_btn.normal_color = "#8A8A8A"
    delete_btn.hover_color = "#A3A3A3"
    
    back_btn.normal_color = "#757575"
    back_btn.hover_color = "#616161"
    
    # Setup hover effects
    setup_hover_effects()
    
    # Bind selection event
    tree.bind("<<TreeviewSelect>>", on_item_select)
    
    # Load initial data
    load_customer_data()
    
    if not parent_window:
        root.mainloop()

def SearchWindow(parent_window, apply_callback):
    """Popup Search window - 650x500"""
    
    def perform_search():
        """Perform search and close window"""
        firstname = firstname_entry.get().strip()
        surname = surname_entry.get().strip()
        phone = phone_entry.get().strip()
        
        # Apply search to main window
        apply_callback(firstname, surname, phone)
        
        # Close search window
        search_root.destroy()
    
    def clear_and_close():
        """Clear search and close window"""
        apply_callback("", "", "")  # Clear filter
        search_root.destroy()
    
    # Create search window
    search_root = tk.Toplevel(parent_window)
    search_root.title("SPOTLIGHT AGENCY - Customer Search")
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
    
    # Title
    title_label = tk.Label(main_frame, text="CUSTOMER SEARCH", 
                          font=("Helvetica", 24, "bold"),
                          fg="white",
                          bg="#152e41")
    title_label.pack(pady=(0, 30))
    
    # Search criteria frame
    criteria_frame = tk.Frame(main_frame, bg="#152e41")
    criteria_frame.pack(pady=20)
    
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
    firstname_label = tk.Label(criteria_frame, text="FIRST NAME", **label_style)
    firstname_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    firstname_entry = tk.Entry(criteria_frame, **entry_style)
    firstname_entry.grid(row=1, column=0, pady=(0, 20), ipady=5)
    
    # Surname
    surname_label = tk.Label(criteria_frame, text="SURNAME", **label_style)
    surname_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
    
    surname_entry = tk.Entry(criteria_frame, **entry_style)
    surname_entry.grid(row=3, column=0, pady=(0, 20), ipady=5)
    
    # Phone (with +41 hint)
    phone_label = tk.Label(criteria_frame, text="PHONE (+41)", **label_style)
    phone_label.grid(row=4, column=0, sticky="w", pady=(0, 5))
    
    phone_entry = tk.Entry(criteria_frame, **entry_style)
    phone_entry.grid(row=5, column=0, pady=(0, 30), ipady=5)
    
    # Button frame
    button_frame = tk.Frame(main_frame, bg="#152e41")
    button_frame.pack(pady=20)
    
    search_btn = tk.Button(button_frame, text="SEARCH",
                          font=("Helvetica", 14, "bold"),
                          bg="#8A8A8A",
                          fg="white",
                          activebackground="#A3A3A3",
                          width=20,
                          height=2,
                          command=perform_search)
    search_btn.pack(pady=10)
    
    clear_btn = tk.Button(button_frame, text="CLEAR",
                         font=("Helvetica", 14, "bold"),
                         bg="#8A8A8A",
                         fg="white",
                         activebackground="#A3A3A3",
                         width=20,
                         height=2,
                         command=clear_and_close)
    clear_btn.pack(pady=10)
    
    # Set hover colors
    search_btn.normal_color = "#8A8A8A"
    search_btn.hover_color = "#A3A3A3"
    
    clear_btn.normal_color = "#8A8A8A"
    clear_btn.hover_color = "#A3A3A3"
    
    # Setup hover effects
    search_btn.bind("<Enter>", lambda e: search_btn.config(bg="#A3A3A3"))
    search_btn.bind("<Leave>", lambda e: search_btn.config(bg="#8A8A8A"))
    clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg="#A3A3A3"))
    clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg="#8A8A8A"))
    
    # Bind Enter key to search
    firstname_entry.bind('<Return>', lambda e: perform_search())
    surname_entry.bind('<Return>', lambda e: perform_search())
    phone_entry.bind('<Return>', lambda e: perform_search())
    
    # Make window modal
    search_root.transient(parent_window)
    search_root.grab_set()
    search_root.focus_set()
    
    # Focus on first entry
    firstname_entry.focus_set()

# For testing directly
if __name__ == "__main__":
    CustomerView()