import os
import sys
import logging
import ctypes
import tkinter as tk
import tkinter.font as tkfont
import msg_handler
from constants import ISSUE_INFO, WARNING_TITLE
from tkinter import messagebox as msgbox

# --- Internal Helper Functions ---
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

# --- Public Font Loading Function ---
def load_application_font(font_path="assets/Roboto-VariableFont_wdth,wght.ttf"):
    """
    Loads a font from the given path for use in the application.
    Compatible with Windows, macOS, Linux, and PyInstaller.exe.
    This function should ideally be called once at application startup.

    Args:
        font_path: The relative path to the .ttf font file.
    Returns:
        True if font loaded successfully, False otherwise.
    """
    file_name = os.path.basename(__file__) # For error handling context

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
                e_type = "warning"
                context = f"Error occurred while loading font {font_path} on Windows."
                msg_handler.error_handeling(e, e_type, context, file_name)
                return False
        else:
            # For macOS and Linux, try to register font with Tkinter
            try:
                # Create a temporary Tkinter root to load the font
                root = tk.Tk()
                root.withdraw() # Hide the main window

                try:
                    tkfont.Font(root=root, family="Roboto", file=path) # Use 'family' instead of 'name' for actual font name    # type: ignore
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

# --- Global Flag for Font Loading Status ---
_font_loaded_successfully = False

# --- Automatic Font Loading on Module Import ---
# This ensures the font is loaded once when the module is first imported.
# You can customize the font path here if it's always the same.
if not _font_loaded_successfully:
    _font_loaded_successfully = load_application_font("assets/Roboto-VariableFont_wdth,wght.ttf")