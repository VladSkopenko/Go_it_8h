from typing import  Any

from connect import Author, Quote
from mongoengine import connect
from password import user, password
from redis import StrictRedis
from redis_lru import RedisLRU
from colorama import Fore, Style
from tabulate import tabulate
import re

connect(db="web_19", host=f"mongodb+srv://{user}:{password}@goitlearn.x6ks5fo.mongodb.net/?retryWrites=true&w=majority")
client = StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_name_of_author(name: str) -> list[Any] | str:
    author = Author.objects(fullname=name).first()
    if author:
        quotes = Quote.objects(author=author)
        return [i.to_mongo().to_dict() for i in quotes]
    else:
        return "Не знайдено"


@cache
def find_by_tag(tag: str) -> list[Any] | str:
    quotes = Quote.objects(tags=tag)
    if quotes:
        data = [i.to_mongo().to_dict() for i in quotes]
        return data
    else:
        return "Не знайдено"


@cache
def find_by_tags(tags: str)-> list[Any] | str:
    tags_list = tags.split(',')
    quotes = Quote.objects(tags__in=tags_list)
    if quotes:
        data = [i.to_mongo().to_dict() for i in quotes]
        return data
    else:
        return "Не знайдено"


def main():
    while True:
        command = input(Fore.BLUE + "I can searc by tag, tags or name pls enter everything: " + Style.RESET_ALL)
        if "exit" in command:
            print(Fore.RED + "Good luck")
            return None

        elif "name" in command:
            try:
                name_aut = command.split(":")[1].strip()

                if re.match("st", name_aut, re.IGNORECASE):
                    data = find_by_name_of_author("Steve Martin")
                else:
                    data = find_by_name_of_author(name_aut)

                table_data = [[d['_id'], d['quote'], ', '.join(d['tags'])] for d in data]
                headers = ['ID', 'Quote', 'Tags']
                table = tabulate(table_data, headers=headers)
                print(Fore.RED + table)
            except TypeError:
                print(Fore.YELLOW + "Что то не то ввел, давай по новой ")

        elif "tags" in command:
            tags_aut = command.split(":")[1]
            data = find_by_tags(tags_aut.strip())
            table_data = [[d['_id'], d['quote'], ', '.join(d['tags'])] for d in data]
            headers = ['ID', 'Quote', 'Tags']
            table = tabulate(table_data, headers=headers)
            print(Fore.RED + table)

        elif "tag" in command:
            try:
                tag_aut = command.split(":")[1]
                if re.match("li", tag_aut, re.IGNORECASE):
                    data = find_by_tag("life")
                else:
                    data = find_by_tag(tag_aut.strip())
                table_data = [[d['_id'], d['quote'], ', '.join(d['tags'])] for d in data]
                headers = ['ID', 'Quote', 'Tags']
                table = tabulate(table_data, headers=headers)
                print(Fore.RED + table)
            except TypeError:
                print(Fore.YELLOW + "Что то не то ввел, давай по новой ")
        else:
            continue


if __name__ == "__main__":
    main()
