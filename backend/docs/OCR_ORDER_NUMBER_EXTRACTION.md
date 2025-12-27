# OCR Order Number Extraction Guide

## Overview
This document describes the enhanced OCR prompt instructions for extracting order numbers from multi-order invoices.

## Enhanced Prompt Instructions

### STEP 5-1. ORDER NUMBER EXTRACTION (CRITICAL)

When processing documents that contain MULTIPLE order numbers for different items:

#### Rules:
1. **Each item MUST include its corresponding "order_number" field**
   - Format: `YYYYMMDD-XXXXX` (e.g., `20251108-8B7C2`)
   - Extract from context (date + identifier pattern)

2. **Pattern Recognition**
   - Look for order number patterns in table rows
   - Match each item with its associated order number
   - Common labels: "주문번호", "Order No", "발주번호"

3. **Context Analysis**
   - Order numbers may appear:
     - In table columns
     - As row headers
     - In item descriptions
     - In separate sections grouped by order

4. **Validation**
   - Verify format matches: `YYYYMMDD-XXXXX`
   - Ensure date portion is valid (YYYY: year, MM: 01-12, DD: 01-31)
   - Confirm identifier portion exists

5. **Fallback Handling**
   - If no order number is found for an item: set `"order_number": null`
   - If document has single order: extract once and apply to all items
   - If uncertain: prefer null over incorrect extraction

#### Example JSON Output:
```json
{
  "items": [
    {
      "item_number": "1",
      "order_number": "20251108-8B7C2",
      "bean_name": "Colombia Supremo",
      "quantity": 100,
      "unit": "kg"
    },
    {
      "item_number": "2",
      "order_number": "20251115-9D3F1",
      "bean_name": "Ethiopia Yirgacheffe",
      "quantity": 50,
      "unit": "kg"
    }
  ]
}
```

## Post-Processing
The OCR service automatically groups items by order number using `_post_process_ocr_result()`:

- **has_multiple_orders**: Boolean indicating if document contains multiple orders
- **total_order_count**: Number of distinct orders
- **order_groups**: Array of order groups with:
  - `order_number`: The order identifier
  - `order_date`: Extracted from YYYYMMDD portion
  - `items`: Array of items for this order
  - `subtotal`: Sum of amounts for this order

## Database Storage
Each `InboundItem` record stores its order number in the `order_number` column:
- Type: `VARCHAR(100)`
- Nullable: `TRUE` (maintains backward compatibility)
- Indexed: `YES` (for query performance)

## Migration
To apply the database schema change, run:
```bash
psql -U username -d database_name -f backend/migrations/add_order_number_to_inbound_items.sql
```

Or wait for the SQLAlchemy model to auto-create the column on next deployment.
