
"""mapper.py"""

import sys

def process_command_line_arguments():
    """Process and print command-line arguments."""
    for arg_index in range(1, len(sys.argv)):  # Loop through arguments excluding script name
        argument = sys.argv[arg_index].strip()
        print(argument)

def clean_and_split_line(line):
    """Clean and split a line into individual data points."""
    line = line.strip()
    line = line.replace(',', '').replace('+', '')  # Remove unwanted characters
    return line.split(' ')

def process_countries_file(file_path):
    """Process data from the countries.txt file."""
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    country, total_cases, new_cases, total_deaths, new_deaths, total_recovered, new_recovered, active_cases, deaths_m, total_tests, tests_m = clean_and_split_line(line)
                    # Print formatted output
                    print(f'{country}:{total_cases}:{active_cases}:{total_deaths}:{total_recovered}:{total_tests}:{deaths_m}:{tests_m}:{new_cases}:{new_deaths}:{new_recovered}:')
                except ValueError as e:
                    print("Error processing line:", e)
    except FileNotFoundError:
        print("File not found:", file_path)
    except IOError as e:
        print("Error reading file:", e)

def main():
    # Process command-line arguments
    process_command_line_arguments()

    # Process data from countries.txt file
    process_countries_file('countries.txt')

if __name__ == "__main__":
    main()
