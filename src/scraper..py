# Example scraper template
# Replace with your own scraping logic

import requests
from bs4 import BeautifulSoup
import pandas as pd



def scrape_books():
    import os
    url = "http://books.toscrape.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print("Status code:", response.status_code)
        print("First 200 chars:\n", response.text[:200])

        soup = BeautifulSoup(response.text, "html.parser")

        books = []
        for item in soup.select(".product_pod"):
            title = item.h3.a["title"]
            price = item.select_one(".price_color").text.strip("£")
            rating = item.p["class"][1]
            books.append([title, float(price), rating])

        os.makedirs("data", exist_ok=True)
        df = pd.DataFrame(books, columns=["Title", "Price", "Rating"])
        df.to_csv("data/cleaned_data.csv", index=False)
        print("Scraped and saved to data/cleaned_data.csv")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    scrape_books()
