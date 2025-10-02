#სასტუმროს დაჯავშნის სააგენტო - Back-End

from dataclasses import dataclass, field
from datetime import date
import logging


@dataclass
class Room:  #attributes
    room_number: int
    room_type: str
    price_per_night: float
    is_available: bool
    max_guests: int = 1

    #class Room-ის მეთოდები
    def book_room(self):
        if not self.is_available:
            raise ValueError(f"Room {self.room_number} is not available")
        self.is_available = False

    def release_room(self):
        self.is_available = True

    def calculate_price(self, nights: int):
        if nights <= 0:
            raise ValueError(f"nights must be greater than 0")
        return round(self.price_per_night * nights, 2)

    def __str__(self):  #ოთახის დეტალების სტრინგის სახით დაბრუნება
        status = "Available" if self.is_available else "Unavailable"
        return f"Room {self.room_number} - {self.room_type} - {self.price_per_night} - max{self.max_guests} - {status}"


@dataclass
class Customer:  #attributes
    name: str
    budget: float
    booked_rooms: list = field(default_factory = list)
    points : int = 0

    #მეთოდები
    # ოთახის დამატება დაჯავშნაში
    def add_room(self, room: Room):
        if room not in self.booked_rooms:
            self.booked_rooms.append(room)


    # ოთახის წაშლა დაჯავშნიდან
    def remove_room(self, room: Room):
        if room in self.booked_rooms:
            self.booked_rooms.remove(room)

    #გადახდა და ბიუჯეტის შემოწმება
    def pay_for_booking(self, total_price: float):
        if total_price < 0:
            raise ValueError(f"total_price must be greater than 0")
        if self.budget >= total_price:
            self.budget = round(self.budget - total_price, 2)
            self.points += int(total_price // 10)
            return True
        return False

    #სტრიგის სახით დაბრუნება დაჯავშნილი ოთახები+ღირებულება
    def show_booking_summary(self):
        rooms: list = []
        for room in self.booked_rooms:
            rooms.append(room)
        return f"Customer: {self.name} - Budget : ${self.budget} - Rooms: {rooms}"



#ფასის სეზონურად გამოთვლა
season_multipliers = {
    "high": 1.5,
    "middle": 1.2,
    "low": 0.8
}

def season_s(datetime: date):
    month = datetime.month
    if month in (5,6,7,8):
        return  "high"
    elif month in (4,9,10):
        return "middle"
    return "low"


def apply_seasonal_price(base_total: float, start: date):
    mult = season_multipliers[season_s(start)]
    return round(base_total * mult, 2)



#ლოგირების ფაილის შექმნა
_logger = logging.getLogger("hotel_booking")
_logger.setLevel(logging.INFO)

if not _logger.handlers:
    #ლოგების ჩაწერა ამ ფაილში
    f_h = logging.FileHandler("hotel_booking.log", mode="a", encoding="utf-8")
    f_h.setLevel(logging.INFO)

    #ლოგირების ჩაწერის ფორმატირება
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    f_h.setFormatter(formatter)
    _logger.addHandler(f_h)



class Hotel:  #attributes
    def __init__(self, name: str, rooms):
        self.name = name
        self.rooms = rooms
        self.bookings_log = []

    #ოთახის მოძებნა
    def _find_room(self, room_number: int):
        for r in self.rooms:
            if r.room_number == room_number:
                return r
        return None


    #თავისუფალი ოთახების სია
    def show_available_rooms(self, room_type = None):
        result = []
        for r in self.rooms:
            if not r.is_available:
                continue
            if room_type is None or r.room_type.lower() == room_type.lower():
                result.append(r)
        return result


    #ჯამური ღირებულება
    def calculate_total_booking(self, room_number, nights, start_date, end_date=None):
        room = self._find_room(room_number)
        if room is None:
            raise ValueError("Room not Found")
        base_total = room.calculate_price(nights)
        return apply_seasonal_price(base_total, start_date)


    #კონკრეტული ოთახის დაჯავშნა და ლოგირება ფაილში
    def book_room_for_customer(self, customer, room_number, nights, start_date, end_date=None):
        room = self._find_room(room_number)
        if room is None or not room.is_available:
            _logger.info(f"BOOKING FAILED - customer = {customer.name} - room = {room_number} - reason = no_room_or_unavailable")
            return False

        total_price = self.calculate_total_booking(room_number, nights, start_date, end_date)
        if not customer.pay_for_booking(total_price):
            _logger.info(f"BOOKING FAILED - customer = {customer.name} - room = {room_number} - reason = insufficient_funds - price = {total_price}")
            return False

        room.book_room()
        customer.add_room(room)
        self.log_booking(customer.name, room.room_number, room.room_type, nights, start_date, total_price)
        return True


    #ლოგირება დაჯავშნის
    def log_booking(self, customer_name: str, room_number: int, room_type: str, nights: int, start_date: date, total_price: float):
        entry = {
            "customer_name": customer_name,
            "room_number": room_number,
            "room_type": room_type,
            "nights": nights,
            "start_date": start_date.isoformat(),
            "total_price": total_price
        }
        self.bookings_log.append(entry)
        _logger.info(f"BOOKED - {entry}")


    #დაჯავშნის გაუქმება
    def cancel_booking(self, customer, room_number: int):
        room = self._find_room(room_number)
        if room and room in customer.booked_rooms:
            room.release_room()
            customer.remove_room(room)
            entry = {"cancelled": True, "customer": customer.name, "room_number": room_number}
            self.bookings_log.append(entry)
            _logger.info(f"CANCELLED - {entry}")
            return True
        _logger.info(f"CANCEL_FAILED - customer = {customer.name} - room = {room_number}")
        return False


#გატესტვა ჩემი მონაცემებით
if __name__ == "__main__":

    rooms = [
        Room(501, "Single", 80.0, True, 1),
        Room(502, "Double", 120.0, True, 2),
    ]
    hotel = Hotel("Lyon Inn", rooms)
    customer = Customer(name="Elene", budget=300)


    print("Available rooms:")
    for room in hotel.show_available_rooms():
        print(room)


    booking_testing = hotel.book_room_for_customer(customer, room_number=501, nights=2, start_date=date.today())
    print("Booked:", booking_testing)
    print(customer.show_booking_summary())



