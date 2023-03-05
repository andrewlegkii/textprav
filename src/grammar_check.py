import requests
import xml.etree.ElementTree as ET


def grammar_check(text):
    """
    Check the grammar of the given text using LanguageTool API.

    Args:
        text (str): The text to check.

    Returns:
        str: The text with grammar errors highlighted.
    """
    # LanguageTool API endpoint URL
    api_url = 'https://languagetool.org/api/v2/check'

    # Language to use for checking (Russian)
    language = 'ru'

    # Create the payload to send to the LanguageTool API
    payload = {
        'text': text,
        'language': language,
        'enabledOnly': 'false',
        'enabledRules': ''
    }

    # Send the request to the LanguageTool API
    response = requests.post(api_url, data=payload)

    # Parse the XML response
    root = ET.fromstring(response.content)
    errors = root.findall('.//error')

    # If there are no errors, return the original text
    if not errors:
        return text

    # Create a dictionary to store the error offsets and their corresponding messages
    error_dict = {}
    for error in errors:
        offset = int(error.attrib['offset'])
        length = int(error.attrib['length'])
        message = error.attrib['msg']
        error_dict[offset] = (length, message)

    # Create a new string with the errors highlighted
    new_text = ''
    last_index = 0
    for offset in sorted(error_dict.keys()):
        length, message = error_dict[offset]
        new_text += text[last_index:offset]
        new_text += f'[ERROR: {message}]'
        last_index = offset + length
    new_text += text[last_index:]

    return new_text
