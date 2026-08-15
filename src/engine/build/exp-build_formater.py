"""
Här har vi klasser som används för typ artiklar, hear me outs, notiser eller annat
"""
import re

# import scripts
from engine import utils
from ostraloken.src.engine.build import gen_replacment_dict

class Article:
    def __init__(self, title: str, type: str, writer: str, article: str, upplaga_nmr: int):
        self.title = title
        self.type = type
        self.writer = writer
        self.article = article
        self.upplaga_nmr = upplaga_nmr
    