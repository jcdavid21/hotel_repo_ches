import database as db
from datetime import datetime, date, timedelta
import csv
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os

cursor = db.conn.cursor(dictionary=True)


class RestoKitchen:
    def __init__(self):
        self.guest_id = None
        self.guest_info = None
        self.categories = self.get_categories()
        self.cart = []
        self.current_booking_id = None

    def main(self):
        """Main menu"""
        while True:
            print("\n" + "=" * 50)
            print("=== RESTAURANT & KITCHEN MODULE ===")
            print("=" * 50)
            print("1. Take Orders")
            print("2. Sales Report")
            print("3. Inventory Management")
            print("4. Analytics & Reports (CSV/Graphs)")
            print("5. Exit")
            print("=" * 50)

            try:
                choice = int(input("Select option: "))

                if choice == 1:
                    self.take_orders()
                elif choice == 2:
                    self.sales_report_menu()
                elif choice == 3:
                    self.inventory_management()
                elif choice == 4:
                    self.analytics_menu()
                elif choice == 5:
                    print("Exiting Restaurant & Kitchen Module...")
                    break
                else:
                    print("Invalid option! Please select 1-5.")
            except ValueError:
                print("Invalid input! Please enter a number.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def search_guest(self):
        """Search and select a guest"""
        print("\n" + "=" * 50)
        print("GUEST SEARCH")
        print("=" * 50)
        print("1. Search by Guest ID")
        print("2. Search by Name")
        print("3. View All Guests")
        print("4. Cancel")

        try:
            choice = int(input("\nSelect option: "))

            if choice == 1:
                guest_id = int(input("Enter Guest ID: "))
                return self.get_guest_by_id(guest_id)
            elif choice == 2:
                name = input("Enter guest name (first or last): ").strip()
                return self.get_guest_by_name(name)
            elif choice == 3:
                return self.select_from_all_guests()
            elif choice == 4:
                return None
            else:
                print("Invalid option!")
                return None
        except ValueError:
            print("Invalid input!")
            return None

    def get_guest_by_id(self, guest_id):
        """Get guest by ID"""
        query = "SELECT * FROM guests WHERE guest_id = %s"
        cursor.execute(query, (guest_id,))
        guest = cursor.fetchone()

        if guest:
            self.display_guest_info(guest)
            confirm = input("\nIs this the correct guest? (yes/no): ").lower()
            if confirm == 'yes':
                return guest
        else:
            print("Guest not found!")
        return None

    def get_guest_by_name(self, name):
        """Search guests by name"""
        query = """
        SELECT * FROM guests 
        WHERE first_name LIKE %s OR last_name LIKE %s
        """
        search_term = f"%{name}%"
        cursor.execute(query, (search_term, search_term))
        guests = cursor.fetchall()

        if not guests:
            print("No guests found!")
            return None

        if len(guests) == 1:
            self.display_guest_info(guests[0])
            confirm = input("\nIs this the correct guest? (yes/no): ").lower()
            if confirm == 'yes':
                return guests[0]
            return None

        # Multiple guests found
        print(f"\nFound {len(guests)} guests:")
        print("-" * 80)
        print(f"{'ID':<5} {'Name':<30} {'Email':<30} {'Phone':<15}")
        print("-" * 80)

        for guest in guests:
            name = f"{guest['first_name']} {guest['last_name']}"
            print(f"{guest['guest_id']:<5} {name:<30} {guest['email']:<30} {guest['phone']:<15}")

        try:
            guest_id = int(input("\nEnter Guest ID to select: "))
            for guest in guests:
                if guest['guest_id'] == guest_id:
                    self.display_guest_info(guest)
                    return guest
            print("Invalid Guest ID!")
        except ValueError:
            print("Invalid input!")

        return None

    def select_from_all_guests(self):
        """Display all guests and let user select"""
        query = "SELECT * FROM guests ORDER BY last_name, first_name"
        cursor.execute(query)
        guests = cursor.fetchall()

        if not guests:
            print("No guests in database!")
            return None

        print("\n" + "=" * 80)
        print("ALL GUESTS")
        print("=" * 80)
        print(f"{'ID':<5} {'Name':<30} {'Email':<30} {'Phone':<15}")
        print("-" * 80)

        for guest in guests:
            name = f"{guest['first_name']} {guest['last_name']}"
            print(f"{guest['guest_id']:<5} {name:<30} {guest['email']:<30} {guest['phone']:<15}")

        print("=" * 80)

        try:
            guest_id = int(input("\nEnter Guest ID to select (0 to cancel): "))
            if guest_id == 0:
                return None

            for guest in guests:
                if guest['guest_id'] == guest_id:
                    self.display_guest_info(guest)
                    return guest
            print("Invalid Guest ID!")
        except ValueError:
            print("Invalid input!")

        return None

    def display_guest_info(self, guest):
        """Display guest information"""
        print("\n" + "=" * 50)
        print("GUEST INFORMATION")
        print("=" * 50)
        print(f"Guest ID:     {guest['guest_id']}")
        print(f"Name:         {guest['first_name']} {guest['last_name']}")
        print(f"Email:        {guest['email']}")
        print(f"Phone:        {guest['phone']}")
        print(f"Nationality:  {guest['nationality']}")

        # Check for active booking
        booking_query = """
        SELECT b.*, r.room_number, rt.type_name 
        FROM bookings b
        JOIN rooms r ON r.room_id = b.room_id
        JOIN room_types rt ON rt.room_type_id = r.room_type_id
        WHERE b.guest_id = %s AND b.booking_status IN ('confirmed', 'checked_in')
        ORDER BY b.check_in_date DESC LIMIT 1
        """
        cursor.execute(booking_query, (guest['guest_id'],))
        booking = cursor.fetchone()

        if booking:
            print(f"\nActive Booking:")
            print(f"  Booking ID:   {booking['booking_id']}")
            print(f"  Room:         {booking['room_number']} ({booking['type_name']})")
            print(f"  Check-in:     {booking['check_in_date']}")
            print(f"  Check-out:    {booking['check_out_date']}")
            print(f"  Status:       {booking['booking_status']}")
        else:
            print("\nNo active booking")

        print("=" * 50)

    def get_categories(self):
        """Fetch all menu categories"""
        query = "SELECT * FROM menu_categories ORDER BY category_id"
        cursor.execute(query)
        results = cursor.fetchall()
        return results

    def get_menu_items(self, category_id):
        """Get menu items by category"""
        query = """
        SELECT mi.*, mc.category_name 
        FROM menu_items mi 
        JOIN menu_categories mc ON mc.category_id = mi.category_id
        WHERE mi.category_id = %s AND mi.is_available = 1 
        ORDER BY mi.price ASC
        """
        cursor.execute(query, (category_id,))
        result = cursor.fetchall()
        return result

    def get_active_booking(self, guest_id):
        """Get active booking for the guest"""
        query = """
        SELECT booking_id FROM bookings 
        WHERE guest_id = %s AND booking_status IN ('confirmed', 'checked_in')
        ORDER BY check_in_date DESC LIMIT 1
        """
        cursor.execute(query, (guest_id,))
        result = cursor.fetchone()
        return result['booking_id'] if result else None

    def display_cart(self):
        """Display current cart contents"""
        if not self.cart:
            print("\nYour cart is empty!")
            return

        print("\n" + "=" * 70)
        print("YOUR CART")
        print("=" * 70)
        print(f"{'Item Name':<30} {'Quantity':<10} {'Price':<10} {'Subtotal':<10}")
        print("-" * 70)

        total = 0
        for item in self.cart:
            subtotal = item['quantity'] * item['price']
            total += subtotal
            print(f"{item['item_name']:<30} {item['quantity']:<10} ₱{item['price']:<9.2f} ₱{subtotal:<9.2f}")

        print("-" * 70)
        print(f"{'TOTAL:':<50} ₱{total:.2f}")
        print("=" * 70)

    def take_orders(self):
        """Main ordering function"""
        # Search and select guest
        guest = self.search_guest()

        if not guest:
            print("Order cancelled - no guest selected.")
            return

        self.guest_id = guest['guest_id']
        self.guest_info = guest
        self.current_booking_id = self.get_active_booking(self.guest_id)
        self.cart = []  # Reset cart

        print(f"\n{'=' * 50}")
        print(f"Processing order for: {guest['first_name']} {guest['last_name']}")
        print(f"{'=' * 50}")

        while True:
            print("\n--- ORDER MENU ---")
            print("1. Browse Menu & Add Items")
            print("2. View Cart")
            print("3. Checkout")
            print("4. Clear Cart")
            print("5. Cancel Order")

            try:
                choice = int(input("\nSelect option: "))

                if choice == 1:
                    self.browse_and_add_items()
                elif choice == 2:
                    self.display_cart()
                elif choice == 3:
                    if self.cart:
                        self.checkout()
                        break  # Exit after successful checkout
                    else:
                        print("Your cart is empty! Add items first.")
                elif choice == 4:
                    self.cart.clear()
                    print("Cart cleared!")
                elif choice == 5:
                    print("Order cancelled!")
                    break
                else:
                    print("Invalid option!")
            except ValueError:
                print("Invalid input! Please enter a number.")

    def browse_and_add_items(self):
        """Browse menu categories and add items to cart"""
        try:
            print("\n" + "=" * 50)
            print("MENU CATEGORIES")
            print("=" * 50)

            for row in self.categories:
                print(f"{row['category_id']}. {row['category_name']}")

            print("0. Back")

            category_choice = int(input("\nSelect category: "))

            if category_choice == 0:
                return

            if category_choice > len(self.categories) or category_choice <= 0:
                print("Invalid category!")
                return

            items = self.get_menu_items(category_choice)

            if not items:
                print("No items available in this category!")
                return

            print(f"\n{'=' * 70}")
            print(f"{items[0]['category_name'].upper()} MENU")
            print(f"{'=' * 70}")
            print(f"{'ID':<5} {'Item Name':<35} {'Price':<10}")
            print("-" * 70)

            for row in items:
                print(f"{row['menu_item_id']:<5} {row['item_name']:<35} ₱{row['price']:<9.2f}")

            print("-" * 70)

            # Add item to cart
            item_id = int(input("\nEnter item ID to add (0 to cancel): "))

            if item_id == 0:
                return

            # Find the item
            selected_item = None
            for item in items:
                if item['menu_item_id'] == item_id:
                    selected_item = item
                    break

            if not selected_item:
                print("Invalid item ID!")
                return

            quantity = int(input(f"Enter quantity for {selected_item['item_name']}: "))

            if quantity <= 0:
                print("Invalid quantity!")
                return

            # Add to cart
            cart_item = {
                'menu_item_id': selected_item['menu_item_id'],
                'item_name': selected_item['item_name'],
                'price': float(selected_item['price']),
                'quantity': quantity
            }

            # Check if item already in cart
            found = False
            for item in self.cart:
                if item['menu_item_id'] == cart_item['menu_item_id']:
                    item['quantity'] += quantity
                    found = True
                    break

            if not found:
                self.cart.append(cart_item)

            print(f"\n✓ Added {quantity}x {selected_item['item_name']} to cart!")

        except ValueError:
            print("Invalid input! Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def checkout(self):
        """Process the order and save to database"""
        try:
            self.display_cart()

            print("\n--- ORDER TYPE ---")
            print("1. Dine In")
            print("2. Room Service")
            print("3. Takeaway")

            order_type_choice = int(input("Select order type: "))
            order_types = {1: 'dine_in', 2: 'room_service', 3: 'takeaway'}

            if order_type_choice not in order_types:
                print("Invalid order type!")
                return

            order_type = order_types[order_type_choice]

            # Calculate total
            total_amount = sum(item['quantity'] * item['price'] for item in self.cart)

            confirm = input(f"\nConfirm order? Total: ₱{total_amount:.2f} (yes/no): ").lower()

            if confirm != 'yes':
                print("Order cancelled!")
                return

            # Insert order into restaurant_orders
            insert_order_query = """
            INSERT INTO restaurant_orders 
            (booking_id, guest_id, order_type, total_amount, order_status, order_date)
            VALUES (%s, %s, %s, %s, 'pending', NOW())
            """
            cursor.execute(insert_order_query,
                           (self.current_booking_id, self.guest_id, order_type, total_amount))

            order_id = cursor.lastrowid

            # Insert order items
            for item in self.cart:
                insert_item_query = """
                INSERT INTO order_items 
                (order_id, menu_item_id, quantity, unit_price)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_item_query,
                               (order_id, item['menu_item_id'], item['quantity'], item['price']))

            # Update inventory (simplified)
            self.update_inventory_usage()

            db.conn.commit()

            print("\n" + "=" * 50)
            print("✓ ORDER PLACED SUCCESSFULLY!")
            print(f"Order ID: {order_id}")
            print(f"Guest: {self.guest_info['first_name']} {self.guest_info['last_name']}")
            print(f"Total Amount: ₱{total_amount:.2f}")
            print(f"Order Type: {order_type.replace('_', ' ').title()}")
            print("=" * 50)

            # Clear cart
            self.cart.clear()

        except Exception as e:
            db.conn.rollback()
            print(f"Error processing order: {e}")

    def update_inventory_usage(self):
        """Update inventory based on order (simplified version)"""
        try:
            for item in self.cart:
                query = """
                INSERT INTO inventory_transactions 
                (item_id, transaction_type, quantity, transaction_date)
                VALUES 
                ((SELECT item_id FROM inventory_items WHERE item_name = 'Rice' LIMIT 1), 
                 'usage', %s, NOW())
                """
                cursor.execute(query, (item['quantity'] * 0.5,))

                update_query = """
                UPDATE inventory_items 
                SET quantity_in_stock = quantity_in_stock - %s
                WHERE item_name = 'Rice' AND quantity_in_stock >= %s
                """
                cursor.execute(update_query, (item['quantity'] * 0.5, item['quantity'] * 0.5))

        except Exception as e:
            print(f"Warning: Could not update inventory - {e}")

    def sales_report_menu(self):
        """Sales report menu"""
        while True:
            print("\n" + "=" * 50)
            print("SALES REPORTS")
            print("=" * 50)
            print("1. Daily Sales Report")
            print("2. Date Range Sales Report")
            print("3. Sales by Guest")
            print("4. Sales by Category")
            print("5. Top Selling Items")
            print("6. Back to Main Menu")

            try:
                choice = int(input("\nSelect option: "))

                if choice == 1:
                    self.daily_sales_report()
                elif choice == 2:
                    self.date_range_sales_report()
                elif choice == 3:
                    self.sales_by_guest()
                elif choice == 4:
                    self.sales_by_category()
                elif choice == 5:
                    self.top_selling_items()
                elif choice == 6:
                    break
                else:
                    print("Invalid option!")
            except ValueError:
                print("Invalid input!")

    def daily_sales_report(self):
        """Display daily sales report"""
        try:
            print("\n" + "=" * 70)
            print("DAILY SALES REPORT")
            print("=" * 70)

            report_date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")

            if not report_date:
                report_date = date.today()

            query = """
            SELECT 
                ro.order_id,
                ro.order_type,
                ro.total_amount,
                ro.order_status,
                ro.order_date,
                g.first_name,
                g.last_name
            FROM restaurant_orders ro
            JOIN guests g ON g.guest_id = ro.guest_id
            WHERE DATE(ro.order_date) = %s
            ORDER BY ro.order_date DESC
            """
            cursor.execute(query, (report_date,))
            orders = cursor.fetchall()

            if not orders:
                print(f"\nNo orders found for {report_date}")
                return

            print(f"\nDate: {report_date}")
            print("-" * 70)
            print(f"{'Order ID':<10} {'Guest':<25} {'Type':<15} {'Amount':<12} {'Status':<12}")
            print("-" * 70)

            total_sales = 0
            for order in orders:
                guest_name = f"{order['first_name']} {order['last_name']}"
                print(f"{order['order_id']:<10} {guest_name:<25} {order['order_type']:<15} "
                      f"₱{order['total_amount']:<11.2f} {order['order_status']:<12}")
                total_sales += float(order['total_amount'])

            print("-" * 70)
            print(f"Total Orders: {len(orders)}")
            print(f"Total Sales: ₱{total_sales:.2f}")
            print("=" * 70)

        except Exception as e:
            print(f"Error generating report: {e}")

    def date_range_sales_report(self):
        """Sales report for a date range"""
        try:
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")

            query = """
            SELECT 
                DATE(ro.order_date) as order_date,
                COUNT(ro.order_id) as total_orders,
                SUM(ro.total_amount) as daily_sales
            FROM restaurant_orders ro
            WHERE DATE(ro.order_date) BETWEEN %s AND %s
            GROUP BY DATE(ro.order_date)
            ORDER BY order_date
            """
            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()

            if not results:
                print("No sales data found for this date range!")
                return

            print("\n" + "=" * 60)
            print(f"SALES REPORT: {start_date} to {end_date}")
            print("=" * 60)
            print(f"{'Date':<15} {'Orders':<15} {'Sales':<15}")
            print("-" * 60)

            total_orders = 0
            total_sales = 0

            for row in results:
                print(f"{str(row['order_date']):<15} {row['total_orders']:<15} ₱{float(row['daily_sales']):<14.2f}")
                total_orders += row['total_orders']
                total_sales += float(row['daily_sales'])

            print("-" * 60)
            print(f"{'TOTAL:':<15} {total_orders:<15} ₱{total_sales:<14.2f}")
            print("=" * 60)

        except Exception as e:
            print(f"Error: {e}")

    def sales_by_guest(self):
        """View sales for specific guest or all guests"""
        print("\n1. Search specific guest")
        print("2. View all guests' sales")

        try:
            choice = int(input("Select option: "))

            if choice == 1:
                guest = self.search_guest()
                if not guest:
                    return

                query = """
                SELECT 
                    ro.order_id,
                    ro.order_date,
                    ro.order_type,
                    ro.total_amount,
                    ro.order_status
                FROM restaurant_orders ro
                WHERE ro.guest_id = %s
                ORDER BY ro.order_date DESC
                """
                cursor.execute(query, (guest['guest_id'],))
                orders = cursor.fetchall()

                if not orders:
                    print(f"\nNo orders found for {guest['first_name']} {guest['last_name']}")
                    return

                print(f"\n{'=' * 70}")
                print(f"ORDERS FOR: {guest['first_name']} {guest['last_name']}")
                print(f"{'=' * 70}")
                print(f"{'Order ID':<12} {'Date':<20} {'Type':<15} {'Amount':<12} {'Status':<12}")
                print("-" * 70)

                total = 0
                for order in orders:
                    print(f"{order['order_id']:<12} {str(order['order_date']):<20} {order['order_type']:<15} "
                          f"₱{float(order['total_amount']):<11.2f} {order['order_status']:<12}")
                    total += float(order['total_amount'])

                print("-" * 70)
                print(f"Total Orders: {len(orders)}")
                print(f"Total Spent: ₱{total:.2f}")
                print("=" * 70)

            elif choice == 2:
                query = """
                SELECT 
                    g.guest_id,
                    g.first_name,
                    g.last_name,
                    COUNT(ro.order_id) as total_orders,
                    SUM(ro.total_amount) as total_spent
                FROM guests g
                LEFT JOIN restaurant_orders ro ON ro.guest_id = g.guest_id
                GROUP BY g.guest_id
                HAVING total_orders > 0
                ORDER BY total_spent DESC
                """
                cursor.execute(query)
                results = cursor.fetchall()

                if not results:
                    print("\nNo orders found!")
                    return

                print("\n" + "=" * 70)
                print("SALES BY GUEST")
                print("=" * 70)
                print(f"{'ID':<5} {'Guest Name':<30} {'Orders':<12} {'Total Spent':<15}")
                print("-" * 70)

                for row in results:
                    name = f"{row['first_name']} {row['last_name']}"
                    print(
                        f"{row['guest_id']:<5} {name:<30} {row['total_orders']:<12} ₱{float(row['total_spent']):<14.2f}")

                print("=" * 70)

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            print(f"Error: {e}")

    def sales_by_category(self):
        """View sales by menu category"""
        try:
            start_date = input("Enter start date (YYYY-MM-DD) or press Enter for all time: ")
            end_date = input("Enter end date (YYYY-MM-DD) or press Enter for all time: ")

            if start_date and end_date:
                query = """
                SELECT 
                    mc.category_name,
                    COUNT(DISTINCT ro.order_id) as orders,
                    SUM(oi.quantity) as items_sold,
                    SUM(oi.quantity * oi.unit_price) as total_sales
                FROM restaurant_orders ro
                JOIN order_items oi ON oi.order_id = ro.order_id
                JOIN menu_items mi ON mi.menu_item_id = oi.menu_item_id
                JOIN menu_categories mc ON mc.category_id = mi.category_id
                WHERE DATE(ro.order_date) BETWEEN %s AND %s
                GROUP BY mc.category_id, mc.category_name
                ORDER BY total_sales DESC
                """
                cursor.execute(query, (start_date, end_date))
            else:
                query = """
                SELECT 
                    mc.category_name,
                    COUNT(DISTINCT ro.order_id) as orders,
                    SUM(oi.quantity) as items_sold,
                    SUM(oi.quantity * oi.unit_price) as total_sales
                FROM restaurant_orders ro
                JOIN order_items oi ON oi.order_id = ro.order_id
                JOIN menu_items mi ON mi.menu_item_id = oi.menu_item_id
                JOIN menu_categories mc ON mc.category_id = mi.category_id
                GROUP BY mc.category_id, mc.category_name
                ORDER BY total_sales DESC
                """
                cursor.execute(query)

            results = cursor.fetchall()

            if not results:
                print("\nNo sales data found!")
                return

            print("\n" + "=" * 75)
            print("SALES BY CATEGORY")
            print("=" * 75)
            print(f"{'Category':<25} {'Orders':<12} {'Items Sold':<15} {'Total Sales':<15}")
            print("-" * 75)

            total_sales = 0
            for row in results:
                print(
                    f"{row['category_name']:<25} {row['orders']:<12} {row['items_sold']:<15} ₱{float(row['total_sales']):<14.2f}")
                total_sales += float(row['total_sales'])

            print("-" * 75)
            print(f"{'TOTAL:':<52} ₱{total_sales:.2f}")
            print("=" * 75)

        except Exception as e:
            print(f"Error: {e}")

    def top_selling_items(self):
        """Display top selling menu items"""
        try:
            limit = int(input("Enter number of top items to display (default 10): ") or "10")

            query = """
            SELECT 
                mi.item_name,
                mc.category_name,
                SUM(oi.quantity) as total_sold,
                SUM(oi.quantity * oi.unit_price) as total_revenue,
                mi.price as current_price
            FROM order_items oi
            JOIN menu_items mi ON mi.menu_item_id = oi.menu_item_id
            JOIN menu_categories mc ON mc.category_id = mi.category_id
            JOIN restaurant_orders ro ON ro.order_id = oi.order_id
            GROUP BY mi.menu_item_id, mi.item_name, mc.category_name, mi.price
            ORDER BY total_sold DESC
            LIMIT %s
            """
            cursor.execute(query, (limit,))
            results = cursor.fetchall()

            if not results:
                print("\nNo sales data found!")
                return

            print("\n" + "=" * 90)
            print(f"TOP {limit} SELLING ITEMS")
            print("=" * 90)
            print(f"{'Rank':<6} {'Item Name':<30} {'Category':<15} {'Sold':<10} {'Revenue':<15}")
            print("-" * 90)

            for idx, row in enumerate(results, 1):
                print(f"{idx:<6} {row['item_name']:<30} {row['category_name']:<15} "
                      f"{row['total_sold']:<10} ₱{float(row['total_revenue']):<14.2f}")

            print("=" * 90)

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            print(f"Error: {e}")

    def inventory_management(self):
        """Display and manage inventory"""
        while True:
            print("\n" + "=" * 70)
            print("INVENTORY MANAGEMENT")
            print("=" * 70)
            print("1. View All Inventory")
            print("2. View Low Stock Items")
            print("3. View Inventory by Category")
            print("4. Add Stock (Restock)")
            print("5. Back to Main Menu")

            try:
                choice = int(input("\nSelect option: "))

                if choice == 1:
                    self.view_all_inventory()
                elif choice == 2:
                    self.view_low_stock()
                elif choice == 3:
                    self.view_inventory_by_category()
                elif choice == 4:
                    self.restock_item()
                elif choice == 5:
                    break
                else:
                    print("Invalid option!")
            except ValueError:
                print("Invalid input! Please enter a number.")

    def view_all_inventory(self):
        """Display all inventory items"""
        try:
            query = """
            SELECT 
                ii.item_id,
                ii.item_name,
                ic.category_name,
                ii.quantity_in_stock,
                ii.minimum_quantity,
                ii.unit_cost
            FROM inventory_items ii
            JOIN inventory_categories ic ON ic.category_id = ii.category_id
            ORDER BY ii.item_id ASC
            """
            cursor.execute(query)
            items = cursor.fetchall()

            print("\n" + "=" * 90)
            print("ALL INVENTORY ITEMS")
            print("=" * 90)
            print(f"{'ID':<5} {'Item Name':<30} {'Category':<20} {'Stock':<10} {'Min':<8} {'Cost':<10}")
            print("-" * 90)

            for item in items:
                status = "⚠️ LOW" if float(item['quantity_in_stock']) <= float(item['minimum_quantity']) else ""
                print(f"{item['item_id']:<5} {item['item_name']:<30} {item['category_name']:<20} "
                      f"{float(item['quantity_in_stock']):<10.2f} {float(item['minimum_quantity']):<8.2f} "
                      f"₱{float(item['unit_cost']):<9.2f} {status}")

            print("=" * 90)

        except Exception as e:
            print(f"Error viewing inventory: {e}")

    def view_low_stock(self):
        """Display items below minimum quantity"""
        try:
            query = """
            SELECT 
                ii.item_id,
                ii.item_name,
                ic.category_name,
                ii.quantity_in_stock,
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

            print("\n" + "=" * 90)
            print("⚠️ LOW STOCK ITEMS - RESTOCK NEEDED")
            print("=" * 90)
            print(f"{'ID':<5} {'Item Name':<30} {'Category':<20} {'Stock':<10} {'Min':<10}")
            print("-" * 90)

            for item in items:
                shortage = float(item['minimum_quantity']) - float(item['quantity_in_stock'])
                print(f"{item['item_id']:<5} {item['item_name']:<30} {item['category_name']:<20} "
                      f"{float(item['quantity_in_stock']):<10.2f} {float(item['minimum_quantity']):<10.2f} "
                      f"(Need: {shortage:.2f})")

            print("=" * 90)

        except Exception as e:
            print(f"Error viewing low stock: {e}")

    def view_inventory_by_category(self):
        """Display inventory filtered by category"""
        try:
            query = "SELECT * FROM inventory_categories ORDER BY category_id"
            cursor.execute(query)
            categories = cursor.fetchall()

            print("\n--- INVENTORY CATEGORIES ---")
            for cat in categories:
                print(f"{cat['category_id']}. {cat['category_name']}")

            cat_id = int(input("\nSelect category: "))

            item_query = """
            SELECT 
                ii.item_id,
                ii.item_name,
                ii.quantity_in_stock,
                ii.minimum_quantity,
                ii.unit_cost
            FROM inventory_items ii
            WHERE ii.category_id = %s
            ORDER BY ii.item_id ASC
            """
            cursor.execute(item_query, (cat_id,))
            items = cursor.fetchall()

            if not items:
                print("No items in this category!")
                return

            print("\n" + "=" * 80)
            print(f"{'ID':<5} {'Item Name':<35} {'Stock':<12} {'Min':<12} {'Cost':<10}")
            print("-" * 80)

            for item in items:
                status = "⚠️" if float(item['quantity_in_stock']) <= float(item['minimum_quantity']) else ""
                print(f"{item['item_id']:<5} {item['item_name']:<35} "
                      f"{float(item['quantity_in_stock']):<12.2f} "
                      f"{float(item['minimum_quantity']):<12.2f} "
                      f"₱{float(item['unit_cost']):<9.2f} {status}")

            print("=" * 80)

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            print(f"Error: {e}")

    def restock_item(self):
        """Add stock to inventory"""
        try:
            item_id = int(input("\nEnter item ID to restock: "))

            query = "SELECT * FROM inventory_items WHERE item_id = %s"
            cursor.execute(query, (item_id,))
            item = cursor.fetchone()

            if not item:
                print("Item not found!")
                return

            print(f"\nItem: {item['item_name']}")
            print(f"Current Stock: {float(item['quantity_in_stock']):.2f}")

            quantity = float(input("Enter quantity to add: "))

            if quantity <= 0:
                print("Invalid quantity!")
                return

            update_query = """
            UPDATE inventory_items 
            SET quantity_in_stock = quantity_in_stock + %s
            WHERE item_id = %s
            """
            cursor.execute(update_query, (quantity, item_id))

            transaction_query = """
            INSERT INTO inventory_transactions 
            (item_id, transaction_type, quantity, transaction_date)
            VALUES (%s, 'restock', %s, NOW())
            """
            cursor.execute(transaction_query, (item_id, quantity))

            db.conn.commit()

            print(f"\n✓ Successfully added {quantity:.2f} units to {item['item_name']}")
            print(f"New stock level: {float(item['quantity_in_stock']) + quantity:.2f}")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error restocking: {e}")

    def analytics_menu(self):
        """Analytics and reporting menu with CSV export and graphs"""
        while True:
            print("\n" + "=" * 70)
            print("ANALYTICS & REPORTS")
            print("=" * 70)
            print("1. Export Sales Report to CSV")
            print("2. Export Inventory Report to CSV")
            print("3. Generate Sales Graph")
            print("4. Generate Category Sales Chart")
            print("5. Generate Inventory Status Chart")
            print("6. Generate Top Items Chart")
            print("7. Back to Main Menu")

            try:
                choice = int(input("\nSelect option: "))

                if choice == 1:
                    self.export_sales_csv()
                elif choice == 2:
                    self.export_inventory_csv()
                elif choice == 3:
                    self.generate_sales_graph()
                elif choice == 4:
                    self.generate_category_chart()
                elif choice == 5:
                    self.generate_inventory_chart()
                elif choice == 6:
                    self.generate_top_items_chart()
                elif choice == 7:
                    break
                else:
                    print("Invalid option!")
            except ValueError:
                print("Invalid input!")
            except Exception as e:
                print(f"Error: {e}")

    def export_sales_csv(self):
        """Export sales data to CSV"""
        try:
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")

            query = """
            SELECT 
                ro.order_id,
                ro.order_date,
                g.first_name,
                g.last_name,
                g.email,
                ro.order_type,
                mi.item_name,
                mc.category_name,
                oi.quantity,
                oi.unit_price,
                (oi.quantity * oi.unit_price) as subtotal,
                ro.total_amount,
                ro.order_status
            FROM restaurant_orders ro
            JOIN guests g ON g.guest_id = ro.guest_id
            JOIN order_items oi ON oi.order_id = ro.order_id
            JOIN menu_items mi ON mi.menu_item_id = oi.menu_item_id
            JOIN menu_categories mc ON mc.category_id = mi.category_id
            WHERE DATE(ro.order_date) BETWEEN %s AND %s
            ORDER BY ro.order_date DESC, ro.order_id
            """
            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()

            if not results:
                print("No data found for the specified date range!")
                return

            # Create reports directory if it doesn't exist
            os.makedirs('reports', exist_ok=True)

            filename = f'reports/sales_report_{start_date}_to_{end_date}.csv'

            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Order ID', 'Order Date', 'Guest First Name', 'Guest Last Name',
                              'Email', 'Order Type', 'Item Name', 'Category', 'Quantity',
                              'Unit Price', 'Subtotal', 'Order Total', 'Status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for row in results:
                    writer.writerow({
                        'Order ID': row['order_id'],
                        'Order Date': row['order_date'],
                        'Guest First Name': row['first_name'],
                        'Guest Last Name': row['last_name'],
                        'Email': row['email'],
                        'Order Type': row['order_type'],
                        'Item Name': row['item_name'],
                        'Category': row['category_name'],
                        'Quantity': row['quantity'],
                        'Unit Price': float(row['unit_price']),
                        'Subtotal': float(row['subtotal']),
                        'Order Total': float(row['total_amount']),
                        'Status': row['order_status']
                    })

            print(f"\n✓ Sales report exported successfully!")
            print(f"File: {filename}")
            print(f"Total records: {len(results)}")

        except Exception as e:
            print(f"Error exporting CSV: {e}")

    def export_inventory_csv(self):
        """Export inventory data to CSV"""
        try:
            query = """
            SELECT 
                ii.item_id,
                ii.item_name,
                ic.category_name,
                ii.quantity_in_stock,
                ii.minimum_quantity,
                ii.unit_cost,
                (ii.quantity_in_stock * ii.unit_cost) as total_value,
                CASE 
                    WHEN ii.quantity_in_stock <= ii.minimum_quantity THEN 'Low Stock'
                    ELSE 'OK'
                END as status
            FROM inventory_items ii
            JOIN inventory_categories ic ON ic.category_id = ii.category_id
            ORDER BY ii.item_id ASC
            """
            cursor.execute(query)
            results = cursor.fetchall()

            os.makedirs('reports', exist_ok=True)

            filename = f'reports/inventory_report_{date.today()}.csv'

            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Item ID', 'Item Name', 'Category', 'Quantity in Stock',
                              'Minimum Quantity', 'Unit Cost', 'Total Value', 'Status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for row in results:
                    writer.writerow({
                        'Item ID': row['item_id'],
                        'Item Name': row['item_name'],
                        'Category': row['category_name'],
                        'Quantity in Stock': float(row['quantity_in_stock']),
                        'Minimum Quantity': float(row['minimum_quantity']),
                        'Unit Cost': float(row['unit_cost']),
                        'Total Value': float(row['total_value']),
                        'Status': row['status']
                    })

            print(f"\n✓ Inventory report exported successfully!")
            print(f"File: {filename}")
            print(f"Total items: {len(results)}")

        except Exception as e:
            print(f"Error exporting CSV: {e}")

    def generate_sales_graph(self):
        """Generate sales trend graph"""
        try:
            days = int(input("Enter number of days to analyze (default 30): ") or "30")

            end_date = date.today()
            start_date = end_date - timedelta(days=days)

            query = """
            SELECT 
                DATE(ro.order_date) as sale_date,
                COUNT(ro.order_id) as total_orders,
                SUM(ro.total_amount) as daily_sales
            FROM restaurant_orders ro
            WHERE DATE(ro.order_date) BETWEEN %s AND %s
            GROUP BY DATE(ro.order_date)
            ORDER BY sale_date
            """
            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()

            if not results:
                print("No sales data found for the specified period!")
                return

            dates = [row['sale_date'] for row in results]
            sales = [float(row['daily_sales']) for row in results]
            orders = [row['total_orders'] for row in results]

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

            # Sales trend
            ax1.plot(dates, sales, marker='o', linestyle='-', color='green', linewidth=2)
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Sales (₱)', color='green')
            ax1.set_title(f'Daily Sales Trend ({start_date} to {end_date})')
            ax1.grid(True, alpha=0.3)
            ax1.tick_params(axis='x', rotation=45)

            # Orders trend
            ax2.bar(dates, orders, color='blue', alpha=0.7)
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Number of Orders')
            ax2.set_title('Daily Orders')
            ax2.tick_params(axis='x', rotation=45)
            ax2.grid(True, alpha=0.3)

            plt.tight_layout()

            os.makedirs('reports', exist_ok=True)
            filename = f'reports/sales_trend_{date.today()}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')

            print(f"\n✓ Sales graph generated successfully!")
            print(f"File: {filename}")

            plt.show()

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            print(f"Error generating graph: {e}")

    def generate_category_chart(self):
        """Generate category sales pie chart"""
        try:
            days = int(input("Enter number of days to analyze (default 30): ") or "30")

            end_date = date.today()
            start_date = end_date - timedelta(days=days)

            query = """
            SELECT 
                mc.category_name,
                SUM(oi.quantity * oi.unit_price) as category_sales
            FROM restaurant_orders ro
            JOIN order_items oi ON oi.order_id = ro.order_id
            JOIN menu_items mi ON mi.menu_item_id = oi.menu_item_id
            JOIN menu_categories mc ON mc.category_id = mi.category_id
            WHERE DATE(ro.order_date) BETWEEN %s AND %s
            GROUP BY mc.category_id, mc.category_name
            ORDER BY category_sales DESC
            """
            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()

            if not results:
                print("No sales data found!")
                return

            categories = [row['category_name'] for row in results]
            sales = [float(row['category_sales']) for row in results]

            fig, ax = plt.subplots(figsize=(10, 8))

            colors = plt.cm.Set3(range(len(categories)))
            wedges, texts, autotexts = ax.pie(sales, labels=categories, autopct='%1.1f%%',
                                              colors=colors, startangle=90)

            # Make percentage text bold
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')

            ax.set_title(f'Sales by Category ({start_date} to {end_date})', fontsize=14, fontweight='bold')

            # Add legend with sales amounts
            legend_labels = [f'{cat}: ₱{sale:,.2f}' for cat, sale in zip(categories, sales)]
            ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))

            plt.tight_layout()

            os.makedirs('reports', exist_ok=True)
            filename = f'reports/category_sales_{date.today()}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')

            print(f"\n✓ Category chart generated successfully!")
            print(f"File: {filename}")

            plt.show()

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            print(f"Error generating chart: {e}")

    def generate_inventory_chart(self):
        """Generate inventory status bar chart"""
        try:
            query = """
            SELECT 
                ii.item_name,
                ic.category_name,
                ii.quantity_in_stock,
                ii.minimum_quantity
            FROM inventory_items ii
            JOIN inventory_categories ic ON ic.category_id = ii.category_id
            ORDER BY ic.category_name, ii.item_name
            LIMIT 20
            """
            cursor.execute(query)
            results = cursor.fetchall()

            if not results:
                print("No inventory data found!")
                return

            items = [row['item_name'][:20] for row in results]  # Truncate long names
            current_stock = [float(row['quantity_in_stock']) for row in results]
            min_stock = [float(row['minimum_quantity']) for row in results]

            fig, ax = plt.subplots(figsize=(14, 8))

            x = range(len(items))
            width = 0.35

            bars1 = ax.bar([i - width / 2 for i in x], current_stock, width, label='Current Stock', color='green',
                           alpha=0.7)
            bars2 = ax.bar([i + width / 2 for i in x], min_stock, width, label='Minimum Stock', color='red', alpha=0.7)

            ax.set_xlabel('Items')
            ax.set_ylabel('Quantity')
            ax.set_title('Inventory Status - Current vs Minimum Stock', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(items, rotation=45, ha='right')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')

            # Highlight low stock items
            for i, (current, minimum) in enumerate(zip(current_stock, min_stock)):
                if current <= minimum:
                    bars1[i].set_color('orange')

            plt.tight_layout()

            os.makedirs('reports', exist_ok=True)
            filename = f'reports/inventory_status_{date.today()}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')

            print(f"\n✓ Inventory chart generated successfully!")
            print(f"File: {filename}")

            plt.show()

        except Exception as e:
            print(f"Error generating chart: {e}")

    def generate_top_items_chart(self):
        """Generate top selling items bar chart"""
        try:
            limit = int(input("Enter number of top items to display (default 10): ") or "10")
            days = int(input("Enter number of days to analyze (default 30): ") or "30")

            end_date = date.today()
            start_date = end_date - timedelta(days=days)

            query = """
            SELECT 
                mi.item_name,
                SUM(oi.quantity) as total_sold,
                SUM(oi.quantity * oi.unit_price) as total_revenue
            FROM order_items oi
            JOIN menu_items mi ON mi.menu_item_id = oi.menu_item_id
            JOIN restaurant_orders ro ON ro.order_id = oi.order_id
            WHERE DATE(ro.order_date) BETWEEN %s AND %s
            GROUP BY mi.menu_item_id, mi.item_name
            ORDER BY total_sold DESC
            LIMIT %s
            """
            cursor.execute(query, (start_date, end_date, limit))
            results = cursor.fetchall()

            if not results:
                print("No sales data found!")
                return

            items = [row['item_name'] for row in results]
            quantities = [row['total_sold'] for row in results]
            revenues = [float(row['total_revenue']) for row in results]

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

            # Quantities sold
            colors1 = plt.cm.viridis(range(len(items)))
            bars1 = ax1.barh(items, quantities, color=colors1)
            ax1.set_xlabel('Quantity Sold')
            ax1.set_title(f'Top {limit} Items by Quantity ({start_date} to {end_date})', fontweight='bold')
            ax1.grid(True, alpha=0.3, axis='x')

            # Add value labels
            for bar in bars1:
                width = bar.get_width()
                ax1.text(width, bar.get_y() + bar.get_height() / 2,
                         f'{int(width)}', ha='left', va='center', fontweight='bold')

            # Revenue
            colors2 = plt.cm.plasma(range(len(items)))
            bars2 = ax2.barh(items, revenues, color=colors2)
            ax2.set_xlabel('Revenue (₱)')
            ax2.set_title(f'Top {limit} Items by Revenue', fontweight='bold')
            ax2.grid(True, alpha=0.3, axis='x')

            # Add value labels
            for bar in bars2:
                width = bar.get_width()
                ax2.text(width, bar.get_y() + bar.get_height() / 2,
                         f'₱{width:,.0f}', ha='left', va='center', fontweight='bold')

            plt.tight_layout()

            os.makedirs('reports', exist_ok=True)
            filename = f'reports/top_items_{date.today()}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')

            print(f"\n✓ Top items chart generated successfully!")
            print(f"File: {filename}")

            plt.show()

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            print(f"Error generating chart: {e}")


# Example usage
if __name__ == "__main__":
    kitchen = RestoKitchen()
    kitchen.main()