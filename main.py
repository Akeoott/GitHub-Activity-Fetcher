import logging
from input_handler import UserInputHandler
from github_client import GitHubAPIClient
from data_handler import DataHandler
import sys

RESET, GREEN, RED = '\033[0m', '\033[92m', '\033[91m'

VERSION = '3.0.0'

# LogRecord attributes: https://docs.python.org/3/library/logging.html#logrecord-attributes

def configure_logging():
    if input(f"Activate {GREEN}logging{RESET} + {GREEN}save{RESET}? (y/n): ").lower() == "y":
        logging.basicConfig(
            format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d [%(filename)s])',
            datefmt='%d/%m/%Y %I:%M:%S %p',
            filename='Activity-Fetcher-Log.log',
            level=logging.DEBUG
        )
    else:
        class NullHandler(logging.Handler):
            def emit(self, record): pass
        logging.getLogger().addHandler(NullHandler())
        logging.getLogger().setLevel(logging.CRITICAL + 1)

configure_logging()

logging.info(f"Version {VERSION}")

def main():
    try:
        input_handler = UserInputHandler()
        endpoint, username, useragent, token = input_handler.prompt()

        client = GitHubAPIClient(endpoint, username, useragent, token)
        data, (limit, remaining, reset) = client.fetch_events()

        handler = DataHandler(username, token)
        handler.display(data, limit, remaining, reset)
        handler.save(data)

    # If something completely unexpected happens, its gonna get catched!
    except TypeError as e:
        logging.error(f"A TypeError stopped the program: {type(e).__name__} {e}")
        print(f"\n{RED}Unexpected error{RESET}")
        print(f"{RED}{type(e).__name__}{RESET}: {e}")
        print("\nPlease report this issue on GitHub 'Akeoots/GitHub-Activity-Fetcher/issues'")
    except Exception as e:
        logging.error(f"An exception stopped the program: {type(e).__name__} {e}")
        print(f"\n{RED}Unexpected error{RESET}")
        print(f"{RED}{type(e).__name__}{RESET}: {e}")
        print("\nPlease report this issue on GitHub 'Akeoots/GitHub-Activity-Fetcher/issues'")

    input("\nPress Enter To Exit...")
    logging.info("Exiting...")
    sys.exit()

if __name__ == "__main__":
    main()