# Given the db_schema, generate a list of pairs of (question, sql_query) in json
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from src.app import bootstrap

bootstrap.init()

from src.app import settings
from src.llm import llm
from src.llm import models


def generate_pairs(db_schema):
    pairs = []
    for table_info in db_schema:
        res = llm.prompt_for_pairs(table_info)
        p = models.SQLPair(question=res.question, sql_query=res.sql_query)
        pairs.append(vars(p))
    return pairs


def save_pairs(pairs):
    json.dump(pairs, open(os.path.join(settings.APP_ROOT, settings.TEST_PAIRS_PATH), "w"))


if __name__ == '__main__':
    db_schema = json.load(open(os.path.join(settings.APP_ROOT, settings.DB_SCHEMA_PATH)))
    pairs = generate_pairs(db_schema)
    save_pairs(pairs)
