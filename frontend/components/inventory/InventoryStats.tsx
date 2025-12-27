import { motion } from 'framer-motion'
import { Package, AlertTriangle, Coffee, CheckCircle2 } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'

interface InventoryStatsProps {
    totalWeight: number
    lowStockCount: number
    activeVarieties: number
    totalValue?: number // Optional: Total asset value if we calculate it
}

export default function InventoryStats({
    totalWeight,
    lowStockCount,
    activeVarieties,
}: InventoryStatsProps) {
    // Animation variants
    const container = {
        hidden: { opacity: 0 },
        show: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    }

    const item = {
        hidden: { y: 20, opacity: 0 },
        show: { y: 0, opacity: 1 }
    }

    return (
        <motion.div
            variants={container}
            initial="hidden"
            animate="show"
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-6 sm:mb-8"
        >
            {/* Total Stock Weight */}
            <motion.div variants={item}>
                <Card className="bg-white/60 backdrop-blur-md border border-latte-200 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden group">
                    <div className="absolute top-0 right-0 w-24 h-24 bg-latte-100 rounded-full -mr-8 -mt-8 opacity-20 group-hover:scale-110 transition-transform" />
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-latte-100 rounded-lg text-latte-600">
                                <Package className="w-6 h-6" />
                            </div>
                            <span className="text-xs font-bold px-2 py-1 bg-green-100 text-green-700 rounded-full">
                                정상
                            </span>
                        </div>
                        <div className="space-y-1">
                            <h3 className="text-sm font-medium text-latte-500">총 재고량</h3>
                            <div className="text-2xl font-serif font-bold text-latte-900">
                                {totalWeight.toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 1 })}
                                <span className="text-sm font-sans font-normal text-latte-400 ml-1">kg</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </motion.div>

            {/* Low Stock Alerts */}
            <motion.div variants={item}>
                <Card className={`bg-white/60 backdrop-blur-md border shadow-sm hover:shadow-md transition-shadow relative overflow-hidden group ${lowStockCount > 0 ? 'border-red-200' : 'border-latte-200'}`}>
                    <div className={`absolute top-0 right-0 w-24 h-24 rounded-full -mr-8 -mt-8 opacity-20 group-hover:scale-110 transition-transform ${lowStockCount > 0 ? 'bg-red-200' : 'bg-latte-100'}`} />
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between mb-4">
                            <div className={`p-2 rounded-lg ${lowStockCount > 0 ? 'bg-red-100 text-red-600' : 'bg-latte-100 text-latte-600'}`}>
                                <AlertTriangle className="w-6 h-6" />
                            </div>
                            {lowStockCount > 0 && (
                                <span className="text-xs font-bold px-2 py-1 bg-red-100 text-red-700 rounded-full animate-pulse">
                                    확인 필요
                                </span>
                            )}
                        </div>
                        <div className="space-y-1">
                            <h3 className="text-sm font-medium text-latte-500">재고 부족 품목</h3>
                            <div className="text-2xl font-serif font-bold text-latte-900">
                                {lowStockCount}
                                <span className="text-sm font-sans font-normal text-latte-400 ml-1">건</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </motion.div>

            {/* Active Varieties */}
            <motion.div variants={item}>
                <Card className="bg-white/60 backdrop-blur-md border border-latte-200 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden group">
                    <div className="absolute top-0 right-0 w-24 h-24 bg-amber-100 rounded-full -mr-8 -mt-8 opacity-20 group-hover:scale-110 transition-transform" />
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-amber-100 rounded-lg text-amber-600">
                                <Coffee className="w-6 h-6" />
                            </div>
                        </div>
                        <div className="space-y-1">
                            <h3 className="text-sm font-medium text-latte-500">보유 원두 종</h3>
                            <div className="text-2xl font-serif font-bold text-latte-900">
                                {activeVarieties}
                                <span className="text-sm font-sans font-normal text-latte-400 ml-1">종</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </motion.div>

            {/* System Health / Message */}
            <motion.div variants={item}>
                <Card className="bg-gradient-to-br from-latte-800 to-latte-900 border-none shadow-md text-white relative overflow-hidden group">
                    <div className="absolute top-0 right-0 w-32 h-32 bg-white rounded-full -mr-10 -mt-10 opacity-10 group-hover:scale-110 transition-transform" />
                    <CardContent className="p-6 flex flex-col justify-between h-full">
                        <div className="flex items-center gap-2 mb-2 opacity-80">
                            <CheckCircle2 className="w-5 h-5" />
                            <span className="text-sm font-medium">재고 시스템 정상</span>
                        </div>
                        <div>
                            <p className="text-latte-200 text-sm leading-snug">
                                모든 재고 입출고 기록이<br /> 정상적으로 동기화되었습니다.
                            </p>
                        </div>
                    </CardContent>
                </Card>
            </motion.div>
        </motion.div>
    )
}
