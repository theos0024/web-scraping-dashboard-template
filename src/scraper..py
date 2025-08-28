# Example scraper template
# Replace with your own scraping logic

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_books():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    books = []
    for item in soup.select(".product_pod"):
        title = item.h3.a["title"]
        price = item.select_one(".price_color").text.strip("£")
        rating = item.p["class"][1]
        books.append([title, float(price), rating])

    df = pd.DataFrame(books, columns=["Title", "Price", "Rating"])
    df.to_csv("data/cleaned_data.csv", index=False)
    print("Scraped and saved to data/cleaned_data.csv")

if __name__ == "__main__":
    scrape_books()
