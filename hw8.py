from collections import UserDict
import datetime
from datetime import datetime as dtdt, timedelta
import re
import pickle

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __eq__(self, another_value: str) -> bool:
        return self.value == another_value

class Phone(Field):
    def __init__(self, num):
        nums = re.findall(r'\d+', num)
        if (len(str(nums[0]))) == 10:
            super().__init__(num)
        else:
            self.value = None
         
    def __eq__(self, another_value: str) -> bool:
        return self.value == another_value
    
class Birthday(Field):
    def __init__(self, value):
        try:
            time_str = datetime.datetime.strptime(value, "%d.%m.%Y").date()
            self.value = time_str
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if Phone(phone).value:
            self.phones.append(Phone(phone))
            return True
    
    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)
            return('Removed successfully.')
        else:
            return('This user has not such number. Nothing to delete!')

    def edit_phone(self, phone, new_phone):
        if phone in self.phones:
            if Phone(new_phone) != None:
                self.phones[self.phones.index(phone)] = Phone(new_phone)
                return('Number has changed.')
            else:
                return('Invalid number to change phone!')
        else:
            return('This user has not such number. Nothing to change!')

    def find_phone(self, phone):
        if phone in self.phones:
            return Phone(phone)
        else:
            return('This user has no such phone, sorry!')
        
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
                

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join([str(p) for p in self.phones])}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, rec:Record):
        self.data.update({rec.name.value:rec})

    def find(self,name):
        if name in self.data.keys():
            for n,p in self.data.items():
                if n == name:
                    return p
        else:
            return None

    def get_upcoming_birthdays(self):
        today = dtdt.today().date()
        result = []
        for user in self.data:
            try:
                birthday = datetime.datetime.strptime(str(self.data[user].birthday), "%Y-%m-%d").date()
                birthday_this_year = dtdt(year = today.year, month = birthday.month, day = birthday.day).date()
                week_day = birthday_this_year.isoweekday()
                quant_days = (birthday_this_year - today).days
                if 1 <= quant_days <=7:
                    if week_day == 7:
                        result.append({"name":user,"congratulation_date":(birthday_this_year + timedelta(days=1)).strftime('%Y.%m.%d')})
                    elif week_day == 6:
                        result.append({"name":user,"congratulation_date":(birthday_this_year + timedelta(days=2)).strftime('%Y.%m.%d')})
                    else:
                        result.append({"name":user,"congratulation_date":birthday_this_year.strftime('%Y.%m.%d')})
            except:
                pass

        return result

    def delete(self,name):
        if name in self.data.keys():
            del self.data[name]

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
                return  "Value error! Please, enter again your command to add contact correctly."
        except IndexError:
            return "Index out of range! Please, enter again your command to show contact correctly."
        except KeyError:
            return "There is no such contact yet. Add it please."
    return inner

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = 'Nothing has changed!'
    if record is None and Phone(phone) != None:
        record = Record(name)
        book.add_record(record)
        record.add_phone(phone)
        message = "Contact added."
    elif record and Phone(phone) != None:
        record.add_phone(phone)
        message = 'Contact updated'
    return message

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return('No such user in adress book!')
    if birthday:
        record.add_birthday(birthday)
        return 'Birthday was added.'
    else:
        return 'Input birthday to add!'

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return('No such user in adress book!')
    return record.birthday

@input_error
def birthdays(book: AddressBook):
    return book.get_upcoming_birthdays()

@input_error
def show_all(book:AddressBook):
        return '\n'.join(str(i) for i in book.data.values())

@input_error
def show_phone(args, book:AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return 'No such user is adress book!'
    else:
        return ', '.join([str(i) for i in record.phones])

@input_error
def change_phone(args, book:AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return 'No such user is adress book!'
    else:
        return record.edit_phone(old_phone, new_phone)

def save_data(book:AddressBook, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book = book))

        elif command == "change":
            print(change_phone(args, book = book))

        elif command == "phone":
            print(show_phone(args, book = book))

        elif command == "all":
            print(show_all(book=book))

        elif command == "add-birthday":
            print(add_birthday(args, book = book))

        elif command == "show-birthday":
            print(show_birthday(args, book = book))

        elif command == "birthdays":
            print(birthdays(book = book))

        else:
            print("Invalid command.")

    save_data(book)



if __name__ == "__main__":
    main()