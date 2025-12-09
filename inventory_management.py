import database as db

cursor = db.conn.cursor(dictionary=True)


class InventoryManagement:
    def __init__(self, user_info):
        self.user_info = user_info

    def main_menu(self):
        """Main inventory management menu"""
        while True:
            print("\n" + "=" * 70)
            print(f"=== INVENTORY MANAGEMENT - {self.user_info['first_name']} {self.user_info['last_name']} ===")
            print("=" * 70)
            print("1. Inventory Items Management")
            print("2. Menu Items Management")
            print("3. Menu Item Ingredients Management")
            print("4. Categories Management")
            print("5. Inventory Reports")
            print("6. Back to Main Menu")
            print("=" * 70)

            try:
                choice = int(input("Select option: "))

                if choice == 1:
                    self.inventory_items_menu()
                elif choice == 2:
                    self.menu_items_menu()
                elif choice == 3:
                    self.menu_ingredients_menu()
                elif choice == 4:
                    self.categories_menu()
                elif choice == 5:
                    self.inventory_reports_menu()
                elif choice == 6:
                    break
                else:
                    print("Invalid option!")
            except ValueError:
                print("Invalid input! Please enter a number.")
            except Exception as e:
                print(f"An error occurred: {e}")

    # ========== INVENTORY ITEMS MANAGEMENT ==========

    def inventory_items_menu(self):
        """Inventory items management submenu"""
        while True:
            print("\n" + "=" * 70)
            print("INVENTORY ITEMS MANAGEMENT")
            print("=" * 70)
            print("1. View All Inventory Items")
            print("2. Add Inventory Item")
            print("3. Update Inventory Item")
            print("4. Delete Inventory Item")
            print("5. Adjust Stock Quantity")
            print("6. View Low Stock Items")
            print("7. Back")

            try:
                choice = int(input("\nSelect option: "))

                if choice == 1:
                    self.view_all_inventory()
                elif choice == 2:
                    self.add_inventory_item()
                elif choice == 3:
                    self.update_inventory_item()
                elif choice == 4:
                    self.delete_inventory_item()
                elif choice == 5:
                    self.adjust_stock()
                elif choice == 6:
                    self.view_low_stock()
                elif choice == 7:
                    break
                else:
                    print("Invalid option!")
            except ValueError:
                print("Invalid input!")

    def view_all_inventory(self):
        """Display all inventory items"""
        try:
            query = """
            SELECT 
                ii.item_id,
                ii.item_name,
                ic.category_name,
                ii.quantity_in_stock,
                ii.unit,
                ii.minimum_quantity,
                ii.unit_cost
            FROM inventory_items ii
            JOIN inventory_categories ic ON ic.category_id = ii.category_id
            ORDER BY ic.category_name, ii.item_name
            """
            cursor.execute(query)
            items = cursor.fetchall()

            print("\n" + "=" * 110)
            print("ALL INVENTORY ITEMS")
            print("=" * 110)
            print(f"{'ID':<5} {'Item Name':<35} {'Category':<20} {'Stock':<18} {'Min':<18} {'Cost':<12}")
            print("-" * 110)

            for item in items:
                status = "⚠️ LOW" if float(item['quantity_in_stock']) <= float(item['minimum_quantity']) else ""
                stock_display = f"{float(item['quantity_in_stock']):.2f} {item['unit']}"
                min_display = f"{float(item['minimum_quantity']):.2f} {item['unit']}"

                print(f"{item['item_id']:<5} {item['item_name']:<35} {item['category_name']:<20} "
                      f"{stock_display:<18} {min_display:<18} ₱{float(item['unit_cost']):<11.2f} {status}")

            print("=" * 110)

        except Exception as e:
            print(f"Error viewing inventory: {e}")

    def add_inventory_item(self):
        """Add new inventory item"""
        try:
            print("\n--- ADD INVENTORY ITEM ---")

            # Show inventory categories
            query = "SELECT * FROM inventory_categories ORDER BY category_name"
            cursor.execute(query)
            categories = cursor.fetchall()

            print("\nInventory Categories:")
            for cat in categories:
                print(f"{cat['category_id']}. {cat['category_name']}")

            category_id = int(input("\nEnter category ID: "))
            item_name = input("Enter item name: ").strip()
            quantity = float(input("Enter initial quantity: "))
            unit = input("Enter unit (kg, L, pcs, etc.): ").strip()
            minimum_quantity = float(input("Enter minimum quantity threshold: "))
            unit_cost = float(input("Enter unit cost: "))

            insert_query = """
            INSERT INTO inventory_items 
            (item_name, category_id, quantity_in_stock, unit, minimum_quantity, unit_cost)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (item_name, category_id, quantity, unit, minimum_quantity, unit_cost))

            item_id = cursor.lastrowid

            # Log initial stock as restock transaction
            transaction_query = """
            INSERT INTO inventory_transactions 
            (item_id, transaction_type, quantity, transaction_date)
            VALUES (%s, 'restock', %s, NOW())
            """
            cursor.execute(transaction_query, (item_id, quantity))

            db.conn.commit()

            print(f"\n✓ Inventory item '{item_name}' added successfully!")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def update_inventory_item(self):
        """Update inventory item details"""
        try:
            self.view_all_inventory()

            item_id = int(input("\nEnter item ID to update: "))

            query = "SELECT * FROM inventory_items WHERE item_id = %s"
            cursor.execute(query, (item_id,))
            item = cursor.fetchone()

            if not item:
                print("Item not found!")
                return

            print(f"\nCurrent item: {item['item_name']}")
            print("\nWhat do you want to update?")
            print("1. Item Name")
            print("2. Unit Cost")
            print("3. Minimum Quantity")
            print("4. Unit")
            print("5. Cancel")

            choice = int(input("\nSelect option: "))

            if choice == 1:
                new_name = input("Enter new item name: ").strip()
                cursor.execute("UPDATE inventory_items SET item_name = %s WHERE item_id = %s",
                               (new_name, item_id))
            elif choice == 2:
                new_cost = float(input("Enter new unit cost: "))
                cursor.execute("UPDATE inventory_items SET unit_cost = %s WHERE item_id = %s",
                               (new_cost, item_id))
            elif choice == 3:
                new_min = float(input("Enter new minimum quantity: "))
                cursor.execute("UPDATE inventory_items SET minimum_quantity = %s WHERE item_id = %s",
                               (new_min, item_id))
            elif choice == 4:
                new_unit = input("Enter new unit: ").strip()
                cursor.execute("UPDATE inventory_items SET unit = %s WHERE item_id = %s",
                               (new_unit, item_id))
            elif choice == 5:
                return
            else:
                print("Invalid choice!")
                return

            db.conn.commit()
            print("\n✓ Item updated successfully!")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def delete_inventory_item(self):
        """Delete inventory item"""
        try:
            self.view_all_inventory()

            item_id = int(input("\nEnter item ID to delete: "))

            query = "SELECT * FROM inventory_items WHERE item_id = %s"
            cursor.execute(query, (item_id,))
            item = cursor.fetchone()

            if not item:
                print("Item not found!")
                return

            print(f"\nAre you sure you want to delete '{item['item_name']}'?")
            confirm = input("Type 'DELETE' to confirm: ").strip()

            if confirm == 'DELETE':
                cursor.execute("DELETE FROM inventory_items WHERE item_id = %s", (item_id,))
                db.conn.commit()
                print("\n✓ Item deleted successfully!")
            else:
                print("Deletion cancelled.")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def adjust_stock(self):
        """Adjust stock quantity (restock or adjustment)"""
        try:
            self.view_all_inventory()

            item_id = int(input("\nEnter item ID: "))

            query = "SELECT * FROM inventory_items WHERE item_id = %s"
            cursor.execute(query, (item_id,))
            item = cursor.fetchone()

            if not item:
                print("Item not found!")
                return

            print(f"\nCurrent stock: {float(item['quantity_in_stock']):.2f} {item['unit']}")
            print("\nAdjustment type:")
            print("1. Add stock (Restock)")
            print("2. Remove stock (Adjustment)")
            print("3. Set exact quantity")

            adj_type = int(input("\nSelect option: "))

            if adj_type == 1:
                quantity = float(input("Enter quantity to add: "))
                cursor.execute(
                    "UPDATE inventory_items SET quantity_in_stock = quantity_in_stock + %s WHERE item_id = %s",
                    (quantity, item_id))
                cursor.execute(
                    "INSERT INTO inventory_transactions (item_id, transaction_type, quantity, transaction_date) VALUES (%s, 'restock', %s, NOW())",
                    (item_id, quantity))
                print(f"\n✓ Added {quantity} {item['unit']} to stock!")
            elif adj_type == 2:
                quantity = float(input("Enter quantity to remove: "))
                cursor.execute(
                    "UPDATE inventory_items SET quantity_in_stock = quantity_in_stock - %s WHERE item_id = %s",
                    (quantity, item_id))
                cursor.execute(
                    "INSERT INTO inventory_transactions (item_id, transaction_type, quantity, transaction_date) VALUES (%s, 'adjustment', %s, NOW())",
                    (item_id, -quantity))
                print(f"\n✓ Removed {quantity} {item['unit']} from stock!")
            elif adj_type == 3:
                new_quantity = float(input("Enter exact quantity: "))
                diff = new_quantity - float(item['quantity_in_stock'])
                cursor.execute("UPDATE inventory_items SET quantity_in_stock = %s WHERE item_id = %s",
                               (new_quantity, item_id))
                cursor.execute(
                    "INSERT INTO inventory_transactions (item_id, transaction_type, quantity, transaction_date) VALUES (%s, 'adjustment', %s, NOW())",
                    (item_id, diff))
                print(f"\n✓ Stock set to {new_quantity} {item['unit']}!")
            else:
                print("Invalid option!")
                return

            db.conn.commit()

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def view_low_stock(self):
        """Display items below minimum quantity"""
        try:
            query = """
            SELECT 
                ii.item_id,
                ii.item_name,
                ic.category_name,
                ii.quantity_in_stock,
                ii.unit,
                ii.minimum_quantity,
                ii.unit_cost
            FROM inventory_items ii
            JOIN inventory_categories ic ON ic.category_id = ii.category_id
            WHERE ii.quantity_in_stock <= ii.minimum_quantity
            ORDER BY (ii.quantity_in_stock - ii.minimum_quantity)
            """
            cursor.execute(query)
            items = cursor.fetchall()

            if not items:
                print("\n✓ All items are adequately stocked!")
                return

            print("\n" + "=" * 110)
            print("⚠️ LOW STOCK ITEMS - RESTOCK NEEDED")
            print("=" * 110)
            print(f"{'ID':<5} {'Item Name':<35} {'Category':<20} {'Stock':<18} {'Min':<18} {'Shortage':<15}")
            print("-" * 110)

            for item in items:
                shortage = float(item['minimum_quantity']) - float(item['quantity_in_stock'])
                stock_display = f"{float(item['quantity_in_stock']):.2f} {item['unit']}"
                min_display = f"{float(item['minimum_quantity']):.2f} {item['unit']}"
                need_display = f"{shortage:.2f} {item['unit']}"

                print(f"{item['item_id']:<5} {item['item_name']:<35} {item['category_name']:<20} "
                      f"{stock_display:<18} {min_display:<18} {need_display:<15}")

            print("=" * 110)

        except Exception as e:
            print(f"Error viewing low stock: {e}")

    # ========== MENU ITEMS MANAGEMENT ==========

    def menu_items_menu(self):
        """Menu items management submenu"""
        while True:
            print("\n" + "=" * 70)
            print("MENU ITEMS MANAGEMENT")
            print("=" * 70)
            print("1. View All Menu Items")
            print("2. Add Menu Item")
            print("3. Update Menu Item")
            print("4. Delete Menu Item")
            print("5. Toggle Item Availability")
            print("6. Back")

            try:
                choice = int(input("\nSelect option: "))

                if choice == 1:
                    self.view_all_menu_items()
                elif choice == 2:
                    self.add_menu_item()
                elif choice == 3:
                    self.update_menu_item()
                elif choice == 4:
                    self.delete_menu_item()
                elif choice == 5:
                    self.toggle_item_availability()
                elif choice == 6:
                    break
                else:
                    print("Invalid option!")
            except ValueError:
                print("Invalid input!")

    def view_all_menu_items(self):
        """View all menu items"""
        try:
            query = """
            SELECT 
                mi.menu_item_id,
                mi.item_name,
                mc.category_name,
                mi.price,
                mi.is_available
            FROM menu_items mi
            JOIN menu_categories mc ON mc.category_id = mi.category_id
            ORDER BY mc.category_name, mi.item_name
            """
            cursor.execute(query)
            items = cursor.fetchall()

            print("\n" + "=" * 90)
            print("ALL MENU ITEMS")
            print("=" * 90)
            print(f"{'ID':<5} {'Item Name':<40} {'Category':<20} {'Price':<12} {'Available':<12}")
            print("-" * 90)

            for item in items:
                available = "Yes" if item['is_available'] else "No"
                print(f"{item['menu_item_id']:<5} {item['item_name']:<40} {item['category_name']:<20} "
                      f"₱{float(item['price']):<11.2f} {available:<12}")

            print("=" * 90)

        except Exception as e:
            print(f"Error: {e}")

    def add_menu_item(self):
        """Add new menu item"""
        try:
            print("\n--- ADD MENU ITEM ---")

            # Show menu categories
            query = "SELECT * FROM menu_categories ORDER BY category_name"
            cursor.execute(query)
            categories = cursor.fetchall()

            print("\nMenu Categories:")
            for cat in categories:
                print(f"{cat['category_id']}. {cat['category_name']}")

            category_id = int(input("\nEnter category ID: "))
            item_name = input("Enter item name: ").strip()
            price = float(input("Enter price: "))

            insert_query = """
            INSERT INTO menu_items (item_name, category_id, price, is_available)
            VALUES (%s, %s, %s, 1)
            """
            cursor.execute(insert_query, (item_name, category_id, price))
            db.conn.commit()

            print(f"\n✓ Menu item '{item_name}' added successfully!")
            print("\nDon't forget to add ingredients for this item in Menu Item Ingredients Management!")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def update_menu_item(self):
        """Update menu item"""
        try:
            self.view_all_menu_items()

            item_id = int(input("\nEnter menu item ID to update: "))

            query = "SELECT * FROM menu_items WHERE menu_item_id = %s"
            cursor.execute(query, (item_id,))
            item = cursor.fetchone()

            if not item:
                print("Menu item not found!")
                return

            print(f"\nCurrent item: {item['item_name']}")
            print(f"Current price: ₱{float(item['price']):.2f}")

            print("\nWhat do you want to update?")
            print("1. Item Name")
            print("2. Price")
            print("3. Both")
            print("4. Cancel")

            choice = int(input("\nSelect option: "))

            if choice == 1:
                new_name = input("Enter new item name: ").strip()
                cursor.execute("UPDATE menu_items SET item_name = %s WHERE menu_item_id = %s",
                               (new_name, item_id))
            elif choice == 2:
                new_price = float(input("Enter new price: "))
                cursor.execute("UPDATE menu_items SET price = %s WHERE menu_item_id = %s",
                               (new_price, item_id))
            elif choice == 3:
                new_name = input("Enter new item name: ").strip()
                new_price = float(input("Enter new price: "))
                cursor.execute("UPDATE menu_items SET item_name = %s, price = %s WHERE menu_item_id = %s",
                               (new_name, new_price, item_id))
            elif choice == 4:
                return
            else:
                print("Invalid choice!")
                return

            db.conn.commit()
            print("\n✓ Menu item updated successfully!")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def delete_menu_item(self):
        """Delete menu item"""
        try:
            self.view_all_menu_items()

            item_id = int(input("\nEnter menu item ID to delete: "))

            query = "SELECT * FROM menu_items WHERE menu_item_id = %s"
            cursor.execute(query, (item_id,))
            item = cursor.fetchone()

            if not item:
                print("Menu item not found!")
                return

            print(f"\nAre you sure you want to delete '{item['item_name']}'?")
            print("This will also delete all ingredient associations!")
            confirm = input("Type 'DELETE' to confirm: ").strip()

            if confirm == 'DELETE':
                cursor.execute("DELETE FROM menu_items WHERE menu_item_id = %s", (item_id,))
                db.conn.commit()
                print("\n✓ Menu item deleted successfully!")
            else:
                print("Deletion cancelled.")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def toggle_item_availability(self):
        """Toggle menu item availability"""
        try:
            self.view_all_menu_items()

            item_id = int(input("\nEnter menu item ID: "))

            query = "SELECT * FROM menu_items WHERE menu_item_id = %s"
            cursor.execute(query, (item_id,))
            item = cursor.fetchone()

            if not item:
                print("Menu item not found!")
                return

            new_status = 0 if item['is_available'] else 1
            status_text = "Available" if new_status else "Unavailable"

            cursor.execute("UPDATE menu_items SET is_available = %s WHERE menu_item_id = %s",
                           (new_status, item_id))
            db.conn.commit()

            print(f"\n✓ {item['item_name']} is now {status_text}!")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    # ========== MENU ITEM INGREDIENTS MANAGEMENT ==========

    def menu_ingredients_menu(self):
        """Menu item ingredients management"""
        while True:
            print("\n" + "=" * 70)
            print("MENU ITEM INGREDIENTS MANAGEMENT")
            print("=" * 70)
            print("1. View All Menu Item Ingredients")
            print("2. View Ingredients for Specific Menu Item")
            print("3. Add Ingredient to Menu Item")
            print("4. Update Ingredient Quantity")
            print("5. Remove Ingredient from Menu Item")
            print("6. Back")

            try:
                choice = int(input("\nSelect option: "))

                if choice == 1:
                    self.view_all_menu_ingredients()
                elif choice == 2:
                    self.view_menu_item_ingredients()
                elif choice == 3:
                    self.add_menu_ingredient()
                elif choice == 4:
                    self.update_ingredient_quantity()
                elif choice == 5:
                    self.remove_menu_ingredient()
                elif choice == 6:
                    break
                else:
                    print("Invalid option!")
            except ValueError:
                print("Invalid input!")

    def view_all_menu_ingredients(self):
        """View all menu item ingredients"""
        try:
            query = """
            SELECT 
                mi.menu_item_id,
                mi.item_name as menu_item,
                ii.item_id as inv_item_id,
                ii.item_name as ingredient,
                mii.quantity_needed,
                ii.unit,
                ii.quantity_in_stock
            FROM menu_item_ingredients mii
            JOIN menu_items mi ON mi.menu_item_id = mii.menu_item_id
            JOIN inventory_items ii ON ii.item_id = mii.inventory_item_id
            ORDER BY mi.item_name, ii.item_name
            """
            cursor.execute(query)
            results = cursor.fetchall()

            if not results:
                print("\n⚠️ No ingredients configured!")
                return

            print("\n" + "=" * 110)
            print("MENU ITEM INGREDIENTS")
            print("=" * 110)
            print(f"{'Menu ID':<10} {'Menu Item':<30} {'Ingredient':<30} {'Qty Needed':<20} {'In Stock':<18}")
            print("-" * 110)

            for row in results:
                qty_display = f"{float(row['quantity_needed']):.3f} {row['unit']}"
                stock_display = f"{float(row['quantity_in_stock']):.2f} {row['unit']}"

                print(f"{row['menu_item_id']:<10} {row['menu_item']:<30} {row['ingredient']:<30} "
                      f"{qty_display:<20} {stock_display:<18}")

            print("=" * 110)

        except Exception as e:
            print(f"Error: {e}")

    def view_menu_item_ingredients(self):
        """View ingredients for a specific menu item"""
        try:
            self.view_all_menu_items()

            menu_item_id = int(input("\nEnter menu item ID: "))

            query = """
            SELECT 
                mi.item_name as menu_item,
                ii.item_name as ingredient,
                mii.quantity_needed,
                ii.unit,
                ii.quantity_in_stock,
                (ii.quantity_in_stock / mii.quantity_needed) as servings_available
            FROM menu_item_ingredients mii
            JOIN menu_items mi ON mi.menu_item_id = mii.menu_item_id
            JOIN inventory_items ii ON ii.item_id = mii.inventory_item_id
            WHERE mii.menu_item_id = %s
            ORDER BY ii.item_name
            """
            cursor.execute(query, (menu_item_id,))
            results = cursor.fetchall()

            if not results:
                print("\n⚠️ No ingredients configured for this menu item!")
                return

            print("\n" + "=" * 100)
            print(f"INGREDIENTS FOR: {results[0]['menu_item']}")
            print("=" * 100)
            print(f"{'Ingredient':<35} {'Qty Needed':<20} {'In Stock':<20} {'Servings':<15}")
            print("-" * 100)

            min_servings = float('inf')
            for row in results:
                qty_display = f"{float(row['quantity_needed']):.3f} {row['unit']}"
                stock_display = f"{float(row['quantity_in_stock']):.2f} {row['unit']}"
                servings = int(float(row['servings_available']))
                min_servings = min(min_servings, servings)

                print(f"{row['ingredient']:<35} {qty_display:<20} {stock_display:<20} {servings:<15}")

            print("-" * 100)
            print(f"Maximum servings available: {min_servings}")
            print("=" * 100)

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            print(f"Error: {e}")

    def add_menu_ingredient(self):
        """Add ingredient to a menu item"""
        try:
            self.view_all_menu_items()
            menu_item_id = int(input("\nEnter Menu Item ID: "))

            # Verify menu item exists
            cursor.execute("SELECT item_name FROM menu_items WHERE menu_item_id = %s", (menu_item_id,))
            menu_item = cursor.fetchone()

            if not menu_item:
                print("Menu item not found!")
                return

            print(f"\nAdding ingredient to: {menu_item['item_name']}")

            # Show inventory items
            print("\n--- Available Inventory Items ---")
            query = """
            SELECT ii.item_id, ii.item_name, ii.unit, ic.category_name 
            FROM inventory_items ii
            JOIN inventory_categories ic ON ic.category_id = ii.category_id
            WHERE ii.category_id = 4 OR ii.category_id = 5
            ORDER BY ic.category_name, ii.item_name
            """
            cursor.execute(query)
            items = cursor.fetchall()

            current_category = None
            for item in items:
                if item['category_name'] != current_category:
                    print(f"\n{item['category_name']}:")
                    current_category = item['category_name']
                print(f"  {item['item_id']}. {item['item_name']} ({item['unit']})")

            inventory_item_id = int(input("\nEnter Inventory Item ID: "))

            # Get unit for context
            cursor.execute("SELECT unit FROM inventory_items WHERE item_id = %s", (inventory_item_id,))
            inv_item = cursor.fetchone()

            if not inv_item:
                print("Inventory item not found!")
                return

            quantity_needed = float(input(f"Enter quantity needed per serving ({inv_item['unit']}): "))

            insert_query = """
            INSERT INTO menu_item_ingredients (menu_item_id, inventory_item_id, quantity_needed)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (menu_item_id, inventory_item_id, quantity_needed))
            db.conn.commit()

            print("\n✓ Ingredient added successfully!")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def update_ingredient_quantity(self):
        """Update quantity needed for an ingredient"""
        try:
            self.view_all_menu_ingredients()

            menu_item_id = int(input("\nEnter Menu Item ID: "))

            # Show current ingredients for this menu item
            query = """
            SELECT 
                mii.inventory_item_id,
                ii.item_name,
                mii.quantity_needed,
                ii.unit
            FROM menu_item_ingredients mii
            JOIN inventory_items ii ON ii.item_id = mii.inventory_item_id
            WHERE mii.menu_item_id = %s
            """
            cursor.execute(query, (menu_item_id,))
            ingredients = cursor.fetchall()

            if not ingredients:
                print("No ingredients found for this menu item!")
                return

            print("\nCurrent ingredients:")
            for ing in ingredients:
                print(
                    f"{ing['inventory_item_id']}. {ing['item_name']}: {float(ing['quantity_needed']):.3f} {ing['unit']}")

            inventory_item_id = int(input("\nEnter Inventory Item ID: "))
            new_quantity = float(input("Enter new quantity needed: "))

            update_query = """
            UPDATE menu_item_ingredients 
            SET quantity_needed = %s
            WHERE menu_item_id = %s AND inventory_item_id = %s
            """
            cursor.execute(update_query, (new_quantity, menu_item_id, inventory_item_id))
            db.conn.commit()

            print("\n✓ Quantity updated successfully!")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def remove_menu_ingredient(self):
        """Remove ingredient from menu item"""
        try:
            self.view_all_menu_ingredients()

            menu_item_id = int(input("\nEnter Menu Item ID: "))
            inventory_item_id = int(input("Enter Inventory Item ID to remove: "))

            delete_query = """
            DELETE FROM menu_item_ingredients 
            WHERE menu_item_id = %s AND inventory_item_id = %s
            """
            cursor.execute(delete_query, (menu_item_id, inventory_item_id))
            db.conn.commit()

            print("\n✓ Ingredient removed successfully!")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    # ========== CATEGORIES MANAGEMENT ==========

    def categories_menu(self):
        """Categories management"""
        while True:
            print("\n" + "=" * 70)
            print("CATEGORIES MANAGEMENT")
            print("=" * 70)
            print("1. View All Inventory Categories")
            print("2. Add Inventory Category")
            print("3. Update Inventory Category")
            print("4. Delete Inventory Category")
            print("5. View All Menu Categories")
            print("6. Add Menu Category")
            print("7. Update Menu Category")
            print("8. Delete Menu Category")
            print("9. Back")

            try:
                choice = int(input("\nSelect option: "))

                if choice == 1:
                    self.view_inventory_categories()
                elif choice == 2:
                    self.add_inventory_category()
                elif choice == 3:
                    self.update_inventory_category()
                elif choice == 4:
                    self.delete_inventory_category()
                elif choice == 5:
                    self.view_menu_categories()
                elif choice == 6:
                    self.add_menu_category()
                elif choice == 7:
                    self.update_menu_category()
                elif choice == 8:
                    self.delete_menu_category()
                elif choice == 9:
                    break
                else:
                    print("Invalid option!")
            except ValueError:
                print("Invalid input!")

    def view_inventory_categories(self):
        """View all inventory categories"""
        try:
            query = """
            SELECT ic.*, COUNT(ii.item_id) as item_count
            FROM inventory_categories ic
            LEFT JOIN inventory_items ii ON ii.category_id = ic.category_id
            GROUP BY ic.category_id
            ORDER BY ic.category_name
            """
            cursor.execute(query)
            categories = cursor.fetchall()

            print("\n" + "=" * 60)
            print("INVENTORY CATEGORIES")
            print("=" * 60)
            print(f"{'ID':<5} {'Category Name':<40} {'Item Count':<15}")
            print("-" * 60)

            for cat in categories:
                print(f"{cat['category_id']:<5} {cat['category_name']:<40} {cat['item_count']:<15}")

            print("=" * 60)

        except Exception as e:
            print(f"Error: {e}")

    def add_inventory_category(self):
        """Add new inventory category"""
        try:
            category_name = input("\nEnter category name: ").strip()

            cursor.execute("INSERT INTO inventory_categories (category_name) VALUES (%s)", (category_name,))
            db.conn.commit()

            print(f"\n✓ Category '{category_name}' added successfully!")

        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def update_inventory_category(self):
        """Update inventory category"""
        try:
            self.view_inventory_categories()

            category_id = int(input("\nEnter category ID to update: "))
            new_name = input("Enter new category name: ").strip()

            cursor.execute("UPDATE inventory_categories SET category_name = %s WHERE category_id = %s",
                           (new_name, category_id))
            db.conn.commit()

            print("\n✓ Category updated successfully!")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def delete_inventory_category(self):
        """Delete inventory category"""
        try:
            self.view_inventory_categories()

            category_id = int(input("\nEnter category ID to delete: "))

            # Check if category has items
            cursor.execute("SELECT COUNT(*) as count FROM inventory_items WHERE category_id = %s", (category_id,))
            result = cursor.fetchone()

            if result['count'] > 0:
                print(f"\n⚠️ Cannot delete! This category has {result['count']} items.")
                print("Please move or delete all items first.")
                return

            confirm = input("Type 'DELETE' to confirm: ").strip()

            if confirm == 'DELETE':
                cursor.execute("DELETE FROM inventory_categories WHERE category_id = %s", (category_id,))
                db.conn.commit()
                print("\n✓ Category deleted successfully!")
            else:
                print("Deletion cancelled.")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def view_menu_categories(self):
        """View all menu categories"""
        try:
            query = """
            SELECT mc.*, COUNT(mi.menu_item_id) as item_count
            FROM menu_categories mc
            LEFT JOIN menu_items mi ON mi.category_id = mc.category_id
            GROUP BY mc.category_id
            ORDER BY mc.category_name
            """
            cursor.execute(query)
            categories = cursor.fetchall()

            print("\n" + "=" * 60)
            print("MENU CATEGORIES")
            print("=" * 60)
            print(f"{'ID':<5} {'Category Name':<40} {'Item Count':<15}")
            print("-" * 60)

            for cat in categories:
                print(f"{cat['category_id']:<5} {cat['category_name']:<40} {cat['item_count']:<15}")

            print("=" * 60)

        except Exception as e:
            print(f"Error: {e}")

    def add_menu_category(self):
        """Add new menu category"""
        try:
            category_name = input("\nEnter category name: ").strip()

            cursor.execute("INSERT INTO menu_categories (category_name) VALUES (%s)", (category_name,))
            db.conn.commit()

            print(f"\n✓ Category '{category_name}' added successfully!")

        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def update_menu_category(self):
        """Update menu category"""
        try:
            self.view_menu_categories()

            category_id = int(input("\nEnter category ID to update: "))
            new_name = input("Enter new category name: ").strip()

            cursor.execute("UPDATE menu_categories SET category_name = %s WHERE category_id = %s",
                           (new_name, category_id))
            db.conn.commit()

            print("\n✓ Category updated successfully!")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def delete_menu_category(self):
        """Delete menu category"""
        try:
            self.view_menu_categories()

            category_id = int(input("\nEnter category ID to delete: "))

            # Check if category has items
            cursor.execute("SELECT COUNT(*) as count FROM menu_items WHERE category_id = %s", (category_id,))
            result = cursor.fetchone()

            if result['count'] > 0:
                print(f"\n⚠️ Cannot delete! This category has {result['count']} menu items.")
                print("Please move or delete all menu items first.")
                return

            confirm = input("Type 'DELETE' to confirm: ").strip()

            if confirm == 'DELETE':
                cursor.execute("DELETE FROM menu_categories WHERE category_id = %s", (category_id,))
                db.conn.commit()
                print("\n✓ Category deleted successfully!")
            else:
                print("Deletion cancelled.")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    # ========== INVENTORY REPORTS ==========

    def inventory_reports_menu(self):
        """Inventory reports menu"""
        while True:
            print("\n" + "=" * 70)
            print("INVENTORY REPORTS")
            print("=" * 70)
            print("1. Stock Valuation Report")
            print("2. Inventory Transactions Report")
            print("3. Ingredient Usage Report")
            print("4. Low Stock Alert Report")
            print("5. Back")

            try:
                choice = int(input("\nSelect option: "))

                if choice == 1:
                    self.stock_valuation_report()
                elif choice == 2:
                    self.inventory_transactions_report()
                elif choice == 3:
                    self.ingredient_usage_report()
                elif choice == 4:
                    self.view_low_stock()
                elif choice == 5:
                    break
                else:
                    print("Invalid option!")
            except ValueError:
                print("Invalid input!")

    def stock_valuation_report(self):
        """Stock valuation report"""
        try:
            query = """
            SELECT 
                ic.category_name,
                ii.item_name,
                ii.quantity_in_stock,
                ii.unit,
                ii.unit_cost,
                (ii.quantity_in_stock * ii.unit_cost) as total_value
            FROM inventory_items ii
            JOIN inventory_categories ic ON ic.category_id = ii.category_id
            ORDER BY ic.category_name, total_value DESC
            """
            cursor.execute(query)
            items = cursor.fetchall()

            print("\n" + "=" * 100)
            print("STOCK VALUATION REPORT")
            print("=" * 100)
            print(f"{'Category':<20} {'Item':<30} {'Quantity':<20} {'Unit Cost':<15} {'Total Value':<15}")
            print("-" * 100)

            current_category = None
            category_total = 0
            grand_total = 0

            for item in items:
                if current_category != item['category_name']:
                    if current_category is not None:
                        print("-" * 100)
                        print(f"{'Category Total:':<85} ₱{category_total:,.2f}")
                        print()
                    current_category = item['category_name']
                    category_total = 0

                qty_display = f"{float(item['quantity_in_stock']):.2f} {item['unit']}"
                value = float(item['total_value'])
                category_total += value
                grand_total += value

                print(f"{item['category_name']:<20} {item['item_name']:<30} {qty_display:<20} "
                      f"₱{float(item['unit_cost']):<14.2f} ₱{value:,.2f}")

            print("-" * 100)
            print(f"{'Category Total:':<85} ₱{category_total:,.2f}")
            print("=" * 100)
            print(f"{'GRAND TOTAL:':<85} ₱{grand_total:,.2f}")
            print("=" * 100)

        except Exception as e:
            print(f"Error: {e}")

    def inventory_transactions_report(self):
        """Inventory transactions report"""
        try:
            print("\n1. All transactions")
            print("2. Transactions by date range")
            print("3. Transactions by type")

            choice = int(input("\nSelect option: "))

            if choice == 1:
                query = """
                SELECT 
                    it.transaction_id,
                    it.transaction_date,
                    ii.item_name,
                    it.transaction_type,
                    it.quantity,
                    ii.unit
                FROM inventory_transactions it
                JOIN inventory_items ii ON ii.item_id = it.item_id
                ORDER BY it.transaction_date DESC
                LIMIT 50
                """
                cursor.execute(query)
            elif choice == 2:
                start_date = input("Enter start date (YYYY-MM-DD): ")
                end_date = input("Enter end date (YYYY-MM-DD): ")
                query = """
                SELECT 
                    it.transaction_id,
                    it.transaction_date,
                    ii.item_name,
                    it.transaction_type,
                    it.quantity,
                    ii.unit
                FROM inventory_transactions it
                JOIN inventory_items ii ON ii.item_id = it.item_id
                WHERE DATE(it.transaction_date) BETWEEN %s AND %s
                ORDER BY it.transaction_date DESC
                """
                cursor.execute(query, (start_date, end_date))
            elif choice == 3:
                print("\n1. Restock")
                print("2. Usage")
                print("3. Adjustment")
                type_choice = int(input("Select type: "))
                types = {1: 'restock', 2: 'usage', 3: 'adjustment'}
                trans_type = types.get(type_choice)

                query = """
                SELECT 
                    it.transaction_id,
                    it.transaction_date,
                    ii.item_name,
                    it.transaction_type,
                    it.quantity,
                    ii.unit
                FROM inventory_transactions it
                JOIN inventory_items ii ON ii.item_id = it.item_id
                WHERE it.transaction_type = %s
                ORDER BY it.transaction_date DESC
                LIMIT 50
                """
                cursor.execute(query, (trans_type,))
            else:
                print("Invalid option!")
                return

            transactions = cursor.fetchall()

            if not transactions:
                print("\nNo transactions found!")
                return

            print("\n" + "=" * 100)
            print("INVENTORY TRANSACTIONS REPORT")
            print("=" * 100)
            print(f"{'ID':<8} {'Date':<20} {'Item':<30} {'Type':<15} {'Quantity':<20}")
            print("-" * 100)

            for trans in transactions:
                qty_display = f"{float(trans['quantity']):.3f} {trans['unit']}"
                print(f"{trans['transaction_id']:<8} {str(trans['transaction_date']):<20} "
                      f"{trans['item_name']:<30} {trans['transaction_type']:<15} {qty_display:<20}")

            print("=" * 100)

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            print(f"Error: {e}")

    def ingredient_usage_report(self):
        """Ingredient usage report - shows which menu items use which ingredients"""
        try:
            print("\n1. View by Menu Item")
            print("2. View by Ingredient")

            choice = int(input("\nSelect option: "))

            if choice == 1:
                query = """
                SELECT 
                    mi.item_name as menu_item,
                    GROUP_CONCAT(
                        CONCAT(ii.item_name, ' (', mii.quantity_needed, ' ', ii.unit, ')')
                        SEPARATOR ', '
                    ) as ingredients
                FROM menu_items mi
                LEFT JOIN menu_item_ingredients mii ON mii.menu_item_id = mi.menu_item_id
                LEFT JOIN inventory_items ii ON ii.item_id = mii.inventory_item_id
                GROUP BY mi.menu_item_id
                ORDER BY mi.item_name
                """
                cursor.execute(query)
                results = cursor.fetchall()

                print("\n" + "=" * 100)
                print("INGREDIENTS BY MENU ITEM")
                print("=" * 100)

                for row in results:
                    print(f"\n{row['menu_item']}")
                    print(f"  Ingredients: {row['ingredients'] if row['ingredients'] else 'None configured'}")

                print("=" * 100)

            elif choice == 2:
                query = """
                SELECT 
                    ii.item_name as ingredient,
                    GROUP_CONCAT(
                        CONCAT(mi.item_name, ' (', mii.quantity_needed, ' ', ii.unit, ')')
                        SEPARATOR ', '
                    ) as used_in
                FROM inventory_items ii
                LEFT JOIN menu_item_ingredients mii ON mii.inventory_item_id = ii.item_id
                LEFT JOIN menu_items mi ON mi.menu_item_id = mii.menu_item_id
                WHERE ii.category_id IN (4, 5)
                GROUP BY ii.item_id
                ORDER BY ii.item_name
                """
                cursor.execute(query)
                results = cursor.fetchall()

                print("\n" + "=" * 100)
                print("MENU ITEMS BY INGREDIENT")
                print("=" * 100)

                for row in results:
                    print(f"\n{row['ingredient']}")
                    print(f"  Used in: {row['used_in'] if row['used_in'] else 'Not used in any menu item'}")

                print("=" * 100)

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            print(f"Error: {e}")