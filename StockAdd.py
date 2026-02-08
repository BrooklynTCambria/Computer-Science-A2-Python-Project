# StockAdd.py
import tkinter as tk
from tkinter import ttk, messagebox
import database_schema as db

def center_window(window, width=650, height=500):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

class StockAdd:
    def __init__(self, parent_window=None):
        self.parent_window = parent_window
        self.root = None
        self.items = []
        self.current_item_id = None
        self.create_window()
    
    def create_window(self):
        """Create the Stock Add window"""
        # Create the window
        self.root = tk.Toplevel() if self.parent_window else tk.Tk()
        self.root.title("SPOTLIGHT AGENCY - Stock Add")
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
        """Setup hover effects for buttons"""
        def on_enter(e):
            if hasattr(e.widget, 'hover_color'):
                e.widget.config(bg=e.widget.hover_color)
        
        def on_leave(e):
            if hasattr(e.widget, 'normal_color'):
                e.widget.config(bg=e.widget.normal_color)
        
        buttons = [self.back_btn, self.restock_btn, self.delete_btn, self.add_item_btn]
        for btn in buttons:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container frame
        main_frame = tk.Frame(self.root, bg="#152e41")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # TOP FRAME for BACK button (top right)
        top_frame = tk.Frame(main_frame, bg="#152e41")
        top_frame.pack(fill="x", pady=(0, 10))
        
        # BACK Button in top right corner
        self.back_btn = tk.Button(top_frame, text="BACK", 
                                font=("Helvetica", 12, "bold"),
                                bg="#757575",
                                fg="white",
                                activebackground="#616161",
                                width=10,
                                height=1,
                                command=self.go_back)
        self.back_btn.pack(side="right", padx=5, pady=5)
        
        # Title
        title_label = tk.Label(main_frame, text="STOCK ADD", 
                              font=("Helvetica", 20, "bold"),
                              fg="white",
                              bg="#152e41")
        title_label.pack(pady=(0, 30))
        
        # STOCK ITEM Frame
        stock_frame = tk.Frame(main_frame, bg="#152e41")
        stock_frame.pack(pady=(0, 30))
        
        # STOCK ITEM label
        stock_label = tk.Label(stock_frame, text="STOCK ITEM", 
                              font=("Helvetica", 16, "bold"),
                              fg="white",
                              bg="#152e41")
        stock_label.pack(pady=(0, 10))
        
        # Item dropdown
        self.items = db.load_items()
        # Sort items by name
        self.items.sort(key=lambda x: x.name.lower())
        item_names = [f"{item.name} ({item.quantity} available)" for item in self.items]
        
        self.item_var = tk.StringVar()
        self.item_dropdown = ttk.Combobox(stock_frame,
                                         textvariable=self.item_var,
                                         values=item_names,
                                         state="readonly",
                                         width=40,
                                         font=("Helvetica", 12))
        self.item_dropdown.pack(pady=(0, 5))
        
        # Bind selection event
        self.item_dropdown.bind("<<ComboboxSelected>>", self.on_item_selected)
        
        # AMOUNT Frame
        amount_frame = tk.Frame(main_frame, bg="#152e41")
        amount_frame.pack(pady=(0, 30))
        
        # AMOUNT label
        amount_label = tk.Label(amount_frame, text="AMOUNT", 
                               font=("Helvetica", 16, "bold"),
                               fg="white",
                               bg="#152e41")
        amount_label.pack(pady=(0, 10))
        
        # Amount entry
        self.amount_var = tk.StringVar(value="1")
        self.amount_entry = tk.Entry(amount_frame,
                                    font=("Helvetica", 12),
                                    textvariable=self.amount_var,
                                    width=10,
                                    justify="center",
                                    bd=1,
                                    relief="solid",
                                    highlightthickness=1)
        self.amount_entry.pack(pady=(0, 5), ipady=5)
        
        # RESTOCK Button
        self.restock_btn = tk.Button(amount_frame, text="RESTOCK",
                                    font=("Helvetica", 14, "bold"),
                                    bg="#8A8A8A",
                                    fg="white",
                                    activebackground="#A3A3A3",
                                    width=20,
                                    height=2,
                                    command=self.restock_item)
        self.restock_btn.pack(pady=(10, 0))
        
        # Bottom button frame
        bottom_frame = tk.Frame(main_frame, bg="#152e41")
        bottom_frame.pack(fill="x", pady=(20, 0))
        
        # DELETE ITEM button (left side)
        self.delete_btn = tk.Button(bottom_frame, text="DELETE ITEM",
                                   font=("Helvetica", 12, "bold"),
                                   bg="#8A8A8A",
                                   fg="white",
                                   activebackground="#A3A3A3",
                                   width=15,
                                   height=2,
                                   command=self.delete_item)
        self.delete_btn.pack(side="left", padx=(0, 10))
        
        # ADD NEW ITEM button (right side)
        self.add_item_btn = tk.Button(bottom_frame, text="ADD NEW ITEM",
                                     font=("Helvetica", 12, "bold"),
                                     bg="#8A8A8A",
                                     fg="white",
                                     activebackground="#A3A3A3",
                                     width=15,
                                     height=2,
                                     command=self.open_add_item_window)
        self.add_item_btn.pack(side="right", padx=(10, 0))
        
        # Set hover colors
        self.back_btn.normal_color = "#757575"
        self.back_btn.hover_color = "#616161"
        
        self.restock_btn.normal_color = "#8A8A8A"
        self.restock_btn.hover_color = "#A3A3A3"
        
        self.delete_btn.normal_color = "#8A8A8A"
        self.delete_btn.hover_color = "#A3A3A3"
        
        self.add_item_btn.normal_color = "#8A8A8A"
        self.add_item_btn.hover_color = "#A3A3A3"
        
        # Setup hover effects
        self.setup_hover_effects()
        
        # Bind Enter key to restock
        self.amount_entry.bind('<Return>', lambda e: self.restock_item())
        
        # Select first item if available
        if self.items:
            self.item_dropdown.current(0)
            self.on_item_selected()
    
    def on_item_selected(self, event=None):
        """Handle item selection from dropdown"""
        selected_index = self.item_dropdown.current()
        if selected_index != -1 and selected_index < len(self.items):
            self.current_item_id = self.items[selected_index].item_id
    
    def restock_item(self):
        """Add stock to selected item"""
        if self.current_item_id is None:
            messagebox.showwarning("No Selection", "Please select a stock item first.")
            return
        
        # Get amount
        amount_str = self.amount_var.get().strip()
        if not amount_str:
            self.show_error("Amount is required!")
            self.amount_entry.focus_set()
            return
        
        try:
            amount = int(amount_str)
            if amount <= 0:
                self.show_error("Amount must be a positive number!")
                self.amount_entry.focus_set()
                return
        except ValueError:
            self.show_error("Amount must be a whole number!")
            self.amount_entry.focus_set()
            return
        
        # Find and update item
        for item in self.items:
            if item.item_id == self.current_item_id:
                old_quantity = item.quantity
                item.quantity += amount
                
                # Save to database
                db.save_items(self.items)
                
                # Update dropdown display
                selected_index = self.item_dropdown.current()
                new_display = f"{item.name} ({item.quantity} available)"
                
                # Update the item names list
                item_names = list(self.item_dropdown['values'])
                if selected_index < len(item_names):
                    item_names[selected_index] = new_display
                    self.item_dropdown['values'] = item_names
                    self.item_var.set(new_display)
                
                # Show success message
                messagebox.showinfo("Success", 
                                  f"Added {amount} to {item.name}\n"
                                  f"Old quantity: {old_quantity}\n"
                                  f"New quantity: {item.quantity}")
                
                # Reset amount entry
                self.amount_var.set("1")
                break
    
    def delete_item(self):
        """Delete selected item"""
        if self.current_item_id is None:
            messagebox.showwarning("No Selection", "Please select a stock item to delete.")
            return
        
        # Find the item
        selected_item = None
        for item in self.items:
            if item.item_id == self.current_item_id:
                selected_item = item
                break
        
        if not selected_item:
            messagebox.showerror("Error", "Selected item not found!")
            return
        
        # Check if item is used in any rentals
        rentals = db.load_rentals()
        item_in_use = False
        for rental in rentals:
            if selected_item.item_id in rental.items:
                item_in_use = True
                break
        
        if item_in_use:
            messagebox.showerror("Cannot Delete", 
                f"Cannot delete '{selected_item.name}' because it is currently rented or has rental history.\n"
                f"Consider reducing quantity to 0 instead.")
            return
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{selected_item.name}'?\n\n"
            f"This action cannot be undone."
        )
        
        if confirm:
            # Remove from list
            self.items = [item for item in self.items if item.item_id != self.current_item_id]
            
            # Save to database
            db.save_items(self.items)
            
            # Update dropdown
            item_names = [f"{item.name} ({item.quantity} available)" for item in self.items]
            self.item_dropdown['values'] = item_names
            
            if self.items:
                self.item_dropdown.current(0)
                self.on_item_selected()
            else:
                self.item_var.set("")
                self.current_item_id = None
            
            messagebox.showinfo("Success", f"'{selected_item.name}' has been deleted.")
    
    def open_add_item_window(self):
        """Open window to add new item"""
        AddItemWindow(self.root, self.on_new_item_added)
    
    def on_new_item_added(self, new_item):
        """Callback when a new item is added"""
        # Reload items
        self.items = db.load_items()
        self.items.sort(key=lambda x: x.name.lower())
        
        # Update dropdown
        item_names = [f"{item.name} ({item.quantity} available)" for item in self.items]
        self.item_dropdown['values'] = item_names
        
        # Find and select the new item
        for i, item in enumerate(self.items):
            if item.item_id == new_item.item_id:
                self.item_dropdown.current(i)
                self.current_item_id = item.item_id
                self.item_var.set(f"{item.name} ({item.quantity} available)")
                break
    
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)
    
    def go_back(self):
        """Go back to previous window"""
        self.root.destroy()
        if self.parent_window:
            self.parent_window.deiconify()

class AddItemWindow:
    """Window for adding a new item"""
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("SPOTLIGHT AGENCY - Add New Item")
        self.window.geometry("650x500")
        self.window.configure(bg="#152e41")
        self.window.resizable(False, False)
        center_window(self.window, 650, 500)
        
        # Set icon
        try:
            self.window.iconphoto(False, tk.PhotoImage(file="icon.png"))
        except:
            pass
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container frame
        main_frame = tk.Frame(self.window, bg="#152e41")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="ADD NEW ITEM", 
                              font=("Helvetica", 20, "bold"),
                              fg="white",
                              bg="#152e41")
        title_label.pack(pady=(0, 15))
        
        # Form frame
        form_frame = tk.Frame(main_frame, bg="#152e41")
        form_frame.pack(pady=20)
        
        # Style for labels
        label_style = {
            "font": ("Helvetica", 14, "bold"),
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
        
        # ITEM NAME
        item_name_label = tk.Label(form_frame, text="ITEM NAME", **label_style)
        item_name_label.grid(row=0, column=0, sticky="w", pady=(0, 6))
        
        self.item_name_entry = tk.Entry(form_frame, **entry_style)
        self.item_name_entry.grid(row=1, column=0, pady=(0, 30), ipady=5)
        
        # RENT PRICE
        price_label = tk.Label(form_frame, text="RENT PRICE (£)", **label_style)
        price_label.grid(row=2, column=0, sticky="w", pady=(0, 6))
        
        self.price_entry = tk.Entry(form_frame, **entry_style)
        self.price_entry.grid(row=3, column=0, pady=(0, 30), ipady=5)
        
        # AMOUNT
        amount_label = tk.Label(form_frame, text="AMOUNT", **label_style)
        amount_label.grid(row=4, column=0, sticky="w", pady=(0, 6))
        
        self.amount_entry = tk.Entry(form_frame, **entry_style)
        self.amount_entry.grid(row=5, column=0, pady=(0, 30), ipady=5)
        
        # ITEM TYPE (Optional but good to have)
        type_label = tk.Label(form_frame, text="ITEM TYPE", 
                             font=("Helvetica", 12, "bold"),
                             bg="#152e41",
                             fg="white",
                             anchor="w")
        type_label.grid(row=6, column=0, sticky="w", pady=(0, 6))
        
        self.type_entry = tk.Entry(form_frame, 
                                  font=("Helvetica", 12),
                                  width=30,
                                  bd=1,
                                  relief="solid",
                                  highlightthickness=1)
        self.type_entry.grid(row=7, column=0, pady=(0, 30), ipady=5)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg="#152e41")
        button_frame.pack(pady=20)
        
        # ADD button
        add_btn = tk.Button(button_frame, text="ADD",
                           font=("Helvetica", 14, "bold"),
                           bg="#8A8A8A",
                           fg="white",
                           activebackground="#A3A3A3",
                           width=20,
                           height=2,
                           command=self.add_item)
        add_btn.pack(side="left", padx=10)
        
        # BACK button
        back_btn = tk.Button(button_frame, text="BACK",
                            font=("Helvetica", 14, "bold"),
                            bg="#8A8A8A",
                            fg="white",
                            activebackground="#A3A3A3",
                            width=20,
                            height=2,
                            command=self.window.destroy)
        back_btn.pack(side="left", padx=10)
        
        # Set hover colors
        add_btn.normal_color = "#8A8A8A"
        add_btn.hover_color = "#A3A3A3"
        
        back_btn.normal_color = "#8A8A8A"
        back_btn.hover_color = "#A3A3A3"
        
        # Setup hover effects
        add_btn.bind("<Enter>", lambda e: add_btn.config(bg="#A3A3A3"))
        add_btn.bind("<Leave>", lambda e: add_btn.config(bg="#8A8A8A"))
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#A3A3A3"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#8A8A8A"))
        
        # Bind Enter key to add item
        self.item_name_entry.bind('<Return>', lambda e: self.add_item())
        self.price_entry.bind('<Return>', lambda e: self.add_item())
        self.amount_entry.bind('<Return>', lambda e: self.add_item())
        self.type_entry.bind('<Return>', lambda e: self.add_item())
        
        # Make window modal
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.focus_set()
        
        # Focus on first entry
        self.item_name_entry.focus_set()
    
    def add_item(self):
        """Add new item to database"""
        # Get values
        item_name = self.item_name_entry.get().strip()
        price_str = self.price_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        item_type = self.type_entry.get().strip()
        
        # Validate input
        if not item_name:
            self.show_error("Item name is required!")
            self.item_name_entry.focus_set()
            return
        
        if not price_str:
            self.show_error("Rent price is required!")
            self.price_entry.focus_set()
            return
        
        try:
            price = float(price_str)
            if price <= 0:
                self.show_error("Rent price must be a positive number!")
                self.price_entry.focus_set()
                return
        except ValueError:
            self.show_error("Rent price must be a number!")
            self.price_entry.focus_set()
            return
        
        if not amount_str:
            self.show_error("Amount is required!")
            self.amount_entry.focus_set()
            return
        
        try:
            amount = int(amount_str)
            if amount < 0:
                self.show_error("Amount cannot be negative!")
                self.amount_entry.focus_set()
                return
        except ValueError:
            self.show_error("Amount must be a whole number!")
            self.amount_entry.focus_set()
            return
        
        # Check if item with same name already exists
        existing_items = db.load_items()
        for item in existing_items:
            if item.name.lower() == item_name.lower():
                response = messagebox.askyesno(
                    "Item Exists",
                    f"An item named '{item.name}' already exists.\n"
                    f"Do you want to restock it instead?"
                )
                if response:
                    self.window.destroy()
                    return
                else:
                    messagebox.showinfo("Information", 
                                      "Please choose a different name for the new item.")
                    self.item_name_entry.focus_set()
                    return
        
        # Create new item
        item_id = db.get_next_item_id()
        new_item = db.Item(item_id, item_name, item_type, amount, price)
        
        # Save to database
        existing_items.append(new_item)
        db.save_items(existing_items)
        
        # Show success message
        messagebox.showinfo("Success", 
                          f"New item added successfully!\n\n"
                          f"Item: {item_name}\n"
                          f"Type: {item_type if item_type else 'Not specified'}\n"
                          f"Price: £{price:.2f}\n"
                          f"Quantity: {amount}")
        
        # Callback to parent window
        self.callback(new_item)
        
        # Close window
        self.window.destroy()
    
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)

def StockAddWindow(parent_window=None):
    """Wrapper function to create StockAdd instance"""
    return StockAdd(parent_window)

# For testing directly
if __name__ == "__main__":
    StockAdd()