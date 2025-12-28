"use client"

import { RoastingDashboard } from "@/components/roasting/RoastingDashboard"
import { RoastingHistoryTable } from "@/components/roasting/RoastingHistoryTable"
import PageHero from "@/components/ui/page-hero"
import { Flame } from "lucide-react"

// Mock Data
const MOCK_STATS = {
    overview: {
        total_production_kg: 1250.5,
        total_batches: 84,
        avg_loss_rate: 13.2,
    },
    daily_production: Array.from({ length: 30 }, (_, i) => {
        const date = new Date()
        date.setDate(date.getDate() - (29 - i))
        return {
            date: date.toISOString().split('T')[0],
            total_weight: Math.floor(Math.random() * 50) + 10,
            batch_count: Math.floor(Math.random() * 5) + 1,
        }
    }),
    bean_usage: [
        { bean_type: "GREEN_BEAN", bean_name: "에티오피아 예가체프 G1", total_output: 450, percentage: 35 },
        { bean_type: "GREEN_BEAN", bean_name: "콜롬비아 수프리모", total_output: 300, percentage: 24 },
        { bean_type: "BLEND_BEAN", bean_name: "시그니처 블렌드", total_output: 250, percentage: 20 },
        { bean_type: "GREEN_BEAN", bean_name: "브라질 세하도", total_output: 150, percentage: 12 },
        { bean_type: "GREEN_BEAN", bean_name: "과테말라 안티구아", total_output: 100, percentage: 8 },
    ],
    recent_loss_rates: [
        { batch_no: "B-231228-01", roast_date: "2024-12-28", bean_name: "에티오피아 예가체프", loss_rate: 12.5 },
        { batch_no: "B-231228-02", roast_date: "2024-12-28", bean_name: "시그니처 블렌드", loss_rate: 14.2 },
        { batch_no: "B-231227-01", roast_date: "2024-12-27", bean_name: "콜롬비아 수프리모", loss_rate: 13.0 },
    ],
}

// Mock Table Logs
const MOCK_LOGS = Array.from({ length: 15 }, (_, i) => ({
    id: i,
    roast_date: new Date(Date.now() - i * 86400000).toISOString(),
    batch_no: `B-${231228 - i}-01`,
    target_bean: {
        name: i % 3 === 0 ? "시그니처 블렌드" : "에티오피아 예가체프",
        type: i % 3 === 0 ? "BLEND_BEAN" : "GREEN_BEAN",
    },
    input_weight_total: 10,
    output_weight_total: 8.7,
    loss_rate: 13,
    roast_profile: i % 2 === 0 ? "MEDIUM" : "LIGHT"
}))

export default function RoastingDemoPage() {
    return (
        <div className="space-y-6">
            <PageHero
                icon={<Flame />}
                title="로스팅 대시보드 (Demo)"
                description="이상적인 데이터가 채워진 데모 페이지입니다."
            />

            <RoastingDashboard initialData={MOCK_STATS} />

            <div className="space-y-4">
                <h2 className="text-xl font-bold text-latte-900 px-1">최근 생산 이력 (Demo)</h2>
                <RoastingHistoryTable
                    logs={MOCK_LOGS as any}
                    loading={false}
                    onFilterChange={() => { }}
                />
            </div>
        </div>
    )
}
