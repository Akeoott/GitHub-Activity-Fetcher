IMPORTANT!
    After EVERY new release, UPDATE 'version.txt' AND 'constants.py'!

Library info:
    libraries used:
        functional:
            os
            sys
            time
            json
            logging
            requests
        visual:
            pprint
            ctypes
            tkinter
            customtkinter

pyinstaller info:
    If you turn main to an exe file
        Use 'pyinstaller main.spec' for release!
        Use 'pyinstaller main_test.spec' for testing/debugging!

        This is because dependencies the program requires have to be installed

File signing:
    I have no Code Signing Certificate BUT I have a Self-Signed Cert
        This will be used for every release for now