export interface InboundDocument {
    id: number
    contract_number?: string
    supplier_name?: string
    invoice_date?: string
    total_amount?: number

    // Tiered Storage Paths
    thumbnail_image_path?: string
    webview_image_path?: string
    original_image_path?: string

    processing_status: string
    created_at: string
    item_count?: number
    supplier_business_number?: string

    // Additional Metadata
    file_size_bytes?: number
    image_width?: number
    image_height?: number
}

export interface InboundListResponse {
    items: InboundDocument[]
    total: number
    page: number
    size: number
    total_pages: number
}

// Detail Interfaces
export interface InboundDetail {
    document: InboundDocument
    items: InboundItem[]
    detail?: InboundDocumentDetail
    receiver?: InboundReceiver
}

export interface InboundItem {
    id?: number
    bean_name?: string
    unit?: string
    quantity?: number
    unit_price?: number
    supply_amount?: number
    tax_amount?: number
}

export interface InboundDocumentDetail {
    supplier_address?: string
    supplier_representative?: string
    supplier_contact_person?: string
    supplier_phone?: string
}

export interface InboundReceiver {
    name?: string
    business_number?: string
    address?: string
    phone?: string
}
