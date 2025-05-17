import logging, os, ctypes
import customtkinter as ctk

def _load_font(font_path):
    FR_PRIVATE  = 0x10
    FR_NOT_ENUM = 0x20
    path = os.path.abspath(font_path)
    return ctypes.windll.gdi32.AddFontResourceExW(path, FR_PRIVATE, 0)

# Usage
_load_font("assets/Roboto-VariableFont_wdth,wght.ttf")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# Fuck tkinter
class InputInterface(ctk.CTk):
    # Persisted class variables
    fetch_type = 0
    username = ""
    useragent = ""
    token = ""
    repo = ""
    endpoint = ""

    def __init__(self):
        # Use class variables to persist data
        self.fetch_type = InputInterface.fetch_type
        self.username = InputInterface.username
        self.useragent = InputInterface.useragent
        self.token = InputInterface.token
        self.repo = InputInterface.repo
        self.endpoint = InputInterface.endpoint

        super().__init__()

        self.roboto_font = ("Roboto", 14)
        self.roboto_title = ("Roboto", 18, "bold")

        self.geometry("375x390")
        self.title("GitHub Activity Fetcher")

        # Container frame to apply padding once
        self.container = ctk.CTkFrame(self)
        self.container.pack(pady=20, padx=60, fill="both", expand=True)

        # Pages
        self.page1 = ctk.CTkFrame(self.container)
        self.page2 = ctk.CTkFrame(self.container)
        self.page3 = ctk.CTkFrame(self.container)
        self.page4 = ctk.CTkFrame(self.container)

        # Page 1 - Selection
        self.select_type = ctk.CTkLabel(self.page1, text="How do you want to fetch?", font=self.roboto_title)
        self.select_type.pack(pady=10)
        self.user_filter = ctk.CTkButton(self.page1, text="User Events", command=self._switch_user_input, font=self.roboto_font)
        self.user_filter.pack(pady=10)
        self.repo_filter = ctk.CTkButton(self.page1, text="Repo Specific User Events", command=self._switch_repo_input, font=self.roboto_font)
        self.repo_filter.pack(pady=10)

        # Page 2 - User Events
        ctk.CTkLabel(self.page2, text="User Events", font=self.roboto_title).pack(pady=10)

        self.username_user_entry = ctk.CTkEntry(self.page2, placeholder_text="Username*", font=self.roboto_font)
        self.username_user_entry.pack(pady=12, padx=10)

        self.useragent_user_entry = ctk.CTkEntry(self.page2, placeholder_text="Useragent*", font=self.roboto_font)
        self.useragent_user_entry.pack(pady=12, padx=10)

        self.token_user_entry = ctk.CTkEntry(self.page2, placeholder_text="Token (optional)", show="*", font=self.roboto_font)
        self.token_user_entry.pack(pady=12, padx=10)

        self.user_error_label = ctk.CTkLabel(self.page2, text="", text_color="red", font=self.roboto_font)
        self.user_error_label.pack(pady=(0, 5))

        ctk.CTkButton(self.page2, text="Fetch", font=self.roboto_font, command=self._fetch_user_events).pack(pady=10)

        # Page 3 - Repo Events
        ctk.CTkLabel(self.page3, text="Repo Events", font=self.roboto_title).pack(pady=10)

        self.username_repo_entry = ctk.CTkEntry(self.page3, placeholder_text="Username*", font=self.roboto_font)
        self.username_repo_entry.pack(pady=12, padx=10)

        self.useragent_repo_entry = ctk.CTkEntry(self.page3, placeholder_text="Useragent*", font=self.roboto_font)
        self.useragent_repo_entry.pack(pady=12, padx=10)

        self.token_repo_entry = ctk.CTkEntry(self.page3, placeholder_text="Token*", show="*", font=self.roboto_font)
        self.token_repo_entry.pack(pady=12, padx=10)

        self.repo_repo_entry = ctk.CTkEntry(self.page3, placeholder_text="Repository*", font=self.roboto_font)
        self.repo_repo_entry.pack(pady=12, padx=10)

        self.repo_error_label = ctk.CTkLabel(self.page3, text="", text_color="red", font=self.roboto_font)
        self.repo_error_label.pack(pady=(0, 5))

        ctk.CTkButton(self.page3, text="Fetch", command=self._fetch_repo_events, font=self.roboto_font).pack(pady=10)

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

    def _fetch_user_events(self):
        self.username = self.username_user_entry.get().strip()
        self.useragent = self.useragent_user_entry.get().strip()
        self.token = self.token_user_entry.get().strip()

        # Persist values to class variables
        InputInterface.fetch_type = self.fetch_type
        InputInterface.username = self.username
        InputInterface.useragent = self.useragent
        InputInterface.token = self.token
        InputInterface.repo = self.repo

        if not self.username or not self.useragent:
            self.user_error_label.configure(text="Username and Header are required.")
            return
        self.quit()
        self.prompt()

    def _fetch_repo_events(self):
        self.username = self.username_repo_entry.get().strip()
        self.useragent = self.useragent_repo_entry.get().strip()
        self.token = self.token_repo_entry.get().strip()
        self.repo = self.repo_repo_entry.get().strip()

        # Persist values to class variables
        InputInterface.fetch_type = self.fetch_type
        InputInterface.username = self.username
        InputInterface.useragent = self.useragent
        InputInterface.token = self.token
        InputInterface.repo = self.repo

        if not self.username or not self.useragent or not self.token or not self.repo:
            self.repo_error_label.configure(text="Its required to fill out every field.")
            return
        self.quit()
        self.prompt()

    def prompt(self):
        logging.debug(f"Fetch type: {self.fetch_type}")
        endpoint = None
        if self.fetch_type == 1:
            endpoint = f'https://api.github.com/users/{self.username}/events'
        elif self.fetch_type == 2:
            endpoint = f'https://api.github.com/repos/{self.username}/{self.repo}/events'
        elif self.fetch_type == 0:
            logging.warning("Passed endpoint due to fetch type being 0")
            self.destroy
        
        self.endpoint = endpoint

        logging.debug(
            f"Returning to main:\n"
            f"endpoint: {self.endpoint}\n"
            f"username: {self.username}\n"
            f"useragent: {self.useragent}\n"
            f"token: {'[Hidden Token]' if self.token else '[No token]'}\n"
            f"repo: {self.repo if self.repo else '[No repo]'}"
        )

        return self.endpoint, self.username, self.useragent, self.token, self.repo
    
app = InputInterface()
app.mainloop()