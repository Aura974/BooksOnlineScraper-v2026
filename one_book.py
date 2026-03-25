import requests
from bs4 import BeautifulSoup
import re
import csv


url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")

# title
h1 = soup.find("h1")
title = h1.text if h1 else ""

# description
desc_div = soup.find("div", id="product_description")
desc_p = desc_div.find_next_sibling("p") if desc_div else None
desc = desc_p.text if desc_p else ""

# category
breadcrumb = soup.find("ul", class_="breadcrumb")
category = breadcrumb.find_all("li")[-2].text.strip() if breadcrumb else ""

# rating
rating_map = {
    "One": "1 sur 5",
    "Two": "2 sur 5",
    "Three": "3 sur 5",
    "Four": "4 sur 5",
    "Five": "5 sur 5",
}

brute_rate = soup.find("p", class_="star-rating")
rating = rating_map.get(brute_rate["class"][1], "0 sur 5") if brute_rate else "0 sur 5"

# image
div_img = soup.find("div", class_="item active")
img_tag = div_img.find("img") if div_img else None
img_url_brute = str(img_tag.get("src", "")) if img_tag else ""
image_url = "https://books.toscrape.com/" + img_url_brute.replace("../../", "")

# product info
prod_info: dict[str, str] = {}
table = soup.find("table", class_="table-striped")
if table:
    for ligne in table.find_all("tr"):
        th = ligne.find("th")
        td = ligne.find("td")
        if th and td:
            prod_info[th.text] = td.text

# available
availability = prod_info.get("Availability", "")
match = re.search(r"\d+", availability)
stock: int = int(match.group()) if match else 0

book: dict[str, str | int] = {
    "product_page_url": url,
    "title": title,
    "price_including_tax": prod_info["Price (incl. tax)"],
    "price_excluding_tax": prod_info["Price (excl. tax)"],
    "number_available": stock,
    "category": category,
    "review_rating": rating,
    "product_description": desc,
    "universal_product_code": prod_info["UPC"],
    "image_url": image_url,
}

col = [
    "product_page_url", "universal_product_code", "title", "price_including_tax",
    "price_excluding_tax", "number_available", "product_description", "category",
    "review_rating", "image_url"
]

with open("book.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=col)
    writer.writeheader()
    writer.writerow(book)
