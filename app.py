# Initialize FastAPI
from fastapi import FastAPI
from starlette.responses import HTMLResponse

from config import CONFIG
from scraper.scraper import Scraper

app = FastAPI()

@app.get(path="/", response_class=HTMLResponse)
def read_data():
    # Use your existing scraper to fetch and extract data
    scraper = Scraper(CONFIG["URL_MIMOVRSTE"])

    scraper.fetch_html()
    scraper.extract_data()

    data = scraper.data

    # HTML content to display the scraped data
    html_content = f"""
    <html>
    <head>
        <title>Scraped Data</title>
        <style>
            body {{
                background-color: black;
                color: white;
            }}
            h1, h2, ul, li {{
                color: white;
            }}
        </style>
    </head>
    <body>
        <h1>Scraped Data from Sports Betting</h1>

        <h2>Match Titles</h2>
        <ul>
            {''.join(f'<li>{title}</li>' for title in data['match_titles'])}
        </ul>

        <h2>Match Descriptions</h2>
        <ul>
            {''.join(f'<li>{desc}</li>' for desc in data['match_descriptions'])}
        </ul>

        <h2>Match Prices</h2>
        <ul>
            {''.join(f'<li>{price}</li>' for price in data['match_prices'])}
        </ul>
    </body>
    </html>
    """


    return HTMLResponse(content=html_content)