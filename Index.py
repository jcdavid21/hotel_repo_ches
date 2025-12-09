import database as db
from datetime import datetime, date, timedelta
from restaurant_kitchen import RestaurantKitchen
from inventory_management import InventoryManagement

cursor = db.conn.cursor(dictionary=True)


class HotelSystem:
    def __init__(self):
        self.user_type = None  # 'guest' or 'admin'
        self.user_id = None
        self.user_info = None

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
                self.user_id = guest['guest_id']
                self.user_info = guest
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
            resto = RestaurantKitchen(self.user_info, is_guest=True)
            resto.guest_main_menu()
        elif self.user_type == 'admin':
            self.admin_main_menu()

    def admin_main_menu(self):
        """Admin main menu - choose between Restaurant/Kitchen or Inventory"""
        while True:
            print("\n" + "=" * 50)
            print(f"=== ADMIN MENU - {self.user_info['first_name']} {self.user_info['last_name']} ===")
            print("=" * 50)
            print("1. Restaurant & Kitchen Management")
            print("2. Inventory Management")
            print("3. Logout")
            print("=" * 50)

            try:
                choice = int(input("Select option: "))

                if choice == 1:
                    resto = RestaurantKitchen(self.user_info, is_guest=False)
                    resto.admin_main_menu()
                elif choice == 2:
                    inventory = InventoryManagement(self.user_info)
                    inventory.main_menu()
                elif choice == 3:
                    print("Logging out...")
                    self.logout()
                    break
                else:
                    print("Invalid option! Please select 1-3.")
            except ValueError:
                print("Invalid input! Please enter a number.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def logout(self):
        """Clear session data"""
        self.user_type = None
        self.user_id = None
        self.user_info = None


if __name__ == "__main__":
    system = HotelSystem()
    system.main()