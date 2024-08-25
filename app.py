
from app_gui import IkeaApi, clean_folder, extract_product_ids_from_pdf, save_item_images


if __name__ == "__main__":
    # pdf_path = 'assets/shopping_list.pdf'
    pdf_path = 'assets/shopping_list.pdf'
    dst_folder = "output_images"
    clean_folder(dst_folder)
    
    product_ids = extract_product_ids_from_pdf(pdf_path)
    
    api = IkeaApi()
    items = api.get_items(product_ids)
    
    save_item_images(items, dst_folder)