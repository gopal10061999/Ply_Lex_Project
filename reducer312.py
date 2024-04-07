import sys

def parse_line(line):
    parts = line.split(':')[:-1]
    return list(map(float, parts[1:]))

def calculate_percentage(choice, value1, value2):
    if value1 != 0:
        return ((value2 / value1) * 100)
    else:
        return "Cannot divide by zero"

def main():
    # Define initial variables
    Total_Cases, Active_Cases, Total_Deaths, Total_Recovered, Total_Tests, Deaths_M, Tests_M, New_Cases, New_Deaths, New_Recovered = [0] * 10

    # input comes from STDIN (standard input)
    flag = 0
    for line in sys.stdin:
        line = line.strip()
        if flag == 0:
            choice = line
            flag += 1
            continue
        if flag == 1:
            country = line
            flag += 1
            continue
        if 'World' in line:
            Total_Cases, Active_Cases, Total_Deaths, Total_Recovered, Total_Tests, Deaths_M, Tests_M, New_Cases, New_Deaths, New_Recovered = parse_line(line)
            continue
        if country in line:
            Total_Cases2, Active_Cases2, Total_Deaths2, Total_Recovered2, Total_Tests2, Deaths_M2, Tests_M2, New_Cases2, New_Deaths2, New_Recovered2 = parse_line(line)
            continue

    if choice == 'a':
        print(calculate_percentage(Total_Cases, Total_Cases2, Total_Cases), '%')
    elif choice == 'b':
        print(calculate_percentage(Active_Cases, Active_Cases2, Active_Cases), '%')
    elif choice == 'c':
        print(calculate_percentage(Total_Deaths, Total_Deaths2, Total_Deaths), '%')
    elif choice == 'd':
        print(calculate_percentage(Total_Recovered, Total_Recovered2, Total_Recovered), '%')
    elif choice == 'e':
        print(calculate_percentage(Total_Tests, Total_Tests2, Total_Tests), '%')
    elif choice == 'f':
        print(calculate_percentage(Deaths_M, Deaths_M2, Deaths_M), '%')
    elif choice == 'g':
        print(calculate_percentage(Tests_M, Tests_M2, Tests_M), '%')
    elif choice == 'h':
        print(calculate_percentage(New_Cases, New_Cases2, New_Cases), '%')
    elif choice == 'i':
        print(calculate_percentage(New_Deaths, New_Deaths2, New_Deaths), '%')
    elif choice == 'j':
        print(calculate_percentage(New_Recovered, New_Recovered2, New_Recovered), '%')
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
