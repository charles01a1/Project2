from pymongo import InsertOne
from pymongo.errors import BulkWriteError

import json

from config import collection_names


def insert_documents(lines, collection):
    requests = [InsertOne(json.loads(line)) for line in lines]
    try:
        collection.bulk_write(requests, ordered=False)
    except BulkWriteError as bwe:
        print(bwe.details)


def load_json():
    from connection import collections

    for name, collection in collections.items():
        collection.delete_many({})
        with open(f"{name}.json") as f:
            lines = f.readlines(1024)
            while lines:
                insert_documents(lines, collection)
                lines = f.readlines(1024)


def tsv2json(input_file, output_file):
    nested = ["primaryProfession", "knownForTitles", "genres", "characters"]

    with open(input_file, "r") as fin, open(output_file, "w", encoding="utf-8") as fout:
        line = fin.readline()

        titles = [t.strip() for t in line.split("\t")]

        while line:
            line = fin.readline()

            d = {}

            for title, value in zip(titles, line.split("\t")):
                value = value.strip()

                if value == "\\N":
                    d[title] = None
                elif value.isdecimal():
                    d[title] = int(value.strip())
                else:
                    d[title] = [v.strip() for v in value.split(",")] if title in nested else value.strip()

            fout.write(json.dumps(d))
            fout.write("\n")


def prepare_json():
    input_files = [name + ".tsv" for name in collection_names]
    output_files = [name + ".json" for name in collection_names]

    for i, o in zip(input_files, output_files):
        tsv2json(i, o)
