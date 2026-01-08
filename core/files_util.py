import pandas as pd
from pathlib import Path
import PyPDF2, chardet, openpyxl


from .logger import get_logger
from .exception_handler import handle_exception

logger = get_logger(__name__)


# =========================
# CSV
# =========================
def read_csv(path: str):
    try:
        logger.info(f"CSV 読み込み: {path}")

        # まず文字コードを推定
        with open(path, "rb") as f:
            raw = f.read()
            enc = chardet.detect(raw)["encoding"]

        logger.info(f"推定文字コード: {enc}")

        return pd.read_csv(path, encoding=enc)
    except Exception as e:
        handle_exception(None, e, context=f"CSV読み込み失敗: {path}")
        raise


def write_csv(df, path: str):
    try:
        logger.info(f"CSV 書き込み: {path}")
        df.to_csv(path, index=False, encoding="utf-8")
    except Exception as e:
        handle_exception(None, e, context=f"CSV書き込み失敗: {path}")
        raise


# =========================
# Excel
# =========================
def read_excel(path: str, sheet_name=0):
    try:
        logger.info(f"Excel 読み込み: {path}")
        return pd.read_excel(path, sheet_name=sheet_name)
    except Exception as e:
        handle_exception(None, e, context=f"Excel読み込み失敗: {path}")
        raise


def write_excel(df, path: str, sheet_name="Sheet1"):
    try:
        logger.info(f"Excel 書き込み: {path}")
        df.to_excel(path, index=False, sheet_name=sheet_name)
    except Exception as e:
        handle_exception(None, e, context=f"Excel書き込み失敗: {path}")
        raise


# =========================
# PDF
# =========================
def read_pdf_text(path: str):
    try:
        logger.info(f"PDF 読み込み: {path}")
        text = ""
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        handle_exception(None, e, context=f"PDF読み込み失敗: {path}")
        raise