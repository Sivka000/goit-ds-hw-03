import requests
import json
import time

from bs4 import BeautifulSoup
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Сайт для пошуку
site_url = "https://quotes.toscrape.com/"

uri = "mongodb+srv://Sivka:v7ddG9W62P23Oc5L@cluster0.zpagku6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

authors_db = client["authors_db"]
authors_collection = authors_db["authors"]

quotes_db = client["quotes_db"]
quotes_collection = quotes_db["quotes"]


def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def scrape_quotes(max_pages: int):
    quotes_list = []
    authors = {}
    start = time.time()

    for page in range(1, max_pages + 1):
        soup  = get_soup(f"{site_url}/page/{page}/")
        items = soup.select(".quote")
        if not items:
            break

        for q in items:
            text   = q.select_one(".text").get_text(strip=True)
            author = q.select_one(".author").get_text(strip=True)
            tags   = [t.get_text(strip=True) for t in q.select(".tags .tag")]

            quotes_list.append({"quote": text, "author": author, "tags": tags})
            authors.setdefault(
                author,
                site_url + q.select_one(".author + a")["href"]
            )

        elapsed = time.time() - start
        done = page
        total = max_pages
        remaining = total - done
        pct = done / total * 100
        eta = (elapsed / done) * remaining if done else 0

        print(
            f"\r[Page {done}/{total} | {pct:5.1f}%]  "
            f"Elapsed: {elapsed:5.1f}s  "
            f"ETA: {eta:5.1f}s",
            end="", flush=True
        )

    print()
    return quotes_list, authors


def scrape_authors(authors):
    authors_list = []
    total = len(authors)
    start = time.time()

    for idx, (name, url) in enumerate(authors.items(), 1):
        soup = get_soup(url)
        born_date     = soup.select_one(".author-born-date").get_text(strip=True)
        born_location = soup.select_one(".author-born-location").get_text(strip=True)
        description   = soup.select_one(".author-description").get_text(strip=True)
        
        authors_list.append({
            "fullname":      name,
            "born_date":     born_date,
            "born_location": born_location,
            "description":   description
        })

        elapsed = time.time() - start
        remaining = total - idx
        pct = idx / total * 100
        eta = (elapsed / idx) * remaining if idx else 0

        print(
            f"\r[{idx}/{total} | {pct:5.1f}%]  "
            f"Elapsed: {elapsed:5.1f}s  "
            f"ETA: {eta:5.1f}s",
            end="", flush=True
        )

    print()
    return authors_list


def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_to_mongo(collection, data):
    if data:
        collection.insert_many(data)
        print(f"Збережно {len(data)} записів у {collection.name}")


def main():
    quotes, authors = scrape_quotes(200)
    authors = scrape_authors(authors)

    save_json(quotes, "quotes.json")
    save_json(authors, "authors.json")
    print("Дані збережено у quotes.json та authors.json")

    save_to_mongo(authors_collection, authors)
    save_to_mongo(quotes_collection, quotes)
    print("Дані збережено у MongoDB")


if __name__ == "__main__":
    main()