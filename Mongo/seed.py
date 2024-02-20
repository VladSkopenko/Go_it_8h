import json
from connect import Author, Quote
from mongoengine import connect
from password import user, password

connect(db="web_19", host=f"mongodb+srv://{user}:{password}@goitlearn.x6ks5fo.mongodb.net/?retryWrites=true&w=majority")
def load_authors():
    with open("authors.json", 'r', encoding="utf-8") as file:
        data_of_authors = json.load(file)
        for author in data_of_authors:
            aut = Author(fullname=author.get("fullname"),
                         born_date=author.get("born_date"),
                         born_location=author.get("born_location"),
                         description=author.get("description"))
            aut.save()

def load_quotes():
    with open("qoutes.json", "r", encoding="utf-8") as file:
        data_quotes = json.load(file)
        for quote_data in data_quotes:
            author_name = quote_data.get('author')
            author = Author.objects.get(fullname=author_name) if author_name else None
            if author:
                quote = Quote(author=author,
                              tags=quote_data.get("tags"),
                              quote=quote_data.get("quote")
                             )
                quote.save()
            else:
                print(f"Author '{author_name}' not found.")


