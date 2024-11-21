import csv
from datetime import datetime

# Inventory management system class
class Inventory:
    def __init__(self):
        self.items = {}  # Dictionary to store inventory items
        self.customers = {}  # Dictionary to store customer data
        self.purchase_history = []  # List to store purchase history

    # Method to add a new item to the inventory
    def add_item(self, item_id, item_name, item_brand, price, quantity, update_date):
        self.items[item_id] = {
            "name": item_name.upper(),
            "brand": item_brand.upper(),
            "price": price,
            "quantity": quantity,
            "update_date": update_date
        }
        self.update_inventory_status_csv()  # Update inventory CSV file

    # Method to assign a unique customer ID
    def assign_customer_id(self, email, name):
        if email not in self.customers:
            customer_id = f"CUST{len(self.customers) + 1}"
            self.customers[email] = {
                "customer_id": customer_id,
                "email": email,
                "name": name.title()
            }
        return self.customers[email]["customer_id"]

    # Method to update the price of an item
    def update_price(self, item_id, new_price):
        if item_id in self.items:
            self.items[item_id]["price"] = new_price
            self.items[item_id]["update_date"] = self.get_current_timestamp()
            self.update_inventory_status_csv()  # Update inventory CSV file
        else:
            raise ValueError(f"Item ID {item_id} not found")

    # Method to handle the purchase of an item
    def purchase_item(self, item_id, quantity, customer_name, customer_email):
        if item_id not in self.items:
            raise ValueError(f"Item ID {item_id} not found")

        if quantity <= 0:
            raise ValueError("Purchase quantity must be greater than zero")

        if self.items[item_id]["quantity"] < quantity:
            raise ValueError("Not enough inventory to complete the purchase")

        customer_id = self.assign_customer_id(customer_email, customer_name)
        self.items[item_id]["quantity"] -= quantity
        purchase_record = {
            "item_id": item_id,
            "item_price": self.items[item_id]["price"],
            "quantity": quantity,
            "customer_id": customer_id,
            "customer_name": customer_name.title(),
            "customer_email": customer_email,
            "date": self.get_current_timestamp()
        }
        self.purchase_history.append(purchase_record)  # Add purchase record to history
        self.update_purchase_history_csv(purchase_record)  # Update purchase history CSV file
        self.update_inventory_status_csv()  # Update inventory CSV file

    # Method to update the purchase history CSV file
    def update_purchase_history_csv(self, purchase_record):
        with open('purchase_history.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=purchase_record.keys())
            if file.tell() == 0:  # Write header if file is empty
                writer.writeheader()
            writer.writerow(purchase_record)

    # Method to update the inventory status CSV file
    def update_inventory_status_csv(self):
        with open('inventory_status.csv', mode='w', newline='') as file:
            fieldnames = ["item_id", "name", "brand", "price", "quantity", "update_date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # Write header
            for item_id, item_data in self.items.items():
                row = {
                    "item_id": item_id,
                    "name": item_data["name"],
                    "brand": item_data["brand"],
                    "price": item_data["price"],
                    "quantity": item_data["quantity"],
                    "update_date": item_data["update_date"]
                }
                writer.writerow(row)

    # Method to get the details of an item
    def get_item(self, item_id):
        if item_id in self.items:
            return self.items[item_id]
        else:
            raise ValueError(f"Item ID {item_id} not found")

    # Method to get top customers who spent more than a certain amount
    def get_top_customers_from_csv(self, csv_file, min_spent=5000):
        customer_spending = {}
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                customer_id = row["customer_id"]
                spent = int(row["quantity"]) * float(row["item_price"])
                if customer_id not in customer_spending:
                    customer_spending[customer_id] = spent
                else:
                    customer_spending[customer_id] += spent

        # Get customers who spent more than the specified amount
        top_customers = [
            {"customer_id": customer_id, "total_spent": spent}
            for customer_id, spent in customer_spending.items()
            if spent > min_spent
        ]
        return top_customers

    # Static method to get the current timestamp
    @staticmethod
    def get_current_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
