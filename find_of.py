from typing import List, Any

from connect import Author, Quote
from mongoengine import connect
from password import user, password
from redis import StrictRedis
from redis_lru import RedisLRU
from colorama import Fore, Style
from tabulate import tabulate

connect(db="web_19", host=f"mongodb+srv://{user}:{password}@goitlearn.x6ks5fo.mongodb.net/?retryWrites=true&w=majority")
# client = StrictRedis(host="localhost", port=6379, password=None)
# cache = RedisLRU(client)
# @cache
def find_by_name_of_author(name: str) -> list[Any] | str:
    author = Author.objects(fullname=name).first()
    if author:
        quotes = Quote.objects(author=author)
        return [i.to_mongo().to_dict() for i in quotes]
    else:
        return "Не знайдено"

# @cache
def find_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    data = [i.to_mongo().to_dict() for i in quotes]
    return data


# @cache
def find_by_tags(tags):
    ...

def main():
    while True:
        command = input(Fore.BLUE + "I can searc by tag, tags or name pls enter everything: " + Style.RESET_ALL )
        if "exit" in command:
            print(Fore.RED +"Good luck")
            return None
        elif "name" in command:
            name_aut = command.split(":")[1]
            data = find_by_name_of_author(name_aut.strip())
            table_data = [[d['_id'], d['quote'], ', '.join(d['tags'])] for d in data]
            headers = ['ID', 'Quote', 'Tags']
            table = tabulate(table_data, headers=headers)
            print(Fore.RED + table)
        elif "tag" in command:
            tag_aut = command.split(":")[1]
            data = find_by_tag(tag_aut.strip())
            table_data = [[d['_id'], d['quote'], ', '.join(d['tags'])] for d in data]
            headers = ['ID', 'Quote', 'Tags']
            table = tabulate(table_data, headers=headers)
            print(Fore.RED + table)



if __name__ == "__main__":
    main()




