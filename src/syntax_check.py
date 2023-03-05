import nltk


def check_syntax(text):
    """
    Проверяет синтаксическую корректность текста.

    :param text: str, текст для проверки
    :return: list, список предложений с синтаксическими ошибками
    """
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    sentences = nltk.sent_tokenize(text)
    errors = []
    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        grammar = "NP: {<DT>?<JJ>*<NN>}"
        cp = nltk.RegexpParser(grammar)
        tree = cp.parse(tagged)
        for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
            if len(subtree.leaves()) < 3:
                errors.append(sentence)
    return errors
