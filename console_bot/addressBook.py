from collections import UserList
from datetime import datetime, timedelta

class WrongPhoneNumber(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)
        self.validate_phone()
    def validate_phone(self):
        if len(self.value) != 10 or not self.value.isdigit():
            raise WrongPhoneNumber("Wrong phone number!")
    

class Birthday(Field):
    def __init__(self, value):
        try:
            date_object = datetime.strptime(value, '%m.%d.%Y').date()
            super().__init__(date_object)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name: Name, phones: list[type[Phone]] = [], birthday: Birthday = None):
        self.name = name
        self.phones = phones
        self.contact = {"name": name.value, "phones": [phone.value for phone in phones], "birthday": birthday}
        self.birthday = birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
    def __repr__(self):
        return str(self.contact)
    
    def add_phone(self, phone):
        self.phones.append(phone)
        self.contact["phones"].append(phone)
        return "Contact added."
    
    def remove_phone(self, args):
        name, phone = args
        if name.value != self.contact["name"]:
            raise IndexError('There is no such contact in the contacts!')
        else:
            self.phones = list(filter(lambda number: number == phone, self.phones))
            self.contact["phones"] = self.phones
            return "Contact removed."

    def edit_phone(self, phone: Phone, new_phone: Phone):
        self.phones = list(map(lambda p: new_phone if p.value == phone.value else p, self.phones))
        self.contact["phones"] = [p.value for p in self.phones]
        return "Contact updated."

    def find_phone(self, args):
        name = args[0]
        if name == self.name:
            return self.phones
        
    def add_birthday(self, birthday: Birthday, name: Name, book):
        self.birthday = birthday
        self.contact["birthday"] = birthday.value.strftime('%m.%d.%Y')
        return 'Birthday added.'


class AddressBook(UserList):
    def add_record(self, record: Record) -> str:
           self.data.append(record)
           return "Contact added."

    def find(self, name) -> Record:
        book_names = [d.contact.get('name') for d in self.data]
        if name in book_names:
            return self.data[book_names.index(name)]

    def delete(self, name):
        self.data = list(filter(lambda rec: rec.contact["name"] == name, self.data))
        return "The contact was removed."
    
    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today().date()
        for user in self.data:
            birthday = user.birthday.value
            birthday_this_year = birthday.replace(year=2024)
            days_difference = birthday_this_year - today
            if 0 <= days_difference.days <= 7:
                birthday_weekday = birthday_this_year.weekday()
                congratulation_date = birthday_this_year
                if birthday_weekday == 5:
                    congratulation_date += timedelta(days=2)
                elif birthday_weekday == 6:
                    congratulation_date += timedelta(days=1)
                upcoming_birthdays.append({"name": user.name.value, "congratulation_date": congratulation_date.strftime("%Y.%m.%d")})
        return upcoming_birthdays

