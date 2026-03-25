import csv
from utils import clean_filename


def write_csv(books: list[dict[str, str | int]]) -> None:
    if not books:
        return

    filename = clean_filename(str(books[0]["category"])) + ".csv"

    col = [
        "product_page_url", "universal_product_code", "title", "price_including_tax",
        "price_excluding_tax", "number_available", "product_description", "category",
        "review_rating", "image_url"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=col)
        writer.writeheader()
        writer.writerows(books)
