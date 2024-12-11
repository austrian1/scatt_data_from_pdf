import re
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    :param pdf_path: Path to the PDF file.
    :return: A string containing all the text from the PDF.
    """
    # Initialize reader
    reader = PdfReader(pdf_path)
    extracted_text = ""

    # Iterate through pages and extract text
    for page in reader.pages:
        extracted_text += page.extract_text() + "\n"  # Adding newline for separation
    return extracted_text

def parse_extracted_text(text):
    """
    Parses the extracted text and converts it into a structured format.
    :param text: Extracted text from the PDF.
    :return: A list of dictionaries containing parsed data.
    """
    # Define a pattern to extract rows of data
    pattern = r"(\d+)\s([\d.]+)\s([\d.]+)\s([\d%]+)\s([\d%]+)\s([\d%]+)\s([\d%]+)\s([\d%]+)\s([\d%]+)\s([\d.]+)\s([\d.]+)\s([\d.]+)"

    # Find all matches
    matches = re.findall(pattern, text)

    # Convert matches to structured format
    data = []
    for match in matches:
        row = {
            "Result": int(match[0]),
            "Time": float(match[1]),
            "6a0": float(match[2]),
            "9a0": match[3],
            "10.0": match[4],
            "10.5": match[5],
            "10a0": match[6],
            "10a5": match[7],
            "mm/s": match[8],
            "mm/s/250ms": float(match[9]),
        }
        data.append(row)
    return data

def main():
    # Path to your PDF file
    pdf_path = "C:/Users/panos/Documents/projects/python_projects/50ari.pdf"

    # Step 1: Extract text from the PDF
    extracted_text = extract_text_from_pdf(pdf_path)
    print("Extracted Text:")
    print(extracted_text)

    # Step 2: Parse the extracted text
    structured_data = parse_extracted_text(extracted_text)
    
    # Step 3: Print the structured data
    print("\nParsed Data:")
    for row in structured_data:
        print(row)

if __name__ == "__main__":
    main()
