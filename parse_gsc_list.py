import re

input_path = "Documents/gsc_price_list_extracted.txt"
output_path = "Documents/Bean_List_GSC_20251221.md"

def parse_price(line):
    # Extract numbers at the end of the line
    matches = re.findall(r'[\d,]+', line)
    if matches:
        # Return the last valid price-looking number
        for m in reversed(matches):
            if len(m) > 3 and ',' in m:
                return m
            if len(m) >= 4 and m.isdigit(): # 13500
                return f"{int(m):,}"
    return "-"

def run():
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    countries = {}
    current_country = "Other"
    
    # regex for [Country] or [Name]
    # Example: [브라질] NY2...
    
    items = []
    
    # Simple state machine
    # We look for lines starting with [
    
    buffer_item = None
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Detect Country headers loosely (based on file structure)
        if "Brazil" in line and "브라질" in line and "|" in line:
            continue # Skip footer/header noise
            
        if line.startswith("Brazil 브라질"): current_country = "Brazil"
        elif line.startswith("Colombia 콜롬비아"): current_country = "Colombia"
        elif line.startswith("Costa Rica 코스타리카"): current_country = "Costa Rica"
        elif line.startswith("El salvador 엘살바도르"): current_country = "El Salvador"
        elif line.startswith("Guatemala 과테말라"): current_country = "Guatemala"
        elif line.startswith("Honduras 온두라스"): current_country = "Honduras"
        elif line.startswith("Ethiopia 에티오피아"): current_country = "Ethiopia"
        elif line.startswith("Kenya 케냐"): current_country = "Kenya"
        elif line.startswith("Tanzania 탄자니아"): current_country = "Tanzania"
        elif line.startswith("India 인도"): current_country = "India"
        elif line.startswith("Indonesia 인도네시아"): current_country = "Indonesia"
        elif line.startswith("Vietnam 베트남"): current_country = "Vietnam"
        elif line.startswith("Panama 파나마"): current_country = "Panama"
        elif line.startswith("Rwanda 르완다"): current_country = "Rwanda"
        elif line.startswith("Yemen 예멘"): current_country = "Yemen"
        elif line.startswith("Decaf") or "디카페인" in line and len(line) < 10: current_country = "Decaf"
        
        # Parse Item
        if line.startswith("["):
            # Check if it is Korean line or English line
            is_korean = any(ord(c) > 127 for c in line)
            
            if is_korean:
                # Start new item processing or flush previous
                if buffer_item:
                    # Flush previous
                    if current_country not in countries: countries[current_country] = []
                    countries[current_country].append(buffer_item)
                
                # Create new item
                name_part = line.split("BEST")[0].split("SALE")[0].split("SOLDOUT")[0].split("NEW")[0]
                price = parse_price(line)
                
                # Extract notes if possible (after keywords)
                notes = ""
                if "///" in line:
                    notes = line.split("///")[0].split(" ")[-4:] # Gross approx
                    notes = " ".join(notes)
                
                buffer_item = {
                    "name_ko": name_part.strip(),
                    "name_en": "",
                    "price": price,
                    "notes": notes,
                    "raw_ko": line
                }
            else:
                # English line, usually follows Korean line
                if buffer_item:
                    name_part = line.split("BEST")[0].split("SALE")[0].split("SOLDOUT")[0].split("NEW")[0]
                    buffer_item["name_en"] = name_part.strip()
                    buffer_item["raw_en"] = line
                    
                    # Sometimes price is on English line
                    if buffer_item["price"] == "-":
                        buffer_item["price"] = parse_price(line)
                    
    # Flush last
    if buffer_item:
        if current_country not in countries: countries[current_country] = []
        countries[current_country].append(buffer_item)

    # Generate Markdown
    md_lines = []
    md_lines.append(f"# GSC 생두 품종 리스트 ({input_path})")
    md_lines.append(f"**생성일:** 2025-12-21")
    md_lines.append("")
    
    for country, items in countries.items():
        md_lines.append(f"## {country}")
        md_lines.append("| 품명 (한글) | 품명 (영문) | 예상 단가 | 원본 데이터 |")
        md_lines.append("|---|---|---|---|")
        for i in items:
            # Clean up names
            ko = i['name_ko'].replace("[", "").replace("]", "").replace(country, "").strip() # Remove country tag if redundant
            # Remove country name in brackets if present
            
            md_lines.append(f"| {i['name_ko']} | {i['name_en']} | {i['price']} | <details><summary>보기</summary>{i['raw_ko']}<br>{i.get('raw_en','')}</details> |")
        md_lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    
    print(f"Markdown generated at {output_path}")

if __name__ == "__main__":
    run()
