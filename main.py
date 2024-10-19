from config import CONFIG
from scraper.scraper import Scraper

if __name__ == "__main__":
    # Create a scraper instance
    scraper = Scraper(CONFIG["URL_MIMOVRSTE"])

    # Fetch HTML content
    scraper.fetch_html()

    # Extract data
    scraper.extract_data()

    # Analyze data
    scraper.analyze_data()
