"""
    # Observer Pattern – Product-Level Notification System for E-Commerce

    ## Problem:

    Design a product notification system for an e-commerce platform like Amazon or Walmart.

    The platform offers a wide range of **products** from different **brands and models** (e.g., Apple iPhone 16 Pro, Samsung Galaxy Fold 7). Customers should be able to subscribe to specific **products** they are interested in tracking.

    When a **product goes out of stock**, or when it is **restocked**, only the **customers who have subscribed to that specific product** should receive a notification.

    ### Functional Requirements:

    1. Consumers can **subscribe** to specific products.
    2. When a **product is restocked**, notify all subscribed consumers.
    3. When a **product goes out of stock**, notify all subscribed consumers.
    4. Consumers should receive notifications with relevant product information (name, brand, model, quantity).

    ### Real-World Analogy:

    Just like how Amazon users can "watch" or "track" a specific product (e.g., PS5 Console) to get alerts when it becomes available, your system should notify only those users who have explicitly subscribed to that **exact product**, not the whole category.

"""

# Notification.py
from abc import ABC, abstractmethod
from typing import *
from collections import defaultdict

# -------- Observer Interface --------
class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass


# -------- Observable (Subject) Interface --------
class Observable(ABC):
    @abstractmethod
    def subscribe(self, observer: Observer):
        pass

    @abstractmethod
    def unsubscribe(self, observer: Observer):
        pass

    @abstractmethod
    def notify_all(self, message: str):
        pass


# -------- Observer Implementations --------
class Customer(Observer):
    def __init__(self, name: str):
        self.name = name

    def update(self, message: str):
        print(f"[Generic] {self.name} got a message: {message}")


class EmailCustomer(Customer):
    def __init__(self, name: str, email: str):
        super().__init__(name)
        self.email = email

    def update(self, message: str):
        print(f"[Email] {self.name} <{self.email}> got a notification: {message}")


class PhoneCustomer(Customer):
    def __init__(self, name: str, phone: str):
        super().__init__(name)
        self.phone = phone

    def update(self, message: str):
        print(f"[Phone] {self.name} ({self.phone}) got a text: {message}")

        


# -------- Concrete Observable (Category) --------


class Product(Observable):
    def __init__(self, brand, name, model, quantity=0, price=0):
        self.brand = brand
        self.name = name
        self.model = model
        self.quantity = quantity
        self.price = price
        self.observers: Set[Observer] = set()
        self.product_name = self.brand + " " + self.name + " " + self.model

    def subscribe(self, observer: Observer):
        self.observers.add(observer)
        print(f"{observer.name} subscribed to '{self.product_name}'.")

    def unsubscribe(self, observer: Observer):
        if observer in self.observers:
            self.observers.remove(observer)
            print(f"{observer.name} unsubscribed from '{self.product_name}'.")
        else:
            print(f"Unable to unsubscribe {observer.name} as they have not subscribed to '{self.product_name}' product.")

    def notify_all(self, message: str):
        for observer in self.observers:
            observer.update(message)

    def add_stock(self, quantity):
        was_out = self.quantity == 0
        self.quantity += quantity
        if was_out:
            self.notify_all(f"'{self.product_name}' is now back in stock. Quantity: {self.quantity}")
        else:
            print(f"Added {quantity} units to '{self.product_name}' (Now: {self.quantity})")

    def remove_stock(self, quantity):
        self.quantity -= quantity
        if self.quantity < 0:
            print(f"Quantity of '{self.product_name}' went negative. Resetting to 0.")
            self.quantity = 0
        if self.quantity == 0:
            self.notify_all(f"'{self.product_name}' is now out of stock.")
        else:
            print(f"Removed {quantity} units from '{self.product_name}' (Remaining: {self.quantity})")

def print_divider(title: str):
    print("\n" + "=" * 40)
    print(f"  {title}")
    print("=" * 40 + "\n")


# -------- Demo --------
if __name__ == "__main__":
    # Create customers
    print_divider("CREATING CUSTOMERS")
    alice = EmailCustomer("Alice", "alice@example.com")
    bob   = PhoneCustomer("Bob", "+1234567890")
    carol = Customer("Carol")

    # Create product objects
    print_divider("CREATING PRODUCTS")
    iphone = Product("Apple",  "iPhone",    "16 Pro",   quantity=0, price=999)
    galaxy = Product("Samsung","Galaxy",    "Fold 7",   quantity=10, price=1999)

    # Subscriptions
    print_divider("SUBSCRIPTIONS")
    iphone.subscribe(alice)
    iphone.subscribe(carol)
    galaxy.subscribe(bob)

    # Stock updates for iPhone
    print_divider("IPHONE STOCK UPDATES")
    iphone.add_stock(5)
    iphone.remove_stock(5)
    iphone.remove_stock(1)

    # Stock updates for Galaxy
    print_divider("GALAXY STOCK UPDATES")
    galaxy.remove_stock(5)
    galaxy.remove_stock(5)
    galaxy.remove_stock(1)

    # New product
    print_divider("ADDING A NEW PRODUCT")
    laptop = Product("Dell", "Laptop Pro", "XPS 16", quantity=0, price=1999)
    laptop.subscribe(alice)
    laptop.add_stock(3)