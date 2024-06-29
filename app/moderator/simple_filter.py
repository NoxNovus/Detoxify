import re

DEFAULT_SWEAR_WORDS = ["diff"]

def censor_target_words(text, target_words):
    """
    Replaces target words in the text with asterisks.

    Parameters:
    text (str): The input text to be censored.
    target_words (list): A list of target words to be censored.

    Returns:
    str: The censored text.
    """
    def replace_with_asterisks(match):
        word = match.group()
        return '*' * len(word)

    pattern = re.compile('|'.join(map(re.escape, target_words)), re.IGNORECASE)
    censored_text = pattern.sub(replace_with_asterisks, text)

    return censored_text
