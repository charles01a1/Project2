import time

import utils

from shell import Shell

# 0.72 GB (usual size of 291db, can be varied)

# number of docs in each collection:
#   324659
#   79972
#   755907
#   79972


def main():
    start = time.time()

    utils.prepare_json()
    utils.load_json()

    Shell().main_menu()

    end = time.time()

    print(f"Runtime:{end - start}")


if __name__ == "__main__":
    main()
