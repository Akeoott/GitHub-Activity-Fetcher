import logging, sys
from tkinter import messagebox as msgbox

# LogRecord attributes: https://docs.python.org/3/library/logging.html#logrecord-attributes

RESET, GREEN, RED = '\033[0m', '\033[92m', '\033[91m'

def configure_logging():
    # Prevent duplicate log handlers and repeated configuration
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        return
    if msgbox.askyesno(title="GitHub Activity Fetcher", message=f"Activate logging + save log?", icon="info"):
        logging.basicConfig(
            format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d [%(filename)s])',
            datefmt='%d/%m/%Y %I:%M:%S %p',
            filename='Activity-Fetcher-Log.log',
            level=logging.DEBUG
        )
    else:
        class NullHandler(logging.Handler):
            def emit(self, record): pass
        root_logger.addHandler(NullHandler())
        root_logger.setLevel(logging.CRITICAL + 1)

configure_logging()

VERSION = '4.0.0-ALPHA'

logging.info(f"Version {VERSION}")

from input_gui import InputInterface
from github_client import GitHubAPIClient
from data_handler import DataHandler

def main():
    try:
        input_handler = InputInterface()
        endpoint, username, useragent, token, repo = input_handler.prompt()

        client = GitHubAPIClient(endpoint, username, useragent, token, repo)
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