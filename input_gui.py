import logging, os, ctypes
from constants import ISSUE_INFO, WARNING_TITLE, ERROR_TITLE
import msg_handler # error handeler
import customtkinter as ctk
from tkinter import messagebox as msgbox
import sys
import tkinter as tk

full_path = __file__
file_name = os.path.basename(full_path)

def _resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller .exe.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS    # type: ignore
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def _load_font(font_path):
    """
    Loads a font from the given path for use in the application.
    Compatible with Windows, macOS, Linux, and PyInstaller.exe.
    Args:
        font_path: The relative path to the .ttf font file.
    Returns:
        True if font loaded successfully, False otherwise.
    """
    path = _resource_path(font_path)
    if not os.path.exists(path):
        logging.warning(f"Font file not found: {font_path}")
        e_type = "warning"
        context = f"Font file not found: {font_path}. Reinstalling the program is recommended."
        msg_handler.error_handeling(FileNotFoundError(font_path), e_type, context, file_name)
        return False

    try:
        if sys.platform.startswith("win"):
            try:
                FR_PRIVATE = 0x10
                result = ctypes.windll.gdi32.AddFontResourceExW(path, FR_PRIVATE, 0)
                if result == 0:
                    logging.warning(f"Failed to load font: {font_path}. AddFontResourceExW returned 0.")
                    msgbox.showwarning(title=WARNING_TITLE, message=f"Failed to load font: {font_path}\n\nPlease retry or reinstall this program{ISSUE_INFO}\n\nTHIS PROGRAM WILL ATTEMPT TO CONTINUE!")
                    return False
                else:
                    logging.info(f"Successfully loaded font: {font_path}")
                    return True
            except Exception as e:
                logging.error(f"Error loading font on Windows: {e}")
                e_type = "error"
                context = f"Error occurred while loading font {font_path} on Windows."
                msg_handler.error_handeling(e, e_type, context, file_name)
                return False
        else:
            # For macOS and Linux, try to register font with Tkinter
            try:
                import tkinter.font as tkfont
                root = tk.Tk()
                root.withdraw()
                try:
                    tkfont.Font(root=root, name="Roboto", file=path)    # type: ignore
                    logging.info(f"Successfully loaded font: {font_path}")
                    root.destroy()
                    return True
                except tkfont.TclError as e:    # type: ignore
                    logging.warning(f"TclError registering font with Tkinter: {e}")
                    e_type = "warning"
                    context = f"TclError occurred while registering font {font_path} with Tkinter."
                    msg_handler.error_handeling(e, e_type, context, file_name)
                    root.destroy()
                    return False
                except Exception as e:
                    logging.warning(f"Unexpected error registering font with Tkinter: {e}")
                    e_type = "warning"
                    context = f"Unexpected error occurred while registering font {font_path} with Tkinter."
                    msg_handler.error_handeling(e, e_type, context, file_name)
                    root.destroy()
                    return False
            except ImportError as e:
                logging.warning(f"tkinter.font could not be imported: {e}")
                e_type = "warning"
                context = f"tkinter.font could not be imported while loading font<br>{font_path}."
                msg_handler.error_handeling(e, e_type, context, file_name)
                return False
    except Exception as e:
        logging.warning(f"Error loading font: {font_path} - {e}")
        e_type = "warning"
        context = f"A {type(e).__name__} unexpectedly occurred.<br>Error loading font {font_path}"
        msg_handler.error_handeling(e, e_type, context, file_name)
    return False

_load_font("assets/Roboto-VariableFont_wdth,wght.ttf")

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