import re
import PyPDF2

def extract_product_ids_from_pdf(pdf_path):
    product_ids = []
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        # Iterate through each page
        for page in reader.pages:
            text = page.extract_text()
            # Use regular expression to find product IDs (assuming they are 8 or 9 digits long)
            product_ids += re.findall(r'\b\d{8,9}\b', text)
    
    return product_ids
    
if __name__ == "__main__":
    # Path to your PDF file
    pdf_path = 'assets/request.pdf'

    # Extract product IDs
    product_ids = extract_product_ids_from_pdf(pdf_path)

    # Print the product IDs
    for product_id in product_ids:
        print(product_id)