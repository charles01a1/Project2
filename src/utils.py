import json

def tsv2json(input_file,output_file):
    nested = [ "primaryProfession", "knownForTitles", "genres", "characters"]

    arr = []
    file = open(input_file, 'r')
    a = file.readline()


    titles = [t.strip() for t in a.split('\t')]
    for line in file:
        d = {}
        for t, f in zip(titles, line.split('\t')):
            d[t] = [i.strip() for i in f.split(",")] if t in nested else f.strip()

        arr.append(d)

    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(arr, indent=4))

    del arr

def prepare_json(names):

    input_files = [ name + ".tsv" for name in names ]
    output_files = [ name + ".json" for name in names ]

    for i, o in zip(input_files, output_files):
        tsv2json(i, o)

def gen(file_name):
    with open(file_name) as f:
        for chunk in json.loads(f.read()):
            yield chunk