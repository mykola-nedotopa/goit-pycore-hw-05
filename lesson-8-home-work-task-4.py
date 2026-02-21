from functools import wraps
from typing import Callable, Dict, List, Tuple


def input_error(func: Callable):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError as e:
            # Якщо ValueError кинуто з повідомленням — показуємо його
            return str(e) if str(e) else "Give me name and phone please."

        except IndexError:
            return "Enter user name."

        except KeyError:
            return "Contact not found."

    return inner


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    user_input = user_input.strip()
    if not user_input:
        return "", []

    tokens = user_input.split()

    # команда з двох слів
    if len(tokens) >= 2 and tokens[0].lower() == "good" and tokens[1].lower() == "bye":
        return "exit", []

    command = tokens[0].lower()
    args = tokens[1:]
    return command, args


@input_error
def add_contact(args: List[str], contacts: Dict[str, str]) -> str:
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: List[str], contacts: Dict[str, str]) -> str:
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args: List[str], contacts: Dict[str, str]) -> str:
    if len(args) != 1:
        raise ValueError("Enter user name.")
    name = args[0]
    if name not in contacts:
        raise KeyError(name)
    return contacts[name]


@input_error
def show_all(args: List[str], contacts: Dict[str, str]) -> str:
    if not contacts:
        return "No contacts."
    lines = [f"{name}: {phone}" for name, phone in contacts.items()]
    return "\n".join(lines)


def main():
    contacts: Dict[str, str] = {}

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ("exit", "close"):
            print("Good bye!")
            break

        if command == "hello":
            print("How can I help you?")
            continue

        # Якщо команда потребує аргументів, а їх нема — попросимо ввести окремо
        if command in ("add", "change", "phone") and not args:
            args_input = input("Enter the argument for the command: ").strip()
            args = args_input.split() if args_input else []

        if command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(args, contacts))
        elif command == "":
            # порожній ввід — просто ігноруємо
            continue
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()