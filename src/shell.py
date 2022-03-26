class Shell:

    def __init__(self):
        from user import User

        self.usr = User()

    def add(self, args_str, add_option):
        add_options_dict = {
            "-c": self.usr.add_cast_crew,
            "-m": self.usr.add_movie,
        }

        if add_option in add_options_dict:
            args = args_str.split("|")

            add_options_dict[add_option](*args)

    def search(self, args_str, search_option):
        search_options_dict = {
            "-c": self.usr.search_for_members,
            "-g": self.usr.search_for_genres,
            "-t": self.usr.search_for_titles,
        }

        if search_option in search_options_dict:
            args = args_str.split("|")

            search_options_dict[search_option](*args)

    def print_help(self):
        pass

    def add_help(self):
        pass

    def search_help(self):
        pass

    def main_menu(self):
        cmds_dict = {
            "add": self.add,
            "search": self.search,
            "help": self.print_help,
        }

        while True:
            try:
                self.print_help()

                line = input("$ ").strip()

                if line:
                    cmd_name, rest = line.split(" ", 1)
                    if cmd_name in cmds_dict:
                        option, args_str = line.split(" ", 1)
                        cmds_dict[cmd_name](option, args_str)
                    elif cmd_name == "exit" or cmd_name == "quit":
                        return
                    else:
                        print(f"{line}: command not found\n")

            except (KeyboardInterrupt, EOFError):
                return
