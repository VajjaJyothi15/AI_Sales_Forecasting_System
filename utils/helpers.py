import pandas as pd

from utils.column_mapper import standardize_columns


def load_csv(file):
    encodings = ("utf-8-sig", "utf-8", "cp1252", "latin1")
    last_error = None

    for encoding in encodings:
        try:
            if hasattr(file, "seek"):
                file.seek(0)
            return pd.read_csv(
                file,
                encoding=encoding,
                sep=None,
                engine="python"
            )
        except (UnicodeDecodeError, UnicodeError) as exc:
            last_error = exc
        except pd.errors.ParserError as exc:
            last_error = exc

    try:
        if hasattr(file, "seek"):
            file.seek(0)
        return pd.read_csv(
            file,
            encoding="utf-8",
            encoding_errors="replace",
            sep=None,
            engine="python"
        )
    except Exception as exc:
        raise ValueError(f"Unable to read CSV file: {last_error or exc}") from exc


def load_excel(file):
    if hasattr(file, "seek"):
        file.seek(0)
    return pd.read_excel(file)


def load_dataset(file):
    filename = getattr(file, "name", "").lower()

    if filename.endswith((".xlsx", ".xls")):
        return standardize_columns(load_excel(file))

    if filename.endswith(".csv"):
        return standardize_columns(load_csv(file))

    try:
        return standardize_columns(load_csv(file))
    except Exception:
        return standardize_columns(load_excel(file))
