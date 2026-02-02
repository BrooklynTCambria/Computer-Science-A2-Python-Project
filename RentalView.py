# RentalView.py - Updated with fix for tag indexing
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import database_schema as db

def center_window(window, width=650, height=500):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def RentalView(parent_window=None):
    """Main Rental View window"""
    
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
    
    def load_rental_data():
        """Load rental data from database"""
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
        """Delete selected reservation"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a reservation to delete.")
            return
        
        item = tree.item(selected[0])
        
        # Check if item has tags
        if not item['tags']:
            messagebox.showerror("Error", "Cannot delete this item - missing rental ID.")
            return
            
        rental_id = int(item['tags'][0])
        reservation_info = item['values'][0]
        customer_name = item['values'][1]
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete reservation:\n\n{customer_name}\n{reservation_info}"
        )
        
        if confirm:
            # Delete from database
            rentals = db.load_rentals()
            rentals = [r for r in rentals if r.rental_id != rental_id]
            db.save_rentals(rentals)
            
            # Update treeview
            tree.delete(selected[0])
            messagebox.showinfo("Success", "Reservation deleted successfully.")
            delete_btn.config(state="disabled")
            view_btn.config(state="disabled")
            count_label.config(text="0 SELECTED")
    
    def open_search_window():
        """Open Search window"""
        SearchWindow(root, apply_search_filter)
    
    def view_selected_list():
        """View details of selected reservation"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a reservation to view.")
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
            messagebox.showerror("Error", "Reservation not found!")
            return
        
        # Find customer
        customer = None
        for c in customers:
            if c.customer_id == rental.customer_id:
                customer = c
                break
        
        # Build details string
        details = f"RESERVATION DETAILS\n\n"
        details += f"Reservation ID: {rental.rental_id}\n"
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
        
        messagebox.showinfo("Reservation Details", details)
    
    def apply_search_filter(firstname_filter, lastname_filter, date_filter, employee_filter):
        """Apply search filter to the treeview"""
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
        """Go back to previous window"""
        root.destroy()
        if parent_window:
            parent_window.deiconify()
    
    # Create the main window
    root = tk.Toplevel() if parent_window else tk.Tk()
    root.title("SPOTLIGHT AGENCY - Reservation Search")
    root.geometry("800x500")  # Wider for more columns
    root.resizable(False, False)
    center_window(root, 800, 500)
    
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
    title_label = tk.Label(main_frame, text="RESERVATION SEARCH", 
                          font=("Helvetica", 20, "bold"),
                          fg="black",
                          bg="#f0f0f0")
    title_label.pack(pady=(0, 20))
    
    # Top button frame (Search, View Selected, Delete Selected)
    top_button_frame = tk.Frame(main_frame, bg="#f0f0f0")
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
    
    # View Selected List button
    view_btn = tk.Button(top_button_frame, text="VIEW SELECTED LIST",
                        font=("Helvetica", 11, "bold"),
                        bg="#8A8A8A",
                        fg="white",
                        activebackground="#A3A3A3",
                        width=15,
                        height=2,
                        state="disabled",
                        command=view_selected_list)
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
                          bg="#f0f0f0",
                          fg="black")
    count_label.pack(side="right", padx=20)
    
    # Treeview frame with scrollbar
    tree_frame = tk.Frame(main_frame, bg="#f0f0f0")
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
    load_rental_data()
    
    if not parent_window:
        root.mainloop()

def SearchWindow(parent_window, apply_callback):
    """Popup Search window - 650x500"""
    
    def perform_search():
        """Perform search and close window"""
        firstname = firstname_entry.get().strip()
        lastname = lastname_entry.get().strip()
        date = date_entry.get().strip()
        employee = employee_entry.get().strip()
        
        # Apply search to main window
        apply_callback(firstname, lastname, date, employee)
        
        # Close search window
        search_root.destroy()
    
    def clear_and_close():
        """Clear search and close window"""
        apply_callback("", "", "", "")  # Clear filter
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
    search_root.configure(bg="#f0f0f0")
    
    # Main container frame
    main_frame = tk.Frame(search_root, bg="#f0f0f0")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Title
    title_label = tk.Label(main_frame, text="SEARCH", 
                          font=("Helvetica", 24, "bold"),
                          fg="black",
                          bg="#f0f0f0")
    title_label.pack(pady=(0, 30))
    
    # Search criteria frame
    criteria_frame = tk.Frame(main_frame, bg="#f0f0f0")
    criteria_frame.pack(pady=20)
    
    # Style for labels
    label_style = {
        "font": ("Helvetica", 12),
        "bg": "#f0f0f0",
        "fg": "black",
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
    button_frame = tk.Frame(main_frame, bg="#f0f0f0")
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
    lastname_entry.bind('<Return>', lambda e: perform_search())
    date_entry.bind('<Return>', lambda e: perform_search())
    employee_entry.bind('<Return>', lambda e: perform_search())
    
    # Make window modal
    search_root.transient(parent_window)
    search_root.grab_set()
    search_root.focus_set()
    
    # Focus on first entry
    firstname_entry.focus_set()

# For testing directly
if __name__ == "__main__":
    RentalView()