import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd

from config import CONFIG


class Scraper:
    def __init__(self, url: str):
        self.url = url
        self.soup = None
        self.data = {}

    def fetch_html(self):
        """Fetch the HTML content of the page."""
        response = requests.get(self.url, headers=CONFIG["HEADERS"])
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, 'lxml')
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    def extract_data(self):
        """Extract relevant data from the page."""
        if self.soup:
            # Extract titles
            match_titles = [match.get_text() for match in self.soup.find_all('h1', class_='detail__title detail__title--desktop')]

            # Extract descriptions
            match_descriptions = [match.get_text() for match in self.soup.find_all('div', class_='product-short-description')]

            # Extract price
            match_prices = [match.get_text() for match in self.soup.find_all('div', class_='price__wrap__box__final')]

            # Storing extracted data in a list of dictionaries
            self.data = {
                'match_titles': match_titles,
                'match_descriptions': match_descriptions,
                'match_prices': match_prices
            }

        else:
            print("Soup object is empty. Fetch HTML before extracting data.")

    def save_to_csv(self, filename='betting_data.csv'):
        """Save the extracted data to a CSV file."""
        if self.data:
            keys = self.data[0].keys()
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                dict_writer = csv.DictWriter(f, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(self.data)
            print(f"Data saved to {filename}.")
        else:
            print("No data available to save to CSV.")

    def save_to_json(self, filename='betting_data.json'):
        """Save the extracted data to a JSON file."""
        if self.data:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            print(f"Data saved to {filename}.")
        else:
            print("No data available to save to JSON.")

    def analyze_data(self):
        """Analyze the data using pandas."""
        if self.data:
            df = pd.DataFrame(self.data)

            # Print the first 5 rows of the dataframe
            print("Head of the DataFrame:")
            print(df.head())

            # Print the column names
            print("\nColumn names:")
            print(df.columns)

            # Print the shape of the dataframe
            print("\nShape of the DataFrame:")
            print(df.shape)

            # Print summary statistics
            print("\nSummary statistics:")
            print(df.describe())

            # Print information about the dataframe
            print("\nInformation about the DataFrame:")
            print(df.info())
        else:
            print("No data available for analysis.")
