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
        years = ['2020', '2021', '2022']

        for year in years:
                with open(f'Singapore ({year}).txt', 'r') as f1:
                        for line in f1.readlines():
                                line = line.strip()
                                try:
                                        if line == '':
                                                continue
                                        data = line.split(':', maxsplit=1)
                                        data[0] = data[0] + ' ' + year
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
                                        if line == '':
                                                continue
                                        data = line.split(':', maxsplit=1)
                                        data[0] = f"{data[0]} {year}"
                                        f.write(':'.join(data) + '\n')
                                except:
                                        continue

elif(country=='England'):
        file_names = ['England (January–June 2020).txt','England (July–December 2020).txt','England (2021).txt','England (2022).txt']

        for file_name in file_names:
                f1 = open(file_name, 'r')
                for line in f1.readlines():
                        line = line.strip()
                        try:
                                if line == '':
                                        continue
                                data = line.split(':', maxsplit=1)
                                year = file_name.split('(')[-1].split(')')[0]
                                data[0] = f"{data[0]} {year}"
                                f.write(':'.join(data) + '\n')
                        except:
                                continue

elif(country=='India'):
        for filename in ['India (January–May 2020).txt', 'India (June–December 2020).txt', 'India (2021).txt']:
                with open(filename, 'r') as f1:
                        for line in f1:
                                line = line.strip()
                                try:
                                        if line == '':
                                                continue
                                        data = line.split(':', maxsplit=1)
                                        year = filename.split('(')[-1].split(')')[0]  # Extract the year from the filename
                                        data[0] = data[0] + ' ' + year
                                        f.write(':'.join(data) + '\n')
                                except:
                                        continue

elif(country=='Australia'):
        file_names = ['Australia_2020.txt', 'Australia_(Jan-Jun 21).txt', 'Australia(Jul-Dec 21).txt', 'Australia_(2022).txt']

        for file_name in file_names:
                with open(file_name, 'r') as f1:
                        for line in f1.readlines():
                                line = line.strip()
                                try:
                                        if line == '':
                                                continue
                                        data = line.split(':', maxsplit=1)
                                        year = file_name.split('.')[0].split('_')[-1]
                                        data[0] = f"{data[0]} {year}"
                                        f.write(':'.join(data) + '\n')
                                except:
                                        continue
      
else:
        print("invalid country")
        exit()
        
f.close()
# Specify the path to your text file
def read_mapper_output(file_name):
    with open(file_name, 'r', encoding='utf-8') as map_data:
        first_line = map_data.readline()
        last_line = None
        while True:
            line = map_data.readline()
            if not line:
                break
            if line.strip() != '':
                last_line = line
    return first_line, last_line

# Read the mapper output file
first_line, last_line = read_mapper_output("mapper_output.txt")

# Print the results
print(f"From Date: {first_line.split(':')[0]}")
print(f"To Date: {last_line.split(':')[0]}")
