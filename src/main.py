# 0.72 GB (usual size of 291db, can be varied)

# number of docs in each collection:
#   324659
#   79972
#   755907
#   79972


def main():
    import time

    import build_docs
    from shell import Shell

    start = time.time()

    # build_docs.prepare_json()
    # build_docs.load_json()

    end = time.time()

    print(f"Time used on phase 1: {end - start}\n")

    Shell().main_menu()


if __name__ == "__main__":
    main()
