from constants import MSGBOX_ERROR_TITLE, MSGBOX_INFO_TITLE
import logging, os, sys, json, pprint, time
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
            if data == "[]":
                msgbox.showinfo(title=MSGBOX_INFO_TITLE, message="It appears as there is no information present\nThis may be due to the user having a private profile or it not existing.\n\nThis program will now terminate, sorry!\n\nIf you belive that this is false, retry then open an issue on GitHub\n'Akeoots/GitHub-Activity-Fetcher/issues'.")
        else:
            msgbox.showinfo(title=MSGBOX_INFO_TITLE, message="Some information may not be present as you have not entered an access token!")

        # Rate Limit Info Display
        msgbox.showinfo(title=MSGBOX_INFO_TITLE, message=f"Rate Limit information:\nRate Limit: {rate_limit} requests per hour\nRemaining Requests: {rate_remaining}\nRate Limit Reset at: {time.ctime(int(rate_reset)) if rate_reset.isdigit() else '?'}")

        logging.info("Successfully displayed data")
    
    def save(self, data):
        if msgbox.askyesno(title=MSGBOX_INFO_TITLE, message=f"Save as json?\n(will overwrite existing files with the same username!)") is False:
            return
        logging.debug("Attempting to save as JSON")

        try:
            self._write_file(data, f"{self.username}-data.json")

            msgbox.showinfo(title=MSGBOX_INFO_TITLE, message=f"Successfully created {self.username}-data.json")
            logging.info(f"Successfully created {self.username}-data.json")
        except PermissionError as e:
            logging.warning("Permission error.")
            
            if msgbox.askretrycancel(title=MSGBOX_ERROR_TITLE, message=f"You don't have the permission to write here.\n\n{type(e).__name__}:\n{e}") is False:
                sys.exit()
            logging.warning("Attempting alternative path.")
            self._prompt_alternate_path(data)

    def _write_file(self, data, path):
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
    
    def _prompt_alternate_path(self, data):
        while True:
            try:
                if msgbox.askokcancel(title=MSGBOX_INFO_TITLE, message=f"Enter an alternative directory or cancel."):
                    root = tk.Tk()
                    root.withdraw()  # Hide the main window
                    self.directory = filedialog.askdirectory(title="Select a directory")
                else:
                    logging.info("Cancelsed saving as JSON")
                    break

                if os.path.isdir(self.directory):
                    path = os.path.join(self.directory, f"{self.username}-data.json")
                    self._write_file(data, path)
                    
                    logging.info(f"Successfully created {self.username}-data.json")
                    msgbox.showinfo(title=MSGBOX_INFO_TITLE, message=f"{self.username}-data.json was created at: {path}")
                    break
                else:
                    msgbox.showerror(title=MSGBOX_ERROR_TITLE, message=f"Invalid path!")
            except PermissionError:
                logging.warning("Permission error.")