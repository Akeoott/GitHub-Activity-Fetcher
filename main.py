import logging, sys, os
from constants import VERSION, ERROR_TITLE, ISSUE_INFO
import msg_handler # error handeler
from tkinter import messagebox as msgbox

full_path = __file__
file_name = os.path.basename(full_path)

"""
_______________________
How this program works:

1.
main calls input_gui
input_gui returns to main

2.
main calls github_client
github_client returns to main

3.
main calls data_handler
data_handler finishes operation

______________
In exceptions:

Any file calls msg_handler
msg_handler manages error and decides if continue or not

custom_exception contains one custom exception

__________
Constants:

constants contains all constants
"""

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
    msgbox.showerror(title=ERROR_TITLE, message=f"Required modules could not be imported. Exiting.\n\n{ISSUE_INFO}")
    sys.exit()

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

        app = DataHandler(username, data, limit, remaining, reset)
        app.mainloop()

    # If something completely unexpected happens, its gonna get catched!
    except ImportError as e:
        e_type = "error"
        context = "A required module could not be imported."
        logging.error(f"{context}: {e}")
        msg_handler.error_handeling(e, e_type, context, file_name)
    except ValueError as e:
        e_type = "error"
        context = "A value error occurred. Please check your input values."
        logging.error(f"A value error occurred in the code: {e}")
        msg_handler.error_handeling(e, e_type, context, file_name)
    except ConnectionError as e:
        e_type = "error"
        context = "A network connection error occurred. Please check your internet connection."
        logging.error(f"A ConnectionError occurred: {e}")
        msg_handler.error_handeling(e, e_type, context, file_name)
    except TypeError as e:
        e_type = "error"
        context = "A TypeError occurred within the code."
        logging.error(f"{context}: {e}")
        msg_handler.error_handeling(e, e_type, context, file_name)
    except Exception as e:
        e_type = "error"
        context = f"A {type(e).__name__} unexpectedly occurred."
        logging.error(f"An {type(e).__name__} happened unexpectedly.")
        msg_handler.error_handeling(e, e_type, context, file_name)

    logging.info("Exiting...")
    sys.exit()

if __name__ == "__main__":
    main()