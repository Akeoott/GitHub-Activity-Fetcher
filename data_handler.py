import logging, sys, os, json, pprint, time
from constants import ERROR_TITLE, INFO_TITLE
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox as msgbox
from tkinter import filedialog

import font_loader  # Loads font "self.roboto_font" and "self.roboto_title"

full_path = __file__
file_name = os.path.basename(full_path)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class DataHandler(ctk.CTk):
    """
    A CustomTkinter GUI for displaying output from fetching GitHub activity.
    Allows users to view the data and save it.
    """
    def __init__(self, username, data, limit, remaining, reset):
        super().__init__()
        self.username = username
        self.data = data
        pprint.pprint(self.data)
        self.limit = limit
        self.remaining = remaining
        self.reset = reset
        try:
            reset_time = time.ctime(int(self.reset)) if self.reset.isdigit() else "Unknown"
        except Exception as e:
            logging.warning(f"Failed to parse rate reset time: {e}")
            reset_time = "Unknown"
        rate_message = (
            f"Limit: {self.limit} requests/hour\n"
            f"Remaining: {self.remaining}\n"
            f"Resets at: {self.reset}"
        )
        ROBOTO_NORMAL_FONT_TUPLE = ("Roboto", 14)
        ROBOTO_TITLE_FONT_TUPLE = ("Roboto", 18, "bold")

        self.geometry("375x300")
        self.title("GitHub Activity Fetcher")

        self.container = ctk.CTkFrame(self)
        self.container.pack(pady=20, padx=60, fill="both", expand=True)

        self.page1 = ctk.CTkFrame(self.container)
        self.page1.pack(fill="both", expand=True)
        self.page2 = ctk.CTkFrame(self.container)
        self.page2.pack(fill="both", expand=True)

        # Page 1
        ctk.CTkLabel(self.page1, text="Rate Limit Information:", font=ROBOTO_TITLE_FONT_TUPLE).pack(pady=10)
        ctk.CTkLabel(
            self.page1,
            text=rate_message,
            font=ROBOTO_NORMAL_FONT_TUPLE,
            anchor="center",  # Center the widget in the frame
            justify="left"    # But keep the text left-aligned within the label
        ).pack(pady=10, anchor="center", fill="x")
        ctk.CTkButton(self.page1, text="Continue", command=self._save_page, font=ROBOTO_NORMAL_FONT_TUPLE).pack(pady=10)
        ctk.CTkButton(self.page1, text="Exit", command=self._exit, font=ROBOTO_NORMAL_FONT_TUPLE).pack(pady=10)

        # Page 2
        ctk.CTkLabel(self.page2, text="Save as JSON?", font=ROBOTO_TITLE_FONT_TUPLE).pack(pady=10)
        ctk.CTkLabel(self.page2, text="Will overwrite existing files,\nwith the same username!", font=ROBOTO_NORMAL_FONT_TUPLE).pack(pady=10)
        ctk.CTkButton(self.page2, text="Continue", command=self.save, font=ROBOTO_NORMAL_FONT_TUPLE).pack(pady=10)
        ctk.CTkButton(self.page2, text="Exit", command=self._exit, font=ROBOTO_NORMAL_FONT_TUPLE).pack(pady=10)

        self._show_page(self.page1)

    def _show_page(self, page):
        if page.winfo_ismapped():
            return
        # Hide all pages
        for p in [self.page1, self.page2]:
            p.pack_forget()
        # Show the selected one
        page.pack(fill="both", expand=True)
    
    def _exit(self):
        logging.info("User exited...")
        sys.exit()
        
    def _save_page(self):
        logging.info("Switched to saving")
        self._show_page(self.page2) 

    def save(self):
        self.destroy()
        logging.debug("Attempting to save as JSON")
        while True:
            try:
                root = tk.Tk()
                root.withdraw()  # Hide the main window
                self.directory = filedialog.askdirectory(title="Select a directory")
                if not self.directory:  # User cancelled the dialog
                    logging.info("Directory selection cancelled. Aborting save.")
                    sys.exit()
                
                if os.path.isdir(self.directory):
                    path = os.path.join(self.directory, f"{self.username}-data.json")
                    self._write_file(self.data, path)

                    logging.info(f"Successfully created {self.username}-data.json")
                    msgbox.showinfo(title=INFO_TITLE, message=f"{self.username}-data.json was created at: {path}")
                    logging.info("Exiting...")
                    sys.exit()
                else:
                    if msgbox.askretrycancel(title=ERROR_TITLE, message=f"Invalid path!"):
                        pass
                    else:
                        sys.exit()
            except PermissionError:
                logging.warning("Permission error.")
                if msgbox.askretrycancel(title=ERROR_TITLE, message=f"Invalid path!\nPermissionError!"):
                    pass
                else:
                    sys.exit()
                logging.warning("Attempting alternative path.")

    def _write_file(self, data, path):
        with open(path, "w") as f:
            json.dump(data, f, indent=4)