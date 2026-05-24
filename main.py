
from datetime import datetime
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"
HISTORY_FILE = DATA_DIR / "history.txt"
OPERATIONS = {
    "+": "addition",
    "-": "subtraction",
    "*": "multiplication",
    "/": "division",
    "//": "floor division",
    "%": "remainder",
    "**": "power",
    "pct": "percentage",
    "sqrt": "square root (√)",
    "sq": "square (x²)",
    "inv": "1/x",
}


def ensure_storage():
    DATA_DIR.mkdir(exist_ok=True)
    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text("Calculator history\n", encoding="utf-8")


def read_float(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("Error: enter a valid number.")


def choose_operation():
    print("\nChoose an operation:")
    for symbol, name in OPERATIONS.items():
        print(f"{symbol:>2} - {name}")

    while True:
        operation = input("Operation: ").strip()
        if operation in OPERATIONS:
            return operation
        print("Error: this operation does not exist.")


def calculate(first, second, operation):
    if operation in {"/", "//", "%"} and second == 0:
        raise ZeroDivisionError("division by zero is not allowed.")

    if operation == "+":
        return first + second
    if operation == "-":
        return first - second
    if operation == "*":
        return first * second
    if operation == "/":
        return first / second
    if operation == "//":
        return first // second
    if operation == "%":
        return first % second
    if operation == "**":
        return first**second
    if operation == "pct":
        return first * (second / 100)
    if operation == "sqrt":
        if first < 0:
            raise ValueError("Cannot take square root of negative number")
        return first ** 0.5
    if operation == "sq":
        return first ** 2
    if operation == "inv":
        if first == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return 1 / first
    raise ValueError("Unknown operation.")


def save_history(first, second, operation, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if second is None:
        line = f"{timestamp} | {operation}({first}) = {result}\n"
    else:
        line = f"{timestamp} | {first} {operation} {second} = {result}\n"
    with HISTORY_FILE.open("a", encoding="utf-8") as file:
        file.write(line)


def show_history():
    print("\n--- History ---")
    has_records = False
    with HISTORY_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip() == "Calculator history":
                continue
            if line.strip():
                has_records = True
                print(line, end="")

    if not has_records:
        print("History is empty.")


def run_calculator():
    first = read_float("Enter the first number: ")
    operation = choose_operation()
    
    if operation in {"sqrt", "sq", "inv"}:
        second = None 
    else:
        second = read_float(f"Enter the second number (first={first}): ")

    try:
        result = calculate(first, second, operation)
    except ZeroDivisionError as error:
        print(f"Error: {error}")
        return
    except ValueError as error:
        print(f"Error: {error}")
        return

    print(f"Result: {result}")
    save_history(first, second, operation, result)


def main():
    ensure_storage()
    while True:
        print("\n=== Calculator ===")
        print("1. New calculation")
        print("2. Show history")
        print("3. Clear history")
        print("4. Exit")

        choice = input("Choose: ").strip()
        if choice == "1":
            run_calculator()
        elif choice == "2":
            show_history()
        elif choice == "3":
            HISTORY_FILE.write_text("Calculator history\n", encoding="utf-8")
            print("History cleared.")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Error: choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()