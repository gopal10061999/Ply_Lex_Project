import sys
import os
from datetime import datetime

def get_date_input(prompt):
    date_str = input(prompt)
    try:
        return datetime.strptime(date_str, '%d-%m-%Y')
    except ValueError:
        print("Invalid date format. Please use dd-mm-yyyy.")
        sys.exit(1)

def get_query_input():
    print("\nSelect Query:")
    print("a. Change in active cases in %")
    print("b. Change in daily death in %")
    print("c. Change in new recovered in %")
    print("d. Change in new cases in %")
    print("-1 for exit")
    query = input("Enter query option (a, b, c, d): ")
    if query not in ['a', 'b', 'c', 'd', '-1']:
        print("Invalid query input format.")
        sys.exit(1)
    return query

def main():
    country_name = input("Enter country name: ")
    start_date = get_date_input("Enter start date (dd-mm-yyyy): ")
    end_date = get_date_input("Enter end date (dd-mm-yyyy): ")
    query = get_query_input()

    command = "python3 module15/mapper.py {} {} {} {} | sort -n | python3 module15/combiner.py | sort -n | python3 module15/reducer.py".format(
        country_name, start_date.strftime('%d-%m-%Y'), end_date.strftime('%d-%m-%Y'), query)

    os.system(command)

if __name__ == "__main__":
    main()
