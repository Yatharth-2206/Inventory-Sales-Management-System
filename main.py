"""
Project : Inventory & Sales Management System

Author  : Yatharth Aphale

Description:
A command-line application to manage inventory, sales,
stock updates, reports, and data persistence using JSON.

"""

from inventory_manager import *

def main_menu():
    """
    Main menu function to display options and handle user input.
    """
    load_data()  # Load data at the start of the program

    while True:
        print("=" * 60)
        print("Main Menu")
        print("=" * 60)
        print("INVENTORY MANAGEMENT SYSTEM")
        print("=" * 60)
        print("Developed by: Yatharth Aphale")
        print("=" * 60)
        print("\n1. Add Product")
        print("2. Update Stock")
        print("3. Sell Product")
        print("4. Search Product")
        print("5. Low Stock Report")
        print("6. Category Summary")
        print("7. Unique Categories")
        print("8. Unique Products Sold Today")
        print("9. Generate Invoice")
        print("10. Save Data")
        print("11. Load Data")
        print("12. Exit")
        print("=" * 50)
       

        choice = input("Enter your choice (1-12): ").strip()

        if choice == "1":
            add_product()
            press_enter()
        elif choice == "2":
            update_stock()
            press_enter()
        elif choice == "3":
            sell_product()
            press_enter()
        elif choice == "4":
            search_product()
            press_enter()   
        elif choice == "5":
            low_stock_report()
            press_enter()
        elif choice == "6":
            category_summary()
            press_enter()   
        elif choice == "7":
            unique_categories()
            press_enter()
        elif choice == "8":
            unique_products_sold_today()
            press_enter()   
        elif choice == "9":
            generate_invoice()
            press_enter()
        elif choice == "10":
            save_data()
            press_enter()
        elif choice == "11":
            load_data()
            press_enter()
        elif choice == "12":
            save_data()  # Save data before exiting
            print("Thank you for using")
            print("Inventory & Sales Management System")
            print("=" * 50)
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 12.")


if __name__ == "__main__":
    main_menu()




