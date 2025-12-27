'use client';

import { useState, useEffect } from 'react';
import { RoastingLogDetail, RoastingAPI } from '@/lib/api';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';
import {
    X,
    Calendar,
    Scale,
    TrendingDown,
    Coffee,
    FileText,
    ArrowDownRight,
    ArrowUpRight,
    Loader2,
    DollarSign,
    Package
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface RoastingDetailModalProps {
    logId: number | null;
    onClose: () => void;
}

export default function RoastingDetailModal({ logId, onClose }: RoastingDetailModalProps) {
    const [log, setLog] = useState<RoastingLogDetail | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (logId) {
            loadDetail(logId);
        } else {
            setLog(null);
        }
    }, [logId]);

    async function loadDetail(id: number) {
        setLoading(true);
        try {
            const data = await RoastingAPI.getLog(id) as RoastingLogDetail;
            setLog(data);
        } catch (error) {
            console.error('Failed to load roasting detail:', error);
        } finally {
            setLoading(false);
        }
    }

    if (!logId) return null;

    return (
        <AnimatePresence>
            <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
                {/* Backdrop */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    onClick={onClose}
                    className="absolute inset-0 bg-latte-900/60 backdrop-blur-sm"
                />

                {/* Modal Container */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.95, y: 20 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.95, y: 20 }}
                    className="relative w-full max-w-2xl bg-white rounded-[2.5rem] shadow-2xl overflow-hidden border border-latte-100"
                >
                    {/* Header Image/Pattern Area */}
                    <div className="h-32 bg-gradient-to-br from-amber-100/50 to-latte-100/50 relative overflow-hidden">
                        <div className="absolute top-6 right-6 z-10">
                            <button
                                onClick={onClose}
                                className="p-2.5 bg-white/80 hover:bg-white rounded-full text-latte-400 hover:text-latte-600 transition-all shadow-sm backdrop-blur-md"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </div>
                        <div className="absolute -bottom-8 -left-8 w-32 h-32 bg-amber-500/10 rounded-full blur-2xl" />
                        <div className="absolute top-0 right-1/4 w-48 h-48 bg-latte-200/20 rounded-full blur-3xl" />
                    </div>

                    {/* Content */}
                    <div className="px-8 pb-10 -mt-10 overflow-y-auto max-h-[calc(100vh-12rem)] scrollbar-hide">
                        {loading ? (
                            <div className="flex flex-col items-center justify-center py-20">
                                <Loader2 className="w-10 h-10 animate-spin text-amber-500 mb-4" />
                                <p className="text-latte-500 font-medium font-serif">생산 상세 정보를 가져오는 중...</p>
                            </div>
                        ) : log ? (
                            <div className="space-y-8">
                                {/* Batch Title & Date */}
                                <div className="space-y-2">
                                    <div className="flex items-center gap-3">
                                        <span className="px-3 py-1 bg-amber-100 text-amber-700 text-[10px] font-black uppercase tracking-widest rounded-full border border-amber-200">
                                            {log.batch_no}
                                        </span>
                                        <div className="flex items-center gap-1.5 text-latte-400 text-xs font-semibold">
                                            <Calendar className="w-3.5 h-3.5" />
                                            {format(new Date(log.roast_date), 'yyyy년 MM월 dd일 HH:mm', { locale: ko })}
                                        </div>
                                    </div>
                                    <h2 className="text-3xl font-serif font-bold text-latte-900 tracking-tight">
                                        {log.target_bean?.name || 'Unknown Roasted Bean'}
                                    </h2>
                                </div>

                                {/* Key Metrics Grid */}
                                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                    <div className="p-4 bg-latte-50/50 rounded-2xl border border-latte-100 flex flex-col items-center gap-1">
                                        <Scale className="w-4 h-4 text-latte-400" />
                                        <span className="text-[10px] font-bold text-latte-400 uppercase tracking-tighter">Production</span>
                                        <span className="text-lg font-bold font-mono text-latte-900">{log.output_weight_total.toFixed(1)}kg</span>
                                    </div>
                                    <div className="p-4 bg-latte-50/50 rounded-2xl border border-latte-100 flex flex-col items-center gap-1">
                                        <TrendingDown className="w-4 h-4 text-amber-500" />
                                        <span className="text-[10px] font-bold text-latte-400 uppercase tracking-tighter">Loss Rate</span>
                                        <span className="text-lg font-bold font-mono text-amber-600">{log.loss_rate?.toFixed(1)}%</span>
                                    </div>
                                    <div className="p-4 bg-latte-50/50 rounded-2xl border border-latte-100 flex flex-col items-center gap-1">
                                        <DollarSign className="w-4 h-4 text-green-600" />
                                        <span className="text-[10px] font-bold text-latte-400 uppercase tracking-tighter">Cost / Kg</span>
                                        <span className="text-lg font-bold font-mono text-green-700">₩{(log.production_cost || 0).toLocaleString()}</span>
                                    </div>
                                    <div className="p-4 bg-latte-50/50 rounded-2xl border border-latte-100 flex flex-col items-center gap-1">
                                        <Package className="w-4 h-4 text-latte-400" />
                                        <span className="text-[10px] font-bold text-latte-400 uppercase tracking-tighter">SKU</span>
                                        <span className="text-xs font-bold font-mono text-latte-600 truncate max-w-full">{log.target_bean?.sku || 'N/A'}</span>
                                    </div>
                                </div>

                                {/* Environmental Conditions (New) */}
                                {(log.roasting_time || log.ambient_temp || log.humidity) && (
                                    <div className="grid grid-cols-3 gap-4">
                                        <div className="p-3 bg-white rounded-xl border border-latte-100 flex items-center justify-center gap-3 shadow-sm">
                                            <div className="p-2 rounded-full bg-blue-50 text-blue-500">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10" /><polyline points="12 6 12 12 16 14" /></svg>
                                            </div>
                                            <div className="flex flex-col">
                                                <span className="text-[10px] font-bold text-latte-400 uppercase">Duration</span>
                                                <span className="text-sm font-bold font-mono text-latte-700">
                                                    {log.roasting_time ? `${Math.floor(log.roasting_time / 60)}m ${log.roasting_time % 60}s` : '-'}
                                                </span>
                                            </div>
                                        </div>
                                        <div className="p-3 bg-white rounded-xl border border-latte-100 flex items-center justify-center gap-3 shadow-sm">
                                            <div className="p-2 rounded-full bg-orange-50 text-orange-500">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z" /></svg>
                                            </div>
                                            <div className="flex flex-col">
                                                <span className="text-[10px] font-bold text-latte-400 uppercase">Temp</span>
                                                <span className="text-sm font-bold font-mono text-latte-700">
                                                    {log.ambient_temp ? `${log.ambient_temp}℃` : '-'}
                                                </span>
                                            </div>
                                        </div>
                                        <div className="p-3 bg-white rounded-xl border border-latte-100 flex items-center justify-center gap-3 shadow-sm">
                                            <div className="p-2 rounded-full bg-cyan-50 text-cyan-500">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z" /></svg>
                                            </div>
                                            <div className="flex flex-col">
                                                <span className="text-[10px] font-bold text-latte-400 uppercase">Humidity</span>
                                                <span className="text-sm font-bold font-mono text-latte-700">
                                                    {log.humidity ? `${log.humidity}%` : '-'}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                )}

                                {/* Production Flow (Input -> Output) */}
                                <div className="space-y-4">
                                    <h4 className="text-sm font-bold text-latte-400 uppercase tracking-widest flex items-center gap-2">
                                        <Coffee className="w-4 h-4" /> Production Flow
                                    </h4>
                                    <div className="bg-latte-50/30 rounded-3xl p-6 border border-latte-100 space-y-6 relative">
                                        {/* Inputs Section */}
                                        <div className="space-y-4">
                                            <div className="flex items-center gap-2 text-xs font-bold text-latte-400">
                                                <ArrowDownRight className="w-3.5 h-3.5 text-amber-500" />
                                                투입 원료 (Input)
                                            </div>
                                            <div className="space-y-3">
                                                {log.inventory_logs?.filter(il => il.change_amount < 0).map((il) => (
                                                    <div key={il.id} className="flex items-center justify-between p-3 bg-white rounded-xl border border-latte-100 shadow-sm">
                                                        <div className="flex items-center gap-3">
                                                            <div className="w-2 h-2 rounded-full bg-amber-400" />
                                                            <span className="text-sm font-bold text-latte-800">{il.bean?.name || 'Unknown Bean'}</span>
                                                        </div>
                                                        <span className="text-sm font-bold font-mono text-amber-600">{Math.abs(il.change_amount).toFixed(2)}kg</span>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>

                                        {/* Divider with Center Arrow */}
                                        <div className="flex items-center justify-center">
                                            <div className="h-px flex-1 bg-latte-100" />
                                            <div className="mx-4 p-2 bg-white rounded-full border border-latte-100 shadow-inner">
                                                <div className="w-2 h-2 rounded-full bg-latte-200 animate-pulse" />
                                            </div>
                                            <div className="h-px flex-1 bg-latte-100" />
                                        </div>

                                        {/* Output Section */}
                                        <div className="space-y-4">
                                            <div className="flex items-center gap-2 text-xs font-bold text-latte-400">
                                                <ArrowUpRight className="w-3.5 h-3.5 text-green-500" />
                                                생산 완료 (Output)
                                            </div>
                                            <div className="flex items-center justify-between p-3 bg-amber-50/50 rounded-xl border border-amber-100 shadow-sm">
                                                <div className="flex items-center gap-3">
                                                    <div className="w-2 h-2 rounded-full bg-green-500" />
                                                    <span className="text-sm font-bold text-amber-900">{log.target_bean?.name}</span>
                                                </div>
                                                <span className="text-sm font-bold font-mono text-green-700">+{log.output_weight_total.toFixed(2)}kg</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                {/* Notes Section */}
                                {log.notes && (
                                    <div className="space-y-3">
                                        <h4 className="text-sm font-bold text-latte-400 uppercase tracking-widest flex items-center gap-2">
                                            <FileText className="w-4 h-4" /> Production Notes
                                        </h4>
                                        <div className="p-5 bg-latte-50/50 rounded-2xl border border-latte-100">
                                            <p className="text-sm text-latte-600 leading-relaxed italic">
                                                "{log.notes}"
                                            </p>
                                        </div>
                                    </div>
                                )}
                            </div>
                        ) : (
                            <div className="py-20 text-center">
                                <p className="text-latte-400">정보를 불러올 수 없습니다.</p>
                            </div>
                        )}
                    </div>

                    {/* Footer */}
                    <div className="p-6 bg-latte-50/50 border-t border-latte-100 flex justify-end">
                        <button
                            onClick={onClose}
                            className="px-6 py-2.5 bg-latte-900 hover:bg-black text-white rounded-full text-sm font-bold transition-all shadow-md active:scale-95"
                        >
                            닫기
                        </button>
                    </div>
                </motion.div>
            </div>
        </AnimatePresence>
    );
}
