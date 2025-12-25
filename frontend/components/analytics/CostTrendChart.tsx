'use client';

import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  CartesianGrid,
} from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

import { formatCurrency } from '@/lib/utils';

interface CostTrendChartProps {
  data: {
    date: string;
    price: number;
  }[];
}

export function CostTrendChart({ data }: CostTrendChartProps) {
  // Helper to format X-axis date (show MM-DD, and HH:mm if duplicates exist? simplified for now)
  const formatXAxis = (dateStr: string) => {
    if (!dateStr) return '';
    // Expecting "YYYY-MM-DD HH:mm"
    const date = new Date(dateStr);
    // Return "MM-DD"
    return `${date.getMonth() + 1}-${date.getDate()}`;
  };

  return (
    <div className="h-[250px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis
            dataKey="date"
            stroke="#888888"
            fontSize={12}
            tickLine={false}
            axisLine={false}
            tickFormatter={formatXAxis}
            minTickGap={30}
          />
          <YAxis
            stroke="#888888"
            fontSize={12}
            tickLine={false}
            axisLine={false}
            tickFormatter={(value) => `₩${formatCurrency(value)}`}
          />
          <Tooltip
            formatter={(value: number) => [`₩${formatCurrency(value)}`, '단가']}
            labelFormatter={(label) => `${label}`} // Shows full "YYYY-MM-DD HH:mm"
            contentStyle={{
              borderRadius: '8px',
              border: 'none',
              boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
            }}
          />
          <Line
            type="monotone"
            dataKey="price"
            stroke="#D97706"
            strokeWidth={2}
            activeDot={{ r: 8 }}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
