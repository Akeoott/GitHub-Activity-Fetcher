import logging, time, sys

RESET, GREEN, BLUE, YELLOW, RED = '\033[0m', '\033[92m', '\033[94m', '\033[93m', '\033[91m'
TOKEN_DOCS = "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens"
TOKEN_DOCS_FORMATTED = f"Dont know how to get a {GREEN}token{RESET}?\n\033]8;;{TOKEN_DOCS}\033\\Visit this website.\033]8;;\033\\"
TOKEN_PRINT_FORMAT = f"{GREEN}token{RESET}"
SELECTION_ERROR = f"\nSelect a {YELLOW}valid{RESET} option!"

class UserInputHandler:
    def __init__(self):
        self.endpoint = None
        self.username = None
        self.useragent = None
        self.repo = None
        self.token = None

    def prompt(self):
        self._select_mode()
        self._confirm()

        return self.endpoint, self.username, self.useragent, self.token

    def _select_mode(self):
        fetch_type = None
        while fetch_type not in {1, 2}:
            try:
                print("\nSelect what you want to fetch:")
                print(f"List {GREEN}user{RESET} events (1)")
                print(f"List {GREEN}repo{RESET} specific user events (2)")
                fetch_type = int(input("\nEnter here: "))

                if fetch_type not in {1, 2}:
                    print(SELECTION_ERROR)
            except ValueError:
                print(SELECTION_ERROR)

        logging.info(f"Fetch type: {fetch_type}")

        print()
        self.username = input(f"Enter the {GREEN}username{RESET} of the person you want to fetch from: ")
        logging.debug(f"UserName entered: {self.username}")
        self.useragent = input(f"Enter your {GREEN}app name{RESET} or {GREEN}identifier{RESET} (Can be anything): ")
        logging.debug(f"UserAgent entered: {self.useragent}")

        if fetch_type == 1:
            self.endpoint = f'https://api.github.com/users/{self.username}/events'
        elif fetch_type == 2:
            self.repo = input(f"Enter the name of your {GREEN}repository{RESET}: ")
            logging.debug(f"Repository entered: {self.repo}")
            self.endpoint = f'https://api.github.com/repos/{self.username}/{self.repo}/events'

        self._ask_for_token(fetch_type)

    def _ask_for_token(self, fetch_type):
        print()
        if fetch_type == 1:
            print(f"You {YELLOW}may{RESET} need a personal access {TOKEN_PRINT_FORMAT}.")
            print(TOKEN_DOCS_FORMATTED)
            self.token = input(f"\nOptional -> Enter your access {TOKEN_PRINT_FORMAT}: ") or None
            if self.token is None:
                logging.info("Did not enter a token")
            else:
                logging.debug("Entered a token: %s", "[HIDDEN]")

        elif fetch_type == 2:
            while True:
                print(f"You {RED}require{RESET} a personal access {TOKEN_PRINT_FORMAT}.")
                print(TOKEN_DOCS_FORMATTED)
                self.token = input(f"\nEnter your access {TOKEN_PRINT_FORMAT}: ")

                if len(self.token) < 5:
                    print(f"\nToken is {RED}too short{RESET}!")
                else:
                    logging.debug("Entered a token: %s", "[HIDDEN]")
                    break


    def _confirm(self):
        print("\nIs this correct?")
        print(f"Username: {GREEN}{self.username}{RESET}")
        print(f"App name or identifier: {GREEN}{self.useragent}{RESET}")
        print(f"Repository: {BLUE if self.repo is None else GREEN}{self.repo}{RESET}")
        print(f"Your token: {BLUE if self.token is None else GREEN}{'[HIDDEN]' if self.token else 'None'}{RESET}")

        if input("Do you want to continue? (y/n): ").strip().lower() != "y":
            logging.info("Denied input")
            print("Exiting...")
            time.sleep(2)
            sys.exit()

        logging.info("Confirmed input")