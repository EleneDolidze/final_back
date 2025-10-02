#ტესტირება დაჯავშნა მხოლოდ თავისუფალ ოთახებზე ხდება თუ არა
from datetime import date
from back import Hotel, Room, Customer

def create_hotel():
    rooms = [
        Room(501, "Single", 80, True, 1),
        Room(502, "Double", 120, True, 2)
    ]
    return Hotel("Lyon Inn", rooms)

def test_show_available_rooms():
    hotel = create_hotel()
    all_free = hotel.show_available_rooms()
    assert len(all_free) == 2

def test_booking_only_available_rooms():
    hotel = create_hotel()
    customer1 = Customer("Elenn", 1500, booked_rooms = [], points = 0)
    assert hotel.book_room_for_customer(customer1, room_number = 501, nights = 1, start_date = date(2025, 4,17), end_date = date(2025, 4, 20)) is True

    customer2 = Customer("Anna", 1500)
    assert hotel.book_room_for_customer(
        customer2, room_number=501, nights=1,
        start_date=date(2025, 4, 18), end_date=date(2025, 4, 19)) is False

