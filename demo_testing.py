#დემო ვერსია კონსოლური აპლიკაცია

from datetime import date
from back import Hotel, Room, Customer  #back ფაილიდან წამოღებულია კლასები თავისი ატრიბუტებით და მეთოდებით

def create_hotel():
    rooms = [
        Room(501, "Single", 80.0, True, 1),
        Room(502, "Double", 120.0, True, 2),
        Room(503, "Single", 70.0, True, 1),
        Room(504, "Double", 150.0, True, 2),
    ]
    return Hotel("Lyon Inn", rooms)

def ask_budget():
    while True:
        s = input("Budget ($): ").strip()
        try:
            x = float(s)
            if x >= 0:
                return x
            print("Budget must be ≥ 0.")
        except ValueError:
            print("Enter valid number.")

def ask_nights():
    while True:
        s = input("How many nights? ").strip()
        try:
            x = int(s)
            if x >= 1:
                return x
            print("Nights must be ≥ 1.")
        except ValueError:
            print("Enter whole number (Example: 1, 2, 3...).")

def ask_room_type():
    s = input("Room type (Single/Double) — blank =All:").strip()
    if s == "":
        return None
    if s.lower() in ("single", "s"):
        return "Single"
    if s.lower() in ("double", "d"):
        return "Double"
    return None

def choose_room_number(available):
    valid = {r.room_number for r in available}
    while True:
        s = input("Choose room number: ").strip()
        if not s.isdigit():
            print("Enter only number (Example: 501).")
            continue
        rn = int(s)
        if rn in valid:
            return rn
        print("This number is not available. Try again!")

def main():
    print("Welcome to our hotel.")
    hotel = create_hotel()

    name = input("Your name: ").strip() or "Guest"
    budget = ask_budget()
    customer = Customer(name=name, budget=budget)

    while True:
        room_type = ask_room_type()
        nights = ask_nights()
        start = date.today()


        available = hotel.show_available_rooms(room_type)
        if not available:
            print("No available rooms with this criteria. Try again.")
            continue

        print("\nAvailable rooms:")
        for r in available:
            print(f"#{r.room_number} | {r.room_type} | ${r.price_per_night}/nights | max {r.max_guests}")


        rn = choose_room_number(available)


        try:
            total = hotel.calculate_total_booking(rn, nights, start)
        except ValueError as e:
            print(f"Error: {e}. Try again.")
            continue

        print(f"\nTotal cost: ${total:.2f}")

        # 4–5–6–7: გადახდა/ქულები/ლოგი/ჯავშანი
        ok = hotel.book_room_for_customer(customer, rn, nights, start)
        if ok:
            print("Booking was successful.")
            print(customer.show_booking_summary())
            break
        else:
            print("Booking failed. Try again.")

if __name__ == "__main__":
    main()
