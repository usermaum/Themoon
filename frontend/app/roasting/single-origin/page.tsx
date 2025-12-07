'use client'

import { useState, useEffect } from 'react'
import { Bean, BeanAPI, RoastingAPI, RoastProfile, RoastingResponse } from '@/lib/api'
import { Loader2, Bean as BeanIcon, Flame, ArrowRight, Scale, Calculator, AlertTriangle, CheckCircle2 } from 'lucide-react'
import PageHero from '@/components/ui/PageHero'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Badge } from '@/components/ui/Badge'
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

// 싱글 오리진 로스팅 (Goal-Driven: 목표 생산량 기반)
export default function SingleOriginRoastingPage() {
    const [loading, setLoading] = useState(true)
    const [submitting, setSubmitting] = useState(false)
    const [greenBeans, setGreenBeans] = useState<Bean[]>([])

    // 로스팅 결과 상태
    const [result, setResult] = useState<RoastingResponse | null>(null)

    // 입력 상태
    const [selectedBeanId, setSelectedBeanId] = useState<string>('')
    const [roastProfile, setRoastProfile] = useState<RoastProfile>('MEDIUM')
    const [targetWeight, setTargetWeight] = useState<string>('') // 목표 생산량 (Input)
    const [notes, setNotes] = useState('')

    // 계산된 상태 (Simulation Result)
    const [simulation, setSimulation] = useState<{
        requiredInput: number     // 필요 투입량
        expectedLossRate: number  // 예상 손실률 (0.15 etc)
        currentStock: number      // 현재 재고
        isStockShort: boolean     // 재고 부족 여부
        beanName: string
        origin: string
    } | null>(null)

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

    // 1. 초기 데이터 로드
    useEffect(() => {
        loadGreenBeans()
    }, [])

    async function loadGreenBeans() {
        try {
            const response = await BeanAPI.getAll({ limit: 100 })
            // 생두(GREEN_BEAN)만 필터링
            const greens = response.items.filter(b => b.type === 'GREEN_BEAN')
            setGreenBeans(greens)
        } catch (error) {
            console.error('Failed to load beans:', error)
            showDialog('오류', '생두 목록을 불러오는데 실패했습니다.')
        } finally {
            setLoading(false)
        }
    }

    // 2. 시뮬레이션 계산 (생두 선택 or 목표량 변경 시)
    useEffect(() => {
        if (!selectedBeanId || !targetWeight || parseFloat(targetWeight) <= 0) {
            setSimulation(null)
            return
        }

        const bean = greenBeans.find(b => b.id === Number(selectedBeanId))
        if (!bean) return

        const target = parseFloat(targetWeight)

        // 손실률 가져오기 (없으면 기본 15%)
        const lossRate = bean.expected_loss_rate !== undefined ? bean.expected_loss_rate : 0.15

        // 역산 공식: Input = Target / (1 - LossRate)
        const required = target / (1 - lossRate)

        setSimulation({
            requiredInput: required,
            expectedLossRate: lossRate,
            currentStock: bean.quantity_kg,
            isStockShort: bean.quantity_kg < required,
            beanName: bean.name,
            origin: bean.origin || 'Unknown'
        })

    }, [selectedBeanId, targetWeight, greenBeans])

    // 유틸리티
    const showDialog = (title: string, description: string, type: 'alert' | 'confirm' = 'alert', onConfirm?: () => void) => {
        setDialogConfig({ isOpen: true, title, description, type, onConfirm })
    }

    const closeDialog = () => {
        setDialogConfig(prev => ({ ...prev, isOpen: false }))
    }

    // 3. 로스팅 실행 핸들러
    const handleRoast = async (e: React.FormEvent) => {
        e.preventDefault()

        if (!selectedBeanId || !targetWeight || !simulation) return

        // 유효성 검사
        if (simulation.isStockShort) {
            showDialog(
                '재고 부족 경고',
                `현재 재고(${simulation.currentStock.toFixed(1)}kg)가 필요량(${simulation.requiredInput.toFixed(1)}kg)보다 부족합니다. 그래도 진행하시겠습니까? (마이너스 재고 처리됨)`,
                'confirm',
                proceedRoasting
            )
            return
        }

        // 정상 진행 확인
        showDialog(
            '로스팅 시작',
            `다음 내용으로 로스팅을 확정하시겠습니까?\n\n- 목표 생산: ${targetWeight}kg\n- 생두 투입: ${simulation.requiredInput.toFixed(2)}kg\n- 예상 손실률: ${(simulation.expectedLossRate * 100).toFixed(1)}%`,
            'confirm',
            proceedRoasting
        )
    }

    const proceedRoasting = async () => {
        if (!simulation) return

        setSubmitting(true)
        setResult(null)

        try {
            // API 호출 (Input, Output 전송)
            const response = await RoastingAPI.roastSingleOrigin({
                green_bean_id: Number(selectedBeanId),
                input_weight: simulation.requiredInput, // 계산된 투입량
                output_weight: parseFloat(targetWeight), // 목표 생산량
                roast_profile: roastProfile,
                notes: notes
            })

            setResult(response)

            // 성공 후 데이터 리로드 (재고 갱신 확인용)
            await loadGreenBeans()

            // 입력 폼 초기화는 선택적 (연속 작업을 위해 유지할지, 비울지 결정. 여기선 성공 메시지만 표시)
        } catch (error: any) {
            console.error('Roasting failed:', error)
            showDialog('로스팅 실패', error.response?.data?.detail || '처리 중 오류가 발생했습니다.')
        } finally {
            setSubmitting(false)
        }
    }

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[50vh]">
                <Loader2 className="w-8 h-8 animate-spin text-latte-500" />
            </div>
        )
    }

    return (
        <div className="min-h-screen pb-12">
            <PageHero
                title="싱글 오리진 로스팅"
                description="목표 생산량을 입력하면 필요한 생두량을 자동으로 계산하여 로스팅합니다."
                icon={<Flame />}
                image="/images/hero/roasting-hero.png"
                className="mb-8"
            />

            <div className="container mx-auto px-4 max-w-6xl">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                    {/* [좌측] 로스팅 설정 패널 */}
                    <section className="lg:col-span-1 space-y-6">
                        <div className="bg-white rounded-[2rem] p-8 shadow-sm border border-latte-200">
                            <h2 className="text-xl font-serif font-bold mb-6 flex items-center gap-2 text-latte-900">
                                <Calculator className="w-6 h-6 text-latte-400" />
                                생산 계획 설정
                            </h2>

                            <form onSubmit={handleRoast} className="space-y-6">
                                {/* 1. 생두 선택 */}
                                <div className="space-y-2">
                                    <label className="text-sm font-bold text-latte-700">생두 선택</label>
                                    <Select
                                        onValueChange={(value) => setSelectedBeanId(value)}
                                        value={selectedBeanId}
                                    >
                                        <SelectTrigger className="w-full h-12 text-lg bg-latte-50 border-latte-200">
                                            <SelectValue placeholder="생두를 선택하세요" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            {greenBeans.map(bean => (
                                                <SelectItem key={bean.id} value={String(bean.id)}>
                                                    <span className="font-bold mr-2">{bean.origin}</span>
                                                    {bean.name}
                                                    <span className="text-latte-400 ml-2 text-sm">(재고: {bean.quantity_kg.toFixed(1)}kg)</span>
                                                </SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                </div>

                                {/* 2. 로스팅 프로필 */}
                                <div className="space-y-2">
                                    <label className="text-sm font-bold text-latte-700">로스팅 포인트</label>
                                    <div className="grid grid-cols-3 gap-2">
                                        {(['LIGHT', 'MEDIUM', 'DARK'] as RoastProfile[]).map((profile) => (
                                            <label
                                                key={profile}
                                                className={`
                                                    cursor-pointer text-center p-2 rounded-lg border text-sm font-medium transition-all
                                                    ${roastProfile === profile
                                                        ? 'bg-latte-600 text-white border-latte-600 shadow-md'
                                                        : 'bg-white text-latte-600 border-latte-200 hover:bg-latte-50'}
                                                `}
                                            >
                                                <input
                                                    type="radio"
                                                    name="roastProfile"
                                                    value={profile}
                                                    checked={roastProfile === profile}
                                                    onChange={(e) => setRoastProfile(e.target.value as RoastProfile)}
                                                    className="hidden"
                                                />
                                                {profile}
                                            </label>
                                        ))}
                                    </div>
                                </div>

                                {/* 3. 목표 생산량 */}
                                <div className="space-y-2">
                                    <label className="text-sm font-bold text-latte-700">목표 생산량 (Roasted)</label>
                                    <div className="relative">
                                        <Input
                                            type="number"
                                            step="0.1"
                                            min="0.1"
                                            value={targetWeight}
                                            onChange={(e) => setTargetWeight(e.target.value)}
                                            placeholder="0.0"
                                            className="pr-12 text-lg font-mono font-bold h-12"
                                            required
                                        />
                                        <span className="absolute right-4 top-3 text-latte-400 font-bold">kg</span>
                                    </div>
                                    <p className="text-xs text-latte-500">
                                        * 최종적으로 얻고자 하는 원두의 무게를 입력하세요.
                                    </p>
                                </div>

                                {/* 4. 노트 */}
                                <div className="space-y-2">
                                    <label className="text-sm font-bold text-latte-700">노트 (선택)</label>
                                    <textarea
                                        className="w-full p-3 border border-latte-200 rounded-xl bg-latte-50 focus:ring-2 focus:ring-latte-400 outline-none transition-all h-24 text-sm resize-none"
                                        placeholder="로스팅 특이사항, 날씨, 배치 번호 등..."
                                        value={notes}
                                        onChange={(e) => setNotes(e.target.value)}
                                    />
                                </div>

                                <Button
                                    type="submit"
                                    disabled={submitting || !selectedBeanId || !targetWeight || !simulation}
                                    className="w-full h-12 text-lg bg-latte-900 hover:bg-latte-800 disabled:opacity-50"
                                >
                                    {submitting ? (
                                        <>
                                            <Loader2 className="w-5 h-5 animate-spin mr-2" /> 처리 중...
                                        </>
                                    ) : (
                                        <>
                                            <Flame className="w-5 h-5 mr-2" /> 로스팅 실행
                                        </>
                                    )}
                                </Button>
                            </form>
                        </div>
                    </section>

                    {/* [우측] 시뮬레이션 결과 및 명세서 */}
                    <section className="lg:col-span-2 space-y-6">
                        {/* 1. 시뮬레이션 카드 */}
                        <div className={`
                            bg-white rounded-[2rem] p-8 shadow-sm border transition-all duration-300
                            ${simulation ? 'border-latte-200 bg-white' : 'border-dashed border-latte-200 bg-latte-50/50'}
                        `}>
                            <h2 className="text-xl font-serif font-bold mb-6 flex items-center gap-2 text-latte-900">
                                <Scale className="w-6 h-6 text-latte-400" />
                                생산 명세서 (Simulation)
                            </h2>

                            {simulation ? (
                                <div className="space-y-8 animate-in fade-in slide-in-from-bottom-2">
                                    {/* 상단 요약 배지 */}
                                    <div className="flex flex-wrap gap-3">
                                        <Badge variant="outline" className="text-base px-3 py-1 border-latte-200 text-latte-700">
                                            {simulation.origin}
                                        </Badge>
                                        <Badge variant="outline" className="text-base px-3 py-1 border-latte-200 text-latte-700">
                                            {simulation.beanName}
                                        </Badge>
                                        <Badge className="text-base px-3 py-1 bg-latte-100 text-latte-800 hover:bg-latte-200 border-none">
                                            손실률 {(simulation.expectedLossRate * 100).toFixed(1)}% 적용
                                        </Badge>
                                    </div>

                                    {/* 핵심 수치 그리드 */}
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                        {/* Target */}
                                        <div className="bg-green-50 rounded-2xl p-5 border border-green-100">
                                            <p className="text-sm font-bold text-green-700 mb-1">목표 생산량</p>
                                            <p className="text-3xl font-mono font-bold text-green-800">
                                                {parseFloat(targetWeight).toFixed(2)} <span className="text-lg">kg</span>
                                            </p>
                                        </div>

                                        {/* Formula */}
                                        <div className="flex items-center justify-center text-latte-300">
                                            <ArrowRight className="w-8 h-8" />
                                        </div>

                                        {/* Required Input */}
                                        <div className="bg-amber-50 rounded-2xl p-5 border border-amber-100 relative overflow-hidden">
                                            <div className="absolute top-0 right-0 p-2 opacity-10">
                                                <Flame className="w-16 h-16 text-amber-900" />
                                            </div>
                                            <p className="text-sm font-bold text-amber-700 mb-1">
                                                필요 투입량 (자동계산)
                                            </p>
                                            <p className="text-3xl font-mono font-bold text-amber-800">
                                                {simulation.requiredInput.toFixed(2)} <span className="text-lg">kg</span>
                                            </p>
                                            <p className="text-xs text-amber-600 mt-2 font-medium">
                                                = 목표량 ÷ (1 - 손실률)
                                            </p>
                                        </div>
                                    </div>

                                    {/* 재고 상태 체크 */}
                                    <div className={`p-4 rounded-xl border flex items-center gap-3 ${simulation.isStockShort
                                        ? 'bg-red-50 border-red-200 text-red-700'
                                        : 'bg-latte-50 border-latte-200 text-latte-700'
                                        }`}>
                                        {simulation.isStockShort ? (
                                            <AlertTriangle className="w-6 h-6 flex-shrink-0 text-red-500" />
                                        ) : (
                                            <CheckCircle2 className="w-6 h-6 flex-shrink-0 text-green-500" />
                                        )}
                                        <div className="flex-1">
                                            <p className="font-bold">
                                                {simulation.isStockShort ? '재고 부족 경고' : '재고 충분'}
                                            </p>
                                            <p className="text-sm">
                                                현재 보유 재고: <span className="font-mono font-bold">{simulation.currentStock.toFixed(1)} kg</span>
                                                {simulation.isStockShort && (
                                                    <span className="ml-1 font-bold">
                                                        (부족: {(simulation.requiredInput - simulation.currentStock).toFixed(1)} kg)
                                                    </span>
                                                )}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="h-64 flex flex-col items-center justify-center text-latte-400">
                                    <Calculator className="w-12 h-12 mb-3 opacity-20" />
                                    <p className="text-lg font-medium">좌측에서 생두와 목표량을 설정하세요</p>
                                    <p className="text-sm opacity-60">자동으로 로스팅 시뮬레이션 결과가 표시됩니다.</p>
                                </div>
                            )}
                        </div>

                        {/* 2. 결과 성공 메시지 */}
                        {result && (
                            <div className="bg-green-600 text-white rounded-[2rem] p-8 shadow-lg animate-in slide-in-from-bottom-4 relative overflow-hidden">
                                <div className="absolute top-0 right-0 p-8 opacity-10">
                                    <CheckCircle2 className="w-32 h-32" />
                                </div>
                                <h3 className="text-2xl font-serif font-bold mb-4 flex items-center gap-2">
                                    <CheckCircle2 className="w-8 h-8" />
                                    로스팅 완료!
                                </h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 relative z-10">
                                    <div className="space-y-2">
                                        <p className="text-green-100 text-sm">생산된 원두</p>
                                        <p className="text-2xl font-bold">{result.roasted_bean.name}</p>
                                        <p className="text-lg font-mono">SKU: {result.roasted_bean.sku}</p>
                                    </div>
                                    <div className="flex gap-4">
                                        <div className="bg-white/10 rounded-xl p-4 backdrop-blur-sm flex-1">
                                            <p className="text-green-100 text-xs mb-1">최종 생산량</p>
                                            <p className="text-xl font-mono font-bold">
                                                {result.roasted_bean.quantity_kg.toFixed(1)} kg
                                            </p>
                                        </div>
                                        <div className="bg-white/10 rounded-xl p-4 backdrop-blur-sm flex-1">
                                            <p className="text-green-100 text-xs mb-1">최종 손실률</p>
                                            <p className="text-xl font-mono font-bold">
                                                {result.loss_rate_percent.toFixed(1)} %
                                            </p>
                                        </div>
                                    </div>
                                </div>
                                <div className="mt-6 flex justify-end">
                                    <Button
                                        variant="secondary"
                                        className="bg-white text-green-700 hover:bg-green-50"
                                        onClick={() => {
                                            setResult(null)
                                            setTargetWeight('')
                                            setSimulation(null)
                                        }}
                                    >
                                        새로운 로스팅 시작
                                    </Button>
                                </div>
                            </div>
                        )}
                    </section>
                </div>
            </div>

            {/* Alert Dialog */}
            <AlertDialog open={dialogConfig.isOpen} onOpenChange={closeDialog}>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <AlertDialogTitle>{dialogConfig.title}</AlertDialogTitle>
                        <AlertDialogDescription className="whitespace-pre-wrap">
                            {dialogConfig.description}
                        </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                        {dialogConfig.type === 'confirm' && (
                            <AlertDialogCancel onClick={closeDialog}>취소</AlertDialogCancel>
                        )}
                        <AlertDialogAction
                            onClick={() => {
                                if (dialogConfig.onConfirm) dialogConfig.onConfirm()
                                closeDialog()
                            }}
                            className="bg-latte-900 hover:bg-latte-800"
                        >
                            확인
                        </AlertDialogAction>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialog>
        </div>
    )
}
