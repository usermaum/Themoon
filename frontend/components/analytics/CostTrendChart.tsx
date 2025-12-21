"use client"

import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid } from "recharts"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

interface CostTrendChartProps {
    data: {
        date: string
        price: number
    }[]
}

export function CostTrendChart({ data }: CostTrendChartProps) {
    return (
        <Card>
            <CardHeader>
                <CardTitle>단가 변동 추이</CardTitle>
                <CardDescription>
                    최근 입고된 품목의 단가 변화를 보여줍니다.
                </CardDescription>
            </CardHeader>
            <CardContent className="pb-4">
                <div className="h-[250px]">
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={data}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} />
                            <XAxis
                                dataKey="date"
                                stroke="#888888"
                                fontSize={12}
                                tickLine={false}
                                axisLine={false}
                            />
                            <YAxis
                                stroke="#888888"
                                fontSize={12}
                                tickLine={false}
                                axisLine={false}
                                tickFormatter={(value) => `₩${value.toLocaleString()}`}
                            />
                            <Tooltip
                                formatter={(value: number) => [`₩${value.toLocaleString()}`, "단가"]}
                                labelFormatter={(label) => `${label}`}
                            />
                            <Line
                                type="monotone"
                                dataKey="price"
                                stroke="#2563eb"
                                strokeWidth={2}
                                activeDot={{ r: 8 }}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </CardContent>
        </Card>
    )
}
