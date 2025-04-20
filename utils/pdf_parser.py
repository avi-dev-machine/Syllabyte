from PyPDF2 import PdfReader
import docx
import os

class DocumentParser:
    @staticmethod
    def parse_pdf(file_path):
        """Parse PDF file and return text content"""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return None

    @staticmethod
    def parse_docx(file_path):
        """Parse DOCX file and return text content"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            return None

    @staticmethod
    def parse_document(file_path):
        """Parse document based on file extension"""
        _, ext = os.path.splitext(file_path)
        if ext.lower() == '.pdf':
            return DocumentParser.parse_pdf(file_path)
        elif ext.lower() == '.docx':
            return DocumentParser.parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")