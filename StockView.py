# StockView.py
import tkinter as tk
from tkinter import ttk, messagebox
import database_schema as db

def center_window(window, width=650, height=500):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def StockView(parent_window=None):
    """Main Stock View window"""
    
    def setup_hover_effects():
        """Setup hover effects for buttons"""
        def on_enter(e):
            if hasattr(e.widget, 'hover_color'):
                e.widget.config(bg=e.widget.hover_color)
        
        def on_leave(e):
            if hasattr(e.widget, 'normal_color'):
                e.widget.config(bg=e.widget.normal_color)
        
        buttons = [search_btn, delete_btn, back_btn]
        for btn in buttons:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def load_stock_data():
        """Load stock data from database"""
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)
        
        # Load items
        items = db.load_items()
        
        # Sort by name (you can change this to other columns)
        items.sort(key=lambda x: x.name.lower())
        
        # Add item data with tags
        for item in items:
            # Insert with item ID as tag
            tree.insert("", "end", 
                       values=(item.name, item.type, f"£{item.price:.2f}", item.quantity),
                       tags=(str(item.item_id),))
    
    def on_item_select(event):
        """Handle item selection"""
        selected = tree.selection()
        if selected:
            delete_btn.config(state="normal")
            # Update selected count
            count_label.config(text=f"{len(selected)} SELECTED")
        else:
            delete_btn.config(state="disabled")
            count_label.config(text="0 SELECTED")
    
    def delete_selected():
        """Delete selected stock item"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a stock item to delete.")
            return
        
        item = tree.item(selected[0])
        
        # Check if item has tags
        if not item['tags']:
            messagebox.showerror("Error", "Cannot delete this item - missing item ID.")
            return
            
        item_id = int(item['tags'][0])
        item_name = item['values'][0]
        item_type = item['values'][1]
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete stock item:\n\n{item_name}\nType: {item_type}"
        )
        
        if confirm:
            # Check if item is used in any rentals
            rentals = db.load_rentals()
            item_in_use = False
            for rental in rentals:
                if item_id in rental.items:
                    item_in_use = True
                    break
            
            if item_in_use:
                messagebox.showerror("Cannot Delete", 
                    f"Cannot delete '{item_name}' because it is currently rented or has rental history.\n"
                    f"Consider reducing quantity to 0 instead.")
                return
            
            # Delete from database
            items = db.load_items()
            items = [i for i in items if i.item_id != item_id]
            db.save_items(items)
            
            # Update treeview
            tree.delete(selected[0])
            messagebox.showinfo("Success", "Stock item deleted successfully.")
            delete_btn.config(state="disabled")
            count_label.config(text="0 SELECTED")
    
    def open_search_window():
        """Open Search window"""
        SearchWindow(root, apply_search_filter)
    
    def apply_search_filter(name_filter, type_filter, price_min_filter, price_max_filter):
        """Apply search filter to the treeview"""
        # Clear current selection
        tree.selection_remove(tree.selection())
        
        # Show all items first by reattaching all
        for child in tree.get_children():
            tree.reattach(child, '', 'end')
        
        # If no search criteria, show all
        if not name_filter and not type_filter and not price_min_filter and not price_max_filter:
            return
        
        # Hide non-matching items
        for child in tree.get_children():
            item = tree.item(child)
            item_values = item['values']
            
            # Skip items without proper values
            if len(item_values) < 4:
                tree.detach(child)
                continue
            
            item_name = str(item_values[0]).lower()
            item_type = str(item_values[1]).lower()
            item_price_str = str(item_values[2]).lower().replace('£', '').replace(' ', '')
            
            match = True
            
            # Check item name
            if name_filter and name_filter.lower() not in item_name:
                match = False
            
            # Check item type
            if type_filter and type_filter.lower() not in item_type:
                match = False
            
            # Check price range
            try:
                item_price = float(item_price_str)
                
                if price_min_filter:
                    try:
                        min_price = float(price_min_filter)
                        if item_price < min_price:
                            match = False
                    except ValueError:
                        pass
                
                if price_max_filter:
                    try:
                        max_price = float(price_max_filter)
                        if item_price > max_price:
                            match = False
                    except ValueError:
                        pass
            except ValueError:
                # If price can't be parsed, show item anyway
                pass
            
            if not match:
                tree.detach(child)
    
    def sort_treeview(col, reverse):
        """Sort treeview by column"""
        data = [(tree.set(child, col), child) for child in tree.get_children()]
        
        # Determine if it's a price column (contains £)
        if col == 2:  # Price column index
            # Sort by numeric value
            data.sort(key=lambda x: float(x[0].replace('£', '').replace(' ', '')), reverse=reverse)
        elif col == 3:  # Quantity column
            # Sort by numeric value
            data.sort(key=lambda x: int(x[0]), reverse=reverse)
        else:
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
    root.title("SPOTLIGHT AGENCY - Stock Search")
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
    title_label = tk.Label(main_frame, text="STOCK SEARCH", 
                          font=("Helvetica", 20, "bold"),
                          fg="white",
                          bg="#152e41")
    title_label.pack(pady=(0, 20))
    
    # Top button frame (Search, Delete Selected)
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
    columns = ("Item Name", "Type", "Price", "Quantity")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    
    # Define headings with clickable sorting
    tree.heading("Item Name", text="Item Name", 
                 command=lambda: sort_treeview(0, False))
    tree.heading("Type", text="Type", 
                 command=lambda: sort_treeview(1, False))
    tree.heading("Price", text="Price", 
                 command=lambda: sort_treeview(2, False))
    tree.heading("Quantity", text="Quantity", 
                 command=lambda: sort_treeview(3, False))
    
    # Define columns
    tree.column("Item Name", width=200, anchor="w")
    tree.column("Type", width=150, anchor="w")
    tree.column("Price", width=100, anchor="w")
    tree.column("Quantity", width=100, anchor="center")
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Set hover colors
    search_btn.normal_color = "#8A8A8A"
    search_btn.hover_color = "#A3A3A3"
    
    delete_btn.normal_color = "#8A8A8A"
    delete_btn.hover_color = "#A3A3A3"
    
    back_btn.normal_color = "#757575"
    back_btn.hover_color = "#616161"
    
    # Setup hover effects
    setup_hover_effects()
    
    # Bind selection event
    tree.bind("<<TreeviewSelect>>", on_item_select)
    
    # Load initial data
    load_stock_data()
    
    if not parent_window:
        root.mainloop()

def SearchWindow(parent_window, apply_callback):
    """Popup Search window - 650x500"""
    
    def perform_search():
        """Perform search and close window"""
        name = name_entry.get().strip()
        item_type = type_entry.get().strip()
        price_min = price_min_entry.get().strip()
        price_max = price_max_entry.get().strip()
        
        # Validate price inputs
        if price_min:
            try:
                float(price_min)
            except ValueError:
                messagebox.showerror("Invalid Input", "Minimum price must be a number.")
                return
        
        if price_max:
            try:
                float(price_max)
            except ValueError:
                messagebox.showerror("Invalid Input", "Maximum price must be a number.")
                return
        
        # Apply search to main window
        apply_callback(name, item_type, price_min, price_max)
        
        # Close search window
        search_root.destroy()
    
    def clear_and_close():
        """Clear search and close window"""
        apply_callback("", "", "", "")  # Clear filter
        search_root.destroy()
    
    # Create search window
    search_root = tk.Toplevel(parent_window)
    search_root.title("SPOTLIGHT AGENCY - Stock Search")
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
    title_label = tk.Label(main_frame, text="STOCK SEARCH", 
                          font=("Helvetica", 24, "bold"),
                          fg="white",
                          bg="#152e41")
    title_label.pack(pady=(0, 30))
    
    # Search criteria frame
    criteria_frame = tk.Frame(main_frame, bg="#152e41")
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
    
    # Item Name
    name_label = tk.Label(criteria_frame, text="ITEM NAME", **label_style)
    name_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    name_entry = tk.Entry(criteria_frame, **entry_style)
    name_entry.grid(row=1, column=0, pady=(0, 20), ipady=5)
    
    # Item Type
    type_label = tk.Label(criteria_frame, text="ITEM TYPE", **label_style)
    type_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
    
    type_entry = tk.Entry(criteria_frame, **entry_style)
    type_entry.grid(row=3, column=0, pady=(0, 20), ipady=5)
    
    # Price Range Frame
    price_frame = tk.Frame(criteria_frame, bg="#152e41")
    price_frame.grid(row=4, column=0, sticky="w", pady=(0, 5))
    
    price_label = tk.Label(price_frame, text="PRICE RANGE", **label_style)
    price_label.pack(anchor="w")
    
    # Price inputs in one line
    price_inputs_frame = tk.Frame(criteria_frame, bg="#152e41")
    price_inputs_frame.grid(row=5, column=0, sticky="w", pady=(0, 20))
    
    price_min_label = tk.Label(price_inputs_frame, text="Min:", 
                              font=("Helvetica", 11),
                              bg="#152e41")
    price_min_label.pack(side="left", padx=(0, 5))
    
    price_min_entry = tk.Entry(price_inputs_frame, 
                              font=("Helvetica", 12),
                              width=12,
                              bd=1,
                              relief="solid",
                              highlightthickness=1)
    price_min_entry.pack(side="left", padx=(0, 15), ipady=5)
    
    price_max_label = tk.Label(price_inputs_frame, text="Max:", 
                              font=("Helvetica", 11),
                              bg="#152e41")
    price_max_label.pack(side="left", padx=(0, 5))
    
    price_max_entry = tk.Entry(price_inputs_frame, 
                              font=("Helvetica", 12),
                              width=12,
                              bd=1,
                              relief="solid",
                              highlightthickness=1)
    price_max_entry.pack(side="left", ipady=5)
    
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
    name_entry.bind('<Return>', lambda e: perform_search())
    type_entry.bind('<Return>', lambda e: perform_search())
    price_min_entry.bind('<Return>', lambda e: perform_search())
    price_max_entry.bind('<Return>', lambda e: perform_search())
    
    # Make window modal
    search_root.transient(parent_window)
    search_root.grab_set()
    search_root.focus_set()
    
    # Focus on first entry
    name_entry.focus_set()

# For testing directly
if __name__ == "__main__":
    StockView()