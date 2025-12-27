import pdfplumber
import sys

pdf_path = "docs/gsc_price_20251221.pdf"
output_path = "docs/gsc_price_list_extracted.txt"

try:
    with pdfplumber.open(pdf_path) as pdf:
        with open(output_path, "w", encoding="utf-8") as f:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    f.write(text + "\n")
                
                # Also try extracting tables
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        clean_row = [str(cell).replace("\n", " ") if cell else "" for cell in row]
                        f.write(" | ".join(clean_row) + "\n")
                    f.write("\n---\n")
    print(f"Extraction successful: {output_path}")
except Exception as e:
    print(f"Error: {e}")
