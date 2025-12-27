-- Migration: Add order_number column to inbound_items table
-- Date: 2025-12-28
-- Purpose: Support multi-order processing system

-- Add order_number column
ALTER TABLE inbound_items
ADD COLUMN order_number VARCHAR(100);

-- Add index for performance optimization
CREATE INDEX idx_inbound_items_order_number
ON inbound_items(order_number);

-- Add comment to the column (PostgreSQL)
COMMENT ON COLUMN inbound_items.order_number IS '주문번호 (YYYYMMDD-XXXXX 형식)';

-- Verify the changes
-- SELECT column_name, data_type, is_nullable
-- FROM information_schema.columns
-- WHERE table_name = 'inbound_items' AND column_name = 'order_number';
