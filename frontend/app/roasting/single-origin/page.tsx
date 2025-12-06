'use client'

import { useState, useEffect } from 'react'
import { Bean, BeanAPI, RoastingAPI, RoastProfile, RoastingResponse } from '@/lib/api'
import { Loader2, Bean as BeanIcon, Flame, ArrowRight, Scale } from 'lucide-react'

export default function SingleOriginRoastingPage() {
    const [loading, setLoading] = useState(true)
    const [submitting, setSubmitting] = useState(false)
    const [greenBeans, setGreenBeans] = useState<Bean[]>([])
    const [result, setResult] = useState<RoastingResponse | null>(null)

    // Form State
    const [selectedBeanId, setSelectedBeanId] = useState<number | ''>('')
    const [roastProfile, setRoastProfile] = useState<RoastProfile>('LIGHT')
    const [inputWeight, setInputWeight] = useState<string>('')
    const [outputWeight, setOutputWeight] = useState<string>('')
    const [notes, setNotes] = useState('')

    // Derived State
    const lossRate = calculateLossRate(Number(inputWeight), Number(outputWeight))
    const selectedBean = greenBeans.find(b => b.id === Number(selectedBeanId))

    useEffect(() => {
        loadGreenBeans()
    }, [])

    async function loadGreenBeans() {
        try {
            const allBeans = await BeanAPI.getAll()
            // 생두(GREEN_BEAN)만 필터링
            const greens = allBeans.filter(b => b.type === 'GREEN_BEAN')
            setGreenBeans(greens)
        } catch (error) {
            console.error('Failed to load beans:', error)
            alert('생두 목록을 불러오는데 실패했습니다.')
        } finally {
            setLoading(false)
        }
    }

    function calculateLossRate(input: number, output: number) {
        if (!input || input <= 0) return 0
        return ((input - output) / input) * 100
    }

    async function handleRoast(e: React.FormEvent) {
        e.preventDefault()
        if (!selectedBeanId || !inputWeight || !outputWeight) {
            alert('필수 정보를 입력해주세요.')
            return
        }

        setSubmitting(true)
        setResult(null)

        try {
            const response = await RoastingAPI.roastSingleOrigin({
                green_bean_id: Number(selectedBeanId),
                input_weight: Number(inputWeight),
                output_weight: Number(outputWeight),
                roast_profile: roastProfile,
                notes: notes
            })
            setResult(response)
            alert(`로스팅이 완료되었습니다! (손실률: ${response.loss_rate_percent.toFixed(1)}%)`)

            // 입력 폼 초기화는 사용자가 원할 수 있으므로 보류하거나 선택적으로 처리
        } catch (error) {
            console.error('Roasting failed:', error)
            alert('로스팅 처리에 실패했습니다. 재고를 확인해주세요.')
        } finally {
            setSubmitting(false)
        }
    }

    if (loading) {
        return (
            <div className="flex items-center justify-center p-12">
                <Loader2 className="w-8 h-8 animate-spin text-amber-600" />
            </div>
        )
    }

    return (
        <div className="container mx-auto max-w-4xl p-6">
            <header className="mb-8">
                <h1 className="text-3xl font-bold flex items-center gap-3 text-slate-800">
                    <Flame className="w-8 h-8 text-orange-500" />
                    싱글 오리진 로스팅
                </h1>
                <p className="text-slate-500 mt-2">
                    생두를 로스팅하여 원두 재고로 변환합니다. 재고는 자동으로 차감/증가됩니다.
                </p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* 입력 폼 */}
                <section className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                    <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                        <BeanIcon className="w-5 h-5 text-green-600" />
                        로스팅 설정
                    </h2>

                    <form onSubmit={handleRoast} className="space-y-6">
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-700">생두 선택</label>
                            <select
                                className="w-full p-2 border rounded-md"
                                value={selectedBeanId}
                                onChange={(e) => setSelectedBeanId(Number(e.target.value))}
                                required
                            >
                                <option value="">생두를 선택하세요</option>
                                {greenBeans.map(bean => (
                                    <option key={bean.id} value={bean.id}>
                                        {bean.origin} {bean.name} (재고: {bean.quantity_kg}kg)
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-700">로스팅 프로필</label>
                            <div className="flex gap-4">
                                {(['LIGHT', 'MEDIUM', 'DARK'] as RoastProfile[]).map((profile) => (
                                    <label key={profile} className="flex items-center gap-2 cursor-pointer">
                                        <input
                                            type="radio"
                                            name="roastProfile"
                                            value={profile}
                                            checked={roastProfile === profile}
                                            onChange={(e) => setRoastProfile(e.target.value as RoastProfile)}
                                            className="text-amber-600 focus:ring-amber-500"
                                        />
                                        <span className="text-sm font-medium">{profile}</span>
                                    </label>
                                ))}
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-slate-700">투입량 (kg)</label>
                                <div className="relative">
                                    <input
                                        type="number"
                                        step="0.01"
                                        className="w-full p-2 border rounded-md pr-8"
                                        value={inputWeight}
                                        onChange={(e) => setInputWeight(e.target.value)}
                                        required
                                    />
                                    <span className="absolute right-3 top-2 text-slate-400 text-sm">kg</span>
                                </div>
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-slate-700">배출량 (kg)</label>
                                <div className="relative">
                                    <input
                                        type="number"
                                        step="0.01"
                                        className="w-full p-2 border rounded-md pr-8"
                                        value={outputWeight}
                                        onChange={(e) => setOutputWeight(e.target.value)}
                                        required
                                    />
                                    <span className="absolute right-3 top-2 text-slate-400 text-sm">kg</span>
                                </div>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-700">노트 (선택)</label>
                            <textarea
                                className="w-full p-2 border rounded-md h-24 text-sm"
                                placeholder="로스팅 특이사항, 온도, 습도 등..."
                                value={notes}
                                onChange={(e) => setNotes(e.target.value)}
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={submitting || !selectedBeanId}
                            className="w-full bg-amber-900 text-white py-3 rounded-lg font-medium hover:bg-amber-800 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
                        >
                            {submitting ? (
                                <>
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                    처리 중...
                                </>
                            ) : (
                                <>
                                    <Flame className="w-5 h-5" />
                                    로스팅 완료 기록
                                </>
                            )}
                        </button>
                    </form>
                </section>

                {/* 미리보기 및 결과 */}
                <div className="space-y-6">
                    <section className="bg-slate-50 rounded-xl p-6 border border-slate-200">
                        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2 text-slate-700">
                            <Scale className="w-5 h-5" />
                            생산 요약
                        </h2>

                        <div className="space-y-4">
                            <div className="flex justify-between items-center py-2 border-b border-slate-200">
                                <span className="text-slate-600">선택된 생두</span>
                                <span className="font-medium text-slate-900">
                                    {selectedBean ? `${selectedBean.origin} ${selectedBean.name}` : '-'}
                                </span>
                            </div>

                            <div className="flex justify-between items-center py-2 border-b border-slate-200">
                                <span className="text-slate-600">예상 손실률</span>
                                <span className={`font-bold ${lossRate > 20 ? 'text-red-500' : 'text-blue-600'}`}>
                                    {inputWeight && outputWeight ? `${lossRate.toFixed(1)}%` : '-'}
                                </span>
                            </div>

                            <div className="bg-white p-4 rounded-lg border border-slate-200 mt-4">
                                <p className="text-xs text-slate-500 mb-1">SKU 미리보기</p>
                                <p className="font-mono text-sm text-slate-700 font-medium">
                                    {selectedBean ? `${selectedBean.name}-${roastProfile}` : '-'}
                                </p>
                            </div>
                        </div>
                    </section>

                    {result && (
                        <section className="bg-green-50 border border-green-200 rounded-xl p-6 animate-in fade-in slide-in-from-bottom-4">
                            <h3 className="text-lg font-bold text-green-800 mb-2 flex items-center gap-2">
                                <ArrowRight className="w-5 h-5" />
                                생산 완료!
                            </h3>
                            <div className="space-y-2 text-sm text-green-700">
                                <p>원두가 성공적으로 입고되었습니다.</p>
                                <ul className="list-disc list-inside mt-2 space-y-1">
                                    <li>품목: <strong>{result.roasted_bean.name}</strong></li>
                                    <li>수량: {result.roasted_bean.quantity_kg}kg (현재 총 재고)</li>
                                    <li>생산원가: {parseInt(String(result.production_cost)).toLocaleString()}원/kg</li>
                                </ul>
                            </div>
                        </section>
                    )}
                </div>
            </div>
        </div>
    )
}
