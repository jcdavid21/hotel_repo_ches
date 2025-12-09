import database as db
from datetime import datetime, date

cursor = db.conn.cursor(dictionary=True)


class RestaurantKitchen:
    def __init__(self, user_info, is_guest=False):
        self.user_info = user_info
        self.is_guest = is_guest
        self.guest_id = user_info['guest_id'] if is_guest else None
        self.categories = self.get_categories()
        self.cart = []
        self.current_booking_id = None

        if is_guest:
            self.current_booking_id = self.get_active_booking(self.guest_id)

    def guest_main_menu(self):
        """Guest main menu"""
        while True:
            print("\n" + "=" * 50)
            print(f"=== GUEST MENU - {self.user_info['first_name']} {self.user_info['last_name']} ===")
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
                    break
                else:
                    print("Invalid option! Please select 1-4.")
            except ValueError:
                print("Invalid input! Please enter a number.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def admin_main_menu(self):
        """Admin main menu for Restaurant & Kitchen"""
        while True:
            print("\n" + "=" * 50)
            print(f"=== RESTAURANT & KITCHEN - {self.user_info['first_name']} ===")
            print("=" * 50)
            print("1. Take Orders (For Guests)")
            print("2. Order Management")
            print("3. Sales Reports")
            print("4. Back to Main Menu")
            print("=" * 50)

            try:
                choice = int(input("Select option: "))

                if choice == 1:
                    self.admin_take_orders()
                elif choice == 2:
                    self.order_management()
                elif choice == 3:
                    self.sales_report_menu()
                elif choice == 4:
                    break
                else:
                    print("Invalid option! Please select 1-4.")
            except ValueError:
                print("Invalid input! Please enter a number.")
            except Exception as e:
                print(f"An error occurred: {e}")

    # ========== GUEST FUNCTIONS ==========

    def guest_place_order(self):
        """Guest places their own order"""
        self.cart = []  # Reset cart

        print(f"\n{'=' * 50}")
        print(f"PLACING ORDER FOR: {self.user_info['first_name']} {self.user_info['last_name']}")
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

    # ========== ADMIN FUNCTIONS ==========

    def admin_take_orders(self):
        """Admin takes orders for guests"""
        guest = self.search_guest()

        if not guest:
            print("Order cancelled - no guest selected.")
            return

        self.guest_id = guest['guest_id']
        temp_guest_info = guest
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
                        self.checkout(temp_guest_info)
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
            print("5. Back")

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

            cursor.execute("UPDATE restaurant_orders SET order_status = %s WHERE order_id = %s",
                           (new_status, order_id))
            db.conn.commit()

            print(f"\n✓ Order #{order_id} status updated to '{new_status}'!")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error: {e}")

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

    # ========== SALES REPORTS ==========

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
            print("6. Back")

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

            print("\n" + "=" * 70)
            print(f"DAILY SALES REPORT - {report_date}")
            print("=" * 70)
            print(f"{'Order ID':<10} {'Guest':<25} {'Type':<15} {'Amount':<12} {'Status':<12}")
            print("-" * 70)

            total_sales = 0
            for order in orders:
                guest_name = f"{order['first_name']} {order['last_name']}"
                print(f"{order['order_id']:<10} {guest_name:<25} {order['order_type']:<15} "
                      f"₱{float(order['total_amount']):<11.2f} {order['order_status']:<12}")
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
                SUM(oi.quantity * oi.unit_price) as total_revenue
            FROM order_items oi
            JOIN menu_items mi ON mi.menu_item_id = oi.menu_item_id
            JOIN menu_categories mc ON mc.category_id = mi.category_id
            GROUP BY mi.menu_item_id
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
            print(f"{'Rank':<6} {'Item Name':<35} {'Category':<15} {'Sold':<10} {'Revenue':<15}")
            print("-" * 90)

            for idx, row in enumerate(results, 1):
                print(f"{idx:<6} {row['item_name']:<35} {row['category_name']:<15} "
                      f"{row['total_sold']:<10} ₱{float(row['total_revenue']):<14.2f}")

            print("=" * 90)

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            print(f"Error: {e}")

    # ========== SHARED FUNCTIONS ==========

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
        print("=" * 50)

    def get_categories(self):
        """Get menu categories"""
        query = "SELECT * FROM menu_categories ORDER BY category_name"
        cursor.execute(query)
        return cursor.fetchall()

    def get_active_booking(self, guest_id):
        """Get active booking for guest"""
        query = """
                SELECT booking_id FROM bookings 
                WHERE guest_id = %s AND booking_status = 'checked_in'
                LIMIT 1
                """
        cursor.execute(query, (guest_id,))
        result = cursor.fetchone()
        return result['booking_id'] if result else None

    def browse_and_add_items(self):
        """Browse menu and add items to cart"""
        while True:
            print("\n" + "=" * 70)
            print("MENU CATEGORIES")
            print("=" * 70)

            for idx, category in enumerate(self.categories, 1):
                print(f"{idx}. {category['category_name']}")

            print(f"{len(self.categories) + 1}. View All Items")
            print(f"{len(self.categories) + 2}. Back")
            print("=" * 70)

            try:
                choice = int(input("\nSelect category: "))

                if choice == len(self.categories) + 2:
                    break
                elif choice == len(self.categories) + 1:
                    self.display_all_menu_items()
                elif 1 <= choice <= len(self.categories):
                    category_id = self.categories[choice - 1]['category_id']
                    self.display_category_items(category_id)
                else:
                    print("Invalid option!")
            except ValueError:
                print("Invalid input!")

    def display_all_menu_items(self):
        """Display all available menu items"""
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
                    WHERE mi.is_available = 1
                    ORDER BY mc.category_name, mi.item_name
                    """
            cursor.execute(query)
            items = cursor.fetchall()

            if not items:
                print("\nNo menu items available!")
                return

            print("\n" + "=" * 90)
            print("ALL MENU ITEMS")
            print("=" * 90)
            print(f"{'ID':<5} {'Item Name':<40} {'Category':<20} {'Price':<12}")
            print("-" * 90)

            for item in items:
                print(f"{item['menu_item_id']:<5} {item['item_name']:<40} "
                      f"{item['category_name']:<20} ₱{float(item['price']):<11.2f}")

            print("=" * 90)

            self.add_item_to_cart()

        except Exception as e:
            print(f"Error: {e}")

    def display_category_items(self, category_id):
        """Display items in a specific category"""
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
                    WHERE mi.category_id = %s AND mi.is_available = 1
                    ORDER BY mi.item_name
                    """
            cursor.execute(query, (category_id,))
            items = cursor.fetchall()

            if not items:
                print("\nNo items available in this category!")
                return

            print("\n" + "=" * 90)
            print(f"{items[0]['category_name'].upper()} MENU")
            print("=" * 90)
            print(f"{'ID':<5} {'Item Name':<50} {'Price':<12}")
            print("-" * 90)

            for item in items:
                print(f"{item['menu_item_id']:<5} {item['item_name']:<50} "
                      f"₱{float(item['price']):<11.2f}")

            print("=" * 90)

            self.add_item_to_cart()

        except Exception as e:
            print(f"Error: {e}")

    def add_item_to_cart(self):
        """Add selected item to cart"""
        try:
            add = input("\nAdd item to cart? (yes/no): ").lower()

            if add != 'yes':
                return

            menu_item_id = int(input("Enter Menu Item ID: "))

            # Verify item exists and is available
            query = """
                    SELECT mi.menu_item_id, mi.item_name, mi.price, mi.is_available
                    FROM menu_items mi
                    WHERE mi.menu_item_id = %s AND mi.is_available = 1
                    """
            cursor.execute(query, (menu_item_id,))
            item = cursor.fetchone()

            if not item:
                print("Item not found or not available!")
                return

            # Check if enough ingredients are available
            if not self.check_ingredient_availability(menu_item_id):
                print("\n⚠️ Sorry, this item cannot be prepared due to insufficient ingredients!")
                return

            quantity = int(input("Enter quantity: "))

            if quantity <= 0:
                print("Invalid quantity!")
                return

            # Check if item already in cart
            for cart_item in self.cart:
                if cart_item['menu_item_id'] == menu_item_id:
                    cart_item['quantity'] += quantity
                    print(f"\n✓ Updated {item['item_name']} quantity in cart!")
                    return

            # Add new item to cart
            self.cart.append({
                'menu_item_id': menu_item_id,
                'item_name': item['item_name'],
                'price': float(item['price']),
                'quantity': quantity
            })

            print(f"\n✓ Added {quantity}x {item['item_name']} to cart!")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            print(f"Error: {e}")

    def check_ingredient_availability(self, menu_item_id):
        """Check if enough ingredients are available for the menu item"""
        try:
            query = """
                    SELECT 
                        ii.item_id,
                        ii.item_name,
                        ii.quantity_in_stock,
                        mii.quantity_needed,
                        ii.unit
                    FROM menu_item_ingredients mii
                    JOIN inventory_items ii ON ii.item_id = mii.inventory_item_id
                    WHERE mii.menu_item_id = %s
                    """
            cursor.execute(query, (menu_item_id,))
            ingredients = cursor.fetchall()

            for ingredient in ingredients:
                if float(ingredient['quantity_in_stock']) < float(ingredient['quantity_needed']):
                    return False

            return True

        except Exception as e:
            print(f"Error checking ingredients: {e}")
            return False

    def display_cart(self):
        """Display current cart contents"""
        if not self.cart:
            print("\n📭 Your cart is empty!")
            return

        print("\n" + "=" * 70)
        print("YOUR CART")
        print("=" * 70)
        print(f"{'Item Name':<40} {'Qty':<8} {'Price':<12} {'Subtotal':<12}")
        print("-" * 70)

        total = 0
        for item in self.cart:
            subtotal = item['price'] * item['quantity']
            print(f"{item['item_name']:<40} {item['quantity']:<8} "
                  f"₱{item['price']:<11.2f} ₱{subtotal:<11.2f}")
            total += subtotal

        print("-" * 70)
        print(f"{'TOTAL:':<60} ₱{total:.2f}")
        print("=" * 70)

    def checkout(self, guest_info=None):
        """Checkout and create order"""
        try:
            if not self.cart:
                print("Cart is empty!")
                return

            # Display cart one more time
            self.display_cart()

            confirm = input("\nConfirm order? (yes/no): ").lower()

            if confirm != 'yes':
                print("Order cancelled!")
                return

            # Select order type
            print("\nOrder Type:")
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
            total_amount = sum(item['price'] * item['quantity'] for item in self.cart)

            # Use guest_info if provided (admin mode), otherwise use self.user_info
            current_guest_id = guest_info['guest_id'] if guest_info else self.guest_id

            # Insert order
            insert_order_query = """
                    INSERT INTO restaurant_orders 
                    (booking_id, guest_id, order_type, total_amount, order_status, order_date)
                    VALUES (%s, %s, %s, %s, 'pending', NOW())
                    """
            cursor.execute(insert_order_query,
                           (self.current_booking_id, current_guest_id, order_type, total_amount))

            order_id = cursor.lastrowid

            # Insert order items and deduct inventory
            for item in self.cart:
                # Insert order item
                insert_item_query = """
                        INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price)
                        VALUES (%s, %s, %s, %s)
                        """
                cursor.execute(insert_item_query,
                               (order_id, item['menu_item_id'], item['quantity'], item['price']))

                # Deduct ingredients from inventory
                self.deduct_ingredients(item['menu_item_id'], item['quantity'])

            db.conn.commit()

            print("\n" + "=" * 50)
            print("✓ ORDER PLACED SUCCESSFULLY!")
            print("=" * 50)
            print(f"Order ID: {order_id}")
            print(f"Order Type: {order_type.replace('_', ' ').title()}")
            print(f"Total Amount: ₱{total_amount:.2f}")
            print(f"Status: Pending")
            print("=" * 50)

            # Clear cart
            self.cart.clear()

            input("\nPress Enter to continue...")

        except ValueError:
            print("Invalid input!")
        except Exception as e:
            db.conn.rollback()
            print(f"Error processing order: {e}")

    def deduct_ingredients(self, menu_item_id, quantity):
        """Deduct ingredients from inventory based on menu item and quantity"""
        try:
            # Get ingredients for this menu item
            query = """
                    SELECT 
                        mii.inventory_item_id,
                        mii.quantity_needed
                    FROM menu_item_ingredients mii
                    WHERE mii.menu_item_id = %s
                    """
            cursor.execute(query, (menu_item_id,))
            ingredients = cursor.fetchall()

            for ingredient in ingredients:
                total_needed = float(ingredient['quantity_needed']) * quantity

                # Update inventory
                update_query = """
                        UPDATE inventory_items 
                        SET quantity_in_stock = quantity_in_stock - %s
                        WHERE item_id = %s
                        """
                cursor.execute(update_query, (total_needed, ingredient['inventory_item_id']))

                # Log transaction
                transaction_query = """
                        INSERT INTO inventory_transactions 
                        (item_id, transaction_type, quantity, transaction_date)
                        VALUES (%s, 'usage', %s, NOW())
                        """
                cursor.execute(transaction_query, (ingredient['inventory_item_id'], -total_needed))

        except Exception as e:
            raise Exception(f"Error deducting ingredients: {e}")