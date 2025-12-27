"use client"

import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { RoastingDashboard } from "@/components/roasting/RoastingDashboard"
import MascotStatus from "@/components/ui/mascot-status"
import { RoastingLog, RoastingAPI } from "@/lib/api"
import { format } from "date-fns"
import { ko } from "date-fns/locale"
import Link from "next/link"
import {
    Flame,
    ArrowRight,
    Activity,
    Wifi,
    Package,
    History,
    ChevronRight,
    Plus,
    Coffee,
    Clock
} from "lucide-react"

export function RoastingConsole() {
    const [recentLogs, setRecentLogs] = useState<RoastingLog[]>([])

    useEffect(() => {
        // Fetch limited history for the "Mini list"
        RoastingAPI.getHistory({ limit: 4 }).then(setRecentLogs).catch(console.error)
        console.log("Rendering RoastingConsole component...");
    }, [])

    return (
        <div className="min-h-screen bg-[#F8F5F2] text-latte-900 font-sans rounded-3xl overflow-hidden border border-latte-100 shadow-xl">
            {/* 1. Header & Status Bar */}
            <header className="bg-white border-b border-latte-100 sticky top-0 z-20 shadow-sm">
                <div className="max-w-[1600px] mx-auto">
                    <div className="flex items-center justify-between px-6 h-16">
                        <div className="flex items-center gap-3">
                            <div className="bg-latte-900 p-2 rounded-lg">
                                <Flame className="w-5 h-5 text-white" />
                            </div>
                            <h1 className="text-xl font-serif font-bold text-latte-900 tracking-tight">
                                Roasting Console
                                <span className="ml-2 text-[10px] bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-sans">Testnet</span>
                            </h1>
                        </div>

                        {/* Mock System Status */}
                        <div className="flex items-center gap-6 text-xs font-medium text-latte-500 bg-latte-50/50 px-4 py-2 rounded-full border border-latte-100/50">
                            <div className="flex items-center gap-2">
                                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                                <span>System Online</span>
                            </div>
                            <div className="w-px h-3 bg-latte-200" />
                            <div className="flex items-center gap-2">
                                <Wifi className="w-3.5 h-3.5" />
                                <span>Connected</span>
                            </div>
                            <div className="w-px h-3 bg-latte-200" />
                            <div className="flex items-center gap-2">
                                <Activity className="w-3.5 h-3.5" />
                                <span>Idle (24°C)</span>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            {/* 2. Main Dashboard Grid */}
            <main className="max-w-[1600px] mx-auto p-6 bg-[#F8F5F2]">
                <div className="grid grid-cols-1 xl:grid-cols-12 gap-6 items-start h-[calc(100vh-140px)]">

                    {/* Left Column: Analytics (Visuals) - Spans 7 cols */}
                    <div className="xl:col-span-7 flex flex-col gap-6 h-full overflow-hidden">
                        {/* Dashboard Component Wrapper */}
                        <section className="bg-white/60 backdrop-blur-sm rounded-2xl border border-latte-200/60 p-1 shadow-sm h-full overflow-y-auto custom-scrollbar">
                            <RoastingDashboard />
                        </section>
                    </div>

                    {/* Right Column: Operations (Controls) - Spans 5 cols */}
                    <div className="xl:col-span-5 flex flex-col gap-6 h-full">

                        {/* Quick Actions Panel */}
                        <section className="grid grid-cols-2 gap-4">
                            <Link
                                href="/roasting/single-origin"
                                className="group relative flex flex-col justify-between p-6 bg-white rounded-2xl shadow-sm border border-latte-100 hover:border-latte-300 hover:shadow-md transition-all duration-300 h-40 overflow-hidden"
                            >
                                <div className="absolute right-0 top-0 w-32 h-32 bg-gradient-to-br from-latte-100/50 to-transparent rounded-full -mr-10 -mt-10 group-hover:scale-110 transition-transform" />

                                <div className="relative z-10">
                                    <div className="w-10 h-10 bg-latte-50 rounded-xl flex items-center justify-center mb-3 group-hover:bg-latte-900 group-hover:text-white transition-colors">
                                        <Coffee className="w-5 h-5" />
                                    </div>
                                    <h3 className="font-bold text-lg text-latte-900">Single Origin</h3>
                                </div>

                                <div className="relative z-10 flex items-center text-sm font-medium text-latte-500 group-hover:text-latte-900">
                                    New Roast <ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                                </div>
                            </Link>

                            <Link
                                href="/roasting/blend"
                                className="group relative flex flex-col justify-between p-6 bg-white rounded-2xl shadow-sm border border-latte-100 hover:border-latte-300 hover:shadow-md transition-all duration-300 h-40 overflow-hidden"
                            >
                                <div className="absolute right-0 top-0 w-32 h-32 bg-gradient-to-br from-amber-50 to-transparent rounded-full -mr-10 -mt-10 group-hover:scale-110 transition-transform" />

                                <div className="relative z-10">
                                    <div className="w-10 h-10 bg-amber-50 rounded-xl flex items-center justify-center mb-3 group-hover:bg-amber-500 group-hover:text-white transition-colors">
                                        <Package className="w-5 h-5 text-amber-600 group-hover:text-white" />
                                    </div>
                                    <h3 className="font-bold text-lg text-latte-900">Blend Roast</h3>
                                </div>

                                <div className="relative z-10 flex items-center text-sm font-medium text-latte-500 group-hover:text-latte-900">
                                    Create Batch <ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                                </div>
                            </Link>
                        </section>

                        {/* Recent Batches List (Compact) */}
                        <section className="flex-1 bg-white rounded-2xl border border-latte-200 shadow-sm flex flex-col overflow-hidden">
                            <div className="px-6 py-4 border-b border-latte-100 flex items-center justify-between bg-latte-50/30">
                                <h3 className="font-bold text-latte-900 flex items-center gap-2">
                                    <History className="w-4 h-4 text-latte-400" />
                                    Recent Activity
                                </h3>
                                <Link href="/roasting" className="text-xs font-semibold text-latte-500 hover:text-latte-800 flex items-center">
                                    View All <ChevronRight className="w-3 h-3" />
                                </Link>
                            </div>

                            <div className="flex-1 overflow-y-auto p-2 space-y-2 custom-scrollbar">
                                {recentLogs.map((log) => (
                                    <motion.div
                                        key={log.id}
                                        initial={{ opacity: 0, y: 5 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        className="p-3 hover:bg-latte-50/50 rounded-xl transition-colors border border-transparent hover:border-latte-100 group"
                                    >
                                        <div className="flex justify-between items-start mb-1">
                                            <div className="flex flex-col">
                                                <span className="text-[10px] font-bold text-latte-400 font-mono tracking-tight">{log.batch_no}</span>
                                                <h4 className="font-bold text-sm text-latte-900 line-clamp-1">{log.target_bean?.name}</h4>
                                            </div>
                                            <span className="text-xs font-mono font-medium bg-latte-100 text-latte-700 px-2 py-0.5 rounded-md">
                                                {log.output_weight_total}kg
                                            </span>
                                        </div>

                                        <div className="flex items-center justify-between text-xs text-latte-400">
                                            <span className="flex items-center gap-1">
                                                <Clock className="w-3 h-3" />
                                                {format(new Date(log.roast_date), "MM.dd HH:mm")}
                                            </span>
                                            {log.loss_rate && (
                                                <span className={`font-medium ${log.loss_rate > 15 ? 'text-red-500' : 'text-amber-600'}`}>
                                                    Loss: {log.loss_rate.toFixed(1)}%
                                                </span>
                                            )}
                                        </div>
                                    </motion.div>
                                ))}

                                {recentLogs.length === 0 && (
                                    <div className="h-full flex flex-col items-center justify-center p-6">
                                        <MascotStatus
                                            variant="empty"
                                            title="기록 없음"
                                            description="최근 로스팅 이력이 없습니다."
                                            className="transform scale-75"
                                            videoClassName="w-24 h-24"
                                        />
                                    </div>
                                )}
                            </div>
                        </section>
                    </div>

                </div>
            </main>

            <style jsx global>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background-color: rgba(168, 139, 125, 0.2);
          border-radius: 20px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background-color: rgba(168, 139, 125, 0.4);
        }
      `}</style>
        </div>
    )
}
