import logging, os, json, pprint, time

RESET, GREEN, YELLOW, BLUE, RED = '\033[0m', '\033[92m', '\033[93m', '\033[94m', '\033[91m'

class DataHandler:
    def __init__(self, username, token):
        self.username = username
        self.token = token

    def display(self, data, rate_limit, rate_remaining, rate_reset):
        print(f"\n{GREEN}User Events:{RESET}")
        pprint.pprint(data)

        if self.token is None:
            print("\nSome information may not be present as you have not entered an access token!")

        print("\nRate Limit information:")
        print(f"Rate Limit: {rate_limit} requests per hour")
        print(f"Remaining Requests: {rate_remaining}")
        print(f"Rate Limit Reset at: {time.ctime(int(rate_reset)) if rate_reset.isdigit() else '?'}")

        logging.info("Successfully displayed data")

    def save(self, data):
        if input(f"\n{GREEN}Save{RESET} as json? ({RED}will overwrite existing files with the same username!{RESET})\n(y/n): ").strip().lower() != "y":
            return
        logging.debug("Attempting to save as JSON")

        try:
            self._write_file(data, f"{self.username}-data.json")
            print(f"\n{self.username}-data.json was {GREEN}created{RESET} in the same directory!")
            logging.info(f"Successfully created {self.username}-data.json")
        except PermissionError as e:
            logging.warning("Permission Error. Attempting alternative path.")
            print(f"\nYou don't have the {RED}permission{RESET} to write here.")
            print(f"{RED}{type(e).__name__}:{RESET} {e}")
            self._prompt_alternate_path(data)

    def _write_file(self, data, path):
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def _prompt_alternate_path(self, data):
        while True:
            try:
                directory = input(f"Enter an {YELLOW}alternative{RESET} directory or {RED}press enter to cancel{RESET}: ")
                if directory == "":
                    logging.info("Canceled saving as JSON")
                    break
                if os.path.isdir(directory):
                    path = os.path.join(directory, f"{self.username}-data.json")
                    self._write_file(data, path)
                    print(f"\n{self.username}-data.json was {GREEN}created{RESET} at: {path}")
                    logging.info(f"Successfully created {self.username}-data.json")
                    break
                else:
                    print(f"{RED}Invalid path!{RESET}")
            except PermissionError:
                logging.warning("Permission Error. Attempting retry.")