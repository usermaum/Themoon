'use client'

import { useState, useEffect } from 'react'
import { Bean, BeanAPI, Blend, BlendAPI, RoastingAPI } from '@/lib/api'
import { Loader2, Bean as BeanIcon, Flame, ArrowRight, Scale, Calculator, Layers } from 'lucide-react'
import PageHero from '@/components/ui/PageHero'
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"

// 블렌드 로스팅 (Pre-Roast Blending Simulator & Executor)
export default function BlendRoastingPage() {
    const [loading, setLoading] = useState(true)
    const [submitting, setSubmitting] = useState(false)

    // 데이터
    const [blends, setBlends] = useState<Blend[]>([])
    const [availableBeans, setAvailableBeans] = useState<Bean[]>([])

    // 입력 상태
    const [selectedBlendId, setSelectedBlendId] = useState<string>('')
    const [targetWeight, setTargetWeight] = useState<number>(0)

    // Alert Dialog State
    const [dialogConfig, setDialogConfig] = useState<{
        isOpen: boolean
        title: string
        description: string
        type: 'alert' | 'confirm'
        onConfirm?: () => void
    }>({
        isOpen: false,
        title: '',
        description: '',
        type: 'alert'
    })

    const showDialog = (title: string, description: string, type: 'alert' | 'confirm' = 'alert', onConfirm?: () => void) => {
        setDialogConfig({
            isOpen: true,
            title,
            description,
            type,
            onConfirm
        })
    }

    const closeDialog = () => {
        setDialogConfig(prev => ({ ...prev, isOpen: false }))
    }

    // 계산 결과 상태
    const [simulationResult, setSimulationResult] = useState<{
        avgLossRate: number,
        totalRequired: number,
        details: Array<{
            beanName: string,
            origin: string,
            ratio: number,
            lossRate: number,
            requiredAmount: number,
            currentStock: number,
            isStockShort: boolean
        }>
    } | null>(null)

    // 초기 데이터 로드
    useEffect(() => {
        const loadData = async () => {
            try {
                const [beansRes, blendsRes] = await Promise.all([
                    BeanAPI.getAll({ limit: 100 }),
                    BlendAPI.getAll()
                ])

                // 생두만 필터링 (블렌드 구성에 사용됨)
                setAvailableBeans(beansRes.items.filter(b => b.type === 'GREEN_BEAN'))
                setBlends(blendsRes)
            } catch (err) {
                console.error('Failed to load initial data:', err)
                showDialog('오류 발생', '데이터를 불러오는데 실패했습니다.')
            } finally {
                setLoading(false)
            }
        }
        loadData()
    }, [])

    // 시뮬레이션 계산 (블렌드 선택 or 목표량 변경 시)
    useEffect(() => {
        if (!selectedBlendId || targetWeight <= 0) {
            setSimulationResult(null)
            return
        }

        const blend = blends.find(b => b.id.toString() === selectedBlendId)
        if (!blend) return

        let totalRequiredCalc = 0
        const details: any[] = []

        blend.recipe.forEach(item => {
            const bean = availableBeans.find(b => b.id === item.bean_id)
            if (bean) {
                const ratio = item.ratio // 0.4 etc
                const lossRate = bean.expected_loss_rate !== undefined ? bean.expected_loss_rate : 0.15

                // 개별 필요량 역산: (목표량 * 비율) / (1 - 손실률)
                // 예: 10kg의 40%인 4kg를 얻으려면, 손실률 15%일 때 4 / 0.85 = 4.7kg 필요
                const targetPartWeight = targetWeight * ratio
                const requiredAmount = targetPartWeight / (1 - lossRate)

                totalRequiredCalc += requiredAmount

                details.push({
                    beanName: bean.name,
                    origin: bean.origin || 'Unknown',
                    ratio: ratio * 100, // %
                    lossRate: lossRate * 100, // %
                    requiredAmount: requiredAmount,
                    currentStock: bean.quantity_kg,
                    isStockShort: bean.quantity_kg < requiredAmount
                })
            }
        })

        // 평균 손실률 역산
        const avgLossRate = totalRequiredCalc > 0 ? 1 - (targetWeight / totalRequiredCalc) : 0

        setSimulationResult({
            avgLossRate,
            totalRequired: totalRequiredCalc,
            details
        })

    }, [selectedBlendId, targetWeight, blends, availableBeans])

    const handleRoast = async (e: React.FormEvent) => {
        e.preventDefault()

        if (!selectedBlendId || targetWeight <= 0) return

        const proceedRoasting = async () => {
            setSubmitting(true)
            try {
                const res = await RoastingAPI.roastBlend({
                    blend_id: Number(selectedBlendId),
                    output_weight: targetWeight,
                    notes: 'Started from Pre-Roast Blending Simulator'
                })

                showDialog(
                    '로스팅 완료',
                    `블렌드 로스팅이 성공적으로 기록되었습니다.\n\n생산된 원두: ${res.roasted_bean.name}\n생산 원가: ₩${Math.round(res.production_cost).toLocaleString()}/kg`,
                    'alert',
                    () => {
                        setSelectedBlendId('')
                        setTargetWeight(0)
                        setSimulationResult(null)
                    }
                )
            } catch (err) {
                console.error(err)
                showDialog('오류 발생', '로스팅을 기록하는 중 문제가 발생했습니다. 재고를 확인해주세요.')
            } finally {
                setSubmitting(false)
            }
        }

        // 재고 부족 체크
        if (simulationResult?.details.some(d => d.isStockShort)) {
            showDialog(
                '재고 부족 경고',
                '일부 생두의 재고가 부족합니다. 그래도 진행하시겠습니까?',
                'confirm',
                proceedRoasting
            )
            return
        }

        proceedRoasting()
    }

    if (loading) {
        return (
            <div className="flex items-center justify-center p-12">
                <Loader2 className="w-8 h-8 animate-spin text-amber-600" />
            </div>
        )
    }

    return (
        <div className="min-h-screen">
            <PageHero
                title="Pre-Roast Blending"
                description="블렌드 레시피에 따라 여러 생두를 혼합하여 로스팅합니다. 생두별 손실률을 기반으로 필요 투입량을 자동 계산합니다."
                icon={<Layers />}
                image="/images/hero/roasting-hero.png"
                className="mb-8"
            />

            <div className="container mx-auto p-6 max-w-5xl">

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* 왼쪽: 설정 폼 */}
                    <section className="lg:col-span-1 space-y-6">
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                            <h2 className="text-lg font-bold mb-4 flex items-center gap-2 text-slate-700">
                                <Calculator className="w-5 h-5 text-slate-500" />
                                생산 설정
                            </h2>

                            <form onSubmit={handleRoast} className="space-y-6">
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-slate-700">블렌드 선택</label>
                                    <Select
                                        value={selectedBlendId}
                                        onValueChange={(value) => setSelectedBlendId(value)}
                                    >
                                        <SelectTrigger className="w-full h-12 text-lg bg-slate-50 border-slate-200">
                                            <SelectValue placeholder="블렌드를 선택하세요" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            {blends.map(blend => (
                                                <SelectItem key={blend.id} value={String(blend.id)}>
                                                    {blend.name}
                                                </SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                </div>

                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-slate-700">목표 생산량 (Roasted Weight)</label>
                                    <div className="relative">
                                        <input
                                            type="number"
                                            className="w-full p-2 border rounded-md pr-10 text-lg font-bold text-slate-800"
                                            placeholder="0"
                                            value={targetWeight || ''}
                                            onChange={(e) => setTargetWeight(parseFloat(e.target.value) || 0)}
                                            min="0.1"
                                            step="0.1"
                                            required
                                        />
                                        <span className="absolute right-3 top-3 text-slate-500 font-medium">kg</span>
                                    </div>
                                    <p className="text-xs text-slate-500">
                                        * 최종적으로 얻고자 하는 원두의 무게를 입력하세요.
                                    </p>
                                </div>

                                {simulationResult && (
                                    <div className="p-4 bg-amber-50 rounded-lg border border-amber-100 space-y-2">
                                        <div className="flex justify-between text-sm">
                                            <span className="text-amber-700">총 필요 생두량</span>
                                            <span className="font-bold text-amber-900">{simulationResult.totalRequired.toFixed(2)} kg</span>
                                        </div>
                                        <div className="flex justify-between text-sm">
                                            <span className="text-amber-700">예상 평균 손실률</span>
                                            <span className="font-bold text-amber-900">{(simulationResult.avgLossRate * 100).toFixed(1)} %</span>
                                        </div>
                                    </div>
                                )}

                                <button
                                    type="submit"
                                    disabled={submitting || !selectedBlendId || targetWeight <= 0}
                                    className="w-full bg-slate-800 text-white py-3 rounded-lg font-medium hover:bg-slate-900 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                                >
                                    {submitting ? (
                                        <>
                                            <Loader2 className="w-5 h-5 animate-spin" /> 처리 중...
                                        </>
                                    ) : (
                                        <>
                                            <Flame className="w-5 h-5" /> 로스팅 실행 (재고 차감)
                                        </>
                                    )}
                                </button>
                            </form>
                        </div>
                    </section>

                    {/* 오른쪽: 상세 시뮬레이션 결과 */}
                    <section className="lg:col-span-2">
                        {simulationResult ? (
                            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                                <div className="p-6 border-b border-slate-100 bg-slate-50">
                                    <h2 className="text-lg font-bold flex items-center gap-2 text-slate-800">
                                        <Scale className="w-5 h-5 text-blue-600" />
                                        투입 생두 명세서 (Bill of Materials)
                                    </h2>
                                </div>
                                <div className="p-0">
                                    <table className="w-full text-sm text-left">
                                        <thead className="text-xs text-slate-500 uppercase bg-slate-50 border-b border-slate-100">
                                            <tr>
                                                <th className="px-6 py-3">구성 원두</th>
                                                <th className="px-6 py-3 text-right">비율</th>
                                                <th className="px-6 py-3 text-right">손실률</th>
                                                <th className="px-6 py-3 text-right">필요량</th>
                                                <th className="px-6 py-3 text-right">현재 재고</th>
                                            </tr>
                                        </thead>
                                        <tbody className="divide-y divide-slate-100">
                                            {simulationResult.details.map((detail, idx) => (
                                                <tr key={idx} className="hover:bg-slate-50">
                                                    <td className="px-6 py-4 font-medium text-slate-900">
                                                        {detail.beanName}
                                                        <span className="block text-xs text-slate-500 font-normal">{detail.origin}</span>
                                                    </td>
                                                    <td className="px-6 py-4 text-right">{detail.ratio}%</td>
                                                    <td className="px-6 py-4 text-right text-slate-500">
                                                        {detail.lossRate.toFixed(1)}%
                                                    </td>
                                                    <td className="px-6 py-4 text-right font-bold text-slate-800 bg-blue-50/50">
                                                        {detail.requiredAmount.toFixed(2)} kg
                                                    </td>
                                                    <td className={`px-6 py-4 text-right font-medium ${detail.isStockShort ? 'text-red-600' : 'text-green-600'}`}>
                                                        {detail.currentStock} kg
                                                        {detail.isStockShort && (
                                                            <span className="block text-[10px] text-red-500 font-bold">부족!</span>
                                                        )}
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                        <tfoot className="bg-slate-50 border-t border-slate-200">
                                            <tr>
                                                <th className="px-6 py-3 text-base font-bold text-slate-900">합계</th>
                                                <th className="px-6 py-3 text-right text-slate-500">100%</th>
                                                <th className="px-6 py-3 text-right text-slate-500">
                                                    {(simulationResult.avgLossRate * 100).toFixed(1)}% (Avg)
                                                </th>
                                                <th className="px-6 py-3 text-right text-lg font-bold text-blue-600">
                                                    {simulationResult.totalRequired.toFixed(2)} kg
                                                </th>
                                                <th className="px-6 py-3 text-right text-slate-500">-</th>
                                            </tr>
                                        </tfoot>
                                    </table>
                                </div>
                            </div>
                        ) : (
                            <div className="bg-slate-50 border-2 border-dashed border-slate-200 rounded-xl p-12 text-center text-slate-500 h-full flex flex-col items-center justify-center">
                                <BeanIcon className="w-12 h-12 mb-4 text-slate-300" />
                                <p className="text-lg font-medium">블렌드를 선택하고 목표 생산량을 입력하세요.</p>
                                <p className="text-sm">각 생두별 손실률을 고려하여 정확한 투입량을 계산해드립니다.</p>
                            </div>
                        )}
                    </section>
                </div>

                <AlertDialog open={dialogConfig.isOpen} onOpenChange={closeDialog}>
                    <AlertDialogContent>
                        <AlertDialogHeader>
                            <AlertDialogTitle>{dialogConfig.title}</AlertDialogTitle>
                            <AlertDialogDescription>
                                {dialogConfig.description}
                            </AlertDialogDescription>
                        </AlertDialogHeader>
                        <AlertDialogFooter>
                            {dialogConfig.type === 'confirm' && (
                                <AlertDialogCancel onClick={closeDialog}>취소</AlertDialogCancel>
                            )}
                            <AlertDialogAction onClick={() => {
                                if (dialogConfig.onConfirm) dialogConfig.onConfirm()
                                closeDialog()
                            }}>
                                확인
                            </AlertDialogAction>
                        </AlertDialogFooter>
                    </AlertDialogContent>
                </AlertDialog>
            </div>
        </div>
    )
}
