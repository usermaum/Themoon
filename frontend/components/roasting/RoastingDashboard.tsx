"use client"

import { useEffect, useState } from "react"
import { motion } from "framer-motion"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Bar, BarChart, CartesianGrid, LabelList, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"
import { format, subDays } from "date-fns"
import { ko } from "date-fns/locale"
import { Loader2, TrendingDown, TrendingUp, DollarSign, Package, History, Coffee } from "lucide-react"

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
        <div className="space-y-6">
            {/* Bento Grid Layout - Modernized */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 auto-rows-[minmax(180px,auto)]">

                {/* 1. Total Production (Large Card) */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
                    className="col-span-1 md:col-span-2 row-span-1"
                >
                    <Card className="h-full bg-white/60 backdrop-blur-md border-white/20 shadow-xl shadow-latte-900/5 hover:shadow-2xl hover:shadow-latte-900/10 transition-all duration-300 rounded-[2rem] overflow-hidden group">
                        <CardHeader className="flex flex-row items-center justify-between pb-2">
                            <CardTitle className="text-sm font-bold text-latte-600 uppercase tracking-wider">총 생산량</CardTitle>
                            <div className="p-2 bg-latte-100 rounded-full group-hover:bg-latte-200 transition-colors">
                                <Package className="h-4 w-4 text-latte-700" />
                            </div>
                        </CardHeader>
                        <CardContent>
                            <div className="flex items-end justify-between">
                                <div>
                                    <div className="text-5xl font-black text-latte-900 tracking-tight">
                                        {Number(stats.overview.total_production_kg.toFixed(1)).toLocaleString()}
                                        <span className="text-xl text-latte-400 font-medium ml-1">kg</span>
                                    </div>
                                    <p className="text-xs font-medium text-latte-400 mt-2 bg-latte-50 inline-block px-2 py-1 rounded-lg">
                                        최근 30일 • 총 {stats.overview.total_batches} 배치
                                    </p>
                                </div>
                                <div className="h-16 w-32 opacity-80 group-hover:opacity-100 transition-opacity">
                                    <ResponsiveContainer width="100%" height="100%">
                                        <BarChart data={stats.daily_production.slice(-7)}>
                                            <Tooltip cursor={false} content={<></>} />{/* Hide tooltip for sparkline */}
                                            <Bar dataKey="total_weight" fill="#A88B7D" radius={[4, 4, 0, 0]} />
                                        </BarChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </motion.div>

                {/* 2. Loss Rate (Square Card) */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
                    className="col-span-1 row-span-1"
                >
                    <Card className="h-full bg-white/60 backdrop-blur-md border-white/20 shadow-xl shadow-latte-900/5 hover:shadow-2xl hover:shadow-latte-900/10 transition-all duration-300 rounded-[2rem] group relative overflow-hidden">
                        <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-br from-amber-100/50 to-transparent rounded-bl-[4rem] pointer-events-none" />
                        <CardHeader className="flex flex-row items-center justify-between pb-2">
                            <CardTitle className="text-sm font-bold text-latte-600 uppercase tracking-wider">평균 손실률</CardTitle>
                            <div className="p-2 bg-amber-50 rounded-full group-hover:bg-amber-100 transition-colors">
                                <TrendingDown className="h-4 w-4 text-amber-600" />
                            </div>
                        </CardHeader>
                        <CardContent>
                            <div className="text-4xl font-black text-latte-900">{stats.overview.avg_loss_rate.toFixed(1)}<span className="text-xl">%</span></div>
                            <div className="mt-4 h-3 w-full bg-latte-100 rounded-full overflow-hidden">
                                <motion.div
                                    initial={{ width: 0 }}
                                    animate={{ width: `${Math.min((stats.overview.avg_loss_rate / 20) * 100, 100)}%` }}
                                    transition={{ duration: 1, delay: 0.5 }}
                                    className={`h-full ${stats.overview.avg_loss_rate > 15 ? 'bg-red-400' : 'bg-green-500'}`}
                                />
                            </div>
                            <p className="text-xs text-latte-400 mt-3 flex justify-between">
                                <span>목표: 12-15%</span>
                                <span className={stats.overview.avg_loss_rate > 15 ? 'text-red-500 font-bold' : 'text-green-600 font-bold'}>
                                    {stats.overview.avg_loss_rate > 15 ? '높음' : '좋음'}
                                </span>
                            </p>
                        </CardContent>
                    </Card>
                </motion.div>

                {/* 3. Recent Batches (Swapped from Cost) */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
                    className="col-span-1 row-span-1"
                >
                    <Card className="h-full bg-white/60 backdrop-blur-md border-white/20 shadow-xl shadow-latte-900/5 hover:shadow-2xl hover:shadow-latte-900/10 transition-all duration-300 rounded-[2rem] overflow-hidden group">
                        <CardHeader className="flex flex-row items-center justify-between pb-2">
                            <CardTitle className="text-sm font-bold text-latte-600 uppercase tracking-wider">최근 작업</CardTitle>
                            <div className="p-2 bg-blue-50 rounded-full group-hover:bg-blue-100 transition-colors">
                                <History className="h-4 w-4 text-blue-600" />
                            </div>
                        </CardHeader>
                        <CardContent className="p-0 px-6 pb-4">
                            <div className="space-y-3 mt-2">
                                {stats.recent_loss_rates.slice(0, 3).map((log, i) => (
                                    <div key={i} className="flex justify-between items-center text-sm">
                                        <span className="font-medium text-latte-800 truncate max-w-[80px]">{log.batch_no}</span>
                                        <div className="flex items-center gap-2">
                                            <span className="text-xs text-latte-400 truncate max-w-[60px]">{log.bean_name}</span>
                                            <span className={`text-xs font-bold px-1.5 py-0.5 rounded ${log.loss_rate > 15 ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-600'}`}>
                                                {log.loss_rate.toFixed(1)}%
                                            </span>
                                        </div>
                                    </div>
                                ))}
                                {stats.recent_loss_rates.length === 0 && (
                                    <p className="text-xs text-latte-400 text-center py-4">최근 기록 없음</p>
                                )}
                            </div>
                        </CardContent>
                    </Card>
                </motion.div>

                {/* 4. Daily Production Chart (Wide Card) */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}
                    className="col-span-1 md:col-span-3 row-span-2"
                >
                    <Card className="h-full bg-white/80 backdrop-blur-xl border-white/40 shadow-xl shadow-latte-900/5 rounded-[2rem] p-2">
                        <CardHeader>
                            <CardTitle className="text-latte-900 text-lg">생산량 추이</CardTitle>
                            <CardDescription>지난 30일간의 일별 생산량</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="h-[280px] w-full">
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
                                            tickFormatter={(value) => format(new Date(value), 'M/d')}
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
                                            contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                                            cursor={{ fill: '#f4f1ee' }}
                                            formatter={(value: any) => [`${Number(Number(value).toFixed(2))}kg`, '생산량']}
                                            labelFormatter={(label) => format(new Date(label), 'yyyy년 M월 d일')}
                                        />
                                        <Bar
                                            dataKey="total_weight"
                                            fill="url(#colorWeight)"
                                            radius={[6, 6, 0, 0]}
                                        />
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>
                        </CardContent>
                    </Card>
                </motion.div>

                {/* 5. Bean Usage (Tall Card) */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }}
                    className="col-span-1 row-span-2"
                >
                    <Card className="h-full bg-latte-900 text-white shadow-xl shadow-latte-900/20 rounded-[2rem] overflow-hidden border-none relative group">
                        {/* Abstract background shape */}
                        <div className="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full blur-3xl -mr-10 -mt-10 pointer-events-none" />

                        <CardHeader className="relative z-10 border-b border-white/10">
                            <CardTitle className="text-base font-bold text-white flex items-center gap-2">
                                <Coffee className="w-4 h-4 text-amber-400" />
                                인기 생두 (Top 5)
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="p-0 relative z-10">
                            <div className="divide-y divide-white/5">
                                {stats.bean_usage.slice(0, 6).map((bean, i) => (
                                    <div key={i} className="flex items-center p-4 hover:bg-white/5 transition-colors group/item cursor-default">
                                        <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-xs font-bold text-amber-400 mr-3 shrink-0 group-hover/item:bg-amber-400 group-hover/item:text-latte-900 transition-all">
                                            {i + 1}
                                        </div>
                                        <div className="space-y-0.5 flex-1 min-w-0">
                                            <p className="text-sm font-medium text-white/90 truncate" title={bean.bean_name}>
                                                {bean.bean_name}
                                            </p>
                                            <div className="flex items-center gap-2">
                                                <div className="h-1.5 flex-1 bg-white/10 rounded-full overflow-hidden">
                                                    <div className="h-full bg-amber-400/80" style={{ width: `${bean.percentage}%` }} />
                                                </div>
                                                <span className="text-[10px] text-white/50">{bean.total_output.toFixed(0)}kg</span>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                                {stats.bean_usage.length === 0 && (
                                    <div className="p-8 text-center text-white/30 text-sm">
                                        데이터 없음
                                    </div>
                                )}
                            </div>
                        </CardContent>
                    </Card>
                </motion.div>
            </div>
        </div>
    )
}
