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
    temp_data = []  # Temporary storage for 10 rows before summing
    result_sum = 0  # Initialize a variable to store the sum of the "Result" column
    sum_index = 0  # Index to track when to add the sum

    def parse_percentage(value):
        """Converts percentage strings like '6%' to a decimal float (e.g., 6% -> 0.06)."""
        try:
            return float(value.replace('%', '')) / 100
        except ValueError:
            return 0.0  # If the value is not a valid percentage, return 0.0

    # Skip the first line of matches, as it's not part of the data
    matches = matches[1:]

    for match in matches:
        row = {
            "Index": int(match[0]),  # Capture the first number as "Index"
            "Result": float(match[1]),  # Capture the result (second column)
            "Time": float(match[2]),  # Capture the time (third column)
            "6a0": parse_percentage(match[3]),  # Convert 6a0 percentage
            "9a0": parse_percentage(match[4]),  # Convert 9a0 percentage
            "10.0": parse_percentage(match[5]),  # Convert 10.0 percentage
            "10.5": parse_percentage(match[6]),  # Convert 10.5 percentage
            "10a0": parse_percentage(match[7]),  # Convert 10a0 percentage
            "10a5": parse_percentage(match[8]),  # Convert 10a5 percentage
            "mm/s": parse_percentage(match[9]),  # Convert mm/s percentage
            "mm/s/250ms": float(match[10]),  # Capture mm/s/250ms value
        }

        # Add the current result to the sum (only the integer part of Result)
        result_sum += int(row["Result"])

        # Append row to temporary data list
        temp_data.append(row)

        # Every 10th index, add the sum and reset the sum for the next 10 rows
        if row["Index"] % 10 == 0:
            sum_row = {
                "Index": f"Sum_{row['Index']}",  # Indicate this is the sum row
                "Result": result_sum,  # Store the sum of the "Result" column (integer part only)
                "Time": "",
                "6a0": "",
                "9a0": "",
                "10.0": "",
                "10.5": "",
                "10a0": "",
                "10a5": "",
                "mm/s": "",
                "mm/s/250ms": "",
            }
            data.extend(temp_data)  # Add the accumulated rows
            data.append(sum_row)  # Add the sum row
            temp_data = []  # Reset the temporary data
            result_sum = 0  # Reset the sum for the next set of 10 rows

    # Add any remaining rows if they exist (in case the total number of rows isn't a multiple of 10)
    if temp_data:
        data.extend(temp_data)

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
