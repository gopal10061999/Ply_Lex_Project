import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import sys
import os

class NewsAnalyzer:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        self.countries = ["Australia","India","Malaysia","England","Singapore"]

    def get_news(self, country, start, end):
        os.system(f"python3 backjaccard.py {country} {start} {end}")
        with open("reducer_output.txt", 'r') as f:
            data = "".join(line.split(':')[1] for line in f.readlines())
        return data

    def calculate_jaccard_similarity(self, set1, set2):
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union != 0 else 0

    def retrieve_news_and_similarity(self):
        country1 = input("Enter Country Name : ").strip()
        start_data = input("Enter Start Date(dd-mm-yyyy) : ")
        end_data = input("Enter End Date(dd-mm-yyyy) : ")

        australia_news = self.get_news(country1, start_data, end_data)
        australia_words = set(set(word_tokenize(australia_news.lower())) - set(stopwords.words('english')))

        max_similarity = 0
        closest_country = ""

        for country in self.countries:
            try:
                if country != country1:
                    country_news = self.get_news(country, start_data, end_data)
                    country_words = set(set(word_tokenize(country_news.lower())) - set(stopwords.words('english')))
                    similarity = self.calculate_jaccard_similarity(australia_words, country_words)
                    print(f'{country1} & {country} similarity : {similarity}')
                    if similarity > max_similarity:
                        max_similarity = similarity
                        closest_country = country
            except Exception as e:
                print(f"An error occurred while processing {country}: {e}")

        print("The closest country is:", closest_country, "with Jaccard similarity:", max_similarity)

if __name__ == "__main__":
    analyzer = NewsAnalyzer()
    analyzer.retrieve_news_and_similarity()
