from tabulate import tabulate
from colorama import Fore


def table_for_data(func):
    def wrap(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            table_data = [[d['_id'], d['quote'], ', '.join(d['tags'])] for d in result]
            headers = ['ID', 'Quote', 'Tags']
            table = tabulate(table_data, headers=headers, tablefmt="grid")
            print(Fore.RED + table)
        except TypeError as t:
            print(Fore.GREEN + f"Ошибка ввода : {t}")

    return wrap
