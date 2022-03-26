def prepare_json():
    from config import collection_names
    from utils import tsv2json

    input_files = [name + ".tsv" for name in collection_names]
    output_files = [name + ".json" for name in collection_names]

    for i, o in zip(input_files, output_files):
        tsv2json(i, o)


def load_json():
    import json

    from connection import collections

    for name, collection in collections.items():
        collection.delete_many({})
        with open(f"{name}.json") as f:
            docs = [json.loads(line) for line in f]
            collection.insert_many(docs)
