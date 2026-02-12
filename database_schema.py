# database_schema.py
import pickle
import os
from datetime import datetime, timedelta

# File paths
CUSTOMERS_FILE = "customers.pkl"
RENTALS_FILE = "rentals.pkl"
ITEMS_FILE = "items.pkl"

class Customer:
    def __init__(self, customer_id, firstname, surname, phone):
        self.customer_id = customer_id
        self.firstname = firstname
        self.surname = surname
        self.phone = phone
        self.fullname = f"{firstname} {surname}"
    
    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'firstname': self.firstname,
            'surname': self.surname,
            'phone': self.phone,
            'fullname': self.fullname
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['customer_id'], data['firstname'], data['surname'], data['phone'])

class Item:
    def __init__(self, item_id, name, item_type, quantity, price):
        self.item_id = item_id
        self.name = name
        self.type = item_type
        self.quantity = quantity
        self.price = price
    
    def to_dict(self):
        return {
            'item_id': self.item_id,
            'name': self.name,
            'type': self.type,
            'quantity': self.quantity,
            'price': self.price
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['item_id'], data['name'], data['type'], data['quantity'], data['price'])

class Rental:
    def __init__(self, rental_id, customer_id, employee, start_date, end_date, items, total_price, creation_date=None):
        self.rental_id = rental_id
        self.customer_id = customer_id
        self.employee = employee
        self.start_date = start_date
        self.end_date = end_date
        self.items = items  # List of item IDs with quantities
        self.total_price = total_price
        # If creation_date not provided, use current datetime
        self.creation_date = creation_date if creation_date else datetime.now()
    
    def to_dict(self):
        return {
            'rental_id': self.rental_id,
            'customer_id': self.customer_id,
            'employee': self.employee,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'items': self.items,
            'total_price': self.total_price,
            'creation_date': self.creation_date
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['rental_id'], 
            data['customer_id'], 
            data['employee'], 
            data['start_date'], 
            data['end_date'], 
            data['items'], 
            data['total_price'],
            data.get('creation_date', data['start_date'])  # Fallback for old records
        )

# Database functions
def load_customers():
    if os.path.exists(CUSTOMERS_FILE):
        try:
            with open(CUSTOMERS_FILE, 'rb') as f:
                return pickle.load(f)
        except:
            return []
    return []

def save_customers(customers):
    with open(CUSTOMERS_FILE, 'wb') as f:
        pickle.dump(customers, f)

def load_rentals():
    if os.path.exists(RENTALS_FILE):
        try:
            with open(RENTALS_FILE, 'rb') as f:
                return pickle.load(f)
        except:
            return []
    return []

def save_rentals(rentals):
    with open(RENTALS_FILE, 'wb') as f:
        pickle.dump(rentals, f)

def load_items():
    if os.path.exists(ITEMS_FILE):
        try:
            with open(ITEMS_FILE, 'rb') as f:
                return pickle.load(f)
        except:
            return []
    return []

def save_items(items):
    with open(ITEMS_FILE, 'wb') as f:
        pickle.dump(items, f)

def get_next_customer_id():
    customers = load_customers()
    if not customers:
        return 1
    return max(c.customer_id for c in customers) + 1

def get_next_rental_id():
    rentals = load_rentals()
    if not rentals:
        return 1
    return max(r.rental_id for r in rentals) + 1

def get_next_item_id():
    items = load_items()
    if not items:
        return 1
    return max(i.item_id for i in items) + 1

def init_sample_data():
    """Initialize sample data if files don't exist"""
    if not os.path.exists(CUSTOMERS_FILE):
        customers = [
            Customer(1, "John", "Tucker", "555-0101"),
            Customer(2, "Mike", "Howell", "555-0102"),
            Customer(3, "Jane", "Smith", "555-0103"),
            Customer(4, "Robert", "Brown", "555-0104"),
            Customer(5, "Sarah", "Wilson", "555-0105"),
        ]
        save_customers(customers)
    
    if not os.path.exists(ITEMS_FILE):
        items = [
            Item(1, "Stage (size 1)", "Stage", 5, 100.00),
            Item(2, "Stage (size 2)", "Stage", 3, 150.00),
            Item(3, "Microphone", "Audio", 10, 20.00),
            Item(4, "Microphone + stand", "Audio", 8, 25.00),
            Item(5, "Amplifier", "Audio", 4, 50.00),
            Item(6, "Spot Lights", "Lighting", 15, 35.00),
            Item(7, "Speaker", "Audio", 6, 40.00),
            Item(8, "Mixer", "Audio", 3, 60.00),
        ]
        save_items(items)
    
    if not os.path.exists(RENTALS_FILE):
        rentals = [
            Rental(1, 1, "admin", datetime(2025, 12, 31), datetime(2026, 1, 2), 
                  {1: 1, 3: 2, 6: 4}, 300.00),
            Rental(2, 2, "admin", datetime(2025, 1, 7), datetime(2026, 1, 8), 
                  {2: 1, 4: 2, 5: 1}, 285.00),
        ]
        save_rentals(rentals)

# Initialize sample data on import
init_sample_data()