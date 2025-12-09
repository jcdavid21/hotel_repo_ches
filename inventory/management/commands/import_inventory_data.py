import re
import os
from django.core.management.base import BaseCommand
from inventory.models import InventoryCategory, InventoryItem

class Command(BaseCommand):
    help = 'Imports inventory data from hotel_system (1).sql'

    def handle(self, *args, **options):
        file_path = os.path.join(os.getcwd(), 'hotel_system (1).sql')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # Simple Regex Parsing Strategy
        # 1. Parse Categories: INSERT INTO `inventory_categories` ... VALUES (1, 'Cleaning Supplies'), ...
        # 2. Parse Items: INSERT INTO `inventory_items` ... VALUES (1, 'Toilet Paper', 1, 500.00, ...
        
        self.stdout.write("--- clearing existing data ---")
        InventoryItem.objects.all().delete()
        InventoryCategory.objects.all().delete()

        self.stdout.write("--- parsing categories ---")
        # Regex for categories: (id, 'name')
        cat_pattern = re.search(r"INSERT INTO `inventory_categories` .*? VALUES\s+(.*?);", sql_content, re.DOTALL)
        if cat_pattern:
            values_str = cat_pattern.group(1)
            # Split by ), ( to get individual tuples roughly
            # This is a basic parser assuming standard mysqldump format
            tuples = re.findall(r"\((\d+),\s*'([^']+)'\)", values_str)
            for cat_id, cat_name in tuples:
                InventoryCategory.objects.create(
                    category_id=int(cat_id),
                    category_name=cat_name
                )
                self.stdout.write(f"Imported Category: {cat_name}")

        self.stdout.write("--- parsing items ---")
        # Regex for items: (id, 'name', cat_id, qty, min_qty, cost)
        # INSERT INTO `inventory_items` ... VALUES (1, 'Toilet Paper', 1, 500.00, 100.00, 0.50), ...
        item_pattern = re.search(r"INSERT INTO `inventory_items` .*? VALUES\s+(.*?);", sql_content, re.DOTALL)
        if item_pattern:
            values_str = item_pattern.group(1)
            # Regex to match: (1, 'Name', 1, 500.00, 100.00, 0.50)
            # Note: Decimal values can be 50.00
            
            # Using a slightly robust regex for the tuple content
            # Groups: 1=id, 2=name, 3=cat_id, 4=qty, 5=min, 6=cost
            item_tuples = re.findall(r"\((\d+),\s*'([^']+)',\s*(\d+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)\)", values_str)
            
            for item_id, name, cat_id, qty, min_qty, cost in item_tuples:
                try:
                    category = InventoryCategory.objects.get(category_id=int(cat_id))
                    InventoryItem.objects.create(
                        item_id=int(item_id),
                        item_name=name,
                        category=category,
                        quantity_in_stock=float(qty),
                        minimum_quantity=float(min_qty),
                        unit_cost=float(cost)
                    )
                    self.stdout.write(f"Imported Item: {name}")
                except InventoryCategory.DoesNotExist:
                     self.stdout.write(self.style.WARNING(f"Skipping {name}: Category {cat_id} not found"))

        self.stdout.write(self.style.SUCCESS('Data import complete.'))
