import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import Database_schema as db

def center_window(window, width=650, height=500):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def Revenue(parent_window=None):
    
    def setup_hover_effects():
        def on_enter(e):
            if hasattr(e.widget, 'hover_color'):
                e.widget.config(bg=e.widget.hover_color)
        
        def on_leave(e):
            if hasattr(e.widget, 'normal_color'):
                e.widget.config(bg=e.widget.normal_color)
        
        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)
    
    def calculate_today_revenue():
        rentals = db.load_rentals()
        today = date.today()
        
        # Initialize counters
        today_revenue = 0.0
        today_rentals = 0
        
        for rental in rentals:
            # Handle both datetime and date objects
            rental_date = rental.start_date
            
            # If it's a datetime object, extract the date
            if hasattr(rental_date, 'date'):
                rental_date = rental_date.date()
            
            # Check if rental is from today
            if rental_date == today:
                today_revenue += rental.total_price
                today_rentals += 1
        
        return today_revenue, today_rentals
    
    def update_statistics():
        try:
            today_revenue, today_rentals = calculate_today_revenue()
            
            # Update labels with current statistics
            total_revenue_label.config(text=f"£{today_revenue:,.2f}")
            total_rentals_label.config(text=f"{today_rentals}")
        except Exception as e:
            print(f"Error updating statistics: {e}")
            total_revenue_label.config(text="£0.00")
            total_rentals_label.config(text="0")
    
    def go_back():
        root.destroy()
        if parent_window:
            parent_window.deiconify()
    
    # Create the main window
    root = tk.Toplevel() if parent_window else tk.Tk()
    root.title("SPOTLIGHT AGENCY - Revenue")
    root.geometry("650x500")
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
                        bg="#8acbcb",
                        fg="white",
                        activebackground="#7db6b6",
                        width=10,
                        height=1,
                        command=go_back)
    back_btn.pack(side="right", padx=5, pady=5)
    
    # Title - SPOTLIGHT AGENCY
    agency_label = tk.Label(main_frame, text="REVENUE", 
                           font=("Helvetica", 18, "bold"),
                           fg="white",
                           bg="#152e41")
    agency_label.pack(pady=(0, 30))
    
    # Today's date display
    today = date.today()
    date_label = tk.Label(main_frame, 
                         text=f"Today: {today.strftime('%A, %d %B %Y')}",
                         font=("Helvetica", 12),
                         bg="#152e41",
                         fg="white")
    date_label.pack(pady=(0, 30))
    
    # Main statistics display frame
    stats_frame = tk.Frame(main_frame, bg="#152e41")
    stats_frame.pack(fill="both", expand=True, pady=20)
    
    # Style for labels
    label_style = {
        "font": ("Helvetica", 14),
        "bg": "#152e41",
        "fg": "white",
        "anchor": "center"
    }
    
    # Style for values
    value_style = {
        "font": ("Helvetica", 36, "bold"),
        "bg": "#152e41",
        "fg": "white",
        "anchor": "center"
    }
    
    # Total Revenue Section
    revenue_frame = tk.Frame(stats_frame, bg="#152e41")
    revenue_frame.pack(pady=0)
    
    revenue_text = tk.Label(revenue_frame, text="TOTAL REVENUE:", **label_style)
    revenue_text.pack()
    
    total_revenue_label = tk.Label(revenue_frame, text="£0.00", **value_style)
    total_revenue_label.pack(pady=20)
    
    # Total Rentals Section
    rentals_frame = tk.Frame(stats_frame, bg="#152e41")
    rentals_frame.pack(pady=10)
    
    rentals_text = tk.Label(rentals_frame, text="TOTAL RENTALS:", **label_style)
    rentals_text.pack(pady=0)
    
    total_rentals_label = tk.Label(rentals_frame, text="0", **value_style)
    total_rentals_label.pack(pady=10)
    
    # Update button to refresh statistics
    update_frame = tk.Frame(main_frame, bg="#152e41")
    update_frame.pack(pady=20)
    
    update_btn = tk.Button(update_frame, text="REFRESH",
                          font=("Helvetica", 11, "bold"),
                          bg="#8acbcb",
                          fg="white",
                          activebackground="#7db6b6",
                          width=15,
                          height=1,
                          command=update_statistics)
    update_btn.pack()
    
    # Set hover colors
    back_btn.normal_color = "#8acbcb"
    back_btn.hover_color = "#7db6b6"
    
    update_btn.normal_color = "#8acbcb"
    update_btn.hover_color = "#7db6b6"
    
    # Setup hover effects
    setup_hover_effects()
    update_btn.bind("<Enter>", lambda e: update_btn.config(bg="#7db6b6"))
    update_btn.bind("<Leave>", lambda e: update_btn.config(bg="#8acbcb"))
    
    # Calculate and display initial statistics
    update_statistics()
    
    # Auto-refresh every 30 seconds
    def auto_refresh():
        update_statistics()
        root.after(30000, auto_refresh)  # 30 seconds
    
    root.after(30000, auto_refresh)
    
    if not parent_window:
        root.mainloop()

# For testing directly
if __name__ == "__main__":
    Revenue()