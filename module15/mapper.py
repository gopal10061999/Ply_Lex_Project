import sys
from datetime import datetime

def calculate_change(start_value, end_value):
    if start_value == 0:
        return 0
    return ((end_value - start_value) / start_value) * 100

def find_closest_country(query, country_data):
    closest_country = None
    min_difference = float('inf')

    for country, data in country_data.items():
        if query in data:
            value = data[query]
            difference = abs(value - country_data[query][0])

            if difference < min_difference and difference != 0:
                min_difference = difference
                closest_country = country

    return closest_country

def read_country_data():
    country_data = {}
    with open('module15/worldometers_countrylist.txt', 'r') as file:
        for line in file:
            data = line.strip().replace(':', "").replace("-", "")
            country_data[data] = []
    return country_data

def handle_query(country_data, query_type):
    query_file = {
        'a': 'ActiveCases',
        'b': 'DailyDeaths',
        'c': 'RecoveredCases',
        'd': 'NewCases'
    }
    for country in country_data:
        if country.strip() != '':
            try:
                with open('module15/{}_{}.txt'.format(country, query_file[query_type]), 'r+', encoding='utf-8') as abc:
                    for line in abc:
                        try:
                            data = line.strip().split(',')
                            date = datetime.strptime(data[1].strip(), '%d-%m-%Y')
                            value = int(data[2].strip())
                            print("{} {} {}".format(country, date.strftime('%d-%m-%Y'), value))
                        except Exception as e:
                            continue
            except Exception as e:
                pass

def main():
    if len(sys.argv) != 5:
        print("Usage: python mapper.py <country_name> <start_date> <end_date> <query>")
        sys.exit(1)

    country_name = sys.argv[1]
    start_date_str = sys.argv[2]
    end_date_str = sys.argv[3]
    query = sys.argv[4]

    try:
        start_date = datetime.strptime(start_date_str, '%d-%m-%Y')
        end_date = datetime.strptime(end_date_str, '%d-%m-%Y')
    except ValueError:
        print("Invalid date format. Please use dd-mm-yyyy.")
        sys.exit(1)

    country_data = read_country_data()

    if country_name not in country_data:
        print("Country not found.")
        sys.exit(1)

    print("-1,{},{},{},{}".format(country_name, start_date.strftime('%d-%m-%Y'), end_date.strftime('%d-%m-%Y'), query), end='\n')

    if query in ['a', 'b', 'c', 'd']:
        handle_query(country_data, query)
    else:
        print("Invalid query. Please provide a valid query: a, b, c, or d.")

if __name__ == "__main__":
    main()
