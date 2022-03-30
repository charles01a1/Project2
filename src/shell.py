class Shell:

    def __init__(self):
        from user import User

        self.usr = User()

    def add(self, args_str, add_option):
        add_options_dict = {
            "-c": self.usr.add_cast_crew,
            "-m": self.usr.add_movie,
        }

        if add_option in add_options_dict.keys():
            args = args_str.split("|")

            try:
                add_options_dict[add_option](*args)
            except ValueError:
                print(f"add {add_option}: invalid arguments")
        else:
            print(f"add: invalid option {add_option}")

    def search(self, args_str, search_option):
        search_options_dict = {
            "-m": self.usr.search_for_member,
            "-g": self.usr.search_for_genres,
            "-t": self.usr.search_for_titles,
        }

        if search_option in search_options_dict.keys():
            args = args_str.split("|")

            try:
                search_options_dict[search_option](*args)
            except ValueError:
                print(f"add {search_option}: invalid arguments")
        else:
            print(f"search: invalid option {search_option}")

    def print_help(self):
        self.add_help()
        self.search_help()

    def add_help(self):
        print("add usage:\n"
              "add a cast/crew member\t"
                    "add|[-c]|[member_id]|[title_id]|[category]\n"
              "add a movie\t"
                    "add|[-m]|[title_id]|[title]|[start_year]|[runtime]|[list_of_genres]\n")

    def search_help(self):
        print("search usage:\n"
              "search a for genre with a minimum vote count\t"
                    "search|[-g]|[genre]|[minimum_vote_count]\n"
              "search for a cast/crew member\t"
                    "search|[-m]|[case/crew_member_name]\n"
              "search for titles with a list of keywords\t"
                    "search|[-t]|[keyword_1];[keyword_2];...;[keyword_n]|<year_1>;<year_2>;...;<year_n>\n")

    def main_menu(self):
        cmds_dict = {
            "add": (self.add, True),
            "search": (self.search, True),
            "help": (self.print_help, False),
        }

        self.print_help()

        while True:
            try:

                line = input("$ ").strip()
                print("\n")

                if line:
                    cmd_name = line.split("|", 1)[0]
                    if cmd_name in cmds_dict:
                        if cmds_dict[cmd_name][1]:  # commands that take in args
                            try:
                                rest = line.split("|", 1)[1]
                                option, args_str = rest.split("|", 1)
                                cmds_dict[cmd_name][0](args_str, option)
                            except (IndexError, ValueError):  # no arguments provided
                                print(f"{cmd_name}: require arguments")
                        else:
                            cmds_dict[cmd_name][0]()
                    elif cmd_name == "exit" or cmd_name == "quit":
                        return
                    else:
                        print(f"{line}: command not found\n")

            except (KeyboardInterrupt, EOFError):
                return
