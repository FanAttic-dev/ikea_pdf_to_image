from pathlib import Path
import re
import shutil
import PyPDF2
import requests
from pdf_parse_pypdf2 import extract_product_ids_from_pdf
import ikea_api

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

def save_item_images(items, dst):    
    for item in items:
        if not item:
            continue
        # item_name = Path(item["pipUrl"]).stem + ".jpg"
        item_name = item["id"] + ".jpg"
        item_path = Path(dst) / item_name
        if "mainImage" not in item:
            with open(item_path, 'wb') as f:
                f.write(b'')
            continue
        
        image_url = item["mainImage"]["url"]
        image_data = requests.get(image_url).content
        with open(item_path, 'wb') as f:
            f.write(image_data)
            
def clean_folder(folder):
    shutil.rmtree(folder, ignore_errors=True)
    Path(folder).mkdir(parents=True, exist_ok=True)

class IkeaApi:
    def __init__(self):
        self.constants = ikea_api.Constants(country="gb", language="en")
        self.pip_item = ikea_api.PipItem(self.constants)
        
    def get_item(self, product_id):
        req = self.pip_item.get_item(product_id)
        return ikea_api.run(req)
    
    def get_items(self, product_ids):
        items = [self.get_item(id) for id in set(product_ids)]    
        return items
        
if __name__ == "__main__":
    pdf_path = 'assets/request2.pdf'
    dst_folder = "output_images"
    clean_folder(dst_folder)
    
    product_ids = extract_product_ids_from_pdf(pdf_path)
    
    api = IkeaApi()
    items = api.get_items(product_ids)
    
    save_item_images(items, dst_folder)