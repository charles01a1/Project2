import sys

dbname = "291db"

collection_names = ["name.basics", "title.basics", "title.principals",
                    "title.ratings"]

port = sys.argv[-1]

connection_string = f"mongodb://localhost:{port}"
