# import sys
# import os
# from urllib.request import Request, urlopen

# def create_directory(directory_path):
#     if not os.path.exists(directory_path):
#         os.makedirs(directory_path)
#         os.makedirs(directory_path+'/2020')
#         os.makedirs(directory_path+'/2021')
#         os.makedirs(directory_path+'/2022')

# # Example usage:
# directory_path = "news"
# create_directory(directory_path)
# directory_path = "response"
# create_directory(directory_path)
# months = [
#     "January",
#     "February",
#     "March",
#     "April",
#     "May",
#     "June",
#     "July",
#     "August",
#     "September",
#     "October",
#     "November",
#     "December"
# ]
# years = [2020,2021,2022]

# for year in years:
#     for month in months:
#         link= f'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_{month}_{year}'
#         req = Request(link,headers ={'User-Agent':'Mozilla/5.0'})
#         webpage = urlopen(req).read()
#         mydata = webpage.decode("utf8")
#         f=open('news.html','w',encoding="utf-8")
#         f.write(mydata)
#         os.system(f"python3 getNews.py ./news/{year}/{month}.txt")
#         # f1=open(f'./news/{year}/{month}.txt','w+',encoding="utf-8")
#         # f1.write(str1)
#         f.close()

# for year in years:
#     for month in months:
#         try:
#             link= f'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_{month}_{year}'
#             req = Request(link,headers ={'User-Agent':'Mozilla/5.0'})
#             webpage = urlopen(req).read()
#             mydata = webpage.decode("utf8")
#             f=open('response.html','w',encoding="utf-8")
#             f.write(mydata)
#             os.system(f"python3 getresponse.py ./response/{year}/{month}.txt")
#             # f1=open(f'./news/{year}/{month}.txt','w+',encoding="utf-8")
#             # f1.write(str1)
#             f.close()
#         except:
#                 continue
        
import sys
import os
from urllib.request import Request, urlopen

def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        for year in range(2020, 2023):
            os.makedirs(os.path.join(directory_path, str(year)))

def fetch_news_data(years, months):
    for year in years:
        for month in months:
            try:
                link= f'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_{month}_{year}'
                req = Request(link, headers={'User-Agent':'Mozilla/5.0'})
                webpage = urlopen(req).read()
                mydata = webpage.decode("utf8")
                with open('news.html','w',encoding="utf-8") as f:
                    f.write(mydata)
                process_news_data(year, month)
            except Exception as e:
                print(f"An error occurred while fetching news data for {year}-{month}: {e}")
                continue

def process_news_data(year, month):
    try:
        os.system(f"python3 getNews.py ./news/{year}/{month}.txt")
        # Optionally, you can add code here to process the news data further
    except Exception as e:
        print(f"An error occurred while processing news data for {year}-{month}: {e}")

def fetch_response_data(years, months):
    for year in years:
        for month in months:
            try:
                link= f'https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_{month}_{year}'
                req = Request(link, headers={'User-Agent':'Mozilla/5.0'})
                webpage = urlopen(req).read()
                mydata = webpage.decode("utf8")
                with open('response.html','w',encoding="utf-8") as f:
                    f.write(mydata)
                process_response_data(year, month)
            except Exception as e:
                print(f"An error occurred while fetching response data for {year}-{month}: {e}")
                continue

def process_response_data(year, month):
    try:
        os.system(f"python3 getresponse.py ./response/{year}/{month}.txt")
        # Optionally, you can add code here to process the response data further
    except Exception as e:
        print(f"An error occurred while processing response data for {year}-{month}: {e}")

if __name__ == "__main__":
    directory_path_news = "news"
    create_directory(directory_path_news)
    directory_path_response = "response"
    create_directory(directory_path_response)
    
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    years = [2020, 2021, 2022]

    fetch_news_data(years, months)
    fetch_response_data(years, months)
