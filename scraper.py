import requests
from bs4 import BeautifulSoup
import re


def get_category_urls(url: str) -> list[str]:
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    urls: list[str] = []
    nav = soup.find("ul", class_="nav-list")
    if nav:
        for a_tag in nav.find_all("a"):
            href = str(a_tag.get("href", ""))
            urls.append(url + href)

    return urls[1:]


def get_books_urls(category_url: str) -> list[str]:
    urls: list[str] = []
    base_url = "https://books.toscrape.com/catalogue/"
    current_url = category_url

    while True:
        response = requests.get(current_url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        # get all urls
        for article in soup.find_all("article", class_="product_pod"):
            a_tag = article.find("a")
            if a_tag:
                href = str(a_tag.get("href", ""))
                # reconstruct urls
                clean = href.replace("../", "")
                urls.append(base_url + clean)

        # check for "next" button
        next_btn = soup.find("li", class_="next")
        if next_btn:
            next_a = next_btn.find("a")
            if next_a:
                next_href = str(next_a.get("href", ""))
                # construct URL for next page
                current_url = current_url.rsplit("/", 1)[0] + "/" + next_href
        else:
            break

    return urls


def scrape_one_book(book_url: str) -> dict[str, str | int]:
    response = requests.get(book_url)
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

    return {
        "product_page_url":       book_url,
        "title":                  title,
        "price_including_tax":    prod_info.get("Price (incl. tax)", ""),
        "price_excluding_tax":    prod_info.get("Price (excl. tax)", ""),
        "number_available":       stock,
        "category":               category,
        "review_rating":          rating,
        "product_description":    desc,
        "universal_product_code": prod_info.get("UPC", ""),
        "image_url":              image_url,
    }
