import os
import traceback
import random
from console import fx, fg

def log(msg: str, is_error=False, is_success=False):
    """ Logs verbose information about runtime. """
    if bool(os.environ.get("VERBOSE", False)) == True:
        msg = fx.bold(str(msg))
        print(f'{fx.dim("* |")} [{fg.red(msg) if is_error else (fg.white(msg) if not is_success else fg.green(msg))}]')
log("Verbose mode: " + os.environ.get("VERBOSE", "False"), "True")


def query_to_dict(query_string: str) -> dict:
    """ Convert a URL query string to a dictionary """
    query_string_split_pairs = query_string.split("&")
    dict_query_string = { }
    for query in query_string_split_pairs:
        query_split = query.split("=") # name=value === ["name", "value"]
        dict_query_string[query_split[0]] = query_split[1]
        if query_split[1] in ("true", "false"):
            dict_query_string[query_split[0]] = bool(query_split[1]) # Parse boolean values
        elif query_split[1].isdecimal():
            dict_query_string[query_split[0]] = float(query_split[1])
    return dict_query_string


def random_sort(_list: list) -> list:
    """ Returns a randomly sorted list. """
    random_sorted_indices = []
    for _ in _list:
        b = len(_list) - 1
        index = random.randint(a=0, b=b)
        while index in random_sorted_indices:
            index = random.randint(a=0, b=b)
            if index not in random_sorted_indices:
                break
        random_sorted_indices.append(index)
    
    """ Re-structure the list with the randomness. """
    random_list = [0 for i in range(len(_list))]
    for index, random_index in enumerate(random_sorted_indices):
        random_list[index] = _list[random_index]
    return random_list
    