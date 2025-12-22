"use client"

import { useState, useEffect } from "react"
import { useSearchParams, useRouter } from "next/navigation"
import Image from "next/image"
import { format } from "date-fns"
import { Search, Plus, Calendar, FileText, ChevronLeft, ChevronRight, ImageIcon, ExternalLink, RefreshCw, Package, X } from "lucide-react"
import PageHero from "@/components/ui/page-hero"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Skeleton } from "@/components/ui/skeleton"
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
    DialogTrigger,
} from "@/components/ui/dialog"
import { Separator } from "@/components/ui/separator"

// Types (should ideally be in a shared type file)
interface InboundDocument {
    id: number
    contract_number?: string
    supplier_name?: string
    invoice_date?: string
    total_amount?: number
    thumbnail_image_path?: string
    webview_image_path?: string
    processing_status: string
    created_at: string
    item_count?: number
    supplier_business_number?: string
}

interface InboundListResponse {
    items: InboundDocument[]
    total: number
    page: number
    size: number
    total_pages: number
}

// === NEW: Detail Component ===
interface InboundDetail {
    document: InboundDocument
    items: any[]
    detail?: any
    receiver?: any
}

function InboundDetailDialog({ docId, trigger }: { docId: number, trigger: React.ReactNode }) {
    const [detail, setDetail] = useState<InboundDetail | null>(null)
    const [loading, setLoading] = useState(false)

    const fetchDetail = async () => {
        setLoading(true)
        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
            const res = await fetch(`${apiUrl}/api/v1/inbound/${docId}`)
            if (!res.ok) throw new Error("Failed to fetch detail")
            const result = await res.json()
            setDetail(result)
        } catch (error) {
            console.error("Error fetching detail:", error)
        } finally {
            setLoading(false)
        }
    }

    return (
        <Dialog onOpenChange={(open: boolean) => { if (open) fetchDetail() }}>
            <DialogTrigger asChild>
                {trigger}
            </DialogTrigger>
            <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto p-6 bg-white border-[3px] border-black text-black">
                {loading ? (
                    <div className="space-y-4 py-10">
                        <Skeleton className="h-10 w-48 mx-auto" />
                        <Skeleton className="h-32 w-full" />
                        <Skeleton className="h-64 w-full" />
                    </div>
                ) : detail ? (
                    <div className="space-y-6">
                        {/* Header Section */}
                        <div className="flex items-start justify-between">
                            <div className="w-24 h-16 bg-[#8B0000] flex items-center justify-center shrink-0">
                                <div className="text-white text-center leading-none">
                                    <div className="text-xl font-bold">GSC</div>
                                    <div className="text-[8px]">GREEN COFFEE</div>
                                </div>
                            </div>
                            <div className="flex-1 text-center">
                                <h1 className="text-3xl font-bold tracking-tight">거 래 명 세 서</h1>
                                <p className="text-xs text-muted-foreground mt-1 text-black">(공급받는자용)</p>
                            </div>
                            <div className="w-24 hidden sm:block"></div>
                        </div>

                        {/* Info Section */}
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div className="border border-black p-2 space-y-1">
                                <InvoiceInfoRow label="등록번호" value={detail.receiver?.business_number || '-'} />
                                <InvoiceInfoRow label="상호(성명)" value={detail.receiver?.name || 'The Moon Coffee'} />
                                <InvoiceInfoRow label="사업장소재지" value={detail.receiver?.address || '-'} small />
                                <InvoiceInfoRow label="담당자" value={detail.receiver?.phone || '-'} />
                            </div>
                            <div className="border border-black p-2 space-y-1 relative">
                                <InvoiceInfoRow label="등록번호" value={detail.document.supplier_business_number || '-'} />
                                <InvoiceInfoRow label="상호(성명)" value={detail.document.supplier_name || '-'} />
                                <InvoiceInfoRow label="사업장소재지" value={detail.detail?.supplier_address || '-'} small />
                                <InvoiceInfoRow label="대표자/담당" value={detail.detail?.supplier_representative || detail.detail?.supplier_contact_person || '-'} />
                                <div className="absolute top-1 right-1 w-12 h-12 bg-red-100/50 rounded-full border-2 border-red-600/30 flex items-center justify-center pointer-events-none opacity-50 text-red-700/50 text-[10px] font-bold">
                                    인
                                </div>
                            </div>
                        </div>

                        {/* Items Table */}
                        <div className="border-t-2 border-b-2 border-black">
                            <Table className="text-xs">
                                <TableHeader>
                                    <TableRow className="bg-gray-100 hover:bg-gray-100 border-b border-black">
                                        <TableHead className="w-10 text-center text-black font-bold h-8">NO</TableHead>
                                        <TableHead className="text-black font-bold h-8">품목명</TableHead>
                                        <TableHead className="w-16 text-center text-black font-bold h-8">규격</TableHead>
                                        <TableHead className="w-16 text-right text-black font-bold h-8">수량</TableHead>
                                        <TableHead className="w-24 text-right text-black font-bold h-8">단가</TableHead>
                                        <TableHead className="w-28 text-right text-black font-bold h-8">금액</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {detail.items.map((item, idx) => (
                                        <TableRow key={idx} className="border-b border-gray-200 h-8 hover:bg-muted/10">
                                            <TableCell className="text-center py-1 text-black">{idx + 1}</TableCell>
                                            <TableCell className="py-1 font-medium text-black">{item.bean_name}</TableCell>
                                            <TableCell className="text-center py-1 text-black">{item.unit || '1kg'}</TableCell>
                                            <TableCell className="text-right py-1 font-mono text-black">{item.quantity?.toLocaleString()}</TableCell>
                                            <TableCell className="text-right py-1 font-mono text-black">{item.unit_price?.toLocaleString()}</TableCell>
                                            <TableCell className="text-right py-1 font-mono font-bold text-black">{item.supply_amount?.toLocaleString()}</TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </div>

                        {/* Summary Section */}
                        <div className="grid grid-cols-2 gap-4 pt-2">
                            <div className="space-y-1 text-sm border-r border-gray-200 pr-4">
                                <InvoiceSummaryItem label="총 품목 수" value={`${detail.items.length}종`} />
                                <InvoiceSummaryItem label="발행일자" value={detail.document.invoice_date || '-'} />
                                <InvoiceSummaryItem label="계약번호" value={detail.document.contract_number || '-'} />
                            </div>
                            <div className="flex flex-col items-end justify-center">
                                <div className="text-sm font-bold text-muted-foreground mb-1">합계 금액(VAT 포함)</div>
                                <div className="text-2xl font-black font-mono text-black">
                                    {(detail.document.total_amount || 0).toLocaleString()}원
                                </div>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="py-20 text-center text-muted-foreground italic text-black">
                        상세 정보를 불러올 수 없습니다.
                    </div>
                )}
            </DialogContent>
        </Dialog>
    )
}

function InvoiceInfoRow({ label, value, small = false }: { label: string; value: string; small?: boolean }) {
    return (
        <div className="flex items-center text-[11px] leading-tight text-black">
            <span className="w-20 font-bold bg-gray-50 px-1.5 py-1 border-r border-gray-200 shrink-0">{label}</span>
            <span className={`px-2 py-1 flex-1 overflow-hidden text-ellipsis whitespace-nowrap ${small ? 'text-[10px]' : ''}`}>
                {value}
            </span>
        </div>
    )
}

function InvoiceSummaryItem({ label, value }: { label: string; value: string }) {
    return (
        <div className="flex items-center text-xs gap-2 text-black">
            <span className="font-bold text-muted-foreground min-w-[60px]">● {label}:</span>
            <span className="font-medium">{value}</span>
        </div>
    )
}

export default function InvoiceListPage() {
    const router = useRouter()
    const searchParams = useSearchParams()

    // State
    const [loading, setLoading] = useState(true)
    const [data, setData] = useState<InboundListResponse>({ items: [], total: 0, page: 1, size: 20, total_pages: 0 })
    const [selectedImage, setSelectedImage] = useState<string | null>(null)

    // Params
    const page = parseInt(searchParams.get("page") || "1")
    const keyword = searchParams.get("keyword") || ""
    const fromDate = searchParams.get("from_date") || ""
    const toDate = searchParams.get("to_date") || ""

    // Fetch Data
    const fetchData = async () => {
        setLoading(true)
        try {
            const params = new URLSearchParams()
            params.append("page", page.toString())
            params.append("limit", "20")
            if (keyword) params.append("keyword", keyword)
            if (fromDate) params.append("from_date", fromDate)
            if (toDate) params.append("to_date", toDate)

            // Adjust URL based on environment (local vs production) - fallback to localhost
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
            const res = await fetch(`${apiUrl}/api/v1/inbound/list?${params.toString()}`)

            if (!res.ok) throw new Error("Failed to fetch")

            const result = await res.json()
            setData(result)
        } catch (error) {
            console.error("Error fetching invoice list:", error)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchData()
    }, [page, keyword, fromDate, toDate])

    // Handlers
    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault()
        const formData = new FormData(e.target as HTMLFormElement)
        const newKeyword = formData.get("keyword") as string
        const newFrom = formData.get("from_date") as string
        const newTo = formData.get("to_date") as string

        const params = new URLSearchParams()
        if (newKeyword) params.set("keyword", newKeyword)
        if (newFrom) params.set("from_date", newFrom)
        if (newTo) params.set("to_date", newTo)
        params.set("page", "1") // Reset to page 1

        router.push(`/inventory/inbound/list?${params.toString()}`)
    }

    const handlePageChange = (newPage: number) => {
        const params = new URLSearchParams(searchParams.toString())
        params.set("page", newPage.toString())
        router.push(`/inventory/inbound/list?${params.toString()}`)
    }

    // Helper to format currency
    const formatCurrency = (val?: number) => val ? val.toLocaleString() + "원" : "-"

    // Helper to get image URL
    const getImageUrl = (path?: string) => {
        if (!path) return null
        return `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/static/uploads/inbound/${path}`
    }

    return (
        <div className="space-y-6 pb-20">
            <PageHero
                title="명세서 목록 (Invoices)"
                description="등록된 입고 명세서(Invoices) 이력을 조회하고 관리합니다."
                icon={<FileText />}
                image="/images/hero/inbound_hero.png" // Reuse existing hero
                compact={true}
            />

            <div className="container mx-auto px-4 max-w-7xl space-y-6">

                {/* Search & Filter Bar */}
                <Card>
                    <CardContent className="p-4 sm:p-6">
                        <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-4 items-end">
                            <div className="flex-1 w-full space-y-2">
                                <label className="text-sm font-medium text-muted-foreground">검색어 (계약번호/공급처)</label>
                                <div className="relative">
                                    <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                                    <Input
                                        name="keyword"
                                        defaultValue={keyword}
                                        placeholder="계약번호 또는 공급처명 검색..."
                                        className="pl-9"
                                    />
                                </div>
                            </div>
                            <div className="flex gap-2 w-full sm:w-auto">
                                <div className="space-y-2 flex-1 sm:w-40">
                                    <label className="text-sm font-medium text-muted-foreground">시작일</label>
                                    <Input name="from_date" type="date" defaultValue={fromDate} />
                                </div>
                                <div className="space-y-2 flex-1 sm:w-40">
                                    <label className="text-sm font-medium text-muted-foreground">종료일</label>
                                    <Input name="to_date" type="date" defaultValue={toDate} />
                                </div>
                            </div>
                            <div className="flex gap-2 w-full sm:w-auto">
                                <Button type="submit" className="flex-1 sm:flex-none">
                                    <Search className="w-4 h-4 mr-2" /> 조회
                                </Button>
                                <Button
                                    type="button"
                                    variant="outline"
                                    className="px-3"
                                    onClick={() => router.push('/inventory/inbound/list')} // Clear filters
                                >
                                    <RefreshCw className="w-4 h-4" />
                                </Button>
                                <Button
                                    type="button"
                                    className="bg-green-600 hover:bg-green-700"
                                    onClick={() => router.push('/inventory/inbound')}
                                >
                                    <Plus className="w-4 h-4 mr-2" /> 신규 입고
                                </Button>
                            </div>
                        </form>
                    </CardContent>
                </Card>

                {/* Data Table */}
                <Card>
                    <CardHeader className="py-4 px-6">
                        <div className="flex justify-between items-center">
                            <CardTitle className="text-lg">조회 결과</CardTitle>
                            <Badge variant="outline" className="text-muted-foreground">Total: {data.total}</Badge>
                        </div>
                    </CardHeader>
                    <div className="border-t">
                        <Table>
                            <TableHeader>
                                <TableRow className="bg-muted/50">
                                    <TableHead className="w-[80px] text-center">이미지</TableHead>
                                    <TableHead className="w-[120px]">구매일자</TableHead>
                                    <TableHead>계약번호 (Contract No)</TableHead>
                                    <TableHead>공급처</TableHead>
                                    <TableHead className="text-right">총 금액</TableHead>
                                    <TableHead className="w-[100px] text-center">상태</TableHead>
                                    <TableHead className="w-[80px] text-center">동작</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {loading ? (
                                    Array(5).fill(0).map((_, i) => (
                                        <TableRow key={i}>
                                            <TableCell><Skeleton className="h-10 w-10 rounded" /></TableCell>
                                            <TableCell><Skeleton className="h-4 w-20" /></TableCell>
                                            <TableCell><Skeleton className="h-4 w-32" /></TableCell>
                                            <TableCell><Skeleton className="h-4 w-24" /></TableCell>
                                            <TableCell><Skeleton className="h-4 w-20" /></TableCell>
                                            <TableCell><Skeleton className="h-6 w-16" /></TableCell>
                                            <TableCell><Skeleton className="h-8 w-8" /></TableCell>
                                        </TableRow>
                                    ))
                                ) : data.items.length === 0 ? (
                                    <TableRow>
                                        <TableCell colSpan={7} className="h-32 text-center text-muted-foreground">
                                            데이터가 없습니다.
                                        </TableCell>
                                    </TableRow>
                                ) : (
                                    data.items.map((item) => (
                                        <TableRow key={item.id} className="hover:bg-muted/5">
                                            <TableCell className="text-center p-2">
                                                {item.thumbnail_image_path ? (
                                                    <Dialog>
                                                        <DialogTrigger>
                                                            <div className="relative w-10 h-10 rounded border overflow-hidden cursor-pointer hover:opacity-80 transition-opacity">
                                                                <Image
                                                                    src={getImageUrl(item.thumbnail_image_path) || ""}
                                                                    alt="Invoice Thumbnail"
                                                                    fill
                                                                    className="object-cover"
                                                                />
                                                            </div>
                                                        </DialogTrigger>
                                                        <DialogContent className="sm:left-[calc(50%+var(--sidebar-width,0px)/2)] w-fit h-fit max-w-[95vw] max-h-[95vh] p-0 overflow-hidden bg-transparent border-none shadow-none flex flex-col items-center justify-center transition-all duration-300">
                                                            {/* Custom Backdrop for "Click outside to close" focus */}
                                                            <div className="relative group w-fit h-fit flex items-center justify-center">
                                                                <div className="relative w-full max-h-[85vh] overflow-hidden rounded-lg shadow-2xl border border-white/10">
                                                                    <img
                                                                        src={getImageUrl(item.webview_image_path || item.thumbnail_image_path) || ""}
                                                                        alt="Invoice Preview"
                                                                        className="max-w-full max-h-[85vh] object-contain block"
                                                                    />
                                                                </div>

                                                                {/* Floating Button Overlay */}
                                                                <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                                                                    <Button
                                                                        variant="secondary"
                                                                        size="sm"
                                                                        className="bg-white/90 hover:bg-white text-black shadow-lg backdrop-blur-sm"
                                                                        onClick={(e) => {
                                                                            e.stopPropagation();
                                                                            window.open(getImageUrl(item.webview_image_path || item.thumbnail_image_path) || "", "_blank")
                                                                        }}
                                                                    >
                                                                        <ExternalLink className="w-4 h-4 mr-2" /> 새 탭에서 열기
                                                                    </Button>
                                                                </div>
                                                            </div>
                                                            <p className="mt-4 text-white/60 text-sm font-light select-none">
                                                                빈 공간을 클릭하면 닫힙니다.
                                                            </p>
                                                        </DialogContent>
                                                    </Dialog>
                                                ) : (
                                                    <div className="w-10 h-10 rounded bg-muted flex items-center justify-center text-muted-foreground mx-auto">
                                                        <ImageIcon className="w-4 h-4" />
                                                    </div>
                                                )}
                                            </TableCell>
                                            <TableCell className="font-medium text-xs sm:text-sm">
                                                {item.invoice_date || item.created_at?.substring(0, 10)}
                                            </TableCell>
                                            <TableCell>
                                                <div className="font-mono text-xs sm:text-sm">{item.contract_number || '-'}</div>
                                            </TableCell>
                                            <TableCell className="font-medium">
                                                {item.supplier_name}
                                            </TableCell>
                                            <TableCell className="text-right font-mono font-medium">
                                                {formatCurrency(item.total_amount)}
                                            </TableCell>
                                            <TableCell className="text-center">
                                                <Badge variant="outline" className="text-xs bg-muted/50 text-muted-foreground whitespace-nowrap">
                                                    입고완료
                                                </Badge>
                                            </TableCell>
                                            <TableCell className="text-center">
                                                <InboundDetailDialog
                                                    docId={item.id}
                                                    trigger={
                                                        <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-latte-100/50 hover:text-latte-700">
                                                            <FileText className="h-4 w-4 text-muted-foreground" />
                                                        </Button>
                                                    }
                                                />
                                            </TableCell>
                                        </TableRow>
                                    ))
                                )}
                            </TableBody>
                        </Table>
                    </div>

                    {/* Pagination */}
                    {data.total_pages > 1 && (
                        <div className="flex items-center justify-center py-4 gap-2">
                            <Button
                                variant="outline"
                                size="sm"
                                disabled={page <= 1}
                                onClick={() => handlePageChange(page - 1)}
                            >
                                <ChevronLeft className="h-4 w-4" />
                            </Button>
                            <span className="text-sm font-medium text-muted-foreground mx-2">
                                {page} / {data.total_pages}
                            </span>
                            <Button
                                variant="outline"
                                size="sm"
                                disabled={page >= data.total_pages}
                                onClick={() => handlePageChange(page + 1)}
                            >
                                <ChevronRight className="h-4 w-4" />
                            </Button>
                        </div>
                    )}
                </Card>
            </div>
        </div>
    )
}
