import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re


def parse_date(text):
    try:
        return datetime.strptime(text, "%m-%d-%y").date()
    except ValueError:
        return None

def parse_length_to_timedelta(text):
    hours = minutes = 0
    if "hr" in text:
        h_match = re.search(r"(\d+)\s*hr", text)
        if h_match:
            hours = int(h_match.group(1))
    if "min" in text:
        m_match = re.search(r"(\d+)\s*min", text)
        if m_match:
            minutes = int(m_match.group(1))
    return timedelta(hours=hours, minutes=minutes)

def extract_clean_text(selector, label, book):
    tag = book.find("li", class_=selector)
    if tag:
        return ' '.join(tag.get_text(strip=True).replace(label, "").split())
    return None

class DataParser:
    def __init__(self, query):
        URL = f"https://www.audible.com/search?keywords={query}"

        response = requests.get(url=URL)
        web_page = response.text
        soup = BeautifulSoup(web_page, "html.parser")

        self.audio_book_info_list = soup.find_all("li", class_="bc-list-item productListItem")

        self.audio_books = []

        self.get_audio_book_data()

    def get_audio_book_data(self):
        for book in self.audio_book_info_list:
            title_tag = book.find("h3", class_="bc-heading")
            title = title_tag.get_text(strip=True) if title_tag else None

            author = extract_clean_text("authorLabel", "By:", book=book)
            narrator = extract_clean_text("narratorLabel", "Narrated by:", book=book)
            length_raw = extract_clean_text("runtimeLabel", "Length:", book=book)
            release_raw = extract_clean_text("releaseDateLabel", "Release date:", book=book)
            language = extract_clean_text("languageLabel", "Language:", book=book)

            book_data = {
                "title": title,
                "author": author,
                "narrator": narrator,
                "length": parse_length_to_timedelta(length_raw) if length_raw else None,
                "release_date": parse_date(release_raw) if release_raw else None,
                "language": language
            }

            self.audio_books.append(book_data)



