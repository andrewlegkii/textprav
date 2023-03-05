import pymorphy2


def spell_check(text):
    morph = pymorphy2.MorphAnalyzer()
    words = text.split()
    corrected_words = []
    for word in words:
        parsed_word = morph.parse(word)[0]
        if parsed_word.tag.POS is not None and 'LATN' not in parsed_word.tag:
            corrected_words.append(parsed_word.normal_form)
        else:
            corrected_words.append(word)
    result = ' '.join(corrected_words)
    return result
