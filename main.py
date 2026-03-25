from scraper import get_category_urls, get_books_urls, scrape_one_book
from write_csv import write_csv

BASE_URL = "https://books.toscrape.com/"


def main() -> None:
    category_urls = get_category_urls(BASE_URL)

    for category_url in category_urls:
        book_urls = get_books_urls(category_url)
        books: list[dict[str, str | int]] = []

        for book_url in book_urls:
            books.append(scrape_one_book(book_url))

        write_csv(books)


if __name__ == "__main__":
    main()
