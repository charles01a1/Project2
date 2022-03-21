import time
import utils

start = time.time()

def main():

if __name__ == "__main__":

    main()

    dataset_names = [ "name.basics", "title.basics",
                     "title.principals", "title.ratings" ]


    utils.prepare_json(dataset_names)

    from pymongo import MongoClient

    client = MongoClient("mongodb://localhost:27017")

    db = client["291db"]

    collections = { name : db[name] for name in dataset_names}

    for name, collection in collections.items():
        collection.delete_many( {} )
        for doc in utils.gen(name + ".json"):
            collection.insert_one(doc)

    end = time.time()

    print(end - start)