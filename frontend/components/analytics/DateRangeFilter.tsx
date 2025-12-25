'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Calendar } from 'lucide-react';

interface DateRangeFilterProps {
  onDateChange: (startDate: string | null, endDate: string | null) => void;
}

export function DateRangeFilter({ onDateChange }: DateRangeFilterProps) {
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const [activePreset, setActivePreset] = useState<string>('all');

  const handlePreset = (preset: string) => {
    console.log('handlePreset called:', preset);
    setActivePreset(preset);
    const today = new Date();
    let start: Date | null = null;

    switch (preset) {
      case '30days':
        start = new Date(today);
        start.setDate(today.getDate() - 30);
        break;
      case '3months':
        start = new Date(today);
        start.setMonth(today.getMonth() - 3);
        break;
      case '6months':
        start = new Date(today);
        start.setMonth(today.getMonth() - 6);
        break;
      case '1year':
        start = new Date(today);
        start.setFullYear(today.getFullYear() - 1);
        break;
      case 'all':
        setStartDate('');
        setEndDate('');
        onDateChange(null, null);
        return;
    }

    if (start) {
      const startStr = start.toISOString().split('T')[0];
      const endStr = today.toISOString().split('T')[0];

      // UI Update
      setStartDate(startStr);
      setEndDate(endStr);

      // Parent Callback
      onDateChange(startStr, endStr);
    }
  };

  const handleCustomDate = () => {
    setActivePreset('custom');
    if (startDate && endDate) {
      onDateChange(startDate, endDate);
    } else if (!startDate && !endDate) {
      onDateChange(null, null);
    }
  };

  const handleReset = () => {
    setStartDate('');
    setEndDate('');
    setActivePreset('all');
    onDateChange(null, null);
  };

  return (
    <Card className="rounded-[1em]">
      <CardContent className="pt-6">
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Calendar className="h-4 w-4 text-muted-foreground" />
            <h3 className="text-sm font-medium">기간 선택</h3>
          </div>

          <div className="flex flex-col xl:flex-row xl:items-center gap-6">
            {/* Left: Presets */}
            <div className="flex flex-wrap gap-2">
              <Button
                size="sm"
                variant={activePreset === 'all' ? 'secondary' : 'ghost'}
                className={`rounded-full px-4 ${activePreset === 'all' ? 'bg-stone-800 text-white hover:bg-stone-700' : 'bg-[#FFF9F2] border border-[#F5E6D3] text-stone-600 hover:bg-[#F5E6D3]'}`}
                onClick={() => handlePreset('all')}
              >
                전체
              </Button>
              <Button
                size="sm"
                variant={activePreset === '30days' ? 'secondary' : 'ghost'}
                className={`rounded-full px-4 ${activePreset === '30days' ? 'bg-stone-800 text-white hover:bg-stone-700' : 'bg-[#FFF9F2] border border-[#F5E6D3] text-stone-600 hover:bg-[#F5E6D3]'}`}
                onClick={() => handlePreset('30days')}
              >
                최근 30일
              </Button>
              <Button
                size="sm"
                variant={activePreset === '3months' ? 'secondary' : 'ghost'}
                className={`rounded-full px-4 ${activePreset === '3months' ? 'bg-stone-800 text-white hover:bg-stone-700' : 'bg-[#FFF9F2] border border-[#F5E6D3] text-stone-600 hover:bg-[#F5E6D3]'}`}
                onClick={() => handlePreset('3months')}
              >
                최근 3개월
              </Button>
              <Button
                size="sm"
                variant={activePreset === '6months' ? 'secondary' : 'ghost'}
                className={`rounded-full px-4 ${activePreset === '6months' ? 'bg-stone-800 text-white hover:bg-stone-700' : 'bg-[#FFF9F2] border border-[#F5E6D3] text-stone-600 hover:bg-[#F5E6D3]'}`}
                onClick={() => handlePreset('6months')}
              >
                최근 6개월
              </Button>
              <Button
                size="sm"
                variant={activePreset === '1year' ? 'secondary' : 'ghost'}
                className={`rounded-full px-4 ${activePreset === '1year' ? 'bg-stone-800 text-white hover:bg-stone-700' : 'bg-[#FFF9F2] border border-[#F5E6D3] text-stone-600 hover:bg-[#F5E6D3]'}`}
                onClick={() => handlePreset('1year')}
              >
                최근 1년
              </Button>
            </div>

            {/* Separator (Desktop Only) */}
            <div className="hidden xl:block h-5 w-px bg-stone-200" />

            {/* Right: Date Inputs & Reset */}
            <div className="flex flex-wrap items-center gap-4">
              <div className="flex items-center gap-2">
                <label className="text-sm text-stone-500 whitespace-nowrap">시작일</label>
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => {
                    const newStart = e.target.value;
                    setStartDate(newStart);
                    setActivePreset('custom');
                    if (newStart && endDate) {
                      onDateChange(newStart, endDate);
                    }
                  }}
                  className="w-[140px] rounded-full border border-[#F5E6D3] bg-[#FFF9F2] px-4 py-1.5 text-sm text-stone-700 focus:outline-none focus:ring-1 focus:ring-stone-400"
                />
              </div>
              <div className="flex items-center gap-2">
                <label className="text-sm text-stone-500 whitespace-nowrap">종료일</label>
                <input
                  type="date"
                  value={endDate}
                  onChange={(e) => {
                    const newEnd = e.target.value;
                    setEndDate(newEnd);
                    setActivePreset('custom');
                    if (startDate && newEnd) {
                      onDateChange(startDate, newEnd);
                    }
                  }}
                  className="w-[140px] rounded-full border border-[#F5E6D3] bg-[#FFF9F2] px-4 py-1.5 text-sm text-stone-700 focus:outline-none focus:ring-1 focus:ring-stone-400"
                />
              </div>
              <Button
                size="sm"
                variant="outline"
                onClick={handleReset}
                className="rounded-full px-5 bg-[#FFF9F2] border border-[#F5E6D3] text-stone-600 hover:bg-[#F5E6D3]"
              >
                초기화
              </Button>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
