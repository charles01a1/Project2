def add(args, option):
    pass


def search(args, option):
    pass


def print_help():
    pass


def add_help():
    pass


def search_help():
    pass


def main_menu():
    cmds = {
        "add": add,
        "search": search,
        "help": print_help,
    }

    while True:
        try:
            print_help()

            line = input("$ ").strip()
            print()

            if not line: continue

            tokens = line.split(" ", )

            if cmd in cmds:
                func = cmds[cmd]
                try:
                    func(*args)
                except TypeError:
                    print(f"{cmd}: invalid arguments\n")
            elif cmd == "exit" or cmd == "quit":
                quit(0)
            elif cmd == "logout":
                print("Logout successfully\n")
                return
            else:
                print(f"{line}: command not found\n")
        except (KeyboardInterrupt, EOFError):
            quit(0)