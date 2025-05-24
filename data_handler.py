import logging, sys, os, json, pprint, time
from constants import ERROR_TITLE, INFO_TITLE
import tkinter as tk
from tkinter import messagebox as msgbox
from tkinter import filedialog

class DataHandler:
    def __init__(self, username, token):
        self.username = username
        self.token = token

    def display(self, data, rate_limit, rate_remaining, rate_reset):
        pprint.pprint(data)

        # Missing Data Info Display
        if self.token is not None:
            if data == []:
                msgbox.showinfo(title=INFO_TITLE, message="It appears as there is no information present\nThis may be due to the user having a private profile or it not existing.\n\nThis program will now terminate, sorry!\n\nIf you belive that this is false, retry then open an issue on GitHub\n'Akeoots/GitHub-Activity-Fetcher/issues'.")
                sys.exit()
        else:
            msgbox.showinfo(title=INFO_TITLE, message="Some information may not be present as you have not entered an access token!")

        # Rate Limit Info Display
        try:
            reset_time = time.ctime(int(rate_reset)) if rate_reset.isdigit() else "Unknown"
        except Exception as e:
            logging.warning(f"Failed to parse rate reset time: {e}")
            reset_time = "Unknown"
        
        rate_message = (
            f"Rate Limit Information:\n\n"
            f"Limit: {rate_limit} requests/hour\n"
            f"Remaining: {rate_remaining}\n"
            f"Resets at: {reset_time}"
        )
        msgbox.showinfo(title=INFO_TITLE, message=rate_message)

        logging.info("Successfully displayed data")

    def save(self, data):
        if msgbox.askyesno(title=INFO_TITLE, message=f"Save as json?\n(will overwrite existing files with the same username!)") is False:
            return
        logging.debug("Attempting to save as JSON")

        while True:
            try:
                root = tk.Tk()
                root.withdraw()  # Hide the main window
                self.directory = filedialog.askdirectory(title="Select a directory")
                if not self.directory:  # User cancelled the dialog
                    logging.info("Directory selection cancelled. Aborting save.")
                    break
                
                if os.path.isdir(self.directory):
                    path = os.path.join(self.directory, f"{self.username}-data.json")
                    self._write_file(data, path)

                    logging.info(f"Successfully created {self.username}-data.json")
                    msgbox.showinfo(title=INFO_TITLE, message=f"{self.username}-data.json was created at: {path}")
                    break
                else:
                    if msgbox.askretrycancel(title=ERROR_TITLE, message=f"Invalid path!"):
                        pass
                    else:
                        break
            except PermissionError:
                logging.warning("Permission error.")
                if msgbox.askretrycancel(title=ERROR_TITLE, message=f"Invalid path!\nPermissionError!"):
                    pass
                else:
                    break
                logging.warning("Attempting alternative path.")

    def _write_file(self, data, path):
        with open(path, "w") as f:
            json.dump(data, f, indent=4)