from core.files_util import (
    read_csv, write_csv,
    read_excel, write_excel,
    read_pdf_text
)
from core.logger import get_logger

logger = get_logger(__name__)

def test_csv():
    logger.info("=== CSV テスト開始 ===")
    df = read_csv("samples/sample.csv")
    logger.info(f"CSV 読み込み成功: {len(df)} 行")
    write_csv(df, "samples/output.csv")
    logger.info("CSV 書き込み成功")

def test_excel():
    logger.info("=== Excel テスト開始 ===")
    df = read_excel("samples/sample.xlsx")
    logger.info(f"Excel 読み込み成功: {len(df)} 行")
    write_excel(df, "samples/output.xlsx")
    logger.info("Excel 書き込み成功")

def test_pdf():
    logger.info("=== PDF テスト開始 ===")
    text = read_pdf_text("samples/sample.pdf")
    logger.info(f"PDF 読み込み成功（先頭200文字）:\n{text[:200]}")

if __name__ == "__main__":
    test_csv()
    test_excel()
    test_pdf()