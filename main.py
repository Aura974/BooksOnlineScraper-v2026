from scrape_book import scrape_book
from write_csv import write_csv

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
book = scrape_book(url)

write_csv(book)
