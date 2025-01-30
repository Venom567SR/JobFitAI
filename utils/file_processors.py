import PyPDF2 as pdf
import docx
import io

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

def input_word_text(uploaded_file):
    doc = docx.Document(uploaded_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def read_file_text(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        return input_pdf_text(uploaded_file)
    elif uploaded_file.name.endswith(('.docx', '.doc')):
        return input_word_text(uploaded_file)
    else:
        raise ValueError("Unsupported file format. Please upload PDF or Word documents.")
