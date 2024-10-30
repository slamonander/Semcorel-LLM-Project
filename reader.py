def extract_text(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        faqs = file.read().strip()
    return faqs