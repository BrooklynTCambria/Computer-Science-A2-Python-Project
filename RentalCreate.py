# RentalCreate.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import database_schema as db

def center_window(window, width=650, height=500):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

class AutofillWindow:
    def __init__(self, parent, customers, callback):
        self.parent = parent
        self.customers = customers
        self.callback = callback
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Select Customer")
        self.window.geometry("400x300")
        self.window.configure(bg="#152e41")
        self.window.resizable(False, False)
        
        # Center window
        self.window.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (300 // 2)
        self.window.geometry(f"400x300+{x}+{y}")
        
        # Title
        title_label = tk.Label(self.window, text="Select Customer",
                              font=("Helvetica", 14, "bold"),
                              bg="#152e41")
        title_label.pack(pady=10)
        
        # Listbox for customers
        self.listbox = tk.Listbox(self.window, height=10, font=("Helvetica", 11))
        self.listbox.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(self.listbox)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        
        # Populate listbox
        for customer in customers:
            self.listbox.insert(tk.END, f"{customer.fullname} - {customer.phone}")
        
        # Button frame
        button_frame = tk.Frame(self.window, bg="#152e41")
        button_frame.pack(pady=10)
        
        # Select button
        select_btn = tk.Button(button_frame, text="SELECT",
                              font=("Helvetica", 10, "bold"),
                              bg="#8acbcb",
                              fg="white",
                              width=10,
                              command=self.select_customer)
        select_btn.pack(side="left", padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(button_frame, text="CANCEL",
                              font=("Helvetica", 10, "bold"),
                              bg="#8acbcb",
                              fg="white",
                              width=10,
                              command=self.window.destroy)
        cancel_btn.pack(side="left", padx=5)
        
        # Bind double-click and Enter key
        self.listbox.bind("<Double-Button-1>", lambda e: self.select_customer())
        self.listbox.bind("<Return>", lambda e: self.select_customer())
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_set()
        
        # Focus on listbox
        self.listbox.focus_set()
        if customers:
            self.listbox.selection_set(0)
    
    def select_customer(self):
        selection = self.listbox.curselection()
        if selection:
            selected_customer = self.customers[selection[0]]
            self.callback(selected_customer)
            self.window.destroy()

class RentalCreate:
    def __init__(self, parent_window=None, employee="admin"):
        self.parent_window = parent_window
        self.employee = employee
        self.selected_items = {}  # item_id: quantity
        self.root = None
        self.create_window()
    
    def create_window(self):
        # Create the window
        self.root = tk.Toplevel() if self.parent_window else tk.Tk()
        self.root.title("SPOTLIGHT AGENCY - Rental Creation")
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
        
        if not self.parent_window:
            self.root.mainloop()
    
    def setup_hover_effects(self):
        def on_enter(e):
            if hasattr(e.widget, 'hover_color'):
                e.widget.config(bg=e.widget.hover_color)
        
        def on_leave(e):
            if hasattr(e.widget, 'normal_color'):
                e.widget.config(bg=e.widget.normal_color)
        
        buttons = [self.back_btn, self.add_btn, self.remove_btn, self.create_btn, 
                  self.autofill_btn, self.clear_btn]
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
        title_label = tk.Label(main_frame, text="RENTAL CREATION", 
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
        
        # Bottom frame for buttons and total
        bottom_frame = tk.Frame(main_frame, bg="#152e41")
        bottom_frame.pack(fill="x", pady=(10, 0))
        
        # Left side - Clear button and Total label
        left_bottom_frame = tk.Frame(bottom_frame, bg="#152e41")
        left_bottom_frame.pack(side="left", fill="x", expand=True)
        
        # Clear button
        self.clear_btn = tk.Button(left_bottom_frame, text="CLEAR ALL ITEMS",
                                  font=("Helvetica", 10, "bold"),
                                  bg="#8acbcb",
                                  fg="white",
                                  activebackground="#7db6b6",
                                  width=15,
                                  height=1,
                                  command=self.clear_items)
        self.clear_btn.pack(side="left", padx=(0, 20))
        
        # Total label
        self.total_label = tk.Label(left_bottom_frame, text="TOTAL: £0.00",
                                   font=("Helvetica", 14, "bold"),
                                   bg="#152e41",
                                   fg="white")
        self.total_label.pack(side="left")
        
        # Create button
        self.create_btn = tk.Button(bottom_frame, text="CREATE",
                                   font=("Helvetica", 12, "bold"),
                                   bg="#8acbcb",
                                   fg="white",
                                   activebackground="#7db6b6",
                                   width=15,
                                   height=2,
                                   command=self.confirm_create_rental)
        self.create_btn.pack(side="right")
        
        # Set hover colors
        self.back_btn.normal_color = "#8acbcb"
        self.back_btn.hover_color = "#7db6b6"
        
        self.add_btn.normal_color = "#8acbcb"
        self.add_btn.hover_color = "#7db6b6"
        
        self.remove_btn.normal_color = "#8acbcb"
        self.remove_btn.hover_color = "#7db6b6"
        
        self.create_btn.normal_color = "#8acbcb"
        self.create_btn.hover_color = "#7db6b6"
        
        self.autofill_btn.normal_color = "#8acbcb"
        self.autofill_btn.hover_color = "#7db6b6"
        
        self.clear_btn.normal_color = "#8acbcb"
        self.clear_btn.hover_color = "#7db6b6"
        
        # Setup hover effects
        self.setup_hover_effects()
        
        # Bind Enter key to create confirmation
        self.root.bind('<Return>', lambda e: self.confirm_create_rental())
        
        # Focus on first entry
        self.firstname_entry.focus_set()
    
    def setup_customer_column(self, parent_frame):

        # Style for labels
        label_style = {
            "font": ("Helvetica", 11),
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
        self.firstname_entry.pack(pady=(0, 15), ipady=5)
        
        # Last Name
        lastname_label = tk.Label(parent_frame, text="LAST NAME", **label_style)
        lastname_label.pack(pady=(0, 5), anchor="w")
        
        self.lastname_entry = tk.Entry(parent_frame, **entry_style)
        self.lastname_entry.pack(pady=(0, 15), ipady=5)
        
        # Phone Number
        phone_label = tk.Label(parent_frame, text="PHONE NUMBER", **label_style)
        phone_label.pack(pady=(0, 5), anchor="w")
        
        self.phone_entry = tk.Entry(parent_frame, **entry_style)
        self.phone_entry.pack(pady=(0, 20), ipady=5)
        
        # AUTO FILL Button - ALWAYS ENABLED
        self.autofill_btn = tk.Button(parent_frame, text="AUTO FILL",
                                     font=("Helvetica", 11, "bold"),
                                     bg="#8acbcb",
                                     fg="white",
                                     width=15,
                                     height=1,
                                     command=self.show_autofill)
        self.autofill_btn.pack(pady=(10, 0))
    
    def setup_items_column(self, parent_frame):

        # Style for labels
        label_style = {
            "font": ("Helvetica", 11),
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
                              fg="white",
                              bg="#152e41")
        start_label.pack(side="left", padx=(0, 5))
        
        # Create start date picker - cannot select dates before today
        today = datetime.now()
        self.start_date_entry = DateEntry(dates_frame, 
                                         width=12,
                                         background='darkblue',
                                         foreground='white',
                                         borderwidth=2,
                                         date_pattern='dd/mm/yyyy',
                                         mindate=today)
        self.start_date_entry.pack(side="left", padx=(0, 15))
        
        # End Date
        end_label = tk.Label(dates_frame, text="To:",
                            font=("Helvetica", 10),
                            fg="white",
                            bg="#152e41")
        end_label.pack(side="left", padx=(0, 5))
        
        # Create end date picker - set initial date to same as start date (today)
        self.end_date_entry = DateEntry(dates_frame,
                                       width=12,
                                       background='darkblue',
                                       foreground='white',
                                       borderwidth=2,
                                       date_pattern='dd/mm/yyyy',
                                       mindate=today)  # Set minimum to today
        self.end_date_entry.set_date(today)  # Set to same date as start
        self.end_date_entry.pack(side="left")
        
        # Bind start date selection to update end date minimum and set end date to same as start
        self.start_date_entry.bind("<<DateEntrySelected>>", self.on_start_date_selected)
        
        # Also bind to validate when user manually changes end date
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
        
        # Item dropdown
        self.items = db.load_items()
        item_names = [f"{item.name} - £{item.price:.2f} ({item.quantity} available)" 
                     for item in self.items]
        
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
                                 fg="white",
                                 bg="#152e41")
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
            
            # Set end date to the same as start date
            self.end_date_entry.set_date(start_date)
            
            # Set minimum date to start date
            self.end_date_entry.config(mindate=start_date)
            
            # Update total in case days changed
            self.update_total()
        except Exception as e:
            print(f"Error setting end date: {e}")
    
    def validate_end_date(self, event=None):
        try:
            start_date = self.start_date_entry.get_date()
            end_date = self.end_date_entry.get_date()
            
            # If end date is before start date, show error and reset to start date
            if end_date < start_date:
                messagebox.showwarning("Invalid Date", "End date cannot be before start date!")
                self.end_date_entry.set_date(start_date)
            
            # Update total in case days changed
            self.update_total()
        except Exception as e:
            print(f"Error validating end date: {e}")
    
    def show_autofill(self):
        firstname = self.firstname_entry.get().strip().lower()
        lastname = self.lastname_entry.get().strip().lower()
        
        # Load all customers
        all_customers = db.load_customers()
        
        # If no name is entered, show all customers
        if not firstname and not lastname:
            matching_customers = all_customers
        else:
            # Filter customers based on partial match in EITHER firstname OR lastname
            # But also consider what fields are filled
            matching_customers = []
            for customer in all_customers:
                customer_firstname = customer.firstname.lower()
                customer_lastname = customer.surname.lower()
                
                # Initialize matches
                firstname_match = False
                lastname_match = False
                
                # Check firstname if user entered something in firstname field
                if firstname:
                    firstname_match = firstname in customer_firstname
                else:
                    # If firstname field is empty, consider it a match for filtering purposes
                    firstname_match = True
                
                # Check lastname if user entered something in lastname field
                if lastname:
                    lastname_match = lastname in customer_lastname
                else:
                    # If lastname field is empty, consider it a match for filtering purposes
                    lastname_match = True
                
                # If user entered both fields, show customers matching BOTH (intelligent filtering)
                if firstname and lastname:
                    # Show customers where firstname matches OR lastname matches
                    if firstname_match or lastname_match:
                        matching_customers.append(customer)
                elif firstname and not lastname:
                    # Only firstname entered - show if firstname matches
                    if firstname_match:
                        matching_customers.append(customer)
                elif not firstname and lastname:
                    # Only lastname entered - show if lastname matches
                    if lastname_match:
                        matching_customers.append(customer)
                else:
                    # Neither field entered - should show all (handled above)
                    pass
        
        if not matching_customers:
            messagebox.showinfo("No Matches", "No matching customers found.")
            return
        
        # Show autofill window
        AutofillWindow(self.root, matching_customers, self.autofill_customer)
    
    def autofill_customer(self, customer):
        self.firstname_entry.delete(0, tk.END)
        self.firstname_entry.insert(0, customer.firstname)
        
        self.lastname_entry.delete(0, tk.END)
        self.lastname_entry.insert(0, customer.surname)
        
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, customer.phone)
        
        # Focus on item dropdown
        self.item_dropdown.focus_set()
    
    def add_item(self):
        selected_index = self.item_dropdown.current()
        if selected_index == -1:
            messagebox.showwarning("No Selection", "Please select an item from the dropdown.")
            return
        
        # Get selected item
        selected_item = self.items[selected_index]
        quantity = int(self.quantity_var.get())
        
        # Check availability
        if quantity > selected_item.quantity:
            messagebox.showerror("Insufficient Stock", 
                               f"Only {selected_item.quantity} {selected_item.name} available.")
            return
        
        # Add to selected items
        if selected_item.item_id in self.selected_items:
            # Update quantity if item already exists
            self.selected_items[selected_item.item_id] += quantity
            
            # Update display - find and update the existing entry
            for i in range(self.selected_listbox.size()):
                item_text = self.selected_listbox.get(i)
                if selected_item.name in item_text:
                    # Extract current quantity and update
                    if "x" in item_text:
                        parts = item_text.split("x")
                        current_qty = int(parts[1].split()[0])
                        new_qty = current_qty + quantity
                        new_text = f"{selected_item.name} x{new_qty} - £{selected_item.price * new_qty:.2f}"
                        self.selected_listbox.delete(i)
                        self.selected_listbox.insert(i, new_text)
                    break
        else:
            # Add new item
            self.selected_items[selected_item.item_id] = quantity
            display_text = f"{selected_item.name} x{quantity} - £{selected_item.price * quantity:.2f}"
            self.selected_listbox.insert(tk.END, display_text)
        
        self.update_total()
        
        # DON'T clear the dropdown selection - keep it selected
        # Only reset quantity to 1 for next addition
        self.quantity_var.set("1")
    
    def remove_item(self):

        selection = self.selected_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item to remove.")
            return
        
        index = selection[0]
        item_text = self.selected_listbox.get(index)
        
        # Find which item this is
        for item in self.items:
            if item.name in item_text:
                if item.item_id in self.selected_items:
                    del self.selected_items[item.item_id]
                    break
        
        self.selected_listbox.delete(index)
        self.update_total()
    
    def clear_items(self):
        if not self.selected_items:
            messagebox.showinfo("No Items", "There are no items to clear.")
            return
        
        confirm = messagebox.askyesno("Clear Items", 
                                     "Are you sure you want to clear all items from this rental?")
        
        if confirm:
            self.selected_items.clear()
            self.selected_listbox.delete(0, tk.END)
            self.update_total()
            messagebox.showinfo("Items Cleared", "All items have been removed from the rental.")
    
    def update_total(self):
        total = 0.0
        
        for item_id, quantity in self.selected_items.items():
            for item in self.items:
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
    
    def confirm_create_rental(self):
        # Get customer details
        firstname = self.firstname_entry.get().strip()
        lastname = self.lastname_entry.get().strip()
        phone = self.phone_entry.get().strip()
        
        # Basic validation
        if not firstname:
            self.show_error("First name is required!")
            self.firstname_entry.focus_set()
            return
        
        if not lastname:
            self.show_error("Last name is required!")
            self.lastname_entry.focus_set()
            return
        
        if not phone:
            self.show_error("Phone number is required!")
            self.phone_entry.focus_set()
            return
        
        if not self.selected_items:
            self.show_error("Please add at least one item!")
            self.item_dropdown.focus_set()
            return
        
        # Get dates
        try:
            start_date = self.start_date_entry.get_date()
            end_date = self.end_date_entry.get_date()
            
            if end_date < start_date:
                self.show_error("End date must be after start date!")
                return
            
            days = (end_date - start_date).days + 1
        except Exception as e:
            self.show_error(f"Invalid date: {str(e)}")
            return
        
        # Calculate total for display
        total = 0.0
        item_details = []
        
        for item_id, quantity in self.selected_items.items():
            for item in self.items:
                if item.item_id == item_id:
                    item_total = item.price * quantity * days
                    total += item_total
                    item_details.append(f"  • {item.name} x{quantity}: £{item_total:.2f}")
                    break
        
        # Create confirmation message
        confirmation = f"CREATE RENTAL WITH:\n\n"
        confirmation += f"Customer: {firstname} {lastname}\n"
        confirmation += f"Phone: {phone}\n"
        confirmation += f"Dates: {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}\n"
        confirmation += f"Duration: {days} day{'s' if days != 1 else ''}\n"
        confirmation += f"Total: £{total:.2f}\n\n"
        confirmation += "Items:\n" + "\n".join(item_details)
        
        # Show confirmation dialog
        confirm = messagebox.askyesno("Confirm Rental Creation", confirmation)
        
        if confirm:
            self.create_rental()
    
    def create_rental(self):
        # Get customer details
        firstname = self.firstname_entry.get().strip()
        lastname = self.lastname_entry.get().strip()
        phone = self.phone_entry.get().strip()
        
        # Get dates
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        days = (end_date - start_date).days + 1
        
        # Check if customer exists, if not create new
        customers = db.load_customers()
        customer_id = None
        
        for customer in customers:
            if (customer.firstname.lower() == firstname.lower() and 
                customer.surname.lower() == lastname.lower() and 
                customer.phone == phone):
                customer_id = customer.customer_id
                break
        
        if customer_id is None:
            # Create new customer
            customer_id = db.get_next_customer_id()
            new_customer = db.Customer(customer_id, firstname, lastname, phone)
            customers.append(new_customer)
            db.save_customers(customers)
        
        # Calculate total and update item quantities
        total = 0.0
        item_details = []
        
        for item_id, quantity in self.selected_items.items():
            for item in self.items:
                if item.item_id == item_id:
                    item_total = item.price * quantity * days
                    total += item_total
                    item_details.append(f"- {item.name} x{quantity}: £{item_total:.2f}")
                    
                    # Update item quantity
                    item.quantity -= quantity
                    break
        
        # Save updated items
        db.save_items(self.items)
        
        # Create rental
        rental_id = db.get_next_rental_id()
        rental = db.Rental(rental_id, customer_id, self.employee, 
                          start_date, end_date, self.selected_items, total)
        
        # Save rental
        rentals = db.load_rentals()
        rentals.append(rental)
        db.save_rentals(rentals)
        
        # Show success message
        success_msg = f"Rental Created Successfully!\n\n"
        success_msg += f"Rental ID: {rental_id}\n"
        success_msg += f"Customer: {firstname} {lastname}\n"
        success_msg += f"Phone: {phone}\n"
        success_msg += f"Dates: {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}\n"
        success_msg += f"Duration: {days} day{'s' if days != 1 else ''}\n"
        success_msg += f"Total: £{total:.2f}\n\n"
        success_msg += "Items:\n" + "\n".join(item_details)
        
        messagebox.showinfo("Success", success_msg)
        
        # Clear form for next entry
        self.clear_form()
    
    def show_error(self, message):
        messagebox.showerror("Error", message)
    
    def clear_form(self):
        # Clear customer details
        self.firstname_entry.delete(0, tk.END)
        self.lastname_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        
        # Set default dates (today to today)
        today = datetime.now()
        self.start_date_entry.set_date(today)
        self.end_date_entry.set_date(today)
        self.end_date_entry.config(mindate=today)  # Reset minimum date
        
        # Clear selected items
        self.selected_items.clear()
        self.selected_listbox.delete(0, tk.END)
        
        # Reset quantity but DON'T clear dropdown selection
        self.quantity_var.set("1")
        
        # Update total
        self.total_label.config(text="TOTAL: £0.00")
        
        # Focus on first name
        self.firstname_entry.focus_set()
        
        # Reload items (quantities may have changed)
        self.items = db.load_items()
        item_names = [f"{item.name} - £{item.price:.2f} ({item.quantity} available)" 
                     for item in self.items]
        self.item_dropdown['values'] = item_names
        
        # Reset dropdown selection
        self.item_dropdown.set('')
    
    def go_back(self):
        self.root.destroy()
        if self.parent_window:
            self.parent_window.deiconify()

def RentalCreation(parent_window=None, employee="admin"):
    return RentalCreate(parent_window, employee)

# For testing directly
if __name__ == "__main__":
    RentalCreate()