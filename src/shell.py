from user import User


class Shell:

    def __init__(self):
        self.usr = User()

    def add(self, args_str, option):
        options = {
            "-c": self.usr.add_casts,
            "-m": self.usr.add_movie,
        }

        if option in options:
            args = args_str.split("|")

            options[option](*args)

    def search(self, args_str, option):
        options = {
            "-c": self.usr.search_for_members,
            "-g": self.usr.search_for_genres,
            "-t": self.usr.search_for_titles,
        }

        if option in options:
            args = args_str.split("|")

            options[option](*args)

    def print_help(self):
        pass

    def add_help(self):
        pass

    def search_help(self):
        pass

    def main_menu(self):
        cmds = {
            "add": self.add,
            "search": self.search,
            "help": self.print_help,
        }

        while True:
            try:
                self.print_help()

                line = input("$ ").strip()

                if line:
                    cmd, rest = line.split(" ", 1)
                    if cmd in cmds:
                        option, args_str = line.split(" ", 1)
                        cmds[cmd](option, args_str)
                    elif cmd == "exit" or cmd == "quit":
                        return
                    else:
                        print(f"{line}: command not found\n")

            except (KeyboardInterrupt, EOFError):
                quit(0)
