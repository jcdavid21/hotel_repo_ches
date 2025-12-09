from .models import InventoryItem, InventoryCategory, InventoryTransaction
from decimal import Decimal
from django.utils import timezone
from django.db import models, transaction
from django.core.exceptions import ObjectDoesNotExist

# Service Functions

def add_item(item_name, quantity, category_name, cost):
    """
    Adds a new item to the inventory.
    """
    try:
        # Get or create category
        category, _ = InventoryCategory.objects.get_or_create(category_name=category_name)
        
        item = InventoryItem(
            item_name=item_name,
            quantity_in_stock=quantity,
            category=category,
            unit_cost=cost
        )
        item.save()
        print(f"Item '{item_name}' added successfully.")
        return item
    except Exception as e:
        print(f"Error adding item: {e}")
        return None

def remove_item(item_name):
    """
    Removes an item from the inventory (Delete).
    """
    try:
        item = InventoryItem.objects.get(item_name=item_name)
        item.delete()
        print(f"Item '{item_name}' removed successfully.")
        return True
    except InventoryItem.DoesNotExist:
        print(f"Item '{item_name}' not found.")
        return False
    except Exception as e:
        print(f"Error removing item: {e}")
        return False

def update_stock(item_name, quantity, transaction_type='adjustment', department=None):
    """
    Updates the stock of an item (add or subtract quantity).
    Postive quantity for adding/restock, negative for usage/deduction.
    """
    try:
        with transaction.atomic():
            item = InventoryItem.objects.get(item_name=item_name)
            
            # Calculate new quantity
            new_quantity = item.quantity_in_stock + Decimal(quantity)
            
            # Prevent negative stock if it's a usage
            if new_quantity < 0:
                print(f"Error: Insufficient stock for '{item_name}'. Current: {item.quantity_in_stock}")
                return False

            item.quantity_in_stock = new_quantity
            item.save()

            # Log transaction
            log_entry = InventoryTransaction(
                item=item,
                transaction_type=transaction_type,
                quantity=Decimal(quantity),
                department=department,
                transaction_date=timezone.now()
            )
            log_entry.save()
            
            print(f"Stock updated for '{item_name}'. New Quantity: {item.quantity_in_stock}")
            
            # Check for low stock immediately after update
            if item.quantity_in_stock < item.minimum_quantity:
                print(f"ALERT: '{item.item_name}' is below minimum threshold! ({item.quantity_in_stock} < {item.minimum_quantity})")
            
            return True
            
    except InventoryItem.DoesNotExist:
        print(f"Item '{item_name}' not found.")
        return False
    except Exception as e:
        print(f"Error updating stock: {e}")
        return False

def check_low_stock():
    """
    Returns list of items below minimum threshold.
    """
    low_stock_items = InventoryItem.objects.filter(quantity_in_stock__lt=models.F('minimum_quantity'))
    report = []
    print("--- Low Stock Alert ---")
    if not low_stock_items:
        print("All Items Are in Good Stocks.")
    else:
        for item in low_stock_items:
            msg = f"{item.item_name}: Stock {item.quantity_in_stock} (Min: {item.minimum_quantity})"
            print(msg)
            report.append(item)
    return report

def request_cleaning_supplies(staff_name, item_name, quantity_needed):
    """
    Housekeeping requests supplies. Deducts stock and logs it.
    """
    print(f"Housekeeping Request from {staff_name} for {quantity_needed} x {item_name}")
    success = update_stock(item_name, -Decimal(quantity_needed), transaction_type='usage', department='Housekeeping')
    if success:
        # Fetch cost for accounting log
        try:
            item = InventoryItem.objects.get(item_name=item_name)
            total_cost = item.unit_cost * Decimal(quantity_needed) if item.unit_cost else 0
            log_expense_to_accounting(item_name, total_cost, quantity_needed)
        except:
            pass
    return success

def request_ingredients(department_name, item_name, quantity_needed):
    """
    Restaurant/Kitchen requests ingredients.
    """
    print(f"{department_name} Request for {quantity_needed} x {item_name}")
    success = update_stock(item_name, -Decimal(quantity_needed), transaction_type='usage', department=department_name)
    if success:
         # Fetch cost for accounting log
        try:
            item = InventoryItem.objects.get(item_name=item_name)
            total_cost = item.unit_cost * Decimal(quantity_needed) if item.unit_cost else 0
            log_expense_to_accounting(item_name, total_cost, quantity_needed)
        except:
            pass
    return success

def log_expense_to_accounting(item_name, cost, quantity_used):
    """
    Simulates sending a cost usage log to the Accounting Module.
    """
    print(f"[ACCOUNTING LOG] expense recorded: Item={item_name}, Qty={quantity_used}, TotalCost=Php {cost}")
    # In a real system, this would write to an Accounting table or call an Accounting Service API
    return True

def get_all_items():
    """
    Returns all inventory items.
    """
    return InventoryItem.objects.select_related('category').all()
