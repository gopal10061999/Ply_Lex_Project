
import sys

# Define month names
MONTH_NAMES = [
    "january", "february", "march", "april",
    "may", "june", "july", "august",
    "september", "october", "november", "december"
]

def get_date_input(prompt):
    """Get date input from the user."""
    while True:
        try:
            day, month, year = map(int, input(prompt).strip().split('-'))
            if not (1 <= day <= 31 and 1 <= month <= 12):
                raise ValueError("Invalid date format! Please enter a valid date.")
            return day, month, year
        except ValueError as e:
            print(e)

def read_file_lines(file_path):
    """Read lines from a file."""
    try:
        with open(file_path, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file '{file_path}': {e}")
        sys.exit(1)

def write_output(lines, output_file_path):
    """Write lines to an output file."""
    try:
        with open(output_file_path, "w") as output_file:
            output_file.writelines(lines)
    except IOError as e:
        print(f"Error writing to file '{output_file_path}': {e}")
        sys.exit(1)

def process_file(start_date, end_date):
    input_lines = read_file_lines("mapper_output.txt")
    output_lines = []
    flag = False
    for line in input_lines:
        try:
            key = line.split(":")[0].split(' ')
            month_index = MONTH_NAMES.index(key[1].strip().lower())
            day = int(key[0].strip())
            year = int(key[2].strip())
            # Check if the date falls within the specified range
            if (month_index >= start_date[1] and day >= start_date[0] and year >= start_date[2]):
                flag = True
            if flag:
                output_lines.append(line)
            if (month_index >= end_date[1] and day >= end_date[0] and year >= end_date[2]):
                break
        except (ValueError, IndexError):
            continue
    return output_lines

def main():
    # Get start and end dates from the user
    print("Enter Start Date(dd-mm-yyyy) : ")
    start_date = get_date_input("Enter Start Date(dd-mm-yyyy) : ")
    print("Enter End Date(dd-mm-yyyy) : ")
    end_date = get_date_input("Enter End Date(dd-mm-yyyy) : ")

    output_lines = process_file(start_date, end_date)
    write_output(output_lines, "worldwide_responses.txt")

    print("Output is stored in worldwide_responses.txt")

if __name__ == "__main__":
    main()
