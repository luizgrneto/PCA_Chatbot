# ...existing code...
from PyPDF2 import PdfReader

def load_pdf(path):
    reader = PdfReader(path)
    texts = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(texts)