import sys
from datetime import datetime

def calculate_percentage_change(start_value, end_value):
    if start_value == 0:
        return 0
    return ((end_value - start_value) / start_value) * 100

def find_closest_country(given_country, given_value, query, country_data):
    closest_country = None
    min_difference = float('inf')

    for country, values in country_data.items():
        if country != given_country:
            start_value = values[0][1]
            end_value = values[-1][1]
            change = calculate_percentage_change(start_value, end_value)
            difference = abs(change - given_value)
            if difference < min_difference:
                min_difference = difference
                closest_country = country
    
    return closest_country, min_difference

def main():
    country_data = {}
    start_date = None
    end_date = None

    for line in sys.stdin:
        if line.startswith("-1"):
            parts = line.strip().split(',')
            country_name = parts[1]
            start_date = datetime.strptime(parts[2], '%d-%m-%Y')
            end_date = datetime.strptime(parts[3], '%d-%m-%Y')
            query = parts[4]

            if country_name not in country_data:
                country_data[country_name] = []

        else:
            data = line.strip().split()
            country_name = data[0]
            date = datetime.strptime(data[1], '%d-%m-%Y')
            value = int(data[2])
            
            if country_name not in country_data:
                country_data[country_name] = []

            if start_date <= date <= end_date:
                country_data[country_name].append((date, value))

    for country, values in country_data.items():
        start_date, start_value = values[0]
        end_date, end_value = values[-1]
        active_change = calculate_percentage_change(start_value, end_value)

        print(f"For the country {country}:")
        print(f"Change in {query}: {active_change:.2f}%")

        closest_country, min_difference = find_closest_country(country, active_change, query, country_data)
        print(f"Closest country with similar {query}: {closest_country} with a difference of {min_difference:.2f}%")

if __name__ == "__main__":
    main()
