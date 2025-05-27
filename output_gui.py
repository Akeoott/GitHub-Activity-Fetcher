import logging, os, ctypes
from constants import ISSUE_INFO, WARNING_TITLE, ERROR_TITLE
import msg_handler # error handeler
import customtkinter as ctk
from tkinter import messagebox as msgbox
import sys
import tkinter as tk

import font_loader  # Loads font "self.roboto_font" and "self.roboto_title"

""" TEMPORARY! Will be used soon for good output display """

full_path = __file__
file_name = os.path.basename(full_path)

# Shit tkinter is complicated
class InputInterface(ctk.CTk):
    """
    A CustomTkinter GUI for displaying output from fetching GitHub activity.
    Allows users to view the data and save it.
    """
    def __init__(self):
        pass