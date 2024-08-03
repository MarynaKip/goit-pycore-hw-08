from addressBook import AddressBook, Birthday, Name, Phone, Record, WrongPhoneNumber
from serialization import load_data, save_data


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print("Enter the argument for the command.")
        except KeyError as err:
            print(err)
        except IndexError as err:
            print(err)
        except WrongPhoneNumber as err:
            print(err)
        except:
            print('Something went wrong')
    return inner

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    in_bot = True
    while in_bot:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        match command:
            case "hello":
                print("How can I help you?")
            case "add":
                add_contact(args, book)
            case "change":
                change_contact(args, book)
            case "phone":
                show_phone(args, book)
            case "all":
                print(book.data)
            case "add-birthday":
                name, birthday = args
                record = book.find(name)
                print(record.add_birthday(Birthday(birthday), Name(name), book))
            case "show-birthday":
                show_birthday(args, book)
            case "birthdays":
                print(book.get_upcoming_birthdays())
            case "close" | "exit":
                save_data(book)
                print("Good bye!")
                in_bot = False
            case _:
                print("Invalid command.")

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    if record:
        print(record.add_phone(phone))
    else:
        record = Record(Name(name), [Phone(phone)])
        print(book.add_record(record))


@input_error
def change_contact(args, book: AddressBook):
    name, phone, new_phone = args
    record = book.find(name)
    print(record.edit_phone(Phone(phone), Phone(new_phone)))

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    print(book.find(name))

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    print(record.birthday.value.strftime('%m.%d.%Y'))

main()