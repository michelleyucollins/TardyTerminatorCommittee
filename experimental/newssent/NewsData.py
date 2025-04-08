import json
import requests
from bs4 import BeautifulSoup
import csv
import argparse

'''
Required packages are included in the requirements.txt file.

To scrape data for a certain search term type:

python data/newssent/NewsData.py --query <item> 

in your terminal.
'''

parser = argparse.ArgumentParser()
parser.add_argument('--query', default='TTC')
args = parser.parse_args()

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
}
count = 0
prev_news_results = []
while (True):
    response = requests.get(
        f"https://www.google.com/search?q={args.query}&gl=us&tbm=nws&num=100&start={100*count}", headers=headers
    )
    
    soup = BeautifulSoup(response.content, "html.parser")
    news_results = prev_news_results.copy()
    
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
    count += 1
    if news_results == prev_news_results:
        break

    prev_news_results=news_results


file_name = "data/newssent/news_"+args.query+".csv"
with open(file_name, "w", newline="") as csv_file:
    fieldnames = ["link", "title", "snippet", "date", "source"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(news_results)
    print("Data saved to"+file_name)