import json

def generate_markdown(schema_path):
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = json.load(f)

    markdown_output = []
    
    # Order of tables
    table_order = [
        'beans', 'suppliers', 'blends', 
        'inbound_documents', 'inbound_document_details', 
        'inbound_receivers', 'inbound_items', 
        'inventory_logs'
    ]
    
    table_descriptions = {
        'beans': '생두, 원두, 블렌드 원두를 하나의 테이블에서 통합 관리',
        'suppliers': '공급처 관리',
        'blends': '커피 블렌드 레시피 저장',
        'inbound_documents': '입고 내역서 메인 정보 (OCR 결과)',
        'inbound_document_details': '입고 내역서 상세 정보 (공급자, 금액 등)',
        'inbound_receivers': '입고 내역서 공급받는자 정보',
        'inbound_items': '입고 내역서 품목 상세',
        'inventory_logs': '모든 재고 변동 추적 (감사 로그)'
    }

    # Helper translations/descriptions for columns (could be expanded)
    col_desc_map = {
        'id': 'Primary Key',
        'created_at': '생성일시',
        'updated_at': '수정일시',
        'notes': '비고 / 메모',
        # Beans
        'name': '품목명',
        'sku': 'SKU 코드',
        'type': '품목 유형 (GREEN_BEAN/ROASTED_BEAN/BLEND_BEAN)',
        'origin': '원산지',
        'quantity_kg': '현재 재고량 (kg)',
        'avg_price': '평균 단가',
        'name_ko': '품목명 (한글)',
        'name_en': '품목명 (영문)',
        'origin_ko': '원산지 (한글)',
        'origin_en': '원산지 (영문)',
        # Inbound
        'contract_number': '계약 번호',
        'supplier_name': '공급처명',
        'total_amount': '총 금액',
        'image_url': '원본 이미지 URL',
        # ... add more as generic catch-all
    }

    index = 1
    for table_name in table_order:
        if table_name not in schema:
            continue
            
        t_info = schema[table_name]
        desc = table_descriptions.get(table_name, 'Table description')
        
        markdown_output.append(f"### {index}. {table_name} ({desc.split(' ')[0]})")
        markdown_output.append(f"")
        markdown_output.append(f"**목적**: {desc}")
        markdown_output.append(f"")
        markdown_output.append(f"| 컬럼명 | 타입 | 제약 | 설명 |")
        markdown_output.append(f"| --- | --- | --- | --- |")
        
        for col in t_info['columns']:
            c_name = col['name']
            c_type = col['type']
            notnull = "NOT NULL" if col['notnull'] else "NULL"
            pk = "PK" if col['pk'] else ""
            default = f"DEFAULT {col['default']}" if col['default'] is not None else ""
            
            constraints = [x for x in [pk, notnull, default] if x]
            constraint_str = ", ".join(constraints)
            
            # Simple description lookup
            description = col_desc_map.get(c_name, '')
            
            markdown_output.append(f"| `{c_name}` | {c_type} | {constraint_str} | {description} |")
            
        markdown_output.append(f"")
        
        # Foreign Keys
        if t_info['foreign_keys']:
            markdown_output.append(f"**Foreign Keys**:")
            for fk in t_info['foreign_keys']:
                markdown_output.append(f"- `{fk['from']}` → `{fk['table']}.{fk['to']}`")
            markdown_output.append(f"")
            
        markdown_output.append(f"---")
        markdown_output.append(f"")
        index += 1

    return "\n".join(markdown_output)

if __name__ == "__main__":
    output = generate_markdown('schema.json')

    # Write to file with explicit UTF-8 encoding
    with open('schema_tables.md', 'w', encoding='utf-8') as f:
        f.write(output)

    print("✅ schema_tables.md generated successfully with UTF-8 encoding")
