"""Generate messages for the application."""

import sys

def error(text):
    print("***Error. %s" % text)
    sys.exit()

def warn(text, is_suppress_warnings=False):
    if not is_suppress_warnings:
        print("***Warning. %s" % text)
