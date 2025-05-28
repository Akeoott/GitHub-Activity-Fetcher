import logging, os
from constants import ISSUE_INFO, WARNING_TITLE
import customtkinter as ctk

import font_loader  # Loads font "self.roboto_font" and "self.roboto_title"

full_path = __file__
file_name = os.path.basename(full_path)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Shit tkinter is complicated
class InputInterface(ctk.CTk):
    """
    A CustomTkinter GUI for obtaining user inputs for fetching GitHub activity.
    Allows users to choose between fetching general user events or repository-specific user events.
    """
    def __init__(self):
        """Initializes the main application window and its components."""
        super().__init__()
        # Instance variables to store the results
        self.fetch_type_val = 0
        self.username_val = ""
        self.useragent_val = ""
        self.token_val = ""
        self.repo_val = ""
        self.endpoint_val = ""
        self.data_ready = False # Flag to indicate if data is ready

        # In a fonts.py or similar module
        ROBOTO_NORMAL_FONT_TUPLE = ("Roboto", 14)
        ROBOTO_TITLE_FONT_TUPLE = ("Roboto", 18, "bold")

        self.geometry("375x390")
        self.title("GitHub Activity Fetcher")

        # Container frame to apply padding once
        self.container = ctk.CTkFrame(self)
        self.container.pack(pady=20, padx=60, fill="both", expand=True)

        # Pages
        self.page1 = ctk.CTkFrame(self.container)
        self.page2 = ctk.CTkFrame(self.container)
        self.page3 = ctk.CTkFrame(self.container)

        # Page 1 - Selection
        self.select_type = ctk.CTkLabel(self.page1, text="How do you want to fetch?", font=ROBOTO_TITLE_FONT_TUPLE)
        self.select_type.pack(pady=10)
        self.user_filter = ctk.CTkButton(self.page1, text="User Events", command=self._switch_user_input, font=ROBOTO_NORMAL_FONT_TUPLE)
        self.user_filter.pack(pady=10)
        self.repo_filter = ctk.CTkButton(self.page1, text="Repo Specific User Events", command=self._switch_repo_input, font=ROBOTO_NORMAL_FONT_TUPLE)
        self.repo_filter.pack(pady=10)

        # Page 2 - User Events
        ctk.CTkLabel(self.page2, text="User Events", font=ROBOTO_TITLE_FONT_TUPLE).pack(pady=10)

        self.username_user_entry = ctk.CTkEntry(self.page2, placeholder_text="Username*", font=ROBOTO_NORMAL_FONT_TUPLE)
        self.username_user_entry.pack(pady=12, padx=10)

        self.useragent_user_entry = ctk.CTkEntry(self.page2, placeholder_text="Useragent*", font=ROBOTO_NORMAL_FONT_TUPLE)
        self.useragent_user_entry.pack(pady=12, padx=10)

        self.token_user_entry = ctk.CTkEntry(self.page2, placeholder_text="Token (optional)", show="*", font=ROBOTO_NORMAL_FONT_TUPLE)
        self.token_user_entry.pack(pady=12, padx=10)

        self.user_error_label = ctk.CTkLabel(self.page2, text="", text_color="red", font=ROBOTO_NORMAL_FONT_TUPLE)
        self.user_error_label.pack(pady=(0, 5))

        ctk.CTkButton(self.page2, text="Fetch", font=ROBOTO_NORMAL_FONT_TUPLE, command=self._fetch_user_events).pack(pady=10)

        # Page 3 - Repo Events
        ctk.CTkLabel(self.page3, text="Repo Events", font=ROBOTO_TITLE_FONT_TUPLE).pack(pady=10)

        self.username_repo_entry = ctk.CTkEntry(self.page3, placeholder_text="Username*", font=ROBOTO_NORMAL_FONT_TUPLE)
        self.username_repo_entry.pack(pady=12, padx=10)

        self.useragent_repo_entry = ctk.CTkEntry(self.page3, placeholder_text="Useragent*", font=ROBOTO_NORMAL_FONT_TUPLE)
        self.useragent_repo_entry.pack(pady=12, padx=10)

        self.token_repo_entry = ctk.CTkEntry(self.page3, placeholder_text="Token*", show="*", font=ROBOTO_NORMAL_FONT_TUPLE)
        self.token_repo_entry.pack(pady=12, padx=10)

        self.repo_repo_entry = ctk.CTkEntry(self.page3, placeholder_text="Repository*", font=ROBOTO_NORMAL_FONT_TUPLE)
        self.repo_repo_entry.pack(pady=12, padx=10)

        self.repo_error_label = ctk.CTkLabel(self.page3, text="", text_color="red", font=ROBOTO_NORMAL_FONT_TUPLE)
        self.repo_error_label.pack(pady=(0, 5))

        ctk.CTkButton(self.page3, text="Fetch", command=self._fetch_repo_events, font=ROBOTO_NORMAL_FONT_TUPLE).pack(pady=10)

        self._show_page(self.page1)

    def _show_page(self, page):
        if page.winfo_ismapped():
            return
        # Hide all pages
        for p in [self.page1, self.page2, self.page3]:
            p.pack_forget()
        # Show the selected one
        page.pack(fill="both", expand=True)

    def _switch_user_input(self):
        logging.info("Switched to user input")
        self.fetch_type = 1
        logging.debug(f"Fetch type: {self.fetch_type}")
        self._show_page(self.page2)

    def _switch_repo_input(self):
        logging.info("Switched to repo input")
        self.fetch_type = 2
        logging.debug(f"Fetch type: {self.fetch_type}")
        self._show_page(self.page3)

    def _validate_and_store_user_events(self):
        username = self.username_user_entry.get().strip()
        useragent = self.useragent_user_entry.get().strip()
        token = self.token_user_entry.get().strip()

        if not username or not useragent:
            self.user_error_label.configure(text="Username and Useragent are required.")
            return False

        self.username_val = username
        self.useragent_val = useragent
        self.token_val = token
        self.fetch_type_val = 1
        self.repo_val = "" # Ensure repo is cleared for user events
        self.user_error_label.configure(text="") # Clear error
        return True

    def _fetch_user_events(self):
        if self._validate_and_store_user_events():
            self.data_ready = True
            self.destroy() # Close the window, mainloop will exit

    def _validate_and_store_repo_events(self):
        username = self.username_repo_entry.get().strip()
        useragent = self.useragent_repo_entry.get().strip()
        token = self.token_repo_entry.get().strip()
        repo = self.repo_repo_entry.get().strip()

        if not username or not useragent or not token or not repo:
            self.repo_error_label.configure(text="All fields are required for repo events.")
            return False

        self.username_val = username
        self.useragent_val = useragent
        self.token_val = token
        self.repo_val = repo
        self.fetch_type_val = 2
        self.repo_error_label.configure(text="") # Clear error
        return True

    def _fetch_repo_events(self):
        if self._validate_and_store_repo_events():
            self.data_ready = True
            self.destroy() # Close the window, mainloop will exit

    def get_inputs(self):
        """
        Displays the GUI and waits for user input.
        Returns the collected inputs after the user submits the form or closes the window.
        Returns:
            A tuple containing: (endpoint, username, useragent, token, repo).
            Endpoint can be None if inputs are not successfully gathered.
        """
        self.mainloop() # Start the GUI interaction

        # This part executes after self.destroy() is called
        if not self.data_ready: # If window was closed without pressing Fetch
            logging.info("GUI closed without providing input.")
            return None, None, None, None, None

        endpoint = None
        if self.fetch_type_val == 1:
            endpoint = f'https://api.github.com/users/{self.username_val}/events'
        elif self.fetch_type_val == 2:
            endpoint = f'https://api.github.com/repos/{self.username_val}/{self.repo_val}/events'

        logging.debug(
            f"Returning from GUI:\n"
            f"endpoint: {endpoint}\n"
            f"username: {self.username_val}\n"
            f"useragent: {self.useragent_val}\n"
            f"token: {'[Hidden Token]' if self.token_val else '[No token]'}\n"
            f"repo: {self.repo_val if self.repo_val else '[No repo]'}"
        )
        return endpoint, self.username_val, self.useragent_val, self.token_val, self.repo_val

# For testing standalone
if False:
    if __name__ == "__main__":
        logging.basicConfig(level=logging.DEBUG) # Add basic logging for standalone test
        gui = InputInterface()
        endpoint, username, useragent, token, repo = gui.get_inputs() # Using the refactored approach
        if endpoint:
            print("Data obtained from GUI:")
            print(f"  Endpoint: {endpoint}")
            print(f"  Username: {username}")
            print(f"  Useragent: {useragent}")
            print(f"  Token: {'Present' if token else 'Not Present'}")
            print(f"  Repository: {repo if repo else 'N/A'}")
        else:
            print("GUI was closed without submitting data.")