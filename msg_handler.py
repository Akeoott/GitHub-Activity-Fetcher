import logging, sys, traceback
from constants import INFO_TITLE, WARNING_TITLE, ERROR_TITLE, ISSUE_INFO_HTML
from tkinter import messagebox
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt # Import Qt for the TextFormat enum

def error_display(e: Exception, e_type: str, location: str, context: str):

    e_type = e_type.capitalize()

    if location is None:
        logging.warning("No location provided")
        location = "No location provided"
    if context is None:
        logging.warning("No context provided")
        context = "No context provided"

    if e_type == "Info":
        title = INFO_TITLE
        continue_pg = True
    elif e_type == "Warning":
        title = WARNING_TITLE
        continue_pg = True
    elif e_type == "Error":
        title = ERROR_TITLE
        continue_pg = False
    else:
        logging.warning("e_type not recognized")
        title = "ERROR (Could not retrive title)"
        continue_pg = False
        messagebox.showerror(title="ERROR", message=f"Line 28 - e_type not recognized\n\nPlease open an issue on GitHub:\n'Akeoots/GitHub-Activity-Fetcher/issues'")

    app = QApplication(sys.argv)

    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)

    # Use HTML tags for formatting
    message_text = (
        f"<h3>An <span style='color:red;'>{e_type}</span> has ocurred</h3>"
        "Context:<br>"
        f"{context}"
    )
    msg_box.setText(message_text)

    # Corrected line: Use Qt.RichText
    msg_box.setTextFormat(Qt.RichText)  # type: ignore

    # Optional: Add informative text and detailed text
    msg_box.setInformativeText(ISSUE_INFO_HTML)
    msg_box.setDetailedText(f"{type(e).__name__}\n{location}\n\nError:\n{e}")

    if e_type == "Info":
        msg_box.setIcon(QMessageBox.Information)
    elif e_type == "Warning":
        msg_box.setIcon(QMessageBox.Warning)
    elif e_type == "Error":
        msg_box.setIcon(QMessageBox.Critical)
    else:
        msg_box.setIcon(QMessageBox.Information)

    if continue_pg:
        msg_box.setStandardButtons(QMessageBox.Ignore | QMessageBox.Close)
    else:
        msg_box.setStandardButtons(QMessageBox.Close)

    # Show the message box and get the result
    result = msg_box.exec_()

    if result == QMessageBox.Ignore:
        pass
    else:
        sys.exit()

def error_handeling(e: Exception, e_type: str, context: str, file_name: str):
    # First two variables needed to reach 'exc_traceback'
    exc_type, exc_value, exc_traceback = sys.exc_info()
    frames = traceback.extract_tb(exc_traceback)
    try:
        last_frame = frames[-1]
        location: str = f"Line: {last_frame.lineno}\nFile: {file_name}\nFunction: {last_frame.name}"
        # Logging is here
        logging.error(f"An {type(e).__name__} happened unexpectedly. {location}")
        error_display(e=e, e_type=e_type, location=location, context=context)
    except IndexError as e:
        logging.critical(f"An {type(e).__name__} ocurred. {e}")
        app = QApplication(sys.argv)
        msg_box = QMessageBox()
        msg_box.setWindowTitle(ERROR_TITLE)
        msg_box.setIcon(QMessageBox.Critical)
        message_text = (
            f"<h3>An <span style='color:red;'>critical error</span> has ocurred</h3>"
            "Please activate logging, repeat what you did and open an issue on GitHub<br>'Akeoottt/GitHub-Activity-Fetcher/issues<br>"
            "Context:<br>"
            f"{e}"
        )
        msg_box.setText(message_text)
        msg_box.setTextFormat(Qt.RichText)  # type: ignore
        msg_box.setStandardButtons(QMessageBox.Close)
        msg_box.exec_()
        sys.exit()