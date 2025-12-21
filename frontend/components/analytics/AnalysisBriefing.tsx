"use client"

import { TrendingUp, TrendingDown, Minus, Info, Calculator, Calendar } from "lucide-react"

interface AnalysisBriefingProps {
    beanName: string
    data: {
        date: string
        price: number
    }[]
}

export function AnalysisBriefing({ beanName, data }: AnalysisBriefingProps) {
    if (!data || data.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center p-6 text-center text-muted-foreground space-y-2">
                <Info className="h-8 w-8 opacity-20" />
                <p className="text-sm">선택한 기간에 데이터가 없습니다.</p>
            </div>
        )
    }

    const prices = data.map(d => d.price)
    const maxPrice = Math.max(...prices)
    const minPrice = Math.min(...prices)
    const inboundCount = data.length

    // Calculate change from last to current
    let priceDiff = 0
    let percentChange = 0
    if (data.length >= 2) {
        const last = data[data.length - 1].price
        const prev = data[data.length - 2].price
        priceDiff = last - prev
        percentChange = (priceDiff / prev) * 100
    }

    return (
        <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
                <div className="p-3 bg-red-50 rounded-xl border border-red-100">
                    <p className="text-[10px] text-red-600 font-semibold mb-1 uppercase">최고가</p>
                    <p className="text-base font-bold text-red-900">₩{maxPrice.toLocaleString()}</p>
                </div>
                <div className="p-3 bg-blue-50 rounded-xl border border-blue-100">
                    <p className="text-[10px] text-blue-600 font-semibold mb-1 uppercase">최저가</p>
                    <p className="text-base font-bold text-blue-900">₩{minPrice.toLocaleString()}</p>
                </div>
            </div>

            <div className="space-y-4">
                <div className="flex items-start gap-3">
                    <div className="mt-1 p-2 bg-amber-100 rounded-lg text-amber-700">
                        <TrendingUp className="h-4 w-4" />
                    </div>
                    <div>
                        <p className="text-sm font-semibold text-gray-900">최근 가격 변동</p>
                        {data.length >= 2 ? (
                            <div className="flex items-center gap-1.5 mt-0.5">
                                {priceDiff > 0 ? (
                                    <>
                                        <TrendingUp className="h-3.5 w-3.5 text-red-500" />
                                        <span className="text-xs font-medium text-red-600">
                                            {percentChange.toFixed(1)}% 상승
                                        </span>
                                    </>
                                ) : priceDiff < 0 ? (
                                    <>
                                        <TrendingDown className="h-3.5 w-3.5 text-blue-500" />
                                        <span className="text-xs font-medium text-blue-600">
                                            {Math.abs(percentChange).toFixed(1)}% 하락
                                        </span>
                                    </>
                                ) : (
                                    <>
                                        <Minus className="h-3.5 w-3.5 text-gray-400" />
                                        <span className="text-xs font-medium text-gray-500">변동 없음</span>
                                    </>
                                )}
                                <span className="text-[10px] text-gray-400 ml-1">
                                    (이전 입고가 ₩{data[data.length - 2].price.toLocaleString()} 대비)
                                </span>
                            </div>
                        ) : (
                            <p className="text-xs text-gray-500 mt-0.5">데이터가 충분하지 않습니다.</p>
                        )}
                    </div>
                </div>

                <div className="flex items-start gap-3">
                    <div className="mt-1 p-2 bg-emerald-100 rounded-lg text-emerald-700">
                        <Calendar className="h-4 w-4" />
                    </div>
                    <div>
                        <p className="text-sm font-semibold text-gray-900">조회 기간 입고 횟수</p>
                        <p className="text-xs text-gray-500 mt-0.5">
                            총 <span className="font-bold text-emerald-600">{inboundCount}회</span>의 입고 내역이 분석되었습니다.
                        </p>
                    </div>
                </div>

                <div className="flex items-start gap-3">
                    <div className="mt-1 p-2 bg-gray-100 rounded-lg text-gray-600">
                        <Calculator className="h-4 w-4" />
                    </div>
                    <div>
                        <p className="text-sm font-semibold text-gray-900">가치 계산 방식</p>
                        <p className="text-xs text-gray-500 mt-0.5 leading-relaxed">
                            본 분석은 <span className="font-medium text-gray-700">FIFO (선입선출)</span> 방식을 사용하여 실제 먼저 들어온 재고의 단가를 우선적으로 적용합니다.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}
