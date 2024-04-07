

import os

def process_file(file_path, output_file):
    """Process a single file."""
    try:
        with open(file_path, "r", encoding='cp1252') as input_file:
            for line in input_file:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = line.split(':', maxsplit=1)
                    data[0] = data[0] + ' ' + str(year)
                    output_file.write(':'.join(data) + '\n')
                except Exception as e:
                    print("Error processing line:", e)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print("An error occurred:", e)

def process_year(year, month_names, output_file):
    """Process all files for a given year."""
    for month_name in month_names:
        file_path = os.path.join("response", str(year), month_name + ".txt")
        process_file(file_path, output_file)

def main():
    month_names = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]
    output_file_path = "mapper_output.txt"
    try:
        with open(output_file_path, "w") as output_file:
            for year in [2020, 2021, 2022]:
                process_year(year, month_names, output_file)
        print("Output is stored in mapper_output.txt")
    except IOError as e:
        print(f"IOError occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
