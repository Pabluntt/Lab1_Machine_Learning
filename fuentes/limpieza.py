import re
import nltk
from nltk.corpus import stopwords

def _cargar_stopwords_es():
    try:
        return set(stopwords.words("spanish"))
    except LookupError:
        nltk.download("stopwords", quiet=True)
        try:
            return set(stopwords.words("spanish"))
        except LookupError:
            return set()


STOPWORDS_ES = _cargar_stopwords_es()

def limpiar_texto(texto):
    if texto is None:
        texto = ""

    texto = texto.lower()
    texto = re.sub(r"http\S+", " ", texto)
    texto = re.sub(r"@\w+", " ", texto)
    texto = re.sub(r"#", " ", texto)
    texto = re.sub(r"[^a-zA-Záéíóúñü\s]", " ", texto)

    tokens = [t for t in texto.split() if t not in STOPWORDS_ES]

    return " ".join(tokens)