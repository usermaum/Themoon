'use client';

import { formatCurrency } from '@/lib/utils';
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

interface SupplierPieChartProps {
  data: {
    name: string;
    total_amount: number;
    count: number;
  }[];
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d', '#ffc658'];

export function SupplierPieChart({ data }: SupplierPieChartProps) {
  return (
    <Card className="rounded-[1em]">
      <CardHeader>
        <CardTitle>공급자별 매입 비중</CardTitle>
        <CardDescription>총 매입 금액 기준 공급자 점유율입니다.</CardDescription>
      </CardHeader>
      <CardContent className="pb-4">
        <div className="h-[250px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                fill="#8884d8"
                paddingAngle={5}
                dataKey="total_amount"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value: any) => `₩${formatCurrency(value)}`} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
