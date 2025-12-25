'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { useState, useEffect } from 'react';
import { Bean, BeanAPI, RoastingAPI, RoastProfile, RoastingResponse } from '@/lib/api';
import { formatCurrency, formatWeight } from '@/lib/utils';
import {
  Loader2,
  Bean as BeanIcon,
  Flame,
  ArrowRight,
  ArrowLeft,
  Scale,
  Calculator,
  AlertTriangle,
  CheckCircle2,
} from 'lucide-react';
import { Pie, PieChart, Label } from 'recharts';
import { ChartContainer, ChartTooltip, ChartTooltipContent } from '@/components/ui/chart';
import PageHero from '@/components/ui/page-hero';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

// 싱글 오리진 로스팅 (Goal-Driven: 목표 생산량 기반)
export default function SingleOriginRoastingPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [greenBeans, setGreenBeans] = useState<Bean[]>([]);

  // 로스팅 결과 상태
  const [result, setResult] = useState<RoastingResponse | null>(null);

  // 입력 상태
  const [selectedBeanId, setSelectedBeanId] = useState<string>('');
  const [roastProfile, setRoastProfile] = useState<RoastProfile>('LIGHT');
  const [targetWeight, setTargetWeight] = useState<string>(''); // 목표 생산량 (Input)
  const [actualOutputWeight, setActualOutputWeight] = useState<string>(''); // 실제 생산량 (Input - Final)
  const [notes, setNotes] = useState('');

  // 계산된 상태 (Simulation Result)
  const [simulation, setSimulation] = useState<{
    requiredInput: number; // 필요 투입량
    expectedLossRate: number; // 예상 손실률 (0.15 etc)
    currentStock: number; // 현재 재고
    isStockShort: boolean; // 재고 부족 여부
    beanName: string;
    origin: string;
  } | null>(null);

  // Alert Dialog State
  const [dialogConfig, setDialogConfig] = useState<{
    isOpen: boolean;
    title: string;
    description: React.ReactNode;
    type: 'alert' | 'confirm';
    onConfirm?: () => void;
  }>({
    isOpen: false,
    title: '',
    description: '',
    type: 'alert',
  });

  const searchParams = useSearchParams();

  // 1. 초기 데이터 로드 & URL 파라미터 확인
  useEffect(() => {
    loadGreenBeans();

    const beanIdParam = searchParams.get('bean_id');
    if (beanIdParam) {
      setSelectedBeanId(beanIdParam);
    }
  }, [searchParams]);

  async function loadGreenBeans() {
    try {
      const beansRes = await BeanAPI.getAll({ limit: 100, type: ['GREEN_BEAN'] });
      // 생두(GREEN_BEAN)만 필터링
      const greens = beansRes.items;
      setGreenBeans(greens);
    } catch (error) {
      console.error('Failed to load beans:', error);
      showDialog('오류', '생두 목록을 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  }

  // 2. 시뮬레이션 계산 (생두 선택 or 목표량 변경 시)
  useEffect(() => {
    if (!selectedBeanId || !targetWeight || parseFloat(targetWeight) <= 0) {
      setSimulation(null);
      return;
    }

    const bean = greenBeans.find((b) => b.id === Number(selectedBeanId));
    if (!bean) return;

    const target = parseFloat(targetWeight);

    // 손실률 가져오기 (없으면 기본 15%)
    const lossRate = bean.expected_loss_rate !== undefined ? bean.expected_loss_rate : 0.15;

    // 역산 공식: Input = Target / (1 - LossRate)
    const required = target / (1 - lossRate);

    setSimulation({
      requiredInput: required,
      expectedLossRate: lossRate,
      currentStock: bean.quantity_kg,
      isStockShort: bean.quantity_kg < required,
      beanName: bean.name,
      origin: bean.origin || 'Unknown',
    });
    setActualOutputWeight(''); // 초기화: 사용자가 직접 입력해야 함
  }, [selectedBeanId, targetWeight, greenBeans]);

  // 유틸리티
  const showDialog = (
    title: string,
    description: React.ReactNode,
    type: 'alert' | 'confirm' = 'alert',
    onConfirm?: () => void
  ) => {
    setDialogConfig({ isOpen: true, title, description, type, onConfirm });
  };

  const closeDialog = () => {
    setDialogConfig((prev) => ({ ...prev, isOpen: false }));
  };

  // 3. 로스팅 실행 핸들러
  const handleRoast = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedBeanId || !targetWeight || !simulation) return;

    // 유효성 검사
    // 유효성 검사
    if (simulation.isStockShort) {
      showDialog(
        '재고 부족',
        <div className="text-left space-y-5">
          <p className="text-red-900 font-bold text-lg leading-relaxed">
            다음 생두의 재고가 부족하여<br /> 로스팅을 진행할 수 없습니다.
          </p>

          <div className="bg-red-50 p-5 rounded-xl border border-red-100 text-left">
            <span className="block text-red-700 font-bold mb-3 flex items-center gap-2 text-base">
              <AlertTriangle className="w-5 h-5" />
              부족 품목
            </span>
            <span className="block text-red-600 font-bold text-base bg-white/60 px-2 py-1 rounded">
              • {simulation.beanName}
            </span>
          </div>

          <div className="bg-red-900/5 p-4 rounded-xl text-red-800 text-sm font-medium leading-relaxed">
            💡 재고를 입고하거나 투입량을 조정한 후 다시 시도해주세요.
          </div>
        </div>,
        'alert'
      );
      return;
    }

    // 정상 진행 확인
    const actualLoss =
      simulation.requiredInput > 0
        ? (1 - parseFloat(actualOutputWeight) / simulation.requiredInput) * 100
        : 0;

    showDialog(
      '로스팅 결과 저장',
      `다음 내용으로 로스팅 이력을 저장하시겠습니까?\n\n- 실제 투입: ${simulation.requiredInput.toFixed(2)}kg\n- 실제 생산: ${actualOutputWeight}kg\n- 실제 손실률: ${actualLoss.toFixed(1)}%\n\n(목표 생산량: ${targetWeight}kg)`,
      'confirm',
      proceedRoasting
    );
  };

  const proceedRoasting = async () => {
    if (!simulation) return;

    setSubmitting(true);
    setResult(null);

    try {
      // API 호출 (Actual Data 전송)
      const response = await RoastingAPI.roastSingleOrigin({
        green_bean_id: Number(selectedBeanId),
        input_weight: simulation.requiredInput, // 실제 투입량 (시뮬레이션 값 사용)
        output_weight: parseFloat(actualOutputWeight), // 실제 생산량
        roast_profile: roastProfile,
        notes: notes,
      });

      setResult(response);

      // 성공 후 데이터 리로드 (재고 갱신 확인용)
      await loadGreenBeans();

      // 입력 폼 초기화는 선택적 (연속 작업을 위해 유지할지, 비울지 결정. 여기선 성공 메시지만 표시)
    } catch (error: any) {
      console.error('Roasting failed:', error);
      showDialog('로스팅 실패', error.response?.data?.detail || '처리 중 오류가 발생했습니다.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <Loader2 className="w-8 h-8 animate-spin text-latte-500" />
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-12">
      <PageHero
        title="싱글 오리진 로스팅"
        description="목표 생산량을 입력하면 필요한 생두량을 자동으로 계산하여 로스팅합니다."
        icon={<Flame />}
        image="/images/hero/single_origin_roast_hero.png"
        className="mb-8 min-h-[280px]"
      />

      <div className="container mx-auto px-4 max-w-6xl">
        <div className="mb-6">
          <button
            onClick={() => router.back()}
            className="flex items-center gap-2 text-latte-600 hover:text-latte-900 font-bold transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            이전으로
          </button>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* [좌측] 로스팅 설정 패널 (Actual 포함) */}
          <section className="lg:col-span-5 space-y-6 h-full">
            <div className="bg-white rounded-[1em] p-8 shadow-sm border border-latte-200 h-full flex flex-col">
              <h2 className="text-xl font-serif font-bold mb-6 flex items-center gap-2 text-latte-900">
                <Calculator className="w-6 h-6 text-latte-400" />
                생산 계획 설정
              </h2>

              <form onSubmit={handleRoast} className="space-y-6 flex-1 flex flex-col">
                <div className="space-y-6 flex-1">
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
                        {greenBeans.map((bean) => (
                          <SelectItem key={bean.id} value={String(bean.id)}>
                            <div className="flex flex-col items-start text-left">
                              <div>
                                <span className="font-bold mr-2 text-latte-700">
                                  [{bean.origin_ko || bean.origin}]
                                </span>
                                <span className="font-medium text-latte-900">
                                  {bean.name_ko || bean.name}
                                </span>
                                <span
                                  className={`ml-2 text-xs ${bean.quantity_kg < 5 ? 'text-red-500 font-bold' : 'text-latte-400'}`}
                                >
                                  ({formatWeight(bean.quantity_kg)}kg)
                                </span>
                              </div>
                              {bean.name_en && (
                                <span className="text-xs text-latte-400 font-normal">
                                  {bean.name_en}
                                </span>
                              )}
                            </div>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {/* 2. 로스팅 프로필 (Updated Color) */}
                  <div className="space-y-2">
                    <label className="text-sm font-bold text-latte-700">로스팅 포인트</label>
                    <div className="grid grid-cols-2 gap-4">
                      {(['LIGHT', 'DARK'] as RoastProfile[]).map((profile) => (
                        <label
                          key={profile}
                          className={`
                                                        cursor-pointer rounded-xl p-4 border-2 text-center transition-all
                                                        ${roastProfile === profile
                              ? 'border-latte-400 ring-1 ring-latte-400 bg-latte-50 text-latte-900 font-bold shadow-sm'
                              : 'border-latte-100 text-latte-400 hover:border-latte-300 hover:text-latte-600'
                            }
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
                          {profile === 'LIGHT' ? '신콩' : '탄콩'}
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* 3. 목표 생산량 */}
                  <div className="space-y-2">
                    <label className="text-sm font-bold text-latte-700">
                      목표 생산량 (Roasted)
                    </label>
                    <div className="relative">
                      <Input
                        type="number"
                        step="0.1"
                        min="0.1"
                        value={targetWeight}
                        onChange={(e) => setTargetWeight(e.target.value)}
                        placeholder="0.0"
                        className="pr-16 text-lg font-mono font-bold h-12"
                        required
                      />
                      <span className="absolute right-10 top-3 text-latte-400 font-bold">kg</span>
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

                  {/* 5. 실제 투입 및 결과 (Actual) - Moved from Right Panel */}
                  {simulation && (
                    <div className="pt-8 border-t border-latte-100 mt-8">
                      <h3 className="text-lg font-serif font-bold text-latte-900 mb-6 flex items-center gap-2">
                        <CheckCircle2 className="w-5 h-5 text-green-600" />
                        실제 투입 및 결과 (Actual)
                      </h3>
                      <div className="space-y-5">
                        {/* Actual Input Weight (ReadOnly) */}
                        <div className="flex items-center justify-between">
                          <label className="text-sm font-bold text-latte-700">
                            실제 투입량 (자동계산)
                          </label>
                          <div className="w-36 h-12 flex items-center justify-end px-4 bg-latte-50 border border-latte-200 rounded-xl text-lg font-bold text-latte-900 shadow-sm font-mono">
                            {formatWeight(simulation.requiredInput)}
                            <span className="text-sm font-medium ml-1 text-latte-700">kg</span>
                          </div>
                        </div>

                        {/* Actual Output Weight (Input) */}
                        <div className="flex items-center justify-between">
                          <label className="text-sm font-bold text-latte-700">
                            실제 생산량 (입력)
                          </label>
                          <div className="relative w-36">
                            <Input
                              type="number"
                              step="0.01"
                              value={actualOutputWeight}
                              onChange={(e) => setActualOutputWeight(e.target.value)}
                              className="h-12 pr-12 text-right text-lg font-mono font-bold bg-white border-latte-300 focus:border-latte-600"
                              placeholder="0.00"
                            />
                            <span className="absolute right-4 top-1/2 -translate-y-1/2 text-latte-400 font-medium text-sm">
                              kg
                            </span>
                          </div>
                        </div>

                        {/* Actual Loss Rate (Calculated) */}
                        <div className="p-4 bg-white rounded-xl border border-latte-100 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] flex items-center justify-between">
                          <span className="text-sm font-bold text-latte-600">실제 손실률</span>
                          <span className="text-2xl font-mono font-bold text-amber-500">
                            {actualOutputWeight && parseFloat(actualOutputWeight) > 0
                              ? (
                                (1 - parseFloat(actualOutputWeight) / simulation.requiredInput) *
                                100
                              ).toFixed(1)
                              : '0.0'}
                            %
                          </span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                <Button
                  type="submit"
                  disabled={
                    submitting ||
                    !selectedBeanId ||
                    !targetWeight ||
                    !simulation ||
                    !actualOutputWeight
                  }
                  className="w-full h-12 text-lg bg-latte-900 hover:bg-latte-800 disabled:opacity-50 mt-auto"
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
          <section className="lg:col-span-7 space-y-6 h-full flex flex-col">
            {/* 1. 시뮬레이션 카드 */}
            <div
              className={`
                            bg-white rounded-[1em] p-8 shadow-sm border transition-all duration-300 flex-1 flex flex-col
                            ${simulation ? 'border-latte-200 bg-white' : 'border-dashed border-latte-200 bg-latte-50/50'}
                        `}
            >
              <h2 className="text-xl font-serif font-bold mb-6 flex items-center gap-2 text-latte-900">
                <Scale className="w-6 h-6 text-latte-400" />
                예상 생산 명세서 (Expected)
              </h2>

              {simulation ? (
                <div className="space-y-8 animate-in fade-in slide-in-from-bottom-2 flex-1">
                  {/* 상단 요약 배지 */}
                  <div className="flex flex-wrap gap-3">
                    <Badge
                      variant="outline"
                      className="text-base px-3 py-1 border-latte-200 text-latte-700"
                    >
                      {simulation.origin}
                    </Badge>
                    <Badge
                      variant="outline"
                      className="text-base px-3 py-1 border-latte-200 text-latte-700"
                    >
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
                        {formatWeight(targetWeight)} <span className="text-lg">kg</span>
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
                        {formatWeight(simulation.requiredInput)} <span className="text-lg">kg</span>
                      </p>
                      <p className="text-xs text-amber-600 mt-2 font-medium">
                        = 목표량 ÷ (1 - 손실률)
                      </p>
                    </div>
                  </div>

                  {/* 재고 상태 체크 */}
                  <div
                    className={`p-4 rounded-xl border flex items-center gap-3 ${simulation.isStockShort
                      ? 'bg-red-50 border-red-200 text-red-700'
                      : 'bg-latte-50 border-latte-200 text-latte-700'
                      }`}
                  >
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
                        현재 보유 재고:{' '}
                        <span className="font-mono font-bold">
                          {formatWeight(simulation.currentStock)} kg
                        </span>
                        {simulation.isStockShort && (
                          <span className="ml-1 font-bold">
                            (부족: {(simulation.requiredInput - simulation.currentStock).toFixed(1)}{' '}
                            kg)
                          </span>
                        )}
                      </p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-latte-400">
                  <Calculator className="w-12 h-12 mb-3 opacity-20" />
                  <p className="text-lg font-medium">좌측에서 생두와 목표량을 설정하세요</p>
                  <p className="text-sm opacity-60">
                    자동으로 로스팅 시뮬레이션 결과가 표시됩니다.
                  </p>
                </div>
              )}
            </div>

            {/* 2. 결과 성공 메시지 (Graph Added) */}
            {result && (
              <div className="bg-green-600 text-white rounded-[1em] p-8 shadow-lg animate-in slide-in-from-bottom-4 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-8 opacity-10">
                  <CheckCircle2 className="w-32 h-32" />
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 relative z-10">
                  {/* Left Info */}
                  <div className="lg:col-span-2 space-y-6">
                    <h3 className="text-2xl font-serif font-bold mb-4 flex items-center gap-2">
                      <CheckCircle2 className="w-8 h-8" />
                      로스팅 완료!
                    </h3>
                    <div className="space-y-2">
                      <p className="text-green-100 text-sm">생산된 원두</p>
                      <p className="text-3xl font-bold">{result.roasted_bean.name}</p>
                      <div className="flex flex-wrap gap-2 mt-2">
                        <Badge className="bg-white/20 hover:bg-white/30 text-white border-white/20 font-mono text-sm">
                          BATCH: {result.batch_no}
                        </Badge>
                        <Badge className="bg-white/10 hover:bg-white/20 text-green-50 border-white/10 font-mono text-sm">
                          SKU: {result.roasted_bean.sku}
                        </Badge>
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-white/10 rounded-xl p-4 backdrop-blur-sm border border-white/10">
                        <p className="text-green-100 text-xs mb-1">최종 생산량</p>
                        <p className="text-2xl font-mono font-bold">
                          {result.roasted_bean.quantity_kg.toFixed(2)} kg
                        </p>
                      </div>
                      <div className="bg-white/10 rounded-xl p-4 backdrop-blur-sm border border-white/10">
                        <p className="text-green-100 text-xs mb-1">최종 손실률</p>
                        <p className="text-2xl font-mono font-bold">
                          {result.loss_rate_percent.toFixed(1)} %
                        </p>
                      </div>
                      <div className="bg-white/10 rounded-xl p-4 backdrop-blur-sm border border-white/10">
                        <p className="text-green-100 text-xs mb-1">kg당 원가 (FIFO)</p>
                        <p className="text-xl font-mono font-bold">
                          ₩{formatCurrency(result.production_cost)}
                        </p>
                      </div>
                      <div className="bg-white/10 rounded-xl p-4 backdrop-blur-sm border border-white/10">
                        <p className="text-green-100 text-xs mb-1">총 생산 원가</p>
                        <p className="text-xl font-mono font-bold">
                          ₩
                          {formatCurrency(result.production_cost * result.roasted_bean.quantity_kg)}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Right Chart */}
                  <div className="flex flex-col items-center justify-center bg-white/5 rounded-2xl p-4 backdrop-blur-sm border border-white/10">
                    <ChartContainer
                      config={{
                        production: { label: '생산', color: '#ffffff' },
                        loss: { label: '손실', color: 'rgba(255,255,255,0.2)' },
                      }}
                      className="mx-auto aspect-square max-h-[160px] w-full"
                    >
                      <PieChart>
                        <ChartTooltip content={<ChartTooltipContent hideLabel />} cursor={false} />
                        <Pie
                          data={[
                            {
                              browser: 'production',
                              visitors: 100 - result.loss_rate_percent,
                              fill: '#ffffff',
                            },
                            {
                              browser: 'loss',
                              visitors: result.loss_rate_percent,
                              fill: 'rgba(255,255,255,0.2)',
                            },
                          ]}
                          dataKey="visitors"
                          nameKey="browser"
                          innerRadius={50}
                          outerRadius={75}
                          strokeWidth={0}
                        >
                          <Label
                            content={({ viewBox }) => {
                              if (viewBox && 'cx' in viewBox && 'cy' in viewBox) {
                                return (
                                  <text
                                    x={viewBox.cx}
                                    y={viewBox.cy}
                                    textAnchor="middle"
                                    dominantBaseline="middle"
                                  >
                                    <tspan
                                      x={viewBox.cx}
                                      y={viewBox.cy}
                                      className="fill-white text-2xl font-bold"
                                    >
                                      {result.loss_rate_percent.toFixed(1)}%
                                    </tspan>
                                    <tspan
                                      x={viewBox.cx}
                                      y={(viewBox.cy || 0) + 20}
                                      className="fill-green-100 text-xs"
                                    >
                                      손실률
                                    </tspan>
                                  </text>
                                );
                              }
                            }}
                          />
                        </Pie>
                      </PieChart>
                    </ChartContainer>
                    <p className="text-green-100 text-xs mt-2 font-medium">손실 vs 생산 비율</p>
                  </div>
                </div>

                <div className="mt-8 flex justify-end border-t border-white/10 pt-6">
                  <Button
                    variant="secondary"
                    className="bg-white text-green-700 hover:bg-green-50 shadow-lg border-0 font-bold px-8 h-12 text-lg"
                    onClick={() => {
                      setResult(null);
                      setTargetWeight('');
                      setActualOutputWeight('');
                      setSimulation(null);
                      setSelectedBeanId('');
                      setRoastProfile('LIGHT');
                      setNotes('');
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

      {/* Alert Dialog (Receipt Style) */}
      <AlertDialog open={dialogConfig.isOpen} onOpenChange={closeDialog}>
        <AlertDialogContent className="bg-[#FFFBF5] border-2 border-dashed border-[#D7CCC8] rounded-[2.5rem] shadow-2xl p-0 max-w-xl overflow-visible outline-none sm:rounded-[2.5rem]">
          {/* Top Pin Decoration */}
          <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 w-6 h-6 rounded-full bg-red-50 shadow-sm z-20 border-4 border-red-100"></div>

          <div className="p-8 relative">
            {/* Vintage Title */}
            <AlertDialogHeader className="space-y-6">
              <div className="text-center space-y-2 pb-6 border-b-2 border-dashed border-[#D7CCC8]">
                <AlertDialogTitle className="font-serif italic text-3xl text-red-900 font-bold tracking-tight">
                  {dialogConfig.title}
                </AlertDialogTitle>
              </div>

              <AlertDialogDescription className="whitespace-pre-wrap font-mono text-[#5D4037] text-lg font-bold leading-relaxed bg-[#FAF7F2] p-8 rounded-xl border border-[#EFEBE9] text-left" asChild>
                <div className="w-full">{dialogConfig.description}</div>
              </AlertDialogDescription>
            </AlertDialogHeader>

            <AlertDialogFooter className="mt-8 gap-3 sm:space-x-4 sm:justify-center w-full">
              {dialogConfig.type === 'confirm' && (
                <AlertDialogCancel
                  onClick={closeDialog}
                  className="border-none bg-transparent text-[#8D6E63] hover:bg-[#D7CCC8]/20 hover:text-[#5D4037] rounded-xl px-6 font-bold"
                >
                  취소
                </AlertDialogCancel>
              )}
              <AlertDialogAction
                onClick={() => {
                  if (dialogConfig.onConfirm) dialogConfig.onConfirm();
                  closeDialog();
                }}
                className="bg-[#5D4037] hover:bg-[#4E342E] text-[#EFEBE9] rounded-xl px-8 shadow-lg hover:shadow-xl transition-all font-bold"
              >
                확인
              </AlertDialogAction>
            </AlertDialogFooter>
          </div>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
