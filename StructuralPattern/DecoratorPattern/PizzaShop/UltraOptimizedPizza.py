""" Decorator Pattern – Build-Your-Own Pizza Ordering Service (LLD / OOD Prompt)

**Focus:** SOLID principles + Decorator pattern.  
**Scope:** In-memory domain model only (no DB, no threading/locks, no networking).

---

## Problem Statement

You’re designing the **core domain objects** for a startup pizza-delivery service that lets customers compose *any* pizza at runtime. Instead of predefining every combination (Small-Thin-Mushroom-ExtraCheese-Farmhouse, etc.), the system should let us **wrap** a base pizza with additional features (crust, toppings, specials) dynamically—classic Decorator use case.

Customers can add multiple pizzas to an order (cart), see per-item pricing, a delivery fee, and an order total, then print a simple receipt.

---

## Menu Data (initial set)

| Category | Items | Price | Notes |
|----------|-------|-------|-------|
| **Size** *(mandatory)* | Small 10″ ($8), Medium 14″ ($10), Large 18″ ($12) | Base pizza price. Exactly one per pizza. |
| **Crust** *(choose one)* | Thin ($1), Regular ($2), Deep Dish ($3) | Optional but if supplied must be exactly one. |
| **Topping(s)** *(0+)* | Pepperoni ($1.50), Mushroom ($1.00), Extra Cheese ($1.25) | Can stack; order doesn’t matter for cost. |
| **Special Add-Ons** *(0+)* | Farmhouse (+$5), Margarita (+$2), Veggie Delight (+$5) | Marketing bundles; just price + label for now. |

> Prices are additive. Description should list everything applied.

---

## Functional Requirements

1. **Create a pizza with a size** (required).
2. **Add exactly one crust** (if provided; replaceable).
3. **Add zero or more toppings** (repeatable).
4. **Add zero or more “special” bundles** (repeatable).
5. **Compute pizza cost** as sum of size + all add-ons.
6. **Generate human-readable description** concatenating all chosen components.
7. **Shopping cart / order**: hold N pizzas (each with its own composition) and a quantity per line item.
8. **Order total** = sum(line_item_cost × qty) + flat delivery fee.
9. **Print simple receipt**: order id, customer name, line items w/ extended cost, delivery fee, grand total.

---

## Design Goals (Tie to SOLID)

- **Single Responsibility:** Each decorator adds *exactly one* concern (crust, topping, special).
- **Open/Closed:** Add a new topping by data extension—not by modifying existing classes.
- **Liskov Substitution:** Any decorated pizza must behave as a `Pizza` (supports `cost()`, `description()`).
- **Interface Segregation:** Keep the pizza interface minimal—don’t force irrelevant methods.
- **Dependency Inversion:** High-level code (`Order`, cart) depends on the `Pizza` abstraction, not concrete implementations.

---

## Pattern Guidance

Use the **Decorator pattern**:

- Start with a **base component**: `Pizza` interface / abstract class.
- Concrete base: `SizePizza` (wraps a `Size` enum constant).
- Decorators wrap another `Pizza` and add:
  - Cost delta
  - Description suffix
- Chain decorators to build the full pizza composition at runtime.

You *may* implement separate decorators (`CrustPizza`, `ToppingPizza`, `SpecialPizza`) **or** a single generic `AddonPizza` that accepts any priced menu item—be ready to discuss trade-offs.

---

## Business Rule Considerations (Discuss / Enforce)

- **One crust max** per pizza.
- Prevent (or allow and sum) **duplicate toppings**? Clarify; either is OK if explained.
- **Money precision:** floats vs `Decimal` / integer cents.
- **Menu growth:** how to add new items without changing client code?
- **Receipt formatting vs pricing logic:** separate responsibilities?

"""

from abc import ABC, abstractmethod
from typing import List, Optional

from enum import Enum

class PricedItem(Enum):
    def __init__(self, price, desc):
        self.price = price
        self.desc = desc

class Size(PricedItem):
    SMALL = (8.0, 'Small Pizza (10")')
    MEDIUM = (10.0, 'Medium Pizza (14")')
    LARGE = (12.0, 'Large Pizza (18")')

class Crust(PricedItem):
    THIN = (1.0, "Thin Crust")
    REGULAR = (2.0, "Regular Crust")
    DEEPDISH = (3.0, "Deep Dish Crust")



class Topping(PricedItem):
    PEPPERONI = (1.5, "Pepperoni")
    MUSHROOM = (1.0, "Mushroom")
    EXTRACHEESE = (1.25, "Extra Cheese")


class Special(PricedItem):
    FARMHOUSE = (5.0, "Farmhouse")
    MARGARITA = (2.0, "Margarita")
    VEGGIEDELIGHT = (5.0, "Veggie Delight")

    

# Base Pizza class
class Food(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> float:
        pass

class Pizza(Food):
    pass

class SizePizza(Pizza):
    def __init__(self, size: Size):
        self._size = size
    def get_description(self) -> str:
        return self._size.desc
    
    def get_cost(self) -> float:
        return self._size.price
    
class PizzaDecorator(Pizza):
    def __init__(self, base_pizza: Pizza):
        self._base_pizza = base_pizza

    def get_description(self) -> str:
        return self._base_pizza.get_description()
    
    def get_cost(self) -> float:
        return self._base_pizza.get_cost()
    

class AddOnPizza(PizzaDecorator):
    def __init__(self, base_pizza: Pizza, priced_item: PricedItem):
        super().__init__(base_pizza)
        self._add_on = priced_item

    def get_description(self) -> str:
        return f"{self._base_pizza.get_description()}, {self._add_on.desc}"
    
    def get_cost(self) -> float:
        return self._base_pizza.get_cost() + self._add_on.price
    

# Crust Decorators
class CrustPizza(AddOnPizza):
    def __init__(self, base_pizza: Pizza, crust: Crust):
        super().__init__(base_pizza, crust)
    

# Toppings
class ToppingPizza(AddOnPizza):
    def __init__(self, base_pizza: Pizza, topping: Topping):
        super().__init__(base_pizza, topping)
    
    
# Special
class SpecialPizza(AddOnPizza):
    def __init__(self, base_pizza: Pizza, special: Special):
        super().__init__(base_pizza, special)
    
    
class CartItem:
    def __init__(self, food: Food, quanitity: int):
        self._food = food
        self.quantity = quanitity

    def total(self) -> float:
        return self._food.get_cost() * self.quantity
    
    def display(self) -> str:
        return f"{self._food.get_description()} x {self.quantity}"
    
class Customer:
    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name
    
class BasePizzaFactory:
    @staticmethod
    def get_base_pizza_size(size: Size) -> Pizza:
        return SizePizza(size)
    
class AddonPizzaFactory:
    @staticmethod
    def get_addon_pizza(base_pizza: Pizza ,priced_item: PricedItem) -> Pizza:
        return AddOnPizza(base_pizza, priced_item) 
    
class FoodBuilder:
    @abstractmethod
    def make_food(self, quantity: int) -> CartItem:
        pass

class PizzaBuilder(FoodBuilder):
    def __init__(self, size: Size = Size.SMALL, crust: Optional[Crust] = None, toppings: Optional[List[Topping]] = None, special: Optional[Special] = None):
        self._size = size
        self._crust = crust
        self._toppings = toppings
        self._special = special
        self._pizza = None

    def _build_pizza(self, quantity: int = 1) -> CartItem:
        self._pizza = BasePizzaFactory.get_base_pizza_size(self._size)
        if self._crust:
            self._pizza = AddonPizzaFactory.get_addon_pizza(self._pizza, self._crust)
        if self._toppings:
            for topping in self._toppings:
                self._pizza = AddonPizzaFactory.get_addon_pizza(self._pizza, topping)
        if self._special:
            self._pizza = AddonPizzaFactory.get_addon_pizza(self._pizza, self._special)

        return CartItem(self._pizza, quantity)
    
    def make_food(self, quantity: int = 1):
        return self._build_pizza(quantity)

        
class Order:
    DELIVERY_FEE = 3.99
    _next_id= 1

    def __init__(self, items: List[CartItem], customer: Customer):
        self._items: List[CartItem] = items
        self._customer = customer
        self.id = Order._next_id
        Order._next_id += 1

    def _calculate_total(self) -> float:
        return sum(item.total() for item in self._items) + self.DELIVERY_FEE
    
    def _order_description(self) -> str:
        description: List[str] = []
        for item in self._items:
            description.append(item.display())
        return ", ".join(description)
    
    def print_receipt(self) -> str:
        print(f"Order ID     : {self.id}")
        print(f"Customer     : {self._customer.get_name()}")
        print(f"--------------------- Items Ordered ---------------------")
        for item in self._items:
            print(f"{item.display()} : {item.total()}")
        print(f"Delivery Fee : ${self.DELIVERY_FEE:.2f}")
        print(f"Order Total  : ${self._calculate_total():.2f}")
    
if __name__ == "__main__":
    c1 = Customer("Sushil Bhandary")
    topping_list1: List[Topping] = [Topping.MUSHROOM, Topping.EXTRACHEESE]
    p1 = PizzaBuilder(Size.LARGE, Crust.REGULAR, topping_list1, Special.FARMHOUSE).make_food()
    p2 = PizzaBuilder(Size.MEDIUM, special=Special.VEGGIEDELIGHT).make_food(2)
    topping_list3: List[Topping] = [Topping.EXTRACHEESE]
    p3 = PizzaBuilder(Size.SMALL, Crust.THIN, topping_list3).make_food(3)

    # p1 = SpecialPizza(ToppingPizza(ToppingPizza(CrustPizza(SizePizza(Size.LARGE), Crust.REGULAR), Topping.MUSHROOM), Topping.EXTRACHEESE), Special.FARMHOUSE)
    # p2 = SpecialPizza(SizePizza(Size.MEDIUM), Special.VEGGIEDELIGHT)
    # p3 = CrustPizza(ToppingPizza(SizePizza(Size.SMALL), Topping.EXTRACHEESE), Crust.THIN)

    items: List[CartItem] = [p1, p2, p3]
    
    order1 = Order(items, c1)

    order1.print_receipt()
