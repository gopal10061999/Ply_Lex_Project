

import sys

MONTH_NAMES = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

def open_file(file_path, mode='r', encoding=None):
    """Open a file with error handling."""
    try:
        return open(file_path, mode, encoding=encoding)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except IOError as e:
        print(f"Error opening file '{file_path}': {e}")

def process_month_files(year, month_names, output_file):
    """Process files for a given year and month names."""
    for month in month_names:
        file_path = f"news/{year}/{month}.txt"
        file_content = read_file_lines(file_path)
        if file_content:
            process_file_content(file_content, year, output_file)

def read_file_lines(file_path):
    """Read lines from a file."""
    try:
        with open_file(file_path, encoding='cp1252') as file:
            return file.readlines()
    except:
        return []

def process_file_content(file_content, year, output_file):
    """Process content of a file and write to output."""
    for line in file_content:
        line = line.strip()
        try:
            if line:
                data = line.split(':', maxsplit=1)
                data[0] = data[0] + ' ' + str(year)
                output_file.write(':'.join(data) + '\n')
        except Exception as e:
            print(f"Error processing line: {e}")

def main():
    with open("mapper_output.txt", "w") as output_file:
        for year in [2020, 2021, 2022]:
            process_month_files(year, MONTH_NAMES, output_file)

    print("Output is stored in mapper_output.txt")

if __name__ == "__main__":
    main()
