import requests
from utils import clean_filename


def download_image(book: dict[str, str | int], folder: str) -> None:
    title_clean = clean_filename(str(book["title"]))
    image_url = str(book["image_url"])
    response = requests.get(image_url)
    with open(f"{folder}/{title_clean}.jpg", "wb") as f:
        f.write(response.content)
