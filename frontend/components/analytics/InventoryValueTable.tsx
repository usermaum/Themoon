import { useState } from "react"
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search, ChevronLeft, ChevronRight, X } from "lucide-react"

interface InventoryValueTableProps {
    data: {
        bean_name: string
        quantity_kg: number
        avg_price: number
        total_value: number
    }[]
}

export function InventoryValueTable({ data }: InventoryValueTableProps) {
    const [searchTerm, setSearchTerm] = useState("")
    const [currentPage, setCurrentPage] = useState(1)
    const itemsPerPage = 10

    const totalValue = data.reduce((sum, item) => sum + item.total_value, 0)

    // Filter Logic
    const filteredData = data.filter(item =>
        item.bean_name.toLowerCase().includes(searchTerm.toLowerCase())
    )

    // Pagination Logic
    const totalPages = Math.ceil(filteredData.length / itemsPerPage)
    const startIndex = (currentPage - 1) * itemsPerPage
    const currentData = filteredData.slice(startIndex, startIndex + itemsPerPage)

    const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearchTerm(e.target.value)
        setCurrentPage(1) // Reset to first page on search
    }

    return (
        <Card>
            <CardHeader>
                <CardTitle>재고 자산 가치</CardTitle>
                <CardDescription>
                    현재 보유 재고의 평가액 (FIFO 기준)
                </CardDescription>
            </CardHeader>
            <CardContent>
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
                    <div className="text-2xl font-bold">
                        총 자산: ₩{totalValue.toLocaleString()}
                    </div>
                    <div className="relative w-full md:w-64">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                        <Input
                            placeholder="품목 검색..."
                            value={searchTerm}
                            onChange={handleSearch}
                            className="pl-9 pr-8"
                        />
                        {searchTerm && (
                            <button
                                onClick={() => {
                                    setSearchTerm("")
                                    setCurrentPage(1)
                                }}
                                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground focus:outline-none"
                            >
                                <X className="h-4 w-4" />
                            </button>
                        )}
                    </div>
                </div>

                <div className="bg-white rounded-[1em] shadow-sm overflow-hidden border border-latte-200">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>품목명</TableHead>
                                <TableHead className="text-right">보유량 (kg)</TableHead>
                                <TableHead className="text-right">평균단가</TableHead>
                                <TableHead className="text-right">평가액</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {currentData.length > 0 ? (
                                currentData.map((item) => (
                                    <TableRow key={item.bean_name}>
                                        <TableCell className="font-medium">{item.bean_name}</TableCell>
                                        <TableCell className="text-right">{item.quantity_kg.toLocaleString()} kg</TableCell>
                                        <TableCell className="text-right">₩{item.avg_price.toLocaleString()}</TableCell>
                                        <TableCell className="text-right">₩{item.total_value.toLocaleString()}</TableCell>
                                    </TableRow>
                                ))
                            ) : (
                                <TableRow>
                                    <TableCell colSpan={4} className="h-24 text-center">
                                        검색 결과가 없습니다.
                                    </TableCell>
                                </TableRow>
                            )}
                        </TableBody>
                    </Table>
                </div>

                {/* Pagination Controls */}
                {totalPages > 1 && (
                    <div className="flex items-center justify-center space-x-2 py-4">
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                            disabled={currentPage === 1}
                        >
                            <ChevronLeft className="h-4 w-4" />
                            이전
                        </Button>
                        <div className="text-sm font-medium">
                            {currentPage} / {totalPages} 페이지
                        </div>
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                            disabled={currentPage === totalPages}
                        >
                            다음
                            <ChevronRight className="h-4 w-4" />
                        </Button>
                    </div>
                )}
            </CardContent>
        </Card>
    )
}
