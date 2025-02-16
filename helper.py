import PyPDF2


def extract_text_from_pdf():
    with open("./resume.pdf", "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        # Loop through all the pages and extract text
        for page in reader.pages:
            text += page.extract_text()
    return text
