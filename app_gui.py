import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pathlib import Path
import re
import shutil
import PyPDF2
import requests
import ikea_api
import threading

def extract_product_ids_from_pdf(pdf_path):
    if not Path(pdf_path).is_file():
        # If the path is not a file, assume it's a URL
        return re.findall(r'(\d+):\d+', pdf_path)
    
    product_ids = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            product_ids += re.findall(r'\b\d{8,9}\b', text)
        
    return product_ids

def save_item_images(items, dst, progress_bar=None):
    total_items = len(items)
    for idx, item in enumerate(items):
        if progress_bar:
            # Update progress bar
            progress_bar['value'] = (idx + 1) / total_items * 100
            root.update_idletasks()
        
        if not item:
            continue
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
    
    def get_items(self, product_ids, progress_bar=None):
        product_ids = list(set(product_ids))
        total_ids = len(product_ids)
        items = []
        for idx, id in enumerate(product_ids):
            items.append(self.get_item(id))
            
            if progress_bar:
                # Update progress bar
                progress_bar['value'] = (idx + 1) / total_ids * 100
                root.update_idletasks()
        return items

def process_pdf():
    pdf_path = pdf_path_entry.get()
    dst_folder = dst_folder_entry.get()
    
    if not pdf_path or not dst_folder:
        messagebox.showerror("Error", "Please provide both PDF path and destination folder.")
        return
    
    clean_folder(dst_folder)
    
    product_ids = extract_product_ids_from_pdf(pdf_path)
    
    api = IkeaApi()
    items = api.get_items(product_ids, progress_bar_api)
    
    save_item_images(items, dst_folder, progress_bar_save)
    
    # Re-enable buttons and reset text
    process_button.config(text="Process", state=tk.NORMAL)
    browse_pdf_button.config(state=tk.NORMAL)
    browse_dst_button.config(state=tk.NORMAL)
    
    messagebox.showinfo("Success", "Images have been saved successfully.")

def start_processing():
    # Show progress bars
    progress_bar_api.grid()
    progress_bar_save.grid()
    progress_label_api.grid()
    progress_label_save.grid()
    
    # Disable buttons and change text
    process_button.config(text="Processing...", state=tk.DISABLED)
    browse_pdf_button.config(state=tk.DISABLED)
    browse_dst_button.config(state=tk.DISABLED)
    
    threading.Thread(target=process_pdf).start()

if __name__ == "__main__":

    # Create the main application window
    root = tk.Tk()
    root.title("PDF to Image Extractor")

    # PDF Path
    tk.Label(root, text="PDF Path:").grid(row=0, column=0, padx=10, pady=10)
    pdf_path_entry = tk.Entry(root, width=50)
    pdf_path_entry.grid(row=0, column=1, padx=10, pady=10)
    browse_pdf_button = tk.Button(root, text="Browse", command=lambda: pdf_path_entry.insert(0, filedialog.askopenfilename()))
    browse_pdf_button.grid(row=0, column=2, padx=10, pady=10)

    # Destination Folder
    tk.Label(root, text="Destination Folder:").grid(row=1, column=0, padx=10, pady=10)
    dst_folder_entry = tk.Entry(root, width=50)
    dst_folder_entry.grid(row=1, column=1, padx=10, pady=10)
    browse_dst_button = tk.Button(root, text="Browse", command=lambda: dst_folder_entry.insert(0, filedialog.askdirectory()))
    browse_dst_button.grid(row=1, column=2, padx=10, pady=10)

    # Process Button
    process_button = tk.Button(root, text="Process", command=start_processing)
    process_button.grid(row=2, column=0, columnspan=3, pady=20)

    # Label and Progress Bar for API calls
    progress_label_api = tk.Label(root, text="Loading items...")
    progress_label_api.grid(row=3, column=0, columnspan=3, pady=5)
    progress_bar_api = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress_bar_api.grid(row=4, column=0, columnspan=3, pady=10)

    # Label and Progress Bar for Saving Images
    progress_label_save = tk.Label(root, text="Saving images...")
    progress_label_save.grid(row=5, column=0, columnspan=3, pady=5)
    progress_bar_save = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress_bar_save.grid(row=6, column=0, columnspan=3, pady=10)

    # Hide progress bars initially
    progress_label_api.grid_remove()
    progress_bar_api.grid_remove()
    progress_label_save.grid_remove()
    progress_bar_save.grid_remove()

    # Run the main loop
    root.mainloop()