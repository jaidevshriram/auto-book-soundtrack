import re

def lower_text(x):
    return x.lower()

def remove_extra_whitespace(x):
    return ' '.join(x.split())

def remove_punctuation(x):
    return re.sub(r'[^\w\s]', '', x)