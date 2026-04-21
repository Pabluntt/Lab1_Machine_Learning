import re
from nltk.corpus import stopwords

STOPWORDS_ES = set(stopwords.words("spanish"))

def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"http\S+", " ", texto)
    texto = re.sub(r"@\w+", " ", texto)
    texto = re.sub(r"#", " ", texto)
    texto = re.sub(r"[^a-zA-Záéíóúñü\s]", " ", texto)

    tokens = [t for t in texto.split() if t not in STOPWORDS_ES]

    return " ".join(tokens)