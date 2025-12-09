import os
import sys


if 'TERM' not in os.environ:
    os.environ['TERM'] = 'xterm'

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


def main_menu():
    """Main entry point for the integrated hotel system"""
    while True:
        clear_screen()
        print("=" * 50)
        print("=== INTEGRATED HOTEL MANAGEMENT SYSTEM ===")
        print("=" * 50)
        print("1. Restaurant & Kitchen System")
        print("2. Inventory & Supply Management")
        print("3. Exit")
        print("=" * 50)

        try:
            choice = int(input("Select system to access: "))

            if choice == 1:
                # Launch Restaurant System
                from Index import RestoKitchen
                kitchen = RestoKitchen()
                kitchen.main()

            elif choice == 2:
                # Launch Inventory System
                from cli import main as inventory_main
                inventory_main()

            elif choice == 3:
                print("Thank you for using the Hotel Management System!")
                break
            else:
                print("Invalid option! Please select 1-3.")
                input("Press Enter to continue...")

        except ValueError:
            print("Invalid input! Please enter a number.")
            input("Press Enter to continue...")
        except Exception as e:
            print(f"An error occurred: {e}")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main_menu()