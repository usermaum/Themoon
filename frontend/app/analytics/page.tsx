"use client"

import { useEffect, useState, useRef } from "react"
import { motion, AnimatePresence, useMotionValue, useTransform, animate } from "framer-motion"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { CostTrendChart } from "@/components/analytics/CostTrendChart"
import { SupplierPieChart } from "@/components/analytics/SupplierPieChart"
import { InventoryValueTable } from "@/components/analytics/InventoryValueTable"
import { DateRangeFilter } from "@/components/analytics/DateRangeFilter"
import { AnalysisBriefing } from "@/components/analytics/AnalysisBriefing"
import PageHero from "@/components/ui/page-hero"
import { BarChart3, TrendingUp, DollarSign } from "lucide-react"
import axios from "axios"

function Counter({ value, prefix = "", suffix = "" }: { value: number, prefix?: string, suffix?: string }) {
    const count = useMotionValue(0)
    const rounded = useTransform(count, (latest) => {
        return prefix + Math.round(latest).toLocaleString() + suffix
    })

    useEffect(() => {
        const controls = animate(count, value, { duration: 1.5, ease: "easeOut" })
        return controls.stop
    }, [value, count])

    return <motion.div>{rounded}</motion.div>
}


export default function AnalyticsPage() {
    const [supplierStats, setSupplierStats] = useState([])
    const [costTrends, setCostTrends] = useState([])
    const [inventoryValue, setInventoryValue] = useState([])
    const [inventoryStats, setInventoryStats] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [startDate, setStartDate] = useState<string | null>(null)
    const [endDate, setEndDate] = useState<string | null>(null)
    const [availableBeans, setAvailableBeans] = useState<string[]>([])
    const [selectedBeanForTrend, setSelectedBeanForTrend] = useState<string>("예가체프")

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

            // 3. Fetch Inventory (Filtered by Date)
            const inventoryRes = await axios.get("http://localhost:8000/api/v1/analytics/stats/inventory", {
                params: dateParams
            })
            const invData = inventoryRes.data
            setInventoryValue(invData.items || [])
            setInventoryStats(invData)

            // 4. Fetch All Beans (for Selector and possibly other lists)
            const beansRes = await axios.get("http://localhost:8000/api/v1/beans/", {
                params: { size: 100 }
            })
            const allBeans = beansRes.data.items

            // Set Available Beans for Selector (Unique names)
            const beanNames = Array.from(new Set(allBeans.map((b: any) => b.name))) as string[]
            setAvailableBeans(beanNames)

            // 2. Fetch Cost Trends (Using selectedBeanForTrend)
            // Note: If selectedBeanForTrend is not in list (initial load), default to first available or "예가체프"
            const targetBean = selectedBeanForTrend || (beanNames.length > 0 ? beanNames[0] : "예가체프")

            const trendRes = await axios.get("http://localhost:8000/api/v1/analytics/stats/item/trends", {
                params: { bean_name: targetBean, ...dateParams }
            })
            setCostTrends(trendRes.data)

            setLoading(false)
        } catch (error) {
            console.error("Failed to fetch analytics data", error)
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchData(startDate, endDate)
    }, [startDate, endDate, selectedBeanForTrend]) // Re-fetch when date or bean changes

    const handleDateChange = (start: string | null, end: string | null) => {
        setStartDate(start)
        setEndDate(end)
    }

    // ... if loading ...
    if (loading) {
        return <div className="p-8">데이터를 불러오는 중...</div>
    }

    return (
        <div className="space-y-8 pb-20">
            <PageHero
                title="비즈니스 분석"
                description="원가 분석 및 재고 가치 통계 대시보드입니다."
                icon={<BarChart3 />}
                image="/images/hero/analytics_hero.png"
                className="mb-8"
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
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                            <Card className="col-span-1 rounded-[1em]">
                                <CardHeader>
                                    <CardTitle>공급자 분석</CardTitle>
                                </CardHeader>
                                <CardContent className="pl-2">
                                    <SupplierPieChart data={supplierStats} />
                                </CardContent>
                            </Card>
                            <Card className="rounded-[1em]">
                                <CardHeader>
                                    <div className="flex items-center gap-2">
                                        <TrendingUp className="h-5 w-5 text-blue-500" />
                                        <CardTitle>주요 지표</CardTitle>
                                    </div>
                                </CardHeader>
                                <CardContent className="space-y-6">
                                    <div className="space-y-1">
                                        <div className="flex items-center text-sm text-muted-foreground gap-1.5 mb-1">
                                            <DollarSign className="h-4 w-4" />
                                            <span>총 재고 가치</span>
                                        </div>
                                        <div className="text-4xl font-bold tracking-tight">
                                            <Counter value={inventoryStats?.total_value || 0} prefix="₩" />
                                        </div>
                                        <p className="text-xs text-muted-foreground mt-1">FIFO 기준 평가액</p>
                                    </div>

                                    {/* 공급자별 재고 비중 (1단계) */}
                                    <div className="border-t pt-4">
                                        <h4 className="text-sm font-semibold mb-3 flex items-center gap-2">
                                            <BarChart3 className="h-4 w-4 text-emerald-500" />
                                            공급자별 자산 비중
                                        </h4>
                                        <div className="space-y-2">
                                            {inventoryStats?.suppliers?.slice(0, 3).map((s: any) => (
                                                <div key={s.name} className="flex items-center justify-between text-sm">
                                                    <span className="text-gray-600 truncate mr-2">{s.name}</span>
                                                    <div className="flex items-center gap-3">
                                                        <div className="w-24 h-2 bg-gray-100 rounded-full overflow-hidden hidden sm:block">
                                                            <motion.div
                                                                className="h-full bg-blue-500"
                                                                initial={{ width: 0 }}
                                                                animate={{ width: `${s.percentage}%` }}
                                                                transition={{ duration: 1, ease: "easeOut" }}
                                                            />
                                                        </div>
                                                        <span className="font-medium text-blue-600 w-10 text-right">{Math.round(s.percentage)}%</span>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    {/* 자산 집중도 Top 3 (2단계) */}
                                    <div className="border-t pt-4">
                                        <h4 className="text-sm font-semibold mb-3 flex items-center gap-2">
                                            <TrendingUp className="h-4 w-4 text-amber-500" />
                                            자산 집중도 (Top 3)
                                        </h4>
                                        <motion.div
                                            className="space-y-3"
                                            initial="hidden"
                                            animate="show"
                                            variants={{
                                                hidden: { opacity: 0 },
                                                show: {
                                                    opacity: 1,
                                                    transition: {
                                                        staggerChildren: 0.2,
                                                        delayChildren: 0.2
                                                    }
                                                }
                                            }}
                                        >
                                            {inventoryStats?.top_items?.map((item: any, idx: number) => (
                                                <motion.div
                                                    key={item.bean_name}
                                                    variants={{
                                                        hidden: { opacity: 0, x: -30 },
                                                        show: {
                                                            opacity: 1,
                                                            x: 0,
                                                            transition: {
                                                                duration: 0.5,
                                                                ease: "easeOut"
                                                            }
                                                        }
                                                    }}
                                                    className="flex items-center justify-between bg-gray-50/50 p-2.5 rounded-lg border border-transparent hover:border-amber-200 hover:bg-amber-50/30 transition-colors shadow-sm"
                                                >
                                                    <div className="flex items-center gap-3">
                                                        <span className="flex items-center justify-center text-xs font-bold text-amber-600 bg-amber-100 w-5 h-5 rounded-full">{idx + 1}</span>
                                                        <span className="text-sm font-medium text-gray-700 truncate max-w-[120px]">{item.bean_name}</span>
                                                    </div>
                                                    <span className="text-sm font-bold text-gray-900 font-mono">₩{item.total_value.toLocaleString()}</span>
                                                </motion.div>
                                            ))}
                                        </motion.div>
                                    </div>
                                </CardContent>
                            </Card>
                        </div>
                    </TabsContent>

                    <TabsContent value="cost" className="space-y-4">
                        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-2">
                            <Card className="col-span-1 rounded-[1em]">
                                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                    <div className="space-y-1">
                                        <CardTitle>단가 변동 추이</CardTitle>
                                        <CardDescription>최근 입고된 품목의 단가 변화</CardDescription>
                                    </div>
                                    <div className="w-[180px]">
                                        <Select
                                            value={selectedBeanForTrend}
                                            onValueChange={setSelectedBeanForTrend}
                                        >
                                            <SelectTrigger>
                                                <SelectValue placeholder="품목 선택" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                {availableBeans.map(bean => (
                                                    <SelectItem key={bean} value={bean}>{bean}</SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                    </div>
                                </CardHeader>
                                <CardContent>
                                    <CostTrendChart data={costTrends} />
                                </CardContent>
                            </Card>
                            <Card className="col-span-1 rounded-[1em]">
                                <CardHeader>
                                    <CardTitle>스마트 분석 브리핑</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <AnalysisBriefing
                                        beanName={selectedBeanForTrend}
                                        data={costTrends}
                                    />
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
