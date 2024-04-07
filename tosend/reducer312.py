import sys

def calculate_percentage(numerator, denominator):
    """Calculate percentage and handle division by zero."""
    try:
        percentage = (numerator / denominator) * 100
    except ZeroDivisionError:
        print("Cannot divide by zero")
        return None
    return percentage

def parse_line(line):
    """Parse a line of input and extract values."""
    parts = line.split(':')[:-1]
    return map(float, parts[1:])

def main():
    # Define initial variables
    variables = {
        'a': ('Total_Cases2', 'Total_Cases'),
        'b': ('Active_Cases2', 'Active_Cases'),
        'c': ('Total_Deaths2', 'Total_Deaths'),
        'd': ('Total_Recovered2', 'Total_Recovered'),
        'e': ('Total_Tests2', 'Total_Tests'),
        'f': ('Death_Per_Million2', 'Death_Per_Million'),
        'g': ('Tests_Per_Million2', 'Tests_Per_Million'),
        'h': ('New_Cases2', 'New_Cases'),
        'i': ('New_Deaths2', 'New_Deaths'),
        'j': ('New_Recovered2', 'New_Recovered')
    }

    # input comes from STDIN (standard input)
    flag = 0
    for line in sys.stdin:
        line = line.strip()
        if flag == 0:
            choice = line
            flag += 1
        elif flag == 1:
            country = line
            flag += 1
        elif 'World' in line:
            Total_Cases2, Active_Cases2, Total_Deaths2, Total_Recovered2, Total_Tests2, Death_Per_Million2, Tests_Per_Million2, New_Cases2, New_Deaths2, New_Recovered2 = parse_line(line)
        elif country in line:
            Total_Cases2, Active_Cases2, Total_Deaths2, Total_Recovered2, Total_Tests2, Death_Per_Million2, Tests_Per_Million2, New_Cases2, New_Deaths2, New_Recovered2 = parse_line(line)

    # Calculate and print the percentage based on user's choice
    if choice in variables:
        var2, var1 = variables[choice]
        percentage = calculate_percentage(eval(var2), eval(var1))
        if percentage is not None:
            print(f"{percentage:.2f} %")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
