import os
import sys
import django
from decimal import Decimal

# --- Django Setup (Adapted from demo_runner.py) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Process argument to allow using distinct DB if needed, but defaulting to demo DB
DB_PATH = os.path.join(BASE_DIR, 'inventory', 'db_demo.sqlite3')

from django.conf import settings


if 'TERM' not in os.environ:
    os.environ['TERM'] = 'xterm'


if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': DB_PATH,
            }
        },
        INSTALLED_APPS=[
            'inventory',
        ],
        TIME_ZONE='UTC',
        USE_TZ=True,
        DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
    )

django.setup()

# --- Import Services ---
from inventory.services import (
    add_item,
    remove_item,
    update_stock,
    check_low_stock,
    request_cleaning_supplies,
    request_ingredients,
    get_all_items
)
from inventory.models import InventoryTransaction, InventoryItem

# --- CLI Functions ---

def clear_screen():
    """Clear screen - handles missing TERM variable"""
    try:
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Unix/Linux/Mac
            os.system('clear')
    except Exception:
        # If clearing fails, just print newlines
        print('\n' * 50)

def print_header():
    print("="*35)
    print("=== INVENTORY AND SUPPLY MODULE ===")
    print("="*35)

def display_all_items():
    items = get_all_items()
    print(f"\nTotal Items: {items.count()}")
    print(f"{'ID':<5} {'Name':<20} {'Category':<20} {'Qty':<10} {'Min':<10} {'Cost':<10}")
    print("-" * 85)
    for item in items:
        # Format: Remove decimals for display, Use Peso
        qty = int(item.quantity_in_stock)
        min_qty = int(item.minimum_quantity)
        cost = f"Php {item.unit_cost:.2f}" if item.unit_cost else "Php 0.00"
        print(f"{item.item_id:<5} {item.item_name[:18]:<20} {item.category.category_name[:18]:<20} {qty:<10} {min_qty:<10} {cost:<10}")
    return items

def get_item_by_input_id():
    """
    Helper to prompt for ID and return InventoryItem object.
    Retries on invalid input until cancelled.
    """
    while True:
        try:
            val = input("\nEnter Item ID (or 'c' to cancel): ")
            if val.lower() == 'c':
                return None
            item_id = int(val)
            item = InventoryItem.objects.get(item_id=item_id)
            return item
        except ValueError:
            print("Invalid ID format. Please enter a number.")
        except InventoryItem.DoesNotExist:
            print("Item ID not found. Please try again.")

def menu_inventory():
    while True:
        print("\n--- INVENTORY MANAGEMENT ---")
        print("1. List All Items")
        print("2. Add New Item")
        print("3. Update Stock (ADD/DEDUCT)")
        print("4. Remove Item")
        print("5. Check Low Stock")
        print("0. Back to Main Menu")
        
        choice = input("Select option: ")
        
        if choice == '1':
            display_all_items()
                
        elif choice == '2':
            print("\n-- Add New Item --")
            name = input("Item Name: ")
            cat = input("Category: ")
            try:
                qty = Decimal(input("Initial Quantity: "))
                cost = Decimal(input("Unit Cost: "))
                add_item(name, qty, cat, cost)
            except ValueError:
                print("Invalid number format.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '3':
            # Update Stock
            # Display items first
            display_all_items()
            print("\n-- Update Stock Level --")
            item = get_item_by_input_id()
            if item:
                print(f"Selected: {item.item_name} (Current: {int(item.quantity_in_stock)})")
                print("Determine Action:")
                print("[A] Add Stock (Restock)")
                print("[B] Remove/Deduct Stock (Correction)")
                action = input("Choice: ").upper()
                
                if action in ['A', 'B']:
                    try:
                        qty_input = input("Enter Quantity: ")
                        qty = Decimal(qty_input)
                        if qty < 0:
                            print("Please enter a positive number (logic handles sign).")
                            continue
                        
                        if action == 'B':
                            qty = -qty
                            
                        update_stock(item.item_name, qty, transaction_type='manual_adjustment', department='Admin')
                    except ValueError:
                        print("Invalid number format.")
                else:
                    print("Invalid action selection.")

        elif choice == '4':
            display_all_items()
            print("\n-- Remove Item --")
            item = get_item_by_input_id()
            if item:
                confirm = input(f"Are you sure you want to PERMANENTLY DELETE '{item.item_name}'? (y/n): ")
                if confirm.lower() == 'y':
                    remove_item(item.item_name)

        elif choice == '5':
            # Check Low Stocks
            # Logic updated in services.py to show message if all good
            check_low_stock()

        elif choice == '0':
            break
        else:
            print("Invalid option.")

def menu_departments():
    while True:
        print("\n=== Department Menu ===")
        print("[A] Housekeeping Request")
        print("[B] Kitchen / Restaurant Request")
        print("[C] Lobby (Placeholder/if needed)") 
        print("[0] Back to Main Menu")
        
        choice = input("Select option: ").upper()
        
        if choice == 'A':
            # Housekeeping
            display_all_items() #(Requirement: Display items to avoid requesting non-existent)
            print("\n-- Housekeeping Request --")
            item = get_item_by_input_id()
            if item:
                staff = input("Staff Name: ")
                try:
                    qty = Decimal(input("Quantity Needed: "))
                    request_cleaning_supplies(staff, item.item_name, qty)
                except ValueError:
                    print("Invalid number format.")
        
        elif choice == 'B':
            # Kitchen
            print("\n=== Department Menu (Kitchen) ===")
            print("[A] Restaurant")
            print("[B] Kitchen")
            print("[C] Lobby")
            
            dept_input = input("Enter Department to Request: ").upper()
            dept_map = {'A': 'Restaurant', 'B': 'Kitchen', 'C': 'Lobby'}
            
            if dept_input in dept_map:
                dept_name = dept_map[dept_input]
                display_all_items()
                print(f"\n-- {dept_name} Request --")
                item = get_item_by_input_id()
                if item:
                     try:
                        qty = Decimal(input("Quantity Needed: "))
                        request_ingredients(dept_name, item.item_name, qty)
                     except ValueError:
                         print("Invalid number format.")
            else:
                print("Invalid Department selection.")
        
        elif choice == '0':
            break
        else:
            if choice not in ['A', 'B', '0']: # Simple validation
                print("Invalid option.")

def view_logs():
    print("\n--- TRANSACTION LOGS ---")
    logs = InventoryTransaction.objects.all().order_by('-transaction_date')[:20]
    print(f"Showing last {logs.count()} transactions:")
    print(f"{'Time':<18} {'Type':<20} {'Item':<20} {'Qty':<10} {'Dept':<20}")
    print("-" * 90)
    for log in logs:
        t_str = log.transaction_date.strftime('%Y-%m-%d %H:%M')
        # Handle potential None values for department
        dept = log.department if log.department else "-"
        qty = abs(int(log.quantity))
        # Truncate strings to fit column width
        print(f"{t_str:<18} {log.transaction_type.upper()[:19]:<20} {log.item.item_name[:19]:<20} {qty:<10} {dept[:19]:<20}")

def main():
    clear_screen()
    print_header()
    
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Inventory Management")
        print("2. Department Requests")
        print("3. View Reports / Logs")
        print("0. Exit")
        
        choice = input("Selection: ")
        
        if choice == '1':
            menu_inventory()
        elif choice == '2':
            menu_departments()
        elif choice == '3':
            view_logs()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
