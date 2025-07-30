from data_parser import DataParser
import pandas as pd

URL = "https://docs.google.com/forms/d/e/1FAIpQLSdSPauZGSKTHtlqQfOIGOhzDu82k3aIkbnc8Q83ZUF8Yfp9OQ/viewform"

user_input = input("What audio books would you like the data for? ")

audio_books = DataParser(user_input).audio_books

df = pd.DataFrame(audio_books)
df.to_csv(f"audio_books_searched_by_{user_input}.csv", index=False)