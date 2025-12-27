'use client';

import { useState, useEffect } from 'react';
import { RoastingLog, RoastingAPI } from '@/lib/api';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';
import {
    History,
    Calendar,
    Scale,
    TrendingDown,
    ChevronRight,
    Loader2
} from 'lucide-react';
import { motion } from 'framer-motion';
import MascotStatus from '@/components/ui/mascot-status';
import RoastingDetailModal from './RoastingDetailModal';
import RoastingHistoryFilters from './RoastingHistoryFilters';
import { RoastingHistoryParams } from '@/lib/api'; // Ensure params interface is available


export default function RoastingHistory() {
    const [logs, setLogs] = useState<RoastingLog[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedLogId, setSelectedLogId] = useState<number | null>(null);
    const [filters, setFilters] = useState<RoastingHistoryParams>({});

    const [limit, setLimit] = useState(20);
    const [hasMore, setHasMore] = useState(true);

    const fetchLogs = async (currentFilters: RoastingHistoryParams = {}, currentLimit: number) => {
        setLoading(true);
        try {
            const params = { limit: currentLimit, ...currentFilters };
            const data = await RoastingAPI.getHistory(params);
            setLogs(data);
            // If we received fewer items than requested, we've reached the end
            setHasMore(data.length === currentLimit);
        } catch (error) {
            console.error("Failed to fetch roasting logs", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchLogs(filters, limit);
    }, [filters, limit]);

    const handleFilterChange = (newFilters: RoastingHistoryParams) => {
        setFilters(newFilters);
        setLimit(20); // Reset limit when filter changes
    };

    const handleLoadMore = () => {
        setLimit(prev => prev + 20);
    };

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between mb-2 gap-4">
                <h2 className="text-2xl font-serif font-bold text-latte-900 flex items-center gap-3">
                    <History className="w-6 h-6 text-latte-400" />
                    생산 이력 조회
                </h2>
                <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-latte-400 uppercase tracking-widest bg-latte-50 px-3 py-1 rounded-full border border-latte-100">
                        {loading ? '업데이트 중...' : `총 ${logs.length}건`}
                    </span>
                </div>
            </div>

            <RoastingHistoryFilters onFilterChange={handleFilterChange} />

            <div className="grid grid-cols-1 gap-4">
                {logs.length > 0 ? (
                    logs.map((log, index) => (
                        <motion.div
                            key={log.id}
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.05 }}
                            onClick={() => setSelectedLogId(log.id)}
                            className="group relative bg-white hover:bg-latte-50/50 rounded-2xl p-5 border border-latte-100 shadow-sm transition-all duration-300 hover:shadow-md hover:border-latte-200 cursor-pointer"
                        >
                            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                                {/* Batch Info */}
                                <div className="flex items-center gap-4">
                                    <div className="flex flex-col">
                                        <div className="flex items-center gap-2 mb-1">
                                            <span className="text-xs font-bold text-latte-400 font-mono">
                                                {log.batch_no}
                                            </span>
                                            {log.roast_profile && (
                                                <span className={`
                                                    text-[10px] font-bold px-1.5 py-0.5 rounded-md border
                                                    ${log.roast_profile === 'LIGHT' ? 'bg-lime-50 text-lime-700 border-lime-200' :
                                                        log.roast_profile === 'DARK' ? 'bg-slate-100 text-slate-700 border-slate-200' :
                                                            'bg-orange-50 text-orange-700 border-orange-200'}
                                                `}>
                                                    {log.roast_profile}
                                                </span>
                                            )}
                                        </div>
                                        <h3 className="text-lg font-bold text-latte-900 group-hover:text-amber-900 transition-colors">
                                            {log.target_bean?.name || '알 수 없는 원두'}
                                        </h3>
                                        <div className="flex items-center gap-3 mt-1 text-latte-500 text-xs">
                                            <span className="flex items-center gap-1 font-medium">
                                                <Calendar className="w-3.5 h-3.5" />
                                                {format(new Date(log.roast_date), 'yyyy년 MM월 dd일 HH:mm', { locale: ko })}
                                            </span>
                                        </div>
                                    </div>
                                </div>

                                {/* Stats Summary */}
                                <div className="flex items-center gap-6 md:gap-8 bg-latte-50/50 md:bg-transparent p-3 md:p-0 rounded-xl">
                                    <div className="flex flex-col items-center md:items-end">
                                        <span className="text-[10px] uppercase font-bold text-latte-400 tracking-tighter mb-1 select-none flex items-center gap-1">
                                            <Scale className="w-3 h-3" /> 생산량
                                        </span>
                                        <span className="text-lg font-bold font-mono text-latte-700">
                                            {log.output_weight_total.toFixed(1)}kg
                                        </span>
                                    </div>

                                    <div className="w-px h-8 bg-latte-100 hidden md:block" />

                                    <div className="flex flex-col items-center md:items-end">
                                        <span className="text-[10px] uppercase font-bold text-latte-400 tracking-tighter mb-1 select-none flex items-center gap-1">
                                            <TrendingDown className="w-3 h-3 text-amber-500" /> 손실률
                                        </span>
                                        <span className="text-lg font-bold font-mono text-amber-600">
                                            {log.loss_rate?.toFixed(1)}%
                                        </span>
                                    </div>

                                    <div className="flex items-center justify-center p-2 rounded-full bg-white md:bg-latte-100 group-hover:bg-amber-100 text-latte-300 md:text-latte-400 group-hover:text-amber-600 transition-all duration-300 ml-2">
                                        <ChevronRight className="w-5 h-5" />
                                    </div>
                                </div>
                            </div>

                            {/* Tag or Notes indicator if any */}
                            {log.notes && (
                                <div className="mt-3 pt-3 border-t border-latte-50/50 flex items-center gap-2">
                                    <div className="w-1 h-1 rounded-full bg-latte-300" />
                                    <p className="text-xs text-latte-400 italic line-clamp-1">
                                        {log.notes}
                                    </p>
                                </div>
                            )}
                        </motion.div>
                    ))
                ) : (
                    <MascotStatus
                        variant="search"
                        title="검색 결과가 없습니다"
                        description="다른 기간이나 생두를 선택해보세요."
                    />
                )}
            </div>

            {hasMore && (
                <div className="flex justify-center mt-8">
                    <button
                        onClick={handleLoadMore}
                        disabled={loading}
                        className="text-sm font-bold text-latte-400 hover:text-latte-600 flex items-center gap-2 transition-colors disabled:opacity-50"
                    >
                        {loading ? (
                            <>
                                <Loader2 className="w-4 h-4 animate-spin" /> 로딩 중...
                            </>
                        ) : (
                            <>
                                더 보기 <ChevronRight className="w-4 h-4" />
                            </>
                        )}
                    </button>
                </div>
            )}

            {/* Detail Modal */}
            <RoastingDetailModal
                logId={selectedLogId}
                onClose={() => setSelectedLogId(null)}
            />
        </div>
    );
}
