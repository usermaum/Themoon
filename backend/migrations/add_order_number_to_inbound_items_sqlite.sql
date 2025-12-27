-- Migration: Add order_number column to inbound_items table (SQLite)
-- Date: 2025-12-28
-- Purpose: Support multi-order processing system

-- Add order_number column
ALTER TABLE inbound_items
ADD COLUMN order_number VARCHAR(100);

-- Create index for performance optimization
CREATE INDEX IF NOT EXISTS idx_inbound_items_order_number
ON inbound_items(order_number);

-- Verification query (uncomment to verify)
-- SELECT sql FROM sqlite_master WHERE type='table' AND name='inbound_items';
