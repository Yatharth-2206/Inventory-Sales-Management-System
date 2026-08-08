"""
Project : Inventory & Sales Management System

Author  : Yatharth Aphale

Description:
A command-line application to manage inventory, sales,
stock updates, reports, and data persistence using JSON.

"""

from datetime import datetime
import json

# stores all the products
inventory = {}

# Stores every sale made
sales_log = []


# Stores unique product categories
categories_set = set()


# Global Constants
GST_PERCENTAGE = 18.0  # GST percentage for all products

STOCK_THRESHOLD = 15  # Default threshold for low stock report


def add_product():
    """
    Function to add a new product to the inventory.

    """

    print("\nADD NEW PRODUCT")

    try:
        product_id = input("\nEnter Product ID: ").strip().upper()
        if product_id in inventory:
            print("Product ID already exists. Use 'Update Stock' instead.")
            return

        name = input("Enter Product Name: ").strip().title()
        category = input("Enter Product Category: ").strip().title()
        price = float(input("Enter Product Price(INR): "))
        stock = int(input("Enter Initial Stock Quantity: "))

        if price < 0 or stock < 0:
            print("Price and stock cannot be negative.")
            return

        # Add product to inventory
        inventory[product_id] = {
            "name": name,
            "category": category,
            "price": price,
            "stock": stock,
            "sales_history": [],
        }

        # Add category to categories set
        categories_set.add(category)

        print("\n✓ PRODUCT ADDED SUCCESSFULLY")
        print("-" * 60)
        print(f"Product ID   : {product_id}")
        print(f"Name         : {name}")
        print(f"Category     : {category}")
        print(f"Price        : ₹{price:.2f}")
        print(f"Stock        : {stock}")

    except ValueError:
        print("Invalid input. Price must be a number and stock must be a whole number.")


def update_stock():
    """
    Function to update the stock of an existing product.
    """

    print("\nUPDATE STOCK")

    product_id = input("\nEnter Product ID to update stock: ").strip().upper()
    if product_id not in inventory:
        print("Product ID does not exist.")
        return

    product = inventory[product_id]
    previous_stock = product["stock"]
    try:
        additional_stock = int(input("Enter quantity to add to stock: "))
        if additional_stock <= 0:
            print("Stock quantity cannot be zero or negative.")
            return

        product["stock"] += additional_stock
        print("\n✓ STOCK UPDATED SUCCESSFULLY")
        print("-" * 60)
        print(f"Product ID      : {product_id}")
        print(f"Product Name    : {product['name']}")
        print(f"Previous Stock  : {previous_stock}")
        print(f"Quantity Added  : {additional_stock}")
        print(f"Current Stock   : {product['stock']}")

    except ValueError:
        print("Invalid input. Stock must be a whole number.")


def sell_product():
    """
    Function to sell a product and update inventory and sales log.
    """
    print("\nSELL PRODUCT")

    product_id = input("\nEnter Product ID to sell: ").strip().upper()
    if product_id not in inventory:
        print("Product ID does not exist.")
        return

    product = inventory[product_id]

    try:
        quantity = int(input("Enter quantity to sell: "))
        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return

        if quantity > product["stock"]:
            print(f"Insufficient stock. Available stock: {product['stock']}")
            return

        subtotal = quantity * product["price"]

        discount_percentage = float(input("Enter discount percentage (%): "))

        if not 0 <= discount_percentage <= 100:
            print("Discount percentage must be between 0 and 100.")
            return

        gst_percentage = GST_PERCENTAGE

        discount_amount = subtotal * (discount_percentage / 100)
        gst_amount = (subtotal - discount_amount) * (gst_percentage / 100)
        grand_total = subtotal - discount_amount + gst_amount

        # Update stock
        product["stock"] -= quantity

        # Capture current date and time once
        current_datetime = datetime.now()

        # Record the sale
        sale_record = {
            "product_id": product_id,
            "name": product["name"],
            "quantity": quantity,
            "subtotal": subtotal,
            "discount_percentage": discount_percentage,
            "discount_amount": discount_amount,
            "gst_percentage": gst_percentage,
            "gst_amount": gst_amount,
            "grand_total": grand_total,
            # Date & Time
            "sale_date": current_datetime.strftime("%Y-%m-%d"),
            "sale_time": current_datetime.strftime("%H:%M:%S"),
            "sale_datetime": current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        }
        sales_log.append(sale_record)
        product["sales_history"].append(sale_record)

        print(
            f"Sold {quantity} units of '{product['name']}'. Total price: INR {sale_record['grand_total']}"
        )

        choice = input("\nGenerate Invoice? (Y/N): ").strip().upper()
        if choice == "Y":
            generate_invoice(product_id=product_id)

    except ValueError:
        print("Invalid input. Quantity must be a whole number.")


def search_product():
    """
    Function to search for a product by ID or name.
    """

    print("\nSEARCH PRODUCT")

    search_term = input("\nEnter Product ID or Name to search: ").strip().lower()
    found_products = []

    for product_id, details in inventory.items():
        if search_term == product_id.lower() or search_term in details["name"].lower():
            found_products.append((product_id, details))

    if not found_products:
        print("No products found matching the search criteria.")
        return

    print(f"\n✓ Total Products Found : {len(found_products)}\n")
    for product_id, details in found_products:
        print("-" * 60)
        print(f"ID       : {product_id}")
        print(f"Name     : {details['name']}")
        print(f"Category : {details['category']}")
        print(f"Price    : ₹{details['price']:.2f}")
        print(f"Stock    : {details['stock']}")
    print("-" * 60)


def low_stock_report():
    """
    Function to generate a report of products with low stock.
    """
    low_stock_products = []

    for product_id, details in inventory.items():
        if details["stock"] <= STOCK_THRESHOLD:
            low_stock_products.append((product_id, details))

    if not low_stock_products:
        print("No products with stock below the specified threshold.")
        return

    for product_id, details in low_stock_products:
        print("-" * 60)
        print(f"Product ID      : {product_id}")
        print(f"Product Name    : {details['name']}")
        print(f"Current Stock   : {details['stock']} Units")
        print("Status          : LOW STOCK")
    print("-" * 60)
    print(f"Total Products Requiring Restock : {len(low_stock_products)}")
    print("=" * 60)


def category_summary():
    """
    Function to generate a summary of products by category.
    """
    print("\nCATEGORY SUMMARY")

    category_dictionary = {}

    for product_id, details in inventory.items():
        category = details["category"]
        if category not in category_dictionary:

            category_dictionary[category] = {
                "total_products": 0,
                "total_stock": 0,
                "total_value": 0.0,
            }

        category_dictionary[category]["total_products"] += 1
        category_dictionary[category]["total_stock"] += details["stock"]
        category_dictionary[category]["total_value"] += (
            details["stock"] * details["price"]
        )

    if not category_dictionary:
        print("No products available to summarize.")
        return

    print(f"\nTotal Categories : {len(category_dictionary)}\n")
    for category, summary in category_dictionary.items():
        print("-" * 60)
        print(f"Category Name      : {category}")
        print(f"Total Products     : {summary['total_products']}")
        print(f"Total Stock        : {summary['total_stock']} Units")
        print(f"Inventory Value    : ₹{summary['total_value']:,.2f}")
    print("-" * 60)


def unique_categories():
    """
    Function to display all unique product categories.
    """

    if not categories_set:
        print("No categories available.")
        return

    print("Unique Product Categories:")
    print(f"\nTotal Unique Categories: {len(categories_set)}")
    print("-" * 60)
    for index, category in enumerate(sorted(categories_set), start=1):
        print(f"{index}.  {category}")
    print("-" * 60)


def unique_products_sold_today():
    """
    Function to display all unique products sold today.
    """

    today = datetime.now().strftime("%Y-%m-%d")
    unique_products_today = set()

    for sale in sales_log:
        if sale["sale_date"] == today:
            unique_products_today.add(sale["name"])

    if not unique_products_today:
        print("No products sold today.")
        return

    print("Unique Products Sold Today:")
    print("-" * 60)
    print(f"\nDate                 : {today}")
    print("=" * 60)
    for index, name in enumerate(sorted(unique_products_today), start=1):
        print(f"{index}. {name}")
    print("-" * 60)
    print("Products Sold Today")
    print("-" * 60)
    print("-" * 60)


def generate_invoice(product_id=None):
    """
    Function to generate an invoice for a sale.
    """
    print("\nSALES INVOICE")

    if product_id is None:
        product_id = (
            input("\nEnter Product ID for invoice generation: ").strip().upper()
        )

    if product_id not in inventory:
        print("Product ID does not exist.")
        return

    product = inventory[product_id]

    if not product["sales_history"]:
        print(f"No sales history available for '{product['name']}'.")
        return

    last_sale = product["sales_history"][-1]
    invoice_number = f"INV{len(sales_log):05d}"  # Simple invoice number generation

    print("\n" + "=" * 50)
    print(f"Invoice for Product: {product['name']} (ID: {product_id})")
    print("=" * 50)
    print(f"Invoice Number   : {invoice_number}")
    print(f"Sale Date        : {last_sale['sale_date']}")
    print(f"Sale Time        : {last_sale['sale_time']}")
    print("-" * 60)
    print("SALE DETAILS")
    print("-" * 60)
    print(f"Product ID       : {product_id}")
    print(f"Product Name     : {product['name']}")
    print(f"Quantity         : {last_sale['quantity']}")
    print(f"Unit Price       : ₹{product['price']:.2f}")
    print("-" * 60)
    print("BILL SUMMARY")
    print("-" * 60)
    print(f"Subtotal         : ₹{last_sale['subtotal']:.2f}")
    print(
        f"Discount ({last_sale['discount_percentage']}%) : -₹{last_sale['discount_amount']:.2f}"
    )
    print(
        f"GST ({last_sale['gst_percentage']}%)      : +₹{last_sale['gst_amount']:.2f}"
    )
    print("=" * 60)
    print(f"Grand Total      : ₹{last_sale['grand_total']:.2f}")
    print("=" * 60)
    print("\nThank you for your business!")
    print("Visit Again!")


def save_data():
    """
    Function to save inventory and sales data to JSON files.
    """
    print("\nSAVING DATA...")

    try:

        with open("data/inventory.json", "w") as inventory_file:
            json.dump(inventory, inventory_file, indent=4)
        with open("data/sales_log.json", "w") as sales_file:
            json.dump(sales_log, sales_file, indent=4)
        with open("data/categories.json", "w") as category_file:
            json.dump(list(categories_set), category_file, indent=4)
        print("\n✓ DATA SAVED SUCCESSFULLY")
        print("-" * 60)
        print(f"Inventory File    : inventory.json")
        print(f"Sales Log File    : sales_log.json")
        print(f"Categories File   : categories.json")
        print("-" * 60)

    except Exception as e:
        print(f"Error saving data: {e}")


def load_data():
    """
    Function to load inventory and sales data from JSON files.
    """
    global inventory, sales_log, categories_set

    try:
        with open("data/inventory.json", "r") as inventory_file:
            inventory = json.load(inventory_file)
        with open("data/sales_log.json", "r") as sales_file:
            sales_log = json.load(sales_file)
        with open("data/categories.json", "r") as category_file:
            categories_set = set(json.load(category_file))
        print("\n✓ DATA LOADED SUCCESSFULLY")
        print("-" * 60)
        print(f"Products Loaded     : {len(inventory)}")
        print(f"Sales Records       : {len(sales_log)}")
        print(f"Categories Loaded   : {len(categories_set)}")
        print("-" * 60)

    except FileNotFoundError:
        print("Data files not found. Starting with empty data.")

    except Exception as e:
        print(f"Error loading data: {e}")


def press_enter():
    """
    Pause the program until the user presses Enter.
    """
    input("\nPress Enter to return to the Main Menu...")
