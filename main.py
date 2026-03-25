from scraper import get_category_urls, get_books_urls, scrape_one_book
from write_csv import write_csv
from download_images import download_image
from utils import clean_filename
from tqdm import tqdm
import os


BASE_URL = "https://books.toscrape.com/"


def main() -> None:
    category_urls = get_category_urls(BASE_URL)

    for category_url in tqdm(category_urls, desc="Catégories"):
        book_urls = get_books_urls(category_url)
        books: list[dict[str, str | int]] = []
        folder: str | None = None

        for book_url in tqdm(book_urls, desc="  Livres", leave=False):
            book = scrape_one_book(book_url)
            books.append(book)

            # créer le dossier au premier livre (on connaît la catégorie)
            if folder is None:
                folder = "images/" + clean_filename(str(book["category"]))
                os.makedirs(folder, exist_ok=True)

            download_image(book, folder)

        write_csv(books)


if __name__ == "__main__":
    main()
