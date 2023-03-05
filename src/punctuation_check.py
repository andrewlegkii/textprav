import re


def punctuation_check(text):
    result = re.sub(r'([а-яё]) ([,;:.!?])', r'\1\2', text)
    return result
