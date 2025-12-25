"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Bar, BarChart, CartesianGrid, LabelList, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"
import { format, subDays } from "date-fns"
import { ko } from "date-fns/locale"
import { Loader2, TrendingDown, TrendingUp, DollarSign, Package } from "lucide-react"

interface DashboardStats {
    overview: {
        total_production_kg: number;
        total_batches: number;
        avg_loss_rate: number;
    };
    daily_production: Array<{
        date: string;
        total_weight: number;
        batch_count: number;
    }>;
    bean_usage: Array<{
        bean_type: string;
        bean_name: string;
        total_output: number;
        percentage: number;
    }>;
    recent_loss_rates: Array<{
        batch_no: string;
        roast_date: string;
        bean_name: string;
        loss_rate: number;
    }>;
}

export function RoastingDashboard() {
    const [stats, setStats] = useState<DashboardStats | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")

    useEffect(() => {
        fetchStats()
    }, [])

    const fetchStats = async () => {
        try {
            setLoading(true)
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/roasting/dashboard/stats`)
            if (!res.ok) throw new Error("Failed to fetch stats")
            const data = await res.json()
            setStats(data)
        } catch (err) {
            setError("데이터를 불러오는데 실패했습니다.")
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="flex items-center justify-center p-8 bg-white/50 backdrop-blur-sm rounded-xl border border-latte-200">
                <Loader2 className="h-8 w-8 animate-spin text-latte-500" />
                <span className="ml-2 text-latte-600 font-medium">데이터 분석 중...</span>
            </div>
        )
    }

    if (error || !stats) {
        return (
            <div className="p-4 text-center text-red-500 bg-red-50 rounded-lg border border-red-100">
                {error || "데이터가 없습니다."}
            </div>
        )
    }

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
            {/* KPI Cards */}
            <div className="grid gap-4 md:grid-cols-3">
                <Card className="bg-white/80 backdrop-blur-sm border-latte-200 shadow-sm hover:shadow-md transition-all duration-300">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-latte-600">총 생산량 (30일)</CardTitle>
                        <Package className="h-4 w-4 text-latte-400" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-latte-900">{stats.overview.total_production_kg.toLocaleString()} kg</div>
                        <p className="text-xs text-latte-500 mt-1">
                            총 {stats.overview.total_batches} 배치 생산
                        </p>
                    </CardContent>
                </Card>

                <Card className="bg-white/80 backdrop-blur-sm border-latte-200 shadow-sm hover:shadow-md transition-all duration-300">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-latte-600">평균 손실률</CardTitle>
                        <TrendingDown className="h-4 w-4 text-latte-400" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-latte-900">{stats.overview.avg_loss_rate.toFixed(2)} %</div>
                        <p className="text-xs text-latte-500 mt-1">
                            목표 손실률(13~15%) 관리 필요
                        </p>
                    </CardContent>
                </Card>

                <Card className="bg-white/80 backdrop-blur-sm border-latte-200 shadow-sm hover:shadow-md transition-all duration-300">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-latte-600">예상 생산 비용</CardTitle>
                        <DollarSign className="h-4 w-4 text-latte-400" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-latte-900">₩ -</div>
                        <p className="text-xs text-latte-500 mt-1">
                            원가 데이터 집계 중
                        </p>
                    </CardContent>
                </Card>
            </div>

            {/* Main Charts Area */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">

                {/* Daily Production Chart */}
                <Card className="col-span-4 bg-white/80 backdrop-blur-sm border-latte-200 shadow-sm">
                    <CardHeader>
                        <CardTitle className="text-latte-900">일별 생산 추이</CardTitle>
                        <CardDescription>최근 30일간의 로스팅 생산량(kg)</CardDescription>
                    </CardHeader>
                    <CardContent className="pl-2">
                        <div className="h-[300px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={stats.daily_production}>
                                    <defs>
                                        <linearGradient id="colorWeight" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#A88B7D" stopOpacity={0.8} />
                                            <stop offset="95%" stopColor="#A88B7D" stopOpacity={0.1} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" vertical={false} />
                                    <XAxis
                                        dataKey="date"
                                        tickFormatter={(value) => format(new Date(value), 'MM/dd')}
                                        stroke="#9CA3AF"
                                        fontSize={12}
                                        tickLine={false}
                                        axisLine={false}
                                    />
                                    <YAxis
                                        stroke="#9CA3AF"
                                        fontSize={12}
                                        tickLine={false}
                                        axisLine={false}
                                        tickFormatter={(value) => `${value}kg`}
                                    />
                                    <Tooltip
                                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                                        cursor={{ fill: '#f4f1ee' }}
                                    />
                                    <Bar
                                        dataKey="total_weight"
                                        fill="url(#colorWeight)"
                                        radius={[4, 4, 0, 0]}
                                        barSize={20}
                                    />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </CardContent>
                </Card>

                {/* Bean Usage & Loss Rate Tabs */}
                <Card className="col-span-3 bg-white/80 backdrop-blur-sm border-latte-200 shadow-sm">
                    <CardHeader>
                        <CardTitle className="text-latte-900">상세 분석</CardTitle>
                        <CardDescription>원두 사용 비중 및 품질 지표</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Tabs defaultValue="usage" className="space-y-4">
                            <TabsList className="bg-latte-50 grid w-full grid-cols-2">
                                <TabsTrigger value="usage" className="data-[state=active]:bg-white data-[state=active]:text-latte-900">원두 비중</TabsTrigger>
                                <TabsTrigger value="loss" className="data-[state=active]:bg-white data-[state=active]:text-latte-900">손실률 체크</TabsTrigger>
                            </TabsList>

                            <TabsContent value="usage" className="space-y-4">
                                <div className="space-y-4">
                                    {stats.bean_usage.map((bean, i) => (
                                        <div key={i} className="flex items-center">
                                            <div className="w-12 h-12 rounded-full bg-latte-100 flex items-center justify-center text-xs font-bold text-latte-700 mr-3 shrink-0">
                                                {bean.percentage.toFixed(0)}%
                                            </div>
                                            <div className="space-y-1 flex-1">
                                                <p className="text-sm font-medium leading-none text-latte-900 truncate">{bean.bean_name}</p>
                                                <div className="flex items-center text-xs text-muted-foreground">
                                                    {bean.total_output.toFixed(1)}kg 생산
                                                </div>
                                                {/* Progress bar simulation */}
                                                <div className="h-1.5 w-full bg-latte-50 rounded-full mt-1 overflow-hidden">
                                                    <div
                                                        className="h-full bg-latte-400 rounded-full transition-all duration-500"
                                                        style={{ width: `${bean.percentage}%` }}
                                                    />
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </TabsContent>

                            <TabsContent value="loss" className="h-[300px]">
                                <ResponsiveContainer width="100%" height="100%">
                                    <LineChart data={[...stats.recent_loss_rates].reverse()}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" vertical={false} />
                                        <XAxis dataKey="batch_no" hide />
                                        <YAxis domain={['auto', 'auto']} fontSize={12} stroke="#9CA3AF" tickFormatter={(v) => `${v}%`} width={30} />
                                        <Tooltip />
                                        <Line
                                            type="monotone"
                                            dataKey="loss_rate"
                                            stroke="#EF4444"
                                            strokeWidth={2}
                                            dot={{ r: 2, fill: "#EF4444" }}
                                            activeDot={{ r: 4 }}
                                        />
                                        <referenceLine y={15} label="Target Max" stroke="green" strokeDasharray="3 3" />
                                    </LineChart>
                                </ResponsiveContainer>
                            </TabsContent>
                        </Tabs>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
