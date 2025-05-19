import logging, sys
from tkinter import messagebox as msgbox
from constants import VERSION, MSGBOX_ERROR_TITLE, MSGBOX_ERROR_OPEN_ISSUE_INFO

# LogRecord attributes: https://docs.python.org/3/library/logging.html#logrecord-attributes

def configure_logging():
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        return
    
    logging_req = msgbox.askyesnocancel(title="GitHub Activity Fetcher", message=f"Activate logging + save log?", icon="info")

    if logging_req is True:
        logging.basicConfig(
            format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d [%(filename)s])',
            datefmt='%d/%m/%Y %I:%M:%S %p',
            filename='Activity-Fetcher-Log.log',
            level=logging.DEBUG
        )
    elif logging_req is False:
        class NullHandler(logging.Handler):
            def emit(self, record): pass
        root_logger.addHandler(NullHandler())
        root_logger.setLevel(logging.CRITICAL + 1)
    else:
        sys.exit()

configure_logging()

logging.info(f"Version {VERSION}")

try:
    from input_gui import InputInterface
    from github_client import GitHubAPIClient
    from data_handler import DataHandler
except ImportError as e:
    logging.error(f"ImportError: {e}")
    sys.exit("Required modules could not be imported. Exiting.")

"""
Main function resides here.
This is where all other files get called to make out the entire program.
"""

def main():
    try:
        input_handler = InputInterface()
        # Call the method that runs the GUI and returns inputs
        endpoint, username, useragent, token, repo = input_handler.get_inputs()

        if not endpoint: # Or check any other essential value like username
            logging.warning("No input provided from the GUI. Exiting.")
            sys.exit()

        client = GitHubAPIClient(endpoint, username, useragent, token, repo)
        data, (limit, remaining, reset) = client.fetch_events()

        handler = DataHandler(username, token)
        handler.display(data, limit, remaining, reset)
        handler.save(data)
    
    # If something completely unexpected happens, its gonna get catched!
    except TypeError as e:
        logging.error(f"A TypeError stopped the program: {type(e).__name__} {e}")
        msgbox.showerror(title=MSGBOX_ERROR_TITLE, message=f"Unexpected error\n{type(e).__name__}:\n{e}{MSGBOX_ERROR_OPEN_ISSUE_INFO}")
    except Exception as e:
        logging.error(f"An exception stopped the program: {type(e).__name__} {e}")
        msgbox.showerror(title=MSGBOX_ERROR_TITLE, message=f"Unexpected error\n{type(e).__name__}:\n{e}{MSGBOX_ERROR_OPEN_ISSUE_INFO}")

    logging.info("Exiting...")
    sys.exit()

if __name__ == "__main__":
    main()