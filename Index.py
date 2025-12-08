import database as db
from datetime import datetime, date, timedelta

cursor = db.conn.cursor(dictionary=True)


class RestoKitchen:
    def __init__(self):
        self.user_type = None  # 'guest' or 'admin'
        self.user_id = None
        self.user_info = None
        self.guest_id = None
        self.guest_info = None
        self.categories = self.get_categories()
        self.cart = []
        self.current_booking_id = None

    def login(self):
        """Login function to determine user type"""
        while True:
            print("\n" + "=" * 50)
            print("=== HOTEL RESTAURANT SYSTEM ===")
            print("=" * 50)
            print("1. Guest Login")
            print("2. Admin Login")
            print("3. Exit")
            print("=" * 50)

            try:
                choice = int(input("Select login type: "))

                if choice == 1:
                    if self.guest_login():
                        self.user_type = 'guest'
                        return True
                elif choice == 2:
                    if self.admin_login():
                        self.user_type = 'admin'
                        return True
                elif choice == 3:
                    print("Thank you for using Hotel Restaurant System!")
                    return False
                else:
                    print("Invalid option!")
            except ValueError:
                print("Invalid input! Please enter a number.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def guest_login(self):
        """Guest login using guest ID"""
        try:
            print("\n" + "=" * 50)
            print("GUEST LOGIN")
            print("=" * 50)
            guest_id = input("Enter your Guest ID (or 'back' to return): ").strip()

            if guest_id.lower() == 'back':
                return False

            guest_id = int(guest_id)

            query = "SELECT * FROM guests WHERE guest_id = %s"
            cursor.execute(query, (guest_id,))
            guest = cursor.fetchone()

            if guest:
                self.guest_id = guest['guest_id']
                self.guest_info = guest
                self.user_id = guest['guest_id']
                self.user_info = guest
                self.current_booking_id = self.get_active_booking(self.guest_id)

                print(f"\n✓ Welcome, {guest['first_name']} {guest['last_name']}!")
                input("Press Enter to continue...")
                return True
            else:
                print("Guest ID not found!")
                return False
        except ValueError:
            print("Invalid Guest ID format!")
            return False
        except Exception as e:
            print(f"Login error: {e}")
            return False

    def admin_login(self):
        """Admin login using username and password"""
        try:
            print("\n" + "=" * 50)
            print("ADMIN LOGIN")
            print("=" * 50)
            username = input("Username (or 'back' to return): ").strip()

            if username.lower() == 'back':
                return False

            password = input("Password: ").strip()

            query = "SELECT * FROM staff WHERE username = %s AND password = %s AND role IN ('admin', 'kitchen', 'restaurant', 'manager')"
            cursor.execute(query, (username, password))
            admin = cursor.fetchone()

            if admin:
                self.user_id = admin['staff_id']
                self.user_info = admin
                print(f"\n✓ Welcome, {admin['first_name']} {admin['last_name']} ({admin['role']})!")
                input("Press Enter to continue...")
                return True
            else:
                print("Invalid credentials or insufficient permissions!")
                return False
        except Exception as e:
            print(f"Login error: {e}")
            return False

    def main(self):
        """Main menu dispatcher"""
        if not self.login():
            return

        if self.user_type == 'guest':
            self.guest_main_menu()
        elif self.user_type == 'admin':
            self.admin_main_menu()

    def guest_main_menu(self):
        """Guest main menu"""
        while True:
            print("\n" + "=" * 50)
            print(f"=== GUEST MENU - {self.guest_info['first_name']} {self.guest_info['last_name']} ===")
            print("=" * 50)
            print("1. Browse Menu & Place Order")
            print("2. View My Orders")
            print("3. View Cart")
            print("4. Logout")
            print("=" * 50)

            try:
                choice = int(input("Select option: "))

                if choice == 1:
                    self.guest_place_order()
                elif choice == 2:
                    self.guest_view_orders()
                elif choice == 3:
                    self.display_cart()
                elif choice == 4:
                    print("Logging out...")
                    self.logout()
                    break
                else:
                    print("Invalid option! Please select 1-4.")
            except ValueError:
                print("Invalid input! Please enter a number.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def admin_main_menu(self):
        """Admin main menu"""
        while True:
            print("\n" + "=" * 50)
            print(f"=== ADMIN MENU - {self.user_info['first_name']} {self.user_info['last_name']} ===")
            print("=" * 50)
            print("1. Take Orders (For Guests)")
            print("2. Sales Reports")
            print("3. Inventory Management")
            print("4. Menu Management")
            print("5. Order Management")
            print("6. Logout")
            print("=" * 50)

            try:
                choice = int(input("Select option: "))

                if choice == 1:
                    self.admin_take_orders()
                elif choice == 2:
                    self.sales_report_menu()
                elif choice == 3:
                    self.inventory_management()
                elif choice == 4:
                    self.menu_management()
                elif choice == 5:
                    self.order_management()
                elif choice == 6:
                    print("Logging out...")
                    self.logout()
                    break
                else:
                    print("Invalid option! Please select 1-6.")
            except ValueError:
                print("Invalid input! Please enter a number.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def logout(self):
        """Clear session data"""
        self.user_type = None
        self.user_id = None
        self.user_info = None
        self.guest_id = None
        self.guest_info = None
        self.cart = []
        self.current_booking_id = None

    # ========== GUEST FUNCTIONS ==========

    def guest_place_order(self):
        """Guest places their own order"""
        self.cart = []  # Reset cart

        print(f"\n{'=' * 50}")
        print(f"PLACING ORDER FOR: {self.guest_info['first_name']} {self.guest_info['last_name']}")
        print(f"{'=' * 50}")

        while True:
            print("\n--- ORDER MENU ---")
            print("1. Browse Menu & Add Items")
            print("2. View Cart")
            print("3. Checkout")
            print("4. Clear Cart")
            print("5. Cancel")

            try:
                choice = int(input("\nSelect option: "))

                if choice == 1:
                    self.browse_and_add_items()
                elif choice == 2:
                    self.display_cart()
                elif choice == 3:
                    if self.cart:
                        self.checkout()
                        break
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

    def guest_view_orders(self):
        """View guest's order history"""
        try:
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
            LIMIT 20
            """
            cursor.execute(query, (self.guest_id,))
            orders = cursor.fetchall()

            if not orders:
                print("\nYou have no orders yet.")
                return

            print("\n" + "=" * 80)
            print("YOUR ORDER HISTORY")
            print("=" * 80)
            print(f"{'Order ID':<12} {'Date':<20} {'Type':<15} {'Amount':<12} {'Status':<12}")
            print("-" * 80)

            for order in orders:
                print(f"{order['order_id']:<12} {str(order['order_date']):<20} {order['order_type']:<15} "
                      f"₱{float(order['total_amount']):<11.2f} {order['order_status']:<12}")

            print("=" * 80)

            # Option to view order details
            view_detail = input("\nEnter Order ID to view details (or press Enter to return): ").strip()
            if view_detail:
                try:
                    order_id = int(view_detail)
                    self.view_order_details(order_id)
                except ValueError:
                    print("Invalid Order ID!")

        except Exception as e:
            print(f"Error viewing orders: {e}")

    def view_order_details(self, order_id):
        """View detailed items of an order"""
        try:
            query = """
            SELECT 
                mi.item_name,
                oi.quantity,
                oi.unit_price,
                (oi.quantity * oi.unit_price) as subtotal
            FROM order_items oi
            JOIN menu_items mi ON mi.menu_item_id = oi.menu_item_id
            WHERE oi.order_id = %s
            """
            cursor.execute(query, (order_id,))
            items = cursor.fetchall()

            if not items:
                print("Order not found or no items!")
                return

            print("\n" + "=" * 70)
            print(f"ORDER #{order_id} DETAILS")
            print("=" * 70)
            print(f"{'Item Name':<35} {'Qty':<8} {'Price':<12} {'Subtotal':<12}")
            print("-" * 70)

            total = 0
            for item in items:
                print(f"{item['item_name']:<35} {item['quantity']:<8} "
                      f"₱{float(item['unit_price']):<11.2f} ₱{float(item['subtotal']):<11.2f}")
                total += float(item['subtotal'])

            print("-" * 70)
            print(f"{'TOTAL:':<55} ₱{total:.2f}")
            print("=" * 70)

        except Exception as e:
            print(f"Error viewing order details: {e}")

    # ========== ADMIN FUNCTIONS ==========

    def admin_take_orders(self):
        """Admin takes orders for guests"""
        guest = self.search_guest()

        if not guest:
            print("Order cancelled - no guest selected.")
            return

        self.guest_id = guest['guest_id']
        self.guest_info = guest
        self.current_booking_id = self.get_active_booking(self.guest_id)
        self.cart = []

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
                        break
                    else:
                        print("Cart is empty! Add items first.")
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

    def menu_management(self):
        """Manage menu items"""
        while True:
            print("\n" + "=" * 50)
            print("MENU MANAGEMENT")
            print("=" * 50)
            print("1. View All Menu Items")
            print("2. Add Menu Item")
            print("3. Update Menu Item")
            print("4. Toggle Item Availability")
            print("5. Back to Main Menu")

            try:
                choice = int(input("\nSelect option: "))

                if choice == 1:
                    self.view_all_menu_items()
                elif choice == 2:
                    self.add_menu_item()
                elif choice == 3:
                    self.update_menu_item()
                elif choice == 4:
                    self.toggle_item_availability()
                elif choice == 5:
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
            ORDER BY mc.category_id, mi.menu_item_id
            """
            cursor.execute(query)
            items = cursor.fetchall()

            print("\n" + "=" * 90)
            print("ALL MENU ITEMS")
            print("=" * 90)
            print(f"{'ID':<5} {'Item Name':<35} {'Category':<20} {'Price':<12} {'Available':<12}")
            print("-" * 90)

            for item in items:
                available = "Yes" if item['is_available'] else "No"
                print(f"{item['menu_item_id']:<5} {item['item_name']:<35} {item['category_name']:<20} "
                      f"₱{float(item['price']):<11.2f} {available:<12}")

            print("=" * 90)

        except Exception as e:
            print(f"Error: {e}")

    def add_menu_item(self):
        """Add new menu item"""
        try:
            print("\n--- ADD MENU ITEM ---")

            # Show categories
            print("\nCategories:")
            for cat in self.categories:
                print(f"{cat['category_id']}. {cat['category_name']}")

            category_id = int(input("\nEnter category ID: "))
            item_name = input("Enter item name: ").strip()
            price = float(input("Enter price: "))

            query = """
            INSERT INTO menu_items (item_name, category_id, price, is_available)
            VALUES (%s, %s, %s, 1)
            """
            cursor.execute(query, (item_name, category_id, price))
            db.conn.commit()

            print(f"\n✓ Menu item '{item_name}' added successfully!")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def update_menu_item(self):
        """Update menu item price"""
        try:
            item_id = int(input("\nEnter menu item ID to update: "))

            query = "SELECT * FROM menu_items WHERE menu_item_id = %s"
            cursor.execute(query, (item_id,))
            item = cursor.fetchone()

            if not item:
                print("Menu item not found!")
                return

            print(f"\nCurrent item: {item['item_name']}")
            print(f"Current price: ₱{float(item['price']):.2f}")

            new_price = float(input("Enter new price: "))

            update_query = "UPDATE menu_items SET price = %s WHERE menu_item_id = %s"
            cursor.execute(update_query, (new_price, item_id))
            db.conn.commit()

            print(f"\n✓ Price updated successfully!")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def toggle_item_availability(self):
        """Toggle menu item availability"""
        try:
            item_id = int(input("\nEnter menu item ID: "))

            query = "SELECT * FROM menu_items WHERE menu_item_id = %s"
            cursor.execute(query, (item_id,))
            item = cursor.fetchone()

            if not item:
                print("Menu item not found!")
                return

            new_status = 0 if item['is_available'] else 1
            status_text = "Available" if new_status else "Unavailable"

            update_query = "UPDATE menu_items SET is_available = %s WHERE menu_item_id = %s"
            cursor.execute(update_query, (new_status, item_id))
            db.conn.commit()

            print(f"\n✓ {item['item_name']} is now {status_text}!")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    def order_management(self):
        """Manage orders"""
        while True:
            print("\n" + "=" * 50)
            print("ORDER MANAGEMENT")
            print("=" * 50)
            print("1. View All Orders")
            print("2. View Pending Orders")
            print("3. Update Order Status")
            print("4. View Order Details")
            print("5. Back to Main Menu")

            try:
                choice = int(input("\nSelect option: "))

                if choice == 1:
                    self.view_all_orders()
                elif choice == 2:
                    self.view_pending_orders()
                elif choice == 3:
                    self.update_order_status()
                elif choice == 4:
                    order_id = int(input("Enter Order ID: "))
                    self.view_order_details(order_id)
                elif choice == 5:
                    break
                else:
                    print("Invalid option!")
            except ValueError:
                print("Invalid input!")

    def view_all_orders(self):
        """View all orders"""
        try:
            query = """
            SELECT 
                ro.order_id,
                ro.order_date,
                g.first_name,
                g.last_name,
                ro.order_type,
                ro.total_amount,
                ro.order_status
            FROM restaurant_orders ro
            JOIN guests g ON g.guest_id = ro.guest_id
            ORDER BY ro.order_date DESC
            LIMIT 50
            """
            cursor.execute(query)
            orders = cursor.fetchall()

            print("\n" + "=" * 100)
            print("ALL ORDERS")
            print("=" * 100)
            print(f"{'ID':<8} {'Date':<20} {'Guest':<25} {'Type':<15} {'Amount':<12} {'Status':<12}")
            print("-" * 100)

            for order in orders:
                guest_name = f"{order['first_name']} {order['last_name']}"
                print(f"{order['order_id']:<8} {str(order['order_date']):<20} {guest_name:<25} "
                      f"{order['order_type']:<15} ₱{float(order['total_amount']):<11.2f} {order['order_status']:<12}")

            print("=" * 100)

        except Exception as e:
            print(f"Error: {e}")

    def view_pending_orders(self):
        """View pending orders"""
        try:
            query = """
            SELECT 
                ro.order_id,
                ro.order_date,
                g.first_name,
                g.last_name,
                ro.order_type,
                ro.total_amount
            FROM restaurant_orders ro
            JOIN guests g ON g.guest_id = ro.guest_id
            WHERE ro.order_status = 'pending'
            ORDER BY ro.order_date ASC
            """
            cursor.execute(query)
            orders = cursor.fetchall()

            if not orders:
                print("\n✓ No pending orders!")
                return

            print("\n" + "=" * 90)
            print("PENDING ORDERS")
            print("=" * 90)
            print(f"{'ID':<8} {'Date':<20} {'Guest':<30} {'Type':<15} {'Amount':<12}")
            print("-" * 90)

            for order in orders:
                guest_name = f"{order['first_name']} {order['last_name']}"
                print(f"{order['order_id']:<8} {str(order['order_date']):<20} {guest_name:<30} "
                      f"{order['order_type']:<15} ₱{float(order['total_amount']):<11.2f}")

            print("=" * 90)

        except Exception as e:
            print(f"Error: {e}")

    def update_order_status(self):
        """Update order status"""
        try:
            order_id = int(input("\nEnter Order ID: "))

            query = "SELECT * FROM restaurant_orders WHERE order_id = %s"
            cursor.execute(query, (order_id,))
            order = cursor.fetchone()

            if not order:
                print("Order not found!")
                return

            print(f"\nCurrent status: {order['order_status']}")
            print("\nNew status options:")
            print("1. pending")
            print("2. preparing")
            print("3. completed")
            print("4. cancelled")

            choice = int(input("Select new status: "))
            statuses = {1: 'pending', 2: 'preparing', 3: 'completed', 4: 'cancelled'}

            if choice not in statuses:
                print("Invalid choice!")
                return

            new_status = statuses[choice]

            update_query = "UPDATE restaurant_orders SET order_status = %s WHERE order_id = %s"
            cursor.execute(update_query, (new_status, order_id))
            db.conn.commit()

            print(f"\n✓ Order #{order_id} status updated to '{new_status}'!")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

    # ========== SHARED FUNCTIONS ==========

    def search_guest(self):
        """Search and select a guest (Admin only)"""
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
            print("\nCart is empty!")
            return

        print("\n" + "=" * 70)
        print("CART")
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

            item_id = int(input("\nEnter item ID to add (0 to cancel): "))

            if item_id == 0:
                return

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

            cart_item = {
                'menu_item_id': selected_item['menu_item_id'],
                'item_name': selected_item['item_name'],
                'price': float(selected_item['price']),
                'quantity': quantity
            }

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

            total_amount = sum(item['quantity'] * item['price'] for item in self.cart)

            confirm = input(f"\nConfirm order? Total: ₱{total_amount:.2f} (yes/no): ").lower()

            if confirm != 'yes':
                print("Order cancelled!")
                return

            insert_order_query = """
            INSERT INTO restaurant_orders 
            (booking_id, guest_id, order_type, total_amount, order_status, order_date)
            VALUES (%s, %s, %s, %s, 'pending', NOW())
            """
            cursor.execute(insert_order_query,
                           (self.current_booking_id, self.guest_id, order_type, total_amount))

            order_id = cursor.lastrowid

            for item in self.cart:
                insert_item_query = """
                INSERT INTO order_items 
                (order_id, menu_item_id, quantity, unit_price)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_item_query,
                               (order_id, item['menu_item_id'], item['quantity'], item['price']))

            self.update_inventory_usage()

            db.conn.commit()

            print("\n" + "=" * 50)
            print("✓ ORDER PLACED SUCCESSFULLY!")
            print(f"Order ID: {order_id}")
            print(f"Guest: {self.guest_info['first_name']} {self.guest_info['last_name']}")
            print(f"Total Amount: ₱{total_amount:.2f}")
            print(f"Order Type: {order_type.replace('_', ' ').title()}")
            print("=" * 50)

            self.cart.clear()

        except Exception as e:
            db.conn.rollback()
            print(f"Error processing order: {e}")

    def update_inventory_usage(self):
        """Update inventory based on order"""
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


if __name__ == "__main__":
    kitchen = RestoKitchen()
    kitchen.main()