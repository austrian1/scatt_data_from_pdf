import PyPDF2

def read_pdf(file_path):
    """
    Reads text from a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    extracted_text = ""
    
    try:
        # Open the PDF file in binary read mode
        with open(file_path, 'rb') as pdf_file:
            # Create a PDF Reader object
            reader = PyPDF2.PdfReader(pdf_file)

            # Iterate through each page and extract text
            for page_num, page in enumerate(reader.pages):
                extracted_text += f"\n[Page {page_num + 1}]\n"
                extracted_text += page.extract_text()

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return extracted_text

if __name__ == "__main__":
    # Example usage
    #file_path = input("Enter the path to the PDF file: ")
    text = read_pdf("C:/Users/panos/Documents/projects/python_projects/scatt_data2/analysis_results.pdf")
    
    if text:
        print("\nExtracted text from the PDF:\n")
        print(text)
    else:
        print("No text could be extracted.")