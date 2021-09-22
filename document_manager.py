from docx import Document
import PyPDF2


class DocumentManager:

    def doc_text(self, file):
        doc = Document(file)
        doc_paragraphs = [para.text for para in doc.paragraphs]
        doc_text = '\n'.join(doc_paragraphs)
        return doc_text

    def pdf_text(self, file):
        pdf_text = ""
        pdf_file = open(file, "rb")
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        num_of_pages = read_pdf.getNumPages()

        for page_num in range(num_of_pages):
            page = read_pdf.getPage(page_num)
            pdf_text += page.extractText()
        return pdf_text

    def txt_text(self, file):
        with open(file) as f:
            lines = f.readlines()
            text = '\n'.join(lines)
            return text
