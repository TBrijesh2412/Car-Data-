from datetime import datetime, timedelta
# from prettytable import PrettyTable

class CarCategory:
    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name

class Car:
    def __init__(self, car_id, car_name, rent_per_day, category, available=True):
        self.car_id = car_id
        self.car_name = car_name
        self.rent_per_day = rent_per_day
        self.category = category
        self.available = available

class RentalSystem:
    def __init__(self):
        self.cars = []

        
        self.rented_cars = {}
        self.rent_submission_dates = {}

    def initialize_rent_submission_dates(self):
        today_date = datetime.now().date()
        for i in range(7):
            date = today_date - timedelta(days=i)
            self.rent_submission_dates[date] = 0

    def show_available_cars(self):
        table = PrettyTable()
        table.field_names = ["Car ID", "Car Name", "Category", "Rent per Day"]
        for car in self.cars:
            if car.available:
                table.add_row([car.car_id, car.car_name, car.category.category_name, car.rent_per_day])
        print("\nAvailable Cars:")
        print(table)

    def add_car(self, car_id, car_name, rent_per_day, category):
        for car in self.cars:
            if car.car_id == car_id:
                print("Car with the same ID already exists. Please use a different ID.")
                return
        self.cars.append(Car(car_id, car_name, rent_per_day, category))

    def remove_car(self, car_id):
        for car in self.cars:
            if car.car_id == car_id:
                self.cars.remove(car)
                print("Car removed successfully.")
                return
        print("Car not found.")

    def rent_car(self, car_id, name, phone_number, days, booking_date_str):
        today_date = datetime.now().date()
        booking_date = datetime.strptime(booking_date_str, "%d-%m-%Y").date()

        if booking_date >= today_date:
            for car in self.cars:
                if car.car_id == car_id:
                    if car.available:
                        car.available = False
                        return_date = booking_date + timedelta(days=days)
                        rent_amount = days * car.rent_per_day
                        self.rented_cars[car_id] = {"name": name, "phone_number": phone_number, "booking_date": booking_date, 
                                                     "return_date": return_date, "rent_amount": rent_amount}
                        print("Car rented successfully.")

                        # Update rent submission dates
                        submission_date = datetime.now().date()
                        if submission_date in self.rent_submission_dates:
                            self.rent_submission_dates[submission_date] += 1
                        else:
                            self.rent_submission_dates[submission_date] = 1
                    else:
                        print("Car is not available for rent.")
                    return
            print("Car not found.")
        else:
            print("Invalid booking date. Please select today's date or a future date.")

    def show_rented_cars(self):
        table = PrettyTable()
        table.field_names = ["Car ID", "Name", "Phone Number", "Booking Date", "Return Date", "Rent Amount"]
        for car_id, details in self.rented_cars.items():
            table.add_row([car_id, details['name'], details['phone_number'], 
                           details['booking_date'].strftime('%d-%m-%Y'),
                           details['return_date'].strftime('%d-%m-%Y'),
                           details['rent_amount']])
        print("\nRented Cars:")
        print(table)

    def cancel_booking(self, car_id):
        if car_id in self.rented_cars:
            del self.rented_cars[car_id]
            print("Booking canceled successfully.")
        else:
            print("Car not found in rented list.")

    def submit_rent(self, car_id):
        if car_id in self.rented_cars:
            for car in self.cars:
                if car.car_id == car_id:
                    car.available = True
                    del self.rented_cars[car_id]
                    print("Rent submitted successfully.")
                    return
        print("Car not found in rented list.")

    def extend_rental(self, car_id, days):
        if car_id in self.rented_cars:
            details = self.rented_cars[car_id]
            return_date = details['return_date'] + timedelta(days=days)
            rent_amount = details['rent_amount'] + (days * self.cars[car_id - 1].rent_per_day)
            self.rented_cars[car_id]['return_date'] = return_date
            self.rented_cars[car_id]['rent_amount'] = rent_amount
            print("Rental period extended successfully.")
        else:
            print("Car not found in rented list.")

    def generate_receipt(self, car_id):
        if car_id in self.rented_cars:
            details = self.rented_cars[car_id]
            print("\n===== Rental Receipt =====")
            print(f"Car ID: {car_id}")
            print(f"Name: {details['name']}")
            print(f"Phone Number: {details['phone_number']}")
            print(f"Booking Date: {details['booking_date'].strftime('%d-%m-%Y')}")
            print(f"Return Date: {details['return_date'].strftime('%d-%m-%Y')}")
            print(f"Rent Amount: ${details['rent_amount']}")
            print("==========================")
        else:
            print("Car not found in rented list.")

def main():
    rental_system = RentalSystem()

    # Define car categories
    compact_category = CarCategory(1, "Compact")
    sedan_category = CarCategory(2, "Sedan")
    suv_category = CarCategory(3, "SUV")

    rental_system.add_car(1, "Toyota Camry", 50, sedan_category) 
    rental_system.add_car(2, "Honda Accord", 60, sedan_category) 
    rental_system.add_car(3, "Toyota RAV4", 70, suv_category)      
    rental_system.add_car(4, "Ford Fiesta", 40, compact_category)  

    rental_system.initialize_rent_submission_dates()

    while True:
        print("\n===== Car Rental System =====")
        print("1. Show Available Cars")
        print("2. Add Car")
        print("3. Remove Car")
        print("4. Rent Car")
        print("5. Show Rented Cars")
        print("6. Cancel Booking")
        print("7. Submit Rent")
        print("8. Extend Rental")
        print("9. Generate Receipt")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            rental_system.show_available_cars()
        elif choice == "2":
            car_id = int(input("Enter Car ID: "))
            car_name = input("Enter Car Name: ")
            rent_per_day = int(input("Enter Rent per Day: $"))
            category_id = int(input("Enter Category ID (1. Compact, 2. Sedan, 3. SUV): "))
            category = None
            if category_id == 1:
                category = compact_category
            elif category_id == 2:
                category = sedan_category
            elif category_id == 3:
                category = suv_category
            else:
                print("Invalid category ID. Car not added.")
                continue
            rental_system.add_car(car_id, car_name, rent_per_day, category)
        elif choice == "3":
            car_id = int(input("Enter Car ID to remove: "))
            rental_system.remove_car(car_id)
        elif choice == "4":
            car_id = int(input("Enter Car ID to rent: "))
            name = input("Enter your name: ")
            phone_number = input("Enter your phone number: ")
            if len(phone_number) == 10:
                break
            else:
                print("Invalid Mobile No.")
                main()
            days = int(input("Enter number of days to rent: "))
            booking_date_str = input("Enter booking date (dd-mm-yyyy): ")
            rental_system.rent_car(car_id, name, phone_number, days, booking_date_str)
        elif choice == "5":
            rental_system.show_rented_cars()
        elif choice == "6":
            car_id = int(input("Enter Car ID to cancel booking: "))
            rental_system.cancel_booking(car_id)
        elif choice == "7":
            car_id = int(input("Enter Car ID to submit rent: "))
            rental_system.submit_rent(car_id)
        elif choice == "8":
            car_id = int(input("Enter Car ID to extend rental: "))
            days = int(input("Enter number of days to extend: "))
            rental_system.extend_rental(car_id, days)
        elif choice == "9":
            car_id = int(input("Enter Car ID to generate receipt: "))
            rental_system.generate_receipt(car_id)
        elif choice == "10":
            print("Thank You ...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

main()