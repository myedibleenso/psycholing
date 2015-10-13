import re

def get_lines(storageObj):
    return storageObj.read().split()

def clean_line(line):
    return [re.sub("\n\r", "", r).lower() for r in line.split(",")]
