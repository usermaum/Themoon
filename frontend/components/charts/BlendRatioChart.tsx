'use client';

import { Layers } from 'lucide-react';
import { PolarAngleAxis, PolarGrid, Radar, RadarChart } from 'recharts';
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '@/components/ui/chart';

const chartConfig = {
  ratio: {
    label: '구성 비율',
    color: '#d97706', // Amber-600
  },
} satisfies ChartConfig;

interface BlendRatioChartProps {
  data: Array<{
    beanName: string;
    ratio: number;
  }>;
}

export default function BlendRatioChart({ data }: BlendRatioChartProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8 flex flex-col items-center">
      <h3 className="text-base font-bold text-slate-700 mb-6 flex items-center gap-2 self-start">
        <Layers className="w-4 h-4 text-amber-500" />
        블렌드 구성 비율 (Blend Composition)
      </h3>
      <div className="w-full max-w-sm">
        <ChartContainer config={chartConfig} className="mx-auto aspect-square max-h-[300px]">
          <RadarChart data={data}>
            <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
            <PolarGrid className="stroke-slate-200" />
            <PolarAngleAxis
              dataKey="beanName"
              tick={{ fill: '#475569', fontSize: 12, fontWeight: 600 }}
            />
            <Radar
              dataKey="ratio"
              fill="var(--color-ratio)"
              fillOpacity={0}
              stroke="var(--color-ratio)"
              strokeWidth={2}
              dot={{
                r: 4,
                fillOpacity: 1,
              }}
            />
          </RadarChart>
        </ChartContainer>
      </div>
    </div>
  );
}
