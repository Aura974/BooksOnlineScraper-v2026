import csv
import re


def write_csv(book: dict[str, str | int]) -> None:
    title = str(book["title"])
    title_clean = re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "_").lower()
    filename = f"{title_clean}.csv"

    col = [
        "product_page_url", "universal_product_code", "title", "price_including_tax",
        "price_excluding_tax", "number_available", "product_description", "category",
        "review_rating", "image_url"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=col)
        writer.writeheader()
        writer.writerow(book)
