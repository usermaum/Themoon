"use client"

import { useState, useEffect } from "react"
import { useSearchParams, useRouter } from "next/navigation"
import Image from "next/image"
import { format } from "date-fns"
import { Search, Plus, Calendar, FileText, ChevronLeft, ChevronRight, ImageIcon, ExternalLink, RefreshCw } from "lucide-react"
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
    DialogTrigger,
} from "@/components/ui/dialog"

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
}

interface InboundListResponse {
    items: InboundDocument[]
    total: number
    page: number
    size: number
    total_pages: number
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
                                                        <DialogContent className="max-w-4xl max-h-[90vh] p-0 overflow-hidden bg-transparent border-none shadow-none">
                                                            <div className="relative w-full h-[80vh]">
                                                                <Image
                                                                    src={getImageUrl(item.webview_image_path || item.thumbnail_image_path) || ""}
                                                                    alt="Invoice Preview"
                                                                    fill
                                                                    className="object-contain"
                                                                />
                                                            </div>
                                                            <div className="text-center mt-2">
                                                                <Button
                                                                    variant="secondary"
                                                                    size="sm"
                                                                    onClick={() => window.open(getImageUrl(item.webview_image_path || item.thumbnail_image_path) || "", "_blank")}
                                                                >
                                                                    <ExternalLink className="w-4 h-4 mr-2" /> 원본 보기
                                                                </Button>
                                                            </div>
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
                                                <Button variant="ghost" size="icon" className="h-8 w-8">
                                                    <FileText className="h-4 w-4 text-muted-foreground" />
                                                </Button>
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
