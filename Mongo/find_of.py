from typing import Any
import re
from decorator_table import table_for_data
from colorama import Fore, Style
from connect import Author, Quote
from mongoengine import connect
from password import user, password
from redis import StrictRedis
from redis_lru import RedisLRU


connect(db="web_19", host=f"mongodb+srv://{user}:{password}@goitlearn.x6ks5fo.mongodb.net/?retryWrites=true&w=majority")
client = StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

@table_for_data
@cache
def find_by_name_of_author(name: str) -> list[Any, ...] | str:
    author = Author.objects(fullname=name).first()
    if author:
        quotes = Quote.objects(author=author)
        return [i.to_mongo().to_dict() for i in quotes]
    else:
        return "Не знайдено"

@table_for_data
@cache
def find_by_tag(tag: str) -> list[Any] | str:
    quotes = Quote.objects(tags=tag)
    if quotes:
        data = [i.to_mongo().to_dict() for i in quotes]
        return data
    else:
        return "Не знайдено"
@table_for_data
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
            name_aut = command.split(":")[1].strip()

            if re.match("st", name_aut, re.IGNORECASE):
                find_by_name_of_author("Steve Martin")
            else:
                find_by_name_of_author(name_aut)

        elif "tags" in command:
            tags_aut = command.split(":")[1]
            find_by_tags(tags_aut.strip())

        elif "tag" in command:
            tag_aut = command.split(":")[1]
            if re.match("li", tag_aut, re.IGNORECASE):
                find_by_tag("life")
            else:
                find_by_tag(tag_aut.strip())


if __name__ == "__main__":
    main()
