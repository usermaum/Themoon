'use client';

import { useState, useEffect } from 'react';
import { Bean, BeanAPI } from '@/lib/api';
import { Search, RotateCcw, Calendar, Coffee } from 'lucide-react';
import { DateRangePicker } from '@/components/ui/date-range-picker';
import { DateRange } from 'react-day-picker';
import { format } from 'date-fns';

interface RoastingHistoryFiltersProps {
    onFilterChange: (filters: { start_date?: string; end_date?: string; bean_id?: number; bean_type?: string }) => void;
}

export default function RoastingHistoryFilters({ onFilterChange }: RoastingHistoryFiltersProps) {
    const [dateRange, setDateRange] = useState<DateRange | undefined>();
    const [selectedBeanId, setSelectedBeanId] = useState<number | undefined>(undefined);
    const [selectedType, setSelectedType] = useState<string>('');
    const [beans, setBeans] = useState<Bean[]>([]);

    useEffect(() => {
        // 필터용 생두/블렌드 목록 로드
        const loadBeans = async () => {
            try {
                // 생두와 블렌드 모두 조회 (로스팅 대상)
                const data = await BeanAPI.getAll({
                    limit: 100,
                    type: ['GREEN_BEAN', 'BLEND_BEAN']
                });
                setBeans(data.items);
            } catch (error) {
                console.error("Failed to load beans for filter", error);
            }
        };
        loadBeans();
    }, []);

    const handleApply = () => {
        onFilterChange({
            start_date: dateRange?.from ? format(dateRange.from, 'yyyy-MM-dd') : undefined,
            end_date: dateRange?.to ? format(dateRange.to, 'yyyy-MM-dd') : undefined,
            bean_id: selectedBeanId,
            bean_type: selectedType || undefined
        });
    };

    const handleReset = () => {
        setDateRange(undefined);
        setSelectedBeanId(undefined);
        setSelectedType('');
        onFilterChange({});
    };

    // Filter beans based on selected type for the dropdown
    const filteredBeans = beans.filter(bean => {
        if (!selectedType) return true;
        return bean.type === selectedType;
    });

    return (
        <div className="bg-white/60 backdrop-blur-md p-6 rounded-[2rem] border border-white/20 shadow-xl shadow-latte-900/5 mb-8 animate-in fade-in slide-in-from-bottom-2 duration-500 delay-200">
            <div className="flex flex-col md:flex-row gap-6 items-end">

                {/* Date Range */}
                <div className="flex-1 w-full md:w-auto">
                    <label className="block text-xs font-bold text-latte-600 uppercase tracking-wider mb-2 flex items-center gap-1.5 ml-1">
                        <Calendar className="w-3.5 h-3.5 text-latte-400" /> 조회 기간
                    </label>
                    <DateRangePicker
                        date={dateRange}
                        onSelect={setDateRange}
                        placeholder="전체 기간"
                        className="w-full"
                    />
                </div>

                {/* Bean Type Filter */}
                <div className="w-full md:w-48">
                    <label className="block text-xs font-bold text-latte-600 uppercase tracking-wider mb-2 flex items-center gap-1.5 ml-1">
                        <Coffee className="w-3.5 h-3.5 text-latte-400" /> 원두 유형
                    </label>
                    <div className="relative">
                        <select
                            value={selectedType}
                            onChange={(e) => {
                                setSelectedType(e.target.value);
                                setSelectedBeanId(undefined); // Reset bean selection when type changes
                            }}
                            className="bg-white/50 border border-latte-200 text-latte-800 text-sm rounded-xl focus:ring-2 focus:ring-latte-200 focus:border-latte-400 block w-full p-3 pr-10 appearance-none transition-shadow h-11"
                        >
                            <option value="">전체 유형</option>
                            <option value="GREEN_BEAN">싱글 오리진</option>
                            <option value="BLEND_BEAN">블렌드</option>
                        </select>
                        <div className="absolute inset-y-0 right-0 flex items-center px-3 pointer-events-none text-latte-400">
                            <Search className="w-4 h-4" />
                        </div>
                    </div>
                </div>

                {/* Bean Select */}
                <div className="flex-1 w-full md:w-auto">
                    <label className="block text-xs font-bold text-latte-600 uppercase tracking-wider mb-2 flex items-center gap-1.5 ml-1">
                        <Coffee className="w-3.5 h-3.5 text-latte-400" /> 대상 원두
                    </label>
                    <div className="relative">
                        <select
                            value={selectedBeanId || ''}
                            onChange={(e) => setSelectedBeanId(e.target.value ? Number(e.target.value) : undefined)}
                            disabled={filteredBeans.length === 0}
                            className="bg-white/50 border border-latte-200 text-latte-800 text-sm rounded-xl focus:ring-2 focus:ring-latte-200 focus:border-latte-400 block w-full p-3 pr-10 appearance-none transition-shadow disabled:opacity-50 disabled:cursor-not-allowed h-11"
                        >
                            <option value="">
                                {selectedType
                                    ? (selectedType === 'GREEN_BEAN' ? '전체 싱글 오리진' : '전체 블렌드')
                                    : '전체 생두 및 블렌드'}
                            </option>
                            {filteredBeans.map(bean => (
                                <option key={bean.id} value={bean.id}>
                                    {bean.name} ({bean.type === 'BLEND_BEAN' ? '블렌드' : '싱글'})
                                </option>
                            ))}
                        </select>
                        <div className="absolute inset-y-0 right-0 flex items-center px-3 pointer-events-none text-latte-400">
                            <Search className="w-4 h-4" />
                        </div>
                    </div>
                </div>

                {/* Actions */}
                <div className="flex gap-3 w-full md:w-auto mt-2 md:mt-0">
                    <button
                        onClick={handleApply}
                        className="flex-1 md:flex-none flex items-center justify-center gap-2 text-white bg-latte-800 hover:bg-latte-900 focus:ring-4 focus:outline-none focus:ring-latte-200 font-bold rounded-xl text-sm px-6 py-3 transition-all shadow-lg shadow-latte-900/10 hover:shadow-latte-900/20 active:scale-95 h-11"
                    >
                        <Search className="w-4 h-4" />
                        검색
                    </button>
                    <button
                        onClick={handleReset}
                        className="flex-none p-3 text-latte-500 bg-white/80 border border-latte-200 hover:bg-latte-50 focus:ring-4 focus:outline-none focus:ring-latte-50 font-medium rounded-xl text-center transition-all shadow-sm hover:text-latte-700 active:scale-95 h-11 w-11 flex items-center justify-center"
                        title="필터 초기화"
                    >
                        <RotateCcw className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>
    );
}
