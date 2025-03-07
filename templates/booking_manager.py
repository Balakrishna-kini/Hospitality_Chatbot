import json
from datetime import datetime

class BookingManager:
    def __init__(self, filename='bookings.json'):
        self.filename = filename
        self.bookings = self.load_bookings()

    def load_bookings(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_bookings(self):
        with open(self.filename, 'w') as f:
            json.dump(self.bookings, f, indent=2)

    def add_booking(self, name, check_in, check_out, contact):
        booking = {
            'id': len(self.bookings) + 1,
            'name': name,
            'check_in': check_in,
            'check_out': check_out,
            'contact': contact,
            'timestamp': datetime.now().isoformat()
        }
        self.bookings.append(booking)
        self.save_bookings()
        return booking['id']

    def get_booking(self, booking_id):
        for booking in self.bookings:
            if booking['id'] == booking_id:
                return booking
        return None

    def get_all_bookings(self):
        return self.bookings

