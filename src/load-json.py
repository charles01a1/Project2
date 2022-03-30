def load_json():
    import time
    import json

    from connection import collections

    start = time.time()

    for name, collection in collections.items():
        collection.delete_many({})
        with open(f"{name}.json") as f:
            docs = [json.loads(line) for line in f]
            collection.insert_many(docs)
    
    end = time.time()
    
    print(f"Runtime: {end - start}\n")
    

if __name__ == "__name__":
    load_json()
