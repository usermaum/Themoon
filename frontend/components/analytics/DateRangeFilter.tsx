'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Calendar, RotateCcw } from 'lucide-react';
import { DateRangePicker } from '@/components/ui/date-range-picker';
import { DateRange } from 'react-day-picker';
import { format } from 'date-fns';

interface DateRangeFilterProps {
  onDateChange: (startDate: string | null, endDate: string | null) => void;
}

export function DateRangeFilter({ onDateChange }: DateRangeFilterProps) {
  const [dateRange, setDateRange] = useState<DateRange | undefined>(undefined);
  const [activePreset, setActivePreset] = useState<string>('all');

  const handlePreset = (preset: string) => {
    setActivePreset(preset);
    const today = new Date();
    let start: Date | null = null;
    const end = today;

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
        setDateRange(undefined);
        onDateChange(null, null);
        return;
    }

    if (start) {
      const newRange: DateRange = { from: start, to: end };
      setDateRange(newRange);

      const startStr = format(start, 'yyyy-MM-dd');
      const endStr = format(end, 'yyyy-MM-dd');
      onDateChange(startStr, endStr);
    }
  };

  const handleDateSelect = (range: DateRange | undefined) => {
    setDateRange(range);
    setActivePreset('custom');

    if (range?.from && range?.to) {
      const startStr = format(range.from, 'yyyy-MM-dd');
      const endStr = format(range.to, 'yyyy-MM-dd');
      onDateChange(startStr, endStr);
    } else if (!range) {
      onDateChange(null, null);
    }
  };

  const handleReset = () => {
    setDateRange(undefined);
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

            {/* Right: Date Picker & Reset */}
            <div className="flex flex-wrap items-center gap-4 flex-1">
              <div className="w-[300px]">
                <DateRangePicker
                  date={dateRange}
                  onSelect={handleDateSelect}
                  placeholder="기간 직접 선택"
                />
              </div>
              <Button
                size="icon"
                variant="outline"
                onClick={handleReset}
                className="rounded-full w-10 h-10 bg-[#FFF9F2] border border-[#F5E6D3] text-stone-600 hover:bg-[#F5E6D3] hover:text-stone-800"
                title="초기화"
              >
                <RotateCcw className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
