import os
import django
from django.conf import settings

# 1. Configure Django Settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'db_demo.sqlite3')

# Clean up previous run
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

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

import django
django.setup()

from django.db import connection
from inventory.models import InventoryCategory, InventoryItem, InventoryTransaction

print("--- Setting up SQLite database for demo ---")

# 2. Create tables explicitly using SchemaEditor
# This bypasses the need for migrations and works even if models are managed=False in the file
with connection.schema_editor() as schema_editor:
    print("Creating table: InventoryCategory")
    schema_editor.create_model(InventoryCategory)
    
    print("Creating table: InventoryItem")
    schema_editor.create_model(InventoryItem)
    
    print("Creating table: InventoryTransaction")
    schema_editor.create_model(InventoryTransaction)

print("--- Database tables created ---")

# 3. Import Services and Run Demo
from inventory.services import (
    add_item, 
    check_low_stock, 
    request_cleaning_supplies, 
    request_ingredients,
    update_stock
)

def run_demo():
    print("\n=== RUNNING INVENTORY MODULE DEMO ===\n")

    # A. Add Initial Items
    print(">>> 1. Adding Initial Items...")
    # Categories will be auto-created by logic in add_item so we don't need to pre-seed categories, 
    # but add_item logic: category, _ = InventoryCategory.objects.get_or_create(category_name=category_name)
    
    add_item("Toilet Paper", 500.00, "Cleaning Supplies", 0.50)
    add_item("Bed Sheets", 20.00, "Linens", 15.00) # Low stock
    add_item("Tomatoes", 80.00, "Food Ingredients", 2.50)
    
    # B. Check Low Stock
    print("\n>>> 2. Checking Low Stock Config...")
    check_low_stock()

    # C. Housekeeping Request
    print("\n>>> 3. Housekeeping requests 50 rolls of Toilet Paper...")
    request_cleaning_supplies("Maria", "Toilet Paper", 50)

    # D. Kitchen Request
    print("\n>>> 4. Kitchen requests 10 Tomatoes...")
    request_ingredients("Kitchen", "Tomatoes", 10)

    # E. Check Transaction Log
    print("\n>>> 5. Verifying Transaction Logs...")
    logs = InventoryTransaction.objects.all().order_by('-transaction_date')
    print(f"Found {logs.count()} transaction(s):")
    for log in logs:
        # Format: [TIME] TYPE: ITEM (QTY)
        t_str = log.transaction_date.strftime('%H:%M:%S')
        print(f" - [{t_str}] {log.transaction_type}: {log.item.item_name} (Qty: {log.quantity}) | Dept: {log.department}")

    print("\n=== DEMO COMPLETED ===")

if __name__ == '__main__':
    run_demo()
