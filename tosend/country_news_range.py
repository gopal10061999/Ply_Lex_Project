#extract file
import sys
# start=input().split('-')
# end=input().split('-')
month_names = [
    "january", "february", "march", "april",
    "may", "june", "july", "august",
    "september", "october", "november", "december"
]

country = input("Enter Country Name : ").strip()
f=open("mapper_output.txt","w+", encoding='utf-8')
if(country=='Singapore'):
        file_years = ['2020', '2021', '2022']

        for year in file_years:
                with open(f'Singapore ({year}).txt', 'r') as f1:
                        for line in f1.readlines():
                                line = line.strip()
                                try:
                                        if line == '':
                                                continue
                                        data = line.split(':', maxsplit=1)
                                        data[0] = f'{data[0]} {year}'
                                        f.write(':'.join(data) + '\n')
                                except:
                                        continue
elif(country=='Malaysia'):
        years = ['2020', '2021', '2022', '2023', '2024']
        for year in years:
                filename = f'Malaysia ({year}).txt'
                with open(filename, 'r') as f1:
                        for line in f1.readlines():
                                line = line.strip()
                                try:
                                        if not line:
                                                continue
                                        data = line.split(':', maxsplit=1)
                                        data[0] = data[0] + ' ' + year
                                        f.write(':'.join(data) + '\n')
                                except:
                                        continue
elif(country=='England'):
        file_names = ['England (January–June 2020).txt', 'England (July–December 2020).txt', 'England (2021).txt', 'England (2022).txt']

        for file_name in file_names:
                with open(file_name, 'r') as f1:
                        for line in f1.readlines():
                                line = line.strip()
                                try:
                                        if not line:
                                                continue
                                        data = line.split(':', maxsplit=1)
                                        year = file_name.split('(')[-1].split(')')[0]
                                        data[0] = f"{data[0]} {year}"
                                        f.write(':'.join(data) + '\n')
                                except:
                                        continue
elif(country=='India'):
        files = ['India (January–May 2020).txt', 'India (June–December 2020).txt', 'India (2021).txt']
        for file_name in files:
                with open(file_name, 'r') as f1:
                        for line in f1:
                                line = line.strip()
                                try:
                                        if line:
                                                data = line.split(':', maxsplit=1)
                                                year = file_name.split('(')[-1].split(')')[0]
                                                data[0] = f'{data[0]} {year}'
                                                f.write(':'.join(data) + '\n')
                                except:
                                        continue
elif(country=='Australia'):
        files = ['Australia_2020.txt', 'Australia_(Jan-Jun 21).txt', 'Australia(Jul-Dec 21).txt', 'Australia_(2022).txt']

        for file_name in files:
                with open(file_name, 'r') as f1:
                        for line in f1.readlines():
                                line = line.strip()
                                try:
                                        if line == '':
                                                continue
                                        data = line.split(':', maxsplit=1)
                                        year = file_name.split('.')[0][-4:]
                                        data[0] = f'{data[0]} {year}'
                                        f.write(':'.join(data) + '\n')
                                except:
                                        continue
else:
        print("invalid country")
        exit()
        
f.close()

def get_date_input(prompt):
    return [int(part) for part in input(prompt).split('-')]

def write_filtered_data(input_file, output_file, start_date, end_date):
    flag = False
    with open(input_file, 'r', encoding='utf-8') as f, open(output_file, 'w+', encoding='utf-8') as final:
        while True:
            line = f.readline()
            try:
                if not line:
                    break
                key = line.split(":")[0].split(' ')
                if (month_names.index(key[1].strip().lower()) >= start_month and int(key[2].strip()) >= start_year) and int(key[0].strip()) >= start_date:
                    flag = True
                if int(key[2].strip()) > end_year:
                    break
                if int(key[2].strip()) == end_year and month_names.index(key[1].strip().lower()) > end_month:
                    break
                if int(key[2].strip()) == end_year and month_names.index(key[1].strip().lower()) == end_month and int(key[0].strip()) >= end_date:
                    break
                if flag:
                    final.write(line)
                if month_names.index(key[1].strip().lower()) >= end_month and int(key[0].strip()) >= end_date and int(key[2].strip()) >= end_year:
                    break
            except:
                continue

start_date = get_date_input("Enter Start Date(dd-mm-yyyy) : ")
start_year, start_month, start_date = start_date[2], start_date[1]-1, start_date[0]

end_date = get_date_input("Enter End Date(dd-mm-yyyy) : ")
end_year, end_month, end_date = end_date[2], end_date[1]-1, end_date[0]

write_filtered_data("mapper_output.txt", "country_news_range.txt", start_date, end_date)

print("----Output is stored in country_news_range.txt----")
