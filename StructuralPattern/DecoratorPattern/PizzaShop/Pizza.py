from abc import ABC, abstractmethod
from typing import List

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


class Food(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> float:
        pass  

# Base Pizza class
class Pizza(Food):
    pass

class SmallPizza(Pizza):
    def get_description(self) -> str:
        return Size.SMALL.desc
    
    def get_cost(self) -> float:
        return Size.SMALL.price
    

class MediumPizza(Pizza):
    def get_description(self) -> str:
        return Size.MEDIUM.desc
    
    def get_cost(self) -> float:
        return Size.MEDIUM.price
    
class LargePizza(Pizza):
    def get_description(self) -> str:
        return Size.LARGE.desc
    
    def get_cost(self) -> float:
        return Size.LARGE.price
    
class PizzaDecorator(Pizza):
    def __init__(self, base_pizza: Pizza):
        self._base_pizza = base_pizza

    def get_description(self) -> str:
        return self._base_pizza.get_description()
    
    def get_cost(self) -> float:
        return self._base_pizza.get_cost()
    

# Crust Decorators
class ThinCrust(PizzaDecorator):
    def __init__(self, base_pizza: Pizza):
        super().__init__(base_pizza)

    def get_description(self) -> str:
        return self._base_pizza.get_description() + ", " + Crust.THIN.desc
    
    def get_cost(self) -> float:
        return self._base_pizza.get_cost() + Crust.THIN.price
    
class RegularCrust(PizzaDecorator):
    def __init__(self, base_pizza: Pizza):
        super().__init__(base_pizza)

    def get_description(self) -> str:
        return self._base_pizza.get_description() + ", " + Crust.REGULAR.desc
    
    def get_cost(self) -> float:
        return self._base_pizza.get_cost() + Crust.REGULAR.price
    
class DeepDishCrust(PizzaDecorator):
    def __init__(self, base_pizza: Pizza):
        super().__init__(base_pizza)

    def get_description(self) -> str:
        return self._base_pizza.get_description() + ", " + Crust.DEEPDISH.desc
    
    def get_cost(self) -> float:
        return self._base_pizza.get_cost() + Crust.DEEPDISH.price
    

# Toppings
class Pepperoni(PizzaDecorator):
    def __init__(self, base_pizza: Pizza):
        super().__init__(base_pizza)

    def get_description(self):
        return self._base_pizza.get_description() + ", " + Topping.PEPPERONI.desc
    
    def get_cost(self):
        return self._base_pizza.get_cost() + Topping.PEPPERONI.price
    
class Mushroom(PizzaDecorator):
    def __init__(self, base_pizza: Pizza):
        super().__init__(base_pizza)

    def get_description(self) -> str:
        return self._base_pizza.get_description() + ", " + Topping.MUSHROOM.desc
    
    def get_cost(self) -> float:
        return self._base_pizza.get_cost() + Topping.MUSHROOM.price
    
class ExtraCheese(PizzaDecorator):
    def __init__(self, base_pizza: Pizza):
        super().__init__(base_pizza)

    def get_description(self) -> str:
        return self._base_pizza.get_description() + ", " + Topping.EXTRACHEESE.desc
    
    def get_cost(self) -> float:
        return self._base_pizza.get_cost() + Topping.EXTRACHEESE.price
    
# Special
class Farmhouse(PizzaDecorator):
    def __init__(self, base_pizza: Pizza):
        super().__init__(base_pizza)

    def get_description(self) -> str:
        return self._base_pizza.get_description() + ", " + Special.FARMHOUSE.desc
    
    def get_cost(self) -> float:
        return self._base_pizza.get_cost() + Special.FARMHOUSE.price
    
class Margarita(PizzaDecorator):
    def __init__(self, base_pizza: Pizza):
        super().__init__(base_pizza)

    def get_description(self) -> str:
        return self._base_pizza.get_description() + ", " + Special.MARGARITA.desc
    
    def get_cost(self) -> float:
        return self._base_pizza.get_cost() + Special.MARGARITA.price
    
class VeggieDelight(PizzaDecorator):
    def __init__(self, base_pizza: Pizza):
        super().__init__(base_pizza)

    def get_description(self) -> str:
        return self._base_pizza.get_description() + ", " + Special.VEGGIEDELIGHT.desc
    
    def get_cost(self) -> float:
        return self._base_pizza.get_cost() + Special.VEGGIEDELIGHT.price
    
class CartItem:
    def __init__(self, pizza: Pizza, quanitity: int):
        self.pizza = pizza
        self.quantity = quanitity

    def total(self) -> float:
        return self.pizza.get_cost() * self.quantity
    
    def display(self) -> str:
        return f"{self.pizza.get_description()} x {self.quantity}"
    
class Customer:
    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

# class PizzaShop
        
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
    p1 = Farmhouse(ExtraCheese(Mushroom(RegularCrust(LargePizza()))))
    p2 = VeggieDelight(MediumPizza())
    p3 = ThinCrust(ExtraCheese(SmallPizza()))

    items: List[CartItem] = [CartItem(p1, 1), CartItem(p2, 2), CartItem(p3, 3)]
    
    order1 = Order(items, c1)

    order1.print_receipt()




    


        




