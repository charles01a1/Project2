def prepare_json():
    import time
    
    from config import collection_names
    from utils import tsv2json

    start = time.time()

    input_files = [name + ".tsv" for name in collection_names]
    output_files = [name + ".json" for name in collection_names]

    for i, o in zip(input_files, output_files):
        tsv2json(i, o)
        
    end = time.time()
    
    print(f"Runtime: {end - start}\n")

if __name__ == "__main__":
    prepare_json()