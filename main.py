from scraper import scrape_all_books, scrape_one_book
from write_csv import write_csv

category_url = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
urls = scrape_all_books(category_url)

books: list[dict[str, str | int]] = []

for url in urls:
    books.append(scrape_one_book(url))

write_csv(books)
