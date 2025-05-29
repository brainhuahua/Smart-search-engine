import os
import json
from bs4 import BeautifulSoup
from glob import glob

INPUT_DIR = "data"
OUTPUT_FILE = "books_extracted.jsonl"

def extract_books_from_page(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    books = []

    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]
        price = article.select_one(".price_color").text.strip()
        availability = article.select_one(".availability").text.strip()
        rating = article.get("class", [])
        rating = [cls for cls in rating if cls != "product_pod"]
        rating = rating[0] if rating else "Unrated"
        relative_link = article.h3.a["href"]
        url = os.path.join(base_url, relative_link).replace("../../", "https://books.toscrape.com/catalogue/")

        books.append({
            "title": title,
            "price": price,
            "availability": availability,
            "rating": rating,
            "url": url
        })
    return books


def main():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        for path in sorted(glob(f"{INPUT_DIR}/*.html")):
            with open(path, encoding="utf-8") as f:
                html = f.read()
                books = extract_books_from_page(html, base_url="https://books.toscrape.com")
                for book in books:
                    out_f.write(json.dumps(book, ensure_ascii=False) + "\n")

    print(f"已完成抽取，结果保存在：{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
