import sys
from datetime import datetime

def parse_date(date_str):
    return datetime.strptime(date_str, '%d-%m-%Y')

def process_country_query(parts):
    country_name = parts[1]
    start_date = parse_date(parts[2])
    end_date = parse_date(parts[3])
    query = parts[4]
    return country_name, start_date, end_date, query

def process_data_line(line):
    data = line.strip().split()
    country_n = data[0]
    date = parse_date(data[1])
    value = int(data[2]) if data[2] != 'NA' else None
    return country_n, date, value

def print_country_data(country_n, date, value):
    print("{} {} {}".format(country_n, date.strftime('%d-%m-%Y'), value))

def main():
    country_data = {}
    start_date = None
    end_date = None
    for line in sys.stdin:
        if line.startswith("-1"):
            country_name, start_date, end_date, query = process_country_query(line.strip().split(','))
            print("-1,{},{},{},{}".format(country_name, start_date.strftime('%d-%m-%Y'), end_date.strftime('%d-%m-%Y'), query), end='\n')
        else:
            country_n, date, value = process_data_line(line)
            if country_n not in country_data:
                country_data[country_n] = []
            if start_date <= date and date <= end_date:
                print_country_data(country_n, date, value)

if __name__ == "__main__":
    main()
