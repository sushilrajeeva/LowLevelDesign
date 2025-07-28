from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from enum import Enum, auto
from collections import defaultdict
from datetime import datetime
import time

# Enumerations for Payment Status, Account Status and Ticket Status
class PaymentStatus(Enum):
    COMPLETED   = auto()
    FAILED      = auto()
    PENDING     = auto()
    UNPAID      = auto()
    REFUNDED    = auto()

class AccountStatus(Enum):
    ACTIVE      = auto()
    CLOSED      = auto()
    CANCELLED   = auto()
    BLACKLISTED = auto()
    NONE        = auto()

class TicketStatus(Enum):
    ISSUED      = auto()
    IN_USE      = auto()
    PAID        = auto()
    VALIDATED   = auto()
    CANCELLED   = auto()
    REFUNDED    = auto()


# Person class
class Person:
    def __init__(self, name: str = "", address: str = "", phone:str = "", email: str = ""):
        self._name: Optional[str] = name
        self._address: Optional[str] = address
        self._phone: Optional[str] = phone
        self._email: Optional[str] = email

    def set_name(self, name: str) -> None:
        self._name = name
    def set_address(self, address: str) -> None:
        self._address = address
    def set_phone(self, phone: str) -> None:
        self._phone = phone
    def set_email(self, email: str) -> None:
        self._email = email

    def get_name(self) -> str:
        return self._name
    def get_address(self) -> str:
        return self._address
    def get_phone(self) -> str:
        return self._phone
    def get_email(self) -> str:
        return self._email
    
# Address class
class Address:
    def __init__(self, zip_code: str = "0", street: str = "", city: str = "", state: str = "", country: str = ""):
        self._zip_code: Optional[str] = zip_code
        self._street: Optional[str] = street
        self._city: Optional[str] = city
        self._state: Optional[str] = state
        self._country: Optional[str] = country

    def set_zip_code(self, zip_code: str) -> None:
        self._zip_code = zip_code
    def set_street(self, street: str) -> None:
        self._street = street
    def set_city(self, city: str) -> None:
        self._city = city
    def set_state(self, state: str) -> None:
        self._state = state
    def set_country(self, country: str) -> None:
        self._country = country

    def get_zip_code(self) -> str:
        return self._zip_code
    def get_street(self) -> str:
        return self._street
    def get_city(self) -> str:
        return self._city
    def get_state(self) -> str:
        return self._state
    def get_country(self) -> str:
        return self._country
    
# Parking Spot -> base class for four different types of spots -> accessible, compact, large and motorcycle. This will have instance of Vehicle class


# Vehicle (Abstract class)
class Vehicle(ABC):
    def __init__(self, licenseNo: int):
        self._licenseNo: int = licenseNo
        self.ticket = None # type: ParkingTicket

    def set_lisence_no(self, licenseNo):
        self._licenseNo = licenseNo

    def get_license_no(self) -> int:
        return self._licenseNo

    def assign_ticket(self, ticket) -> None:
        self.ticket = ticket

    def get_ticket(self):
        return self.ticket

    

class Car(Vehicle):
    pass

class Van(Vehicle):
    pass

class Truck(Vehicle):
    pass

class Motorcycle(Vehicle):
    pass


class ParkingSpot(ABC):
    def __init__(self, id):
        self._id = id
        self.is_free: bool = True
        self.vehicle: Vehicle = None

    def get_id(self) -> int:
        return self._id
    
    def set_is_free(self, is_free: bool) -> None:
        self.is_free = is_free
    def get_is_free(self) -> bool:
        return self.is_free
    def get_vehicle(self) -> Vehicle:
        return self.vehicle
    def set_vehicle(self, vehicle: Vehicle) -> None:
        self.vehicle = vehicle
    
    # setter and getter for these
    @abstractmethod
    def assign_vehicle(self, vehicle: Vehicle) -> bool:
        pass

    def remove_vehicle(self) -> bool:
        if not self.is_free and self.vehicle:
            print(f"Slot {self._id} freed (was {self.vehicle.get_license_no()})")
            self.vehicle = None
            self.is_free = True
            return True
        return False

class Handicapped(ParkingSpot):
    def assign_vehicle(self, vehicle: Vehicle) -> bool:
        if self.is_free:
            print(f"Allocated Handicap Spot {self._id} to {vehicle.get_license_no()}")
            self.is_free = False
            self.vehicle = vehicle
            return True
        return False

class Compact(ParkingSpot):
    def assign_vehicle(self, vehicle: Vehicle) -> bool:
        if self.is_free:
            print(f"Allocated Compact Spot {self._id} to {vehicle.get_license_no()}")
            self.is_free = False
            self.vehicle = vehicle
            return True
        return False

class Large(ParkingSpot):
    def assign_vehicle(self, vehicle: Vehicle) -> bool:
        if self.is_free:
            print(f"Allocated Large Spot {self._id} to {vehicle.get_license_no()}")
            self.is_free = False
            self.vehicle = vehicle
            return True
        return False

class MotorcycleSpot(ParkingSpot):
    def assign_vehicle(self, vehicle: Vehicle) -> bool:
        if self.is_free:
            print(f"Allocated Motorcycle Spot {self._id} to {vehicle.get_license_no()}")
            self.is_free = False
            self.vehicle = vehicle
            return True
        return False

class DisplayBoard:
    def __init__(self, id):
        self.id = id
        self.free_count: Dict[int] = defaultdict(int)

    def update(self, spots: List[ParkingSpot]):
        self.free_count.clear()
        for s in spots:
            if s.get_is_free():
                typ = type(s).__name__
                self.free_count[typ] += 1
    
    def show_free_slots(self):
        print("\n Free slots by type:")
        print(f"{'Type':<15} {'Count'}")
        for typ, cnt in self.free_count.items():
            print(f"{typ:<15} {cnt}")

class ParkingRate:
    def __init__(self):
        self.hours = None
        self.rate = None

    def calculate(self, hours, vehicle, spot):
        hrs: int = int(-(-hours//1))
        fee: int = 0
        if hrs >= 1: fee += 4
        if hrs >= 2: fee += 3.5
        if hrs >= 3: fee += 3.5
        if hrs > 3: fee += (hrs-3) * 2.5
        return fee

class ParkingTicket:
    ticket_seed: int = 1000
    def __init__(self, slot_no: int, vehicle: Vehicle):
        self.ticket_no = ParkingTicket.ticket_seed
        ParkingTicket.ticket_seed += 1
        self.slot_no = slot_no
        self.vehicle = vehicle
        self.entry_time = datetime.now()
        self.exit_time = None
        self.amount: float = 0.0
        self.status = TicketStatus.ISSUED
        self.payment = None
        vehicle.assign_ticket(self)
        print("Ticket issued: " + str(self.ticket_no))

    def get_ticket_no(self) -> int:
        return self.ticket_no
    def get_slot_no(self) -> int:
        return self.slot_no
    def get_vehicle(self) -> Vehicle:
        return self.vehicle
    def get_entry_time(self) -> datetime:
        return self.entry_time
    def get_exit_time(self) -> datetime:
        return self.exit_time
    def set_exit_time(self, time: datetime) -> None:
        self.exit_time = time
    def get_amount(self) -> float:
        return self.amount
    def set_amount(self, amount: int) -> None:
        self.amount = amount
    def get_status(self) -> TicketStatus:
        return self.status
    def set_status(self, status: TicketStatus) -> None:
        self.status = status


class Entrance:
    def __init__(self, id):
        self.id = id

    def get_id(self) -> int:
        return self.id
    
    def get_ticket(self, vehicle: Vehicle):
        return ParkingLot.get_instance().park_vehicle(vehicle)

class Exit:
    def __init__(self, id):
        self.id = id

    def get_id(self) -> int:
        return self.id

    def validate_ticket(self, ticket: ParkingTicket):
        now = datetime.now()
        ticket.set_exit_time(now)
        hrs = (now - ticket.get_entry_time()).total_seconds() / 3600.0
        fee = ParkingLot.get_instance().rate.calculate(hrs, ticket.get_vehicle(), ParkingLot.get_instance().get_spot(ticket.get_slot_no()))
        ticket.set_amount(fee)
        print(f"Ticket {ticket.get_ticket_no()} | Parked: {hrs: .2f} hrs | Fee: ${fee: .2f}")
        payment: Payment = CreditCard(fee) if fee > 10 else Cash(fee)
        payment.initiate_transaction()
        ParkingLot.get_instance().free_slot(ticket.get_slot_no())
        ticket.set_status(TicketStatus.PAID)

# Accounts
class Account:
    def __init__(self, user_name: str, password: str, person: Person, status: AccountStatus):
        self.user_name = user_name
        self.password = password
        self.person: Optional[Person] = person
        self.status: AccountStatus = status

    # getter sand setter
    def reset_password(self) -> bool:
        self.password = "Password@123"
        print(f"Password for {self.user_name} reset to default.")
        return True

class Admin(Account):
    def add_parking_spot(self, spot: ParkingSpot) -> bool:
        # Example: call to ParkingLot singleton to add spot
        ParkingLot.get_instance().add_parking_spot(spot)
        print(f"Admin added parking spot: {spot.get_id()}")
        return True
    
    def add_display_board(self, board: DisplayBoard) -> bool:
        ParkingLot.get_instance().add_display_board(board)
        print(f"Admin added display board: {board.id}")
        return True

    def add_entrance(self, entrance: Entrance) -> bool:
        ParkingLot.get_instance().add_entrance(entrance)
        print(f"Admin added entrance: {entrance.get_id()}")
        return True

    def add_exit(self, exit: Exit) -> bool:
        ParkingLot.get_instance().add_exit(exit)
        print(f"Admin added exit: {exit.get_id()}")
        return True

    def reset_password(self,) -> None:
        self.password = "Admin@123"
        print(f"Admin password reset for {self.user_name}")
        return True

        

class Payment(ABC):
    def __init__(self, amount: float):
        self.amount: float = amount
        self.status: Optional[PaymentStatus] = None
        self.timestamp: datetime = datetime.now()

    @abstractmethod
    def initiate_transaction(self):
        pass

class Cash(Payment):
    def initiate_transaction(self):
        self.status = PaymentStatus.COMPLETED
        print(f"Cash payment of ${self.amount} completed.")
        return True

class CreditCard(Payment):
    def initiate_transaction(self):
        self.status = PaymentStatus.COMPLETED
        print(f"Credit card payment of ${self.amount} completed.")
        return True


class ParkingLot:
    _instance = None

    def __init__(self):
        self.rate: ParkingRate = ParkingRate()

        self.entrances: Optional[Dict[str, Entrance]] = {}
        self.exits: Optional[Dict[str, Exit]] = {}
        self.spots: Optional[Dict[int, ParkingSpot]] = {}
        self.tickets: Optional[Dict[str, ParkingTicket]] = {}
        self.display_boards: Optional[List[DisplayBoard]] = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ParkingLot()
        return cls._instance
    
    def add_entrance(self, entrance: Entrance):
        self.entrances[entrance.get_id()] = entrance

    def add_exit(self, exit: Exit):
        self.exits[exit.get_id()] = exit

    def add_parking_spot(self, spot: ParkingSpot):
        self.spots[spot.get_id()] = spot

    def get_all_spots(self) -> List[ParkingSpot]:
        return self.spots.values()
    
    def can_fit(self, vehicle: Vehicle, spot: ParkingSpot) -> bool:
        if isinstance(vehicle, Motorcycle) and isinstance(spot, MotorcycleSpot): return True
        if isinstance(vehicle, Truck) or isinstance(vehicle, Van) and isinstance(spot, Large): return True
        if isinstance(vehicle, Car) and isinstance(spot, Compact) or isinstance(spot, Handicapped): return True
        return False

    def park_vehicle(self, vehicle: Vehicle):
        for spot in self.spots.values():
            if spot.get_is_free() and self.can_fit(vehicle, spot):
                spot.assign_vehicle(vehicle)
                ticket = ParkingTicket(spot.get_id(), vehicle)
                self.tickets[ticket.get_ticket_no()] = ticket
                return ticket
        print("Sorry, parking lot in full. News cars cannot be parked.")
        return None
    
    def add_display_board(self, board: DisplayBoard) -> None:
        self.display_boards.append(board)
    
    def get_spot(self, id) -> ParkingSpot:
        return self.spots.get(id)
    def free_slot(self, id):
        s = self.get_spot(id)
        if s: s.remove_vehicle()

    



def main():
    print("\n====================== PARKING LOT SYSTEM DEMO ======================\n")

    lot = ParkingLot.get_instance()
    lot.add_parking_spot(Handicapped(1))
    lot.add_parking_spot(Compact(2))
    lot.add_parking_spot(Large(3))
    lot.add_parking_spot(MotorcycleSpot(4))

    board = DisplayBoard(1)
    lot.add_display_board(board)

    entrance = Entrance(1)
    exit_panel = Exit(1)

    # SCENARIO 1: CUSTOMER ENTERS, PARKS
    print("\n→→→ SCENARIO 1: Customer enters and parks a car\n")
    car = Car("KA-01-HH-1234")
    print(f"-> Car {car.get_license_no()} arrives at entrance")
    ticket1 = entrance.get_ticket(car)
    print("-> Updating display board after parking:")
    board.update(lot.get_all_spots())
    board.show_free_slots()

    # SCENARIO 2: CUSTOMER EXITS AND PAYS
    print("\n→→→ SCENARIO 2: Customer exits and pays\n")
    print(f"-> Car {car.get_license_no()} proceeds to exit panel")
    time.sleep(1.5)
    exit_panel.validate_ticket(ticket1)
    print("-> Updating display board after exit:")
    board.update(lot.get_all_spots())
    board.show_free_slots()

    # SCENARIO 3: FILLING LOT AND REJECTING ENTRY IF FULL
    print("\n→→→ SCENARIO 3: Multiple customers attempt to enter; lot may become full\n")
    van = Van("KA-01-HH-9999")
    motorcycle = Motorcycle("KA-02-XX-3333")
    truck = Truck("KA-04-AA-9998")
    car2 = Car("DL-09-YY-1234")

    print(f"-> Van {van.get_license_no()} arrives at entrance")
    ticket2 = entrance.get_ticket(van)
    print(f"-> Motorcycle {motorcycle.get_license_no()} arrives at entrance")
    ticket3 = entrance.get_ticket(motorcycle)
    print(f"-> Truck {truck.get_license_no()} arrives at entrance")
    ticket4 = entrance.get_ticket(truck)
    print(f"-> Car {car2.get_license_no()} arrives at entrance")
    ticket5 = entrance.get_ticket(car2)

    print("-> Updating display board after several parkings:")
    board.update(lot.get_all_spots())
    board.show_free_slots()

    # Try to park another car (lot may now be full)
    car3 = Car("UP-01-CC-1001")
    print(f"-> Car {car3.get_license_no()} attempts to park (should be denied if lot is full):")
    ticket6 = entrance.get_ticket(car3)

    board.update(lot.get_all_spots())
    board.show_free_slots()

    print("\n====================== END OF DEMONSTRATION ======================\n")

if __name__ == "__main__":
    main()