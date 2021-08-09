from flask import Flask
from flaskmnd.util.data import DaMongo

class DaFlask(Flask):
    mng: DaMongo

    def __init__(self, *args, **kwargs):
        super(DaFlask, self).__init__(*args, **kwargs)
