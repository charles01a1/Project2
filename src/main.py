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

    build_docs.prepare_json()
    build_docs.load_json()

    Shell().main_menu()

    end = time.time()

    print(f"Runtime: {end - start}\n")


if __name__ == "__main__":
    main()
