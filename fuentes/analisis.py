from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def obtener_frecuencias(textos):
    return Counter(" ".join(textos).split())


def aplicar_tfidf(df):
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(df["texto_limpio"])
    return X, vectorizer


def aplicar_kmeans(X, df):
    k = 4 if len(df) >= 4 else max(1, len(df))

    modelo = KMeans(n_clusters=k, random_state=42, n_init=10)
    df["cluster"] = modelo.fit_predict(X)

    return df, modelo


def aplicar_pca(X, df):
    X_dense = X.toarray()

    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_dense)

    df["pca_1"] = X_pca[:, 0]
    df["pca_2"] = X_pca[:, 1]

    return df