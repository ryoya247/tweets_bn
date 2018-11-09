import unicodedata
import string

def format_text(text):
    text = unicodedata.normalize("NFKC", text)

    table = str.maketrans("", "", string.punctuation  + "「」、。・")
    text = text.translate(table)

    return text
