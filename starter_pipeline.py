from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv


def _pick_first_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Return the first matching column name from a list of candidates."""
    normalized = {str(col).strip().lower(): col for col in df.columns}
    for candidate in candidates:
        col = normalized.get(candidate.lower())
        if col is not None:
            return str(col)
    return None


def read_csv_flexible(csv_path: Path) -> pd.DataFrame:
    """Read CSV trying common encodings to avoid startup friction."""
    last_error: Exception | None = None
    for encoding in ("utf-8", "latin-1", "utf-8-sig"):
        try:
            return pd.read_csv(csv_path, encoding=encoding)
        except Exception as exc:  # noqa: BLE001
            last_error = exc
    raise RuntimeError(f"No se pudo leer el CSV: {csv_path}") from last_error


def standardize_minimum_schema(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    """Map source columns to the minimum schema required by the lab."""
    text_col = _pick_first_column(
        df,
        [
            "texto",
            "text",
            "contenido",
            "caption",
            "description",
            "descripcion",
            "title",
            "titulo",
            "summary",
            "resumen",
        ],
    )
    if text_col is None:
        raise ValueError(
            "No encontre una columna de texto. "
            "Prueba con: texto, text, contenido, caption, description, title."
        )

    id_col = _pick_first_column(df, ["id", "tweet_id", "post_id", "uuid"])
    date_col = _pick_first_column(df, ["fecha", "date", "created_at", "published"])
    url_col = _pick_first_column(df, ["url", "link", "enlace"])

    out = pd.DataFrame()
    if id_col is not None:
        out["id"] = df[id_col].astype(str)
    else:
        out["id"] = [f"row_{i}" for i in range(1, len(df) + 1)]

    out["fuente"] = source_name
    out["texto"] = df[text_col].astype(str).str.strip()

    if date_col is not None:
        out["fecha"] = df[date_col].astype(str)
    if url_col is not None:
        out["url"] = df[url_col].astype(str)

    out = out[out["texto"].notna() & (out["texto"] != "")]
    out = out.drop_duplicates(subset=["texto"]).reset_index(drop=True)
    return out


def save_corpus(df: pd.DataFrame, parquet_path: Path, pickle_path: Path) -> None:
    """Save to Pickle always and to Parquet when available."""
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    pickle_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_pickle(pickle_path)
    try:
        df.to_parquet(parquet_path, index=False)
        print(f"[OK] Parquet guardado en: {parquet_path}")
    except Exception as exc:  # noqa: BLE001
        print(f"[WARN] No se pudo guardar Parquet: {exc}")

    print(f"[OK] Pickle guardado en: {pickle_path}")


def _to_abs(project_root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return project_root / path


def main() -> None:
    load_dotenv()

    project_root = Path(__file__).resolve().parent
    csv_input = _to_abs(
        project_root,
        os.getenv("CSV_INPUT_PATH", "data/raw/fuente_opcional.csv"),
    )
    source_name = os.getenv("CSV_SOURCE_NAME", "csv_opcional")
    parquet_output = _to_abs(
        project_root,
        os.getenv("PARQUET_OUTPUT_NAME", "data/processed/corpus.parquet"),
    )
    pickle_output = _to_abs(
        project_root,
        os.getenv("PICKLE_OUTPUT_NAME", "data/processed/corpus.pkl"),
    )

    if not csv_input.exists():
        print("[INFO] No se encontro el CSV de entrada.")
        print(f"       Ruta esperada: {csv_input}")
        print("       Puedes editar CSV_INPUT_PATH en .env y volver a ejecutar.")
        return

    raw_df = read_csv_flexible(csv_input)
    corpus_df = standardize_minimum_schema(raw_df, source_name)

    save_corpus(corpus_df, parquet_output, pickle_output)
    print(f"[OK] Filas finales en el corpus: {len(corpus_df)}")
    print("[OK] Esquema final:", list(corpus_df.columns))


if __name__ == "__main__":
    main()
