import sys

# Define month names
month_names = [
    "january", "february", "march", "april",
    "may", "june", "july", "august",
    "september", "october", "november", "december"
]

def get_date_input(prompt):
    """Get date input from the user."""
    while True:
        try:
            date_input = input(prompt).strip().split('-')
            if len(date_input) != 3:
                raise ValueError("Invalid date format! Please enter date in dd-mm-yyyy format.")
            
            day = int(date_input[0])
            month = int(date_input[1])
            year = int(date_input[2])
            return day, month, year
        except ValueError as ve:
            print(ve)

def process_file(start_date, end_date):
    try:
        with open("mapper_output.txt", "r") as input_file:
            lines = input_file.readlines()
    except FileNotFoundError:
        print("File 'mapper_output.txt' not found.")
        return

    try:
        with open("worldwide_news.txt", "w") as output_file:
            flag = False
            for line in lines:
                try:
                    key = line.split(":")[0].split(' ')
                    month_index = month_names.index(key[1].strip().lower())
                    day = int(key[0].strip())
                    year = int(key[2].strip())
                    # Check if the date falls within the specified range
                    if (month_index >= start_date[1] and day >= start_date[0] and year >= start_date[2]):
                        flag = True
                    if flag:
                        output_file.write(line)
                    if (month_index >= end_date[1] and day >= end_date[0] and year >= end_date[2]):
                        break
                except (ValueError, IndexError):
                    continue
    except IOError:
        print("An error occurred while writing to 'worldwide_news.txt'.")

def main():
    try:
        # Get start and end dates from the user
        print("Enter Start Date(dd-mm-yyyy) : ")
        start_date = get_date_input("Enter Start Date(dd-mm-yyyy) : ")
        print("Enter End Date(dd-mm-yyyy) : ")
        end_date = get_date_input("Enter End Date(dd-mm-yyyy) : ")
        
        process_file(start_date, end_date)

        print("Output is stored in worldwide_news.txt")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
