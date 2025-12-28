'use client';

import { useState, useEffect } from 'react';
import { RoastingLog, RoastingAPI } from '@/lib/api';
import { History } from 'lucide-react';
import { RoastingHistoryTable } from './RoastingHistoryTable';
import RoastingDetailModal from './RoastingDetailModal';
import { RoastingHistoryParams } from '@/lib/api';

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

    // Handle filter changes from the Table component
    const handleFilterChange = (newFilters: any) => {
        setFilters(prev => ({ ...prev, ...newFilters }));
        setLimit(20); // Reset pagination
    };

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between mb-4">
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

            {/* New Table Component with Integrated Filters */}
            <RoastingHistoryTable
                logs={logs}
                loading={loading}
                onFilterChange={handleFilterChange}
                onRowClick={(log) => setSelectedLogId(log.id)}
            />

            <div className="flex justify-center mt-4 text-xs text-muted-foreground">
                <p>최근 100건의 이력만 표시됩니다. 더 많은 데이터를 보려면 필터를 사용하세요.</p>
            </div>

            <RoastingDetailModal
                logId={selectedLogId}
                onClose={() => setSelectedLogId(null)}
            />
        </div>
    );
}
