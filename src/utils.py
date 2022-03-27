import datetime
import json
import re


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
                elif title == "characters":
                    value = re.sub(r"[\[\]\"]", "", value)
                    d[title] = [v for v in value.split(",")]
                else:
                    d[title] = [v.strip() for v in value.split(",")] if title in nested else value.strip()

            fout.write(json.dumps(d))
            fout.write("\n")


def is_valid_int(num):
    return num.isdigit() and int(num) > 0


def is_valid_year(year):
    return year.isdigit() and datetime.MINYEAR <= int(year) <= datetime.datetime.today().year


def validate_data(assertion_pairs):
    try:
        for f, msg in assertion_pairs.items():
            assert f, msg
        return True
    except AssertionError as error:
        print(f"{error}\n")
        return False
