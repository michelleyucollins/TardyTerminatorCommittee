import json
import requests
from bs4 import BeautifulSoup
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--search', default='TTC')
args = parser.parse_args()

def getNewsData(search):
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    response = requests.get(
        "https://www.google.com/search?q="+search+"&gl=us&tbm=nws&num=1000", headers=headers
    )
    soup = BeautifulSoup(response.content, "html.parser")
    news_results = []

    for el in soup.select("div.SoaBEf"):
        news_results.append(
            {
                "link": el.find("a")["href"],
                "title": el.select_one("div.MBeuO").get_text(),
                "snippet": el.select_one(".GI74Re").get_text(),
                "date": el.select_one(".LfVVr").get_text(),
                "source": el.select_one(".NUnG9d span").get_text()
            }
        )

    with open("news_data.csv", "w", newline="") as csv_file:
        fieldnames = ["link", "title", "snippet", "date", "source"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(news_results)
        print("Data saved to news_data.csv")

getNewsData(args.search)


