from pypdf import PdfReader

pdf_path = "Documents/[지에스씨] 생두 단가표.pdf"
output_path = "Documents/gsc_price_list_pypdf.txt"

try:
    reader = PdfReader(pdf_path)
    with open(output_path, "w", encoding="utf-8") as f:
        for page in reader.pages:
            text = page.extract_text()
            if text:
                f.write(text + "\n")
    print(f"Extraction successful: {output_path}")
except Exception as e:
    print(f"Error: {e}")
