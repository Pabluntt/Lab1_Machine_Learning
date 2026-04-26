import re
import html
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

RUIDO_HTML = {
    "strong",
    "em",
    "div",
    "span",
    "link",
    "href",
    "rel",
    "target",
    "blank",
    "class",
    "style",
    "title",
    "html",
    "body",
    "head",
    "meta",
    "script",
    "iframe",
    "blockquote",
    "br",
    "li",
    "ul",
    "ol",
    "svg",
    "path",
    "viewbox",
    "nbsp",
    "quot",
    "amp",
    "lt",
    "gt",
    "src",
    "img",
    "http",
    "https",
    "www",
    "com",
}

def limpiar_texto(texto):
    if texto is None:
        texto = ""

    texto = html.unescape(str(texto))
    texto = texto.lower()
    texto = re.sub(r"<[^>]+>", " ", texto)
    texto = re.sub(r"&[a-zA-Z]+;", " ", texto)
    texto = re.sub(r"http\S+", " ", texto)
    texto = re.sub(r"@\w+", " ", texto)
    texto = re.sub(r"#", " ", texto)
    texto = re.sub(r"[^a-zA-Záéíóúñü\s]", " ", texto)

    tokens = [
        t
        for t in texto.split()
        if t not in STOPWORDS_ES
        and t not in RUIDO_HTML
        and len(t) > 2
    ]

    return " ".join(tokens)