import os

PATH_SOURCE = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
PATH_PROJECT = os.path.dirname(PATH_SOURCE)

def path_from_source(*args) -> str:
    return os.path.join(PATH_SOURCE, *args)

def path_from_project(*args) -> str:
    return os.path.join(PATH_PROJECT, *args)
