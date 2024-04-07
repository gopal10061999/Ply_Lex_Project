from urllib.request import Request, urlopen
import activecases
import dailyDeaths
import newRecoveries
import newCases
from datetime import datetime

def download_web_page(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    mydata = webpage.decode("utf8")
    with open('webpage.html', 'w', encoding="utf-8") as f:
        f.write(mydata)

def get_country_urls():
    country_urls = {}
    continents = ['Europe', 'North America', 'Asia', 'South America', 'Africa', 'Oceania']
    with open('worldometers_countrylist.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if '-' in line or line.lower() in continents:
                continue
            if line.lower() == 'usa':
                url = 'https://www.worldometers.info/coronavirus/country/us/'
            elif line.lower() == 'vietnam':
                url = 'https://www.worldometers.info/coronavirus/country/viet-nam/'
            else:
                url = f'https://www.worldometers.info/coronavirus/country/{line.replace(" ", "-").lower()}/'
            country_urls[line] = url
    return country_urls

def write_data_to_file(filename, country, values, dates):
    with open(filename, 'w', encoding='utf-8') as file:
        for date, value in zip(dates, values):
            file.write(f"{country},{date},{value}\n")

def process_country_data(country, url):
    download_web_page(url)
    dates1, active_cases = activecases.getCurrentlyInfected()
    dates2, daily_death = dailyDeaths.getDailyDeaths()
    dates3, new_recovered = newRecoveries.getNewRecoveries()
    dates4, new_case = newCases.getNewCases()

    common_dates = set(dates1).intersection(dates2, dates3, dates4)
    converted_dates = [datetime.strptime(date, '%b %d, %Y').strftime('%d-%m-%Y') for date in common_dates]

    write_data_to_file(f'./Module15/{country.replace(" ", "")}_ActiveCases.txt', country, active_cases, converted_dates)
    write_data_to_file(f'./Module15/{country.replace(" ", "")}_DailyDeaths.txt', country, daily_death, converted_dates)
    write_data_to_file(f'./Module15/{country.replace(" ", "")}_RecoveredCases.txt', country, new_recovered, converted_dates)
    write_data_to_file(f'./Module15/{country.replace(" ", "")}_NewCases.txt', country, new_case, converted_dates)

def main():
    country_urls = get_country_urls()
    for country, url in country_urls.items():
        process_country_data(country, url)

if __name__ == "__main__":
    main()
