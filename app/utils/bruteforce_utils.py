import itertools
from typing import List,Generator
def bruteforce_lst_generator(prefix_str:str="",max_str_size:int=5):
    # Characters to iterate through
    characters = 'abcdefghijklmnopqrstuvwxyz0123456789'
    str_list = []
    max_str_size = max(len(prefix_str),max_str_size)
    # Generate strings of length 1 (single characters)
    for char in characters:
        str_list.append(prefix_str + char)
    yield str_list
    # Generate strings of length 2 (combinations with repetition)
    for length in range(2, max_str_size+1):
        str_list = []
        for combo in itertools.product(characters, repeat=length):
            str_list.append(prefix_str + ''.join(combo))
        yield str_list
    return str_list