"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { CostTrendChart } from "@/components/analytics/CostTrendChart"
import { SupplierPieChart } from "@/components/analytics/SupplierPieChart"
import { InventoryValueTable } from "@/components/analytics/InventoryValueTable"
import { DateRangeFilter } from "@/components/analytics/DateRangeFilter"
import { PageHero } from "@/components/PageHero"
import { BarChart3, TrendingUp, DollarSign } from "lucide-react"
import axios from "axios"

export default function AnalyticsPage() {
    const [supplierStats, setSupplierStats] = useState([])
    const [costTrends, setCostTrends] = useState([])
    const [inventoryValue, setInventoryValue] = useState([])
    const [loading, setLoading] = useState(true)
    const [startDate, setStartDate] = useState<string | null>(null)
    const [endDate, setEndDate] = useState<string | null>(null)

    const fetchData = async (start?: string | null, end?: string | null) => {
        // Only set loading on initial load or handle it differently
        // setLoading(true) <--- Removing this to prevent unmounting DateRangeFilter
        try {
            // Build params
            const dateParams: any = {}
            if (start) dateParams.start_date = start
            if (end) dateParams.end_date = end

            // 1. Fetch Supplier Stats
            const supplierRes = await axios.get("http://localhost:8000/api/v1/analytics/stats/supplier", {
                params: dateParams
            })
            setSupplierStats(supplierRes.data)

            // 2. Fetch Cost Trends (Sample: Yirgacheffe)
            const trendRes = await axios.get("http://localhost:8000/api/v1/analytics/stats/item/trends", {
                params: { bean_name: "예가체프", ...dateParams }
            })
            setCostTrends(trendRes.data)

            // 3. Fetch Inventory for Valuation (no date filter)
            // Only fetch if not already loaded or if needed? 
            // For now, let's keep fetching it or optimize.
            // But to be safe, we fetch everything.
            const beansRes = await axios.get("http://localhost:8000/api/v1/beans/")
            const inventoryData = beansRes.data.items.map((bean: any) => ({
                bean_name: bean.name,
                quantity_kg: bean.quantity_kg,
                avg_price: bean.avg_price,
                total_value: bean.quantity_kg * bean.avg_price
            })).filter((item: any) => item.quantity_kg > 0)

            setInventoryValue(inventoryData)

            setLoading(false)
        } catch (error) {
            console.error("Failed to fetch analytics data", error)
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchData()
    }, [])

    const handleDateChange = (start: string | null, end: string | null) => {
        setStartDate(start)
        setEndDate(end)
        fetchData(start, end)
    }

    if (loading) {
        return <div className="p-8">데이터를 불러오는 중...</div>
    }

    return (
        <div className="space-y-8">
            <PageHero
                icon={BarChart3}
                title="비즈니스 분석"
                description="원가 분석 및 재고 가치 통계 대시보드입니다."
                variant="midnight"
            />

            <div className="container mx-auto px-4 max-w-7xl">
                {/* Date Range Filter */}
                <div className="mb-6">
                    <DateRangeFilter onDateChange={handleDateChange} />
                </div>

                <Tabs defaultValue="overview" className="space-y-4">
                    <TabsList>
                        <TabsTrigger value="overview">개요</TabsTrigger>
                        <TabsTrigger value="cost">원가 분석</TabsTrigger>
                        <TabsTrigger value="inventory">재고 가치</TabsTrigger>
                    </TabsList>

                    <TabsContent value="overview" className="space-y-4">
                        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                            <Card className="col-span-4">
                                <CardHeader>
                                    <CardTitle>공급자 분석</CardTitle>
                                </CardHeader>
                                <CardContent className="pl-2">
                                    <SupplierPieChart data={supplierStats} />
                                </CardContent>
                            </Card>
                            <Card className="col-span-3">
                                <CardHeader>
                                    <CardTitle>주요 지표</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="space-y-4">
                                        <div className="flex items-center">
                                            <DollarSign className="mr-2 h-4 w-4 opacity-70" />
                                            <span className="text-sm font-medium">총 재고 가치</span>
                                        </div>
                                        <div className="text-2xl font-bold">
                                            ₩{inventoryValue.reduce((sum: any, item: any) => sum + item.total_value, 0).toLocaleString()}
                                        </div>
                                        <p className="text-xs text-muted-foreground">FIFO 기준 평가액</p>
                                    </div>
                                </CardContent>
                            </Card>
                        </div>
                    </TabsContent>

                    <TabsContent value="cost" className="space-y-4">
                        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-2">
                            <div className="col-span-1">
                                <CostTrendChart data={costTrends} />
                            </div>
                            <Card className="col-span-1">
                                <CardHeader>
                                    <CardTitle>분석 가이드</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-sm text-gray-500">
                                        현재 'Yirgacheffe' 품목의 입고 단가 추이를 보여줍니다.
                                        향후 드롭다운을 통해 품목 선택 기능을 제공할 예정입니다.
                                    </p>
                                </CardContent>
                            </Card>
                        </div>
                    </TabsContent>

                    <TabsContent value="inventory" className="space-y-4">
                        <InventoryValueTable data={inventoryValue} />
                    </TabsContent>
                </Tabs>
            </div>
        </div>
    )
}
