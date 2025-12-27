'use client';

import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';
import { Bean, BeanAPI, Blend, BlendAPI, RoastingAPI } from '@/lib/api';
import { formatCurrency, formatWeight } from '@/lib/utils';
import {
  Loader2,
  Bean as BeanIcon,
  Flame,
  ArrowRight,
  ArrowLeft,
  Scale,
  Calculator,
  Layers,
  AlertTriangle,
  CheckCircle2,
} from 'lucide-react';
import PageHero from '@/components/ui/page-hero';
import BlendRatioChart from '@/components/charts/BlendRatioChart';
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

// 블렌드 로스팅 (Pre-Roast Blending Simulator & Executor)
export default function BlendRoastingPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  // 데이터
  const [blends, setBlends] = useState<Blend[]>([]);
  const [availableBeans, setAvailableBeans] = useState<Bean[]>([]);

  // 입력 상태
  const [selectedBlendId, setSelectedBlendId] = useState<string>('');
  const [targetWeight, setTargetWeight] = useState<number>(0);
  const [actualBeanInputs, setActualBeanInputs] = useState<Record<number, string>>({});
  const [actualBeanLossRates, setActualBeanLossRates] = useState<Record<number, string>>({});
  const [actualOutputWeight, setActualOutputWeight] = useState<string>('');

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

  const showDialog = (
    title: string,
    description: React.ReactNode,
    type: 'alert' | 'confirm' = 'alert',
    onConfirm?: () => void
  ) => {
    setDialogConfig({
      isOpen: true,
      title,
      description,
      type,
      onConfirm,
    });
  };

  const closeDialog = () => {
    setDialogConfig((prev) => ({ ...prev, isOpen: false }));
  };

  // 계산 결과 상태
  const [simulationResult, setSimulationResult] = useState<{
    avgLossRate: number;
    totalRequired: number;
    details: Array<{
      beanId: number;
      beanName: string;
      origin: string;
      ratio: number;
      lossRate: number;
      requiredAmount: number;
      currentStock: number;
      isStockShort: boolean;
    }>;
  } | null>(null);

  // 초기 데이터 로드
  useEffect(() => {
    const loadData = async () => {
      try {
        const [beansRes, blendsRes] = await Promise.all([
          BeanAPI.getAll({ limit: 100, type: ['GREEN_BEAN'] }),
          BlendAPI.getAll(),
        ]);

        // 생두만 필터링 (서버에서 이미 필터링됨)
        setAvailableBeans(beansRes.items);
        setBlends(blendsRes);
      } catch (err) {
        console.error('Failed to load initial data:', err);
        showDialog('오류 발생', '데이터를 불러오는데 실패했습니다.');
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  // 시뮬레이션 계산 (블렌드 선택 or 목표량 변경 시)
  useEffect(() => {
    if (!selectedBlendId || targetWeight <= 0) {
      setSimulationResult(null);
      return;
    }

    const blend = blends.find((b) => b.id.toString() === selectedBlendId);
    if (!blend) return;

    let totalRequiredCalc = 0;
    const details: any[] = [];

    blend.recipe.forEach((item) => {
      const bean = availableBeans.find((b) => b.id === item.bean_id);
      if (bean) {
        const ratio = item.ratio; // 0.4 etc
        const lossRate = bean.expected_loss_rate !== undefined ? bean.expected_loss_rate : 0.15;

        // 개별 필요량 역산: (목표량 * 비율) / (1 - 손실률)
        // 예: 10kg의 40%인 4kg를 얻으려면, 손실률 15%일 때 4 / 0.85 = 4.7kg 필요
        const targetPartWeight = targetWeight * ratio;
        const requiredAmount = targetPartWeight / (1 - lossRate);

        totalRequiredCalc += requiredAmount;

        details.push({
          beanId: bean.id,
          beanName: bean.name,
          origin: bean.origin || 'Unknown',
          ratio: ratio * 100, // %
          lossRate: lossRate * 100, // %
          requiredAmount: requiredAmount,
          currentStock: bean.quantity_kg,
          isStockShort: bean.quantity_kg < requiredAmount,
        });
      }
    });

    // 평균 손실률 역산
    const avgLossRate = totalRequiredCalc > 0 ? 1 - targetWeight / totalRequiredCalc : 0;

    setSimulationResult({
      avgLossRate,
      totalRequired: totalRequiredCalc,
      details,
    });
  }, [selectedBlendId, targetWeight, blends, availableBeans]);

  // Auto-fill Actual Inputs from Simulation
  useEffect(() => {
    if (simulationResult) {
      const inputs: Record<number, string> = {};
      const rates: Record<number, string> = {};
      simulationResult.details.forEach((d) => {
        inputs[d.beanId] = d.requiredAmount.toFixed(2);
        rates[d.beanId] = d.lossRate.toFixed(1);
      });
      setActualBeanInputs(inputs);
      setActualBeanLossRates(rates);
    } else {
      setActualBeanInputs({});
      setActualBeanLossRates({});
    }
  }, [simulationResult]);

  const handleLossRateChange = (beanId: number, newRateStr: string) => {
    setActualBeanLossRates((prev) => ({ ...prev, [beanId]: newRateStr }));

    const newRate = parseFloat(newRateStr);
    if (!isNaN(newRate) && simulationResult && targetWeight > 0) {
      const detail = simulationResult.details.find((d) => d.beanId === beanId);
      if (detail) {
        const ratio = detail.ratio / 100;
        const lossRate = newRate / 100;
        if (lossRate < 0.99) {
          const newReq = (targetWeight * ratio) / (1 - lossRate);
          setActualBeanInputs((prev) => ({ ...prev, [beanId]: newReq.toFixed(2) }));
        }
      }
    }
  };

  const handleRoast = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedBlendId || targetWeight <= 0) return;

    // Calc Total Input from individual inputs
    const inputW = Object.values(actualBeanInputs).reduce(
      (sum, val) => sum + (parseFloat(val) || 0),
      0
    );

    if (inputW <= 0) {
      showDialog('오류', '실제 투입량을 확인해주세요.');
      return;
    }
    if (!actualOutputWeight || parseFloat(actualOutputWeight) <= 0) {
      showDialog('오류', '실제 생산량을 입력해주세요.');
      return;
    }

    const outputW = parseFloat(actualOutputWeight);
    const lossRate = inputW > 0 ? ((inputW - outputW) / inputW) * 100 : 0;

    const proceedRoasting = async () => {
      setSubmitting(true);
      try {
        // @ts-ignore
        const res = await RoastingAPI.roastBlend({
          blend_id: Number(selectedBlendId),
          output_weight: outputW,
          input_weight: inputW,
          notes: 'Recorded from Blend Roasting Page',
        });

        showDialog(
          '로스팅 완료',
          `블렌드 로스팅이 성공적으로 기록되었습니다.\n\n배치 번호: ${res.batch_no}\n생산된 원두: ${res.roasted_bean.name}\n생산 원가: ₩${formatCurrency(res.production_cost)}/kg\n총 생산 원가: ₩${formatCurrency(res.production_cost * res.roasted_bean.quantity_kg)}`,
          'alert',
          () => {
            setSelectedBlendId('');
            setTargetWeight(0);
            setSimulationResult(null);
            setActualBeanInputs({});
            setActualOutputWeight('');
          }
        );
      } catch (err: any) {
        console.error(err);
        showDialog(
          '오류 발생',
          err.response?.data?.detail || '로스팅을 기록하는 중 문제가 발생했습니다.'
        );
      } finally {
        setSubmitting(false);
      }
    };

    // 재고 부족 체크 (시뮬레이션 기준)
    const shortItems = simulationResult?.details.filter((d) => d.isStockShort) || [];
    if (shortItems.length > 0) {
      const shortNames = shortItems.map((d) => d.beanName).join(', ');
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
            <div className="space-y-1">
              {shortItems.map(item => (
                <span key={item.beanId} className="block text-red-600 font-bold text-base bg-white/60 px-2 py-1 rounded">
                  • {item.beanName}
                </span>
              ))}
            </div>
          </div>

          <div className="bg-red-900/5 p-4 rounded-xl text-red-800 text-sm font-medium leading-relaxed">
            💡 재고를 입고하거나 투입량을 조정한 후 다시 시도해주세요.
          </div>
        </div>,
        'alert'
      );
      return;
    }

    showDialog(
      '로스팅 결과 저장',
      <div className="space-y-6">
        <div className="flex justify-center mb-2">
          <div className="w-16 h-16 rounded-full bg-amber-50 flex items-center justify-center shadow-inner">
            <CheckCircle2 className="w-8 h-8 text-amber-600" />
          </div>
        </div>
        <p className="text-center text-latte-600 text-lg font-medium leading-relaxed">
          다음 내용으로<br />블렌드 로스팅 이력을 저장하시겠습니까?
        </p>

        <div className="bg-white rounded-2xl p-5 border border-latte-100 shadow-sm space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-sm font-bold text-latte-500">실제 투입</span>
            <span className="font-mono font-bold text-lg text-latte-900">{inputW.toFixed(2)}<span className="text-sm text-latte-400 ml-0.5">kg</span></span>
          </div>
          <div className="w-full h-px bg-latte-50" />
          <div className="flex justify-between items-center">
            <span className="text-sm font-bold text-latte-500">실제 생산</span>
            <span className="font-mono font-bold text-lg text-latte-900">{outputW}<span className="text-sm text-latte-400 ml-0.5">kg</span></span>
          </div>
          <div className="w-full h-px bg-latte-50" />
          <div className="flex justify-between items-center">
            <span className="text-sm font-bold text-latte-500">실제 손실률</span>
            <span className="font-mono font-bold text-lg text-amber-600">{lossRate.toFixed(1)}<span className="text-sm ml-0.5 text-amber-600/70">%</span></span>
          </div>
        </div>

        <div className="flex justify-center">
          <span className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-full bg-latte-50 text-xs font-bold text-latte-400 border border-latte-100">
            목표 생산량: {targetWeight}kg
          </span>
        </div>
      </div>,
      'confirm',
      proceedRoasting
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-12">
        <Loader2 className="w-8 h-8 animate-spin text-amber-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <PageHero
        title="Pre-Roast Blending"
        description="블렌드 레시피에 따라 여러 생두를 혼합하여 로스팅합니다. 생두별 손실률을 기반으로 필요 투입량을 자동 계산합니다."
        icon={<Layers />}
        image="/images/hero/blend_roast_hero.png"
        className="mb-8 min-h-[280px]"
      />

      <div className="container mx-auto p-6 max-w-5xl">
        <div className="mb-6">
          <button
            onClick={() => router.push('/roasting')}
            className="flex items-center gap-2 text-slate-600 hover:text-slate-900 font-bold transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            이전으로
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* 왼쪽: 설정 폼 */}
          <section className="lg:col-span-5 space-y-6 h-full">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 h-full flex flex-col">
              <h2 className="text-lg font-bold mb-4 flex items-center gap-2 text-slate-700">
                <Calculator className="w-5 h-5 text-slate-500" />
                생산 설정
              </h2>

              <form onSubmit={handleRoast} className="space-y-6 flex-1 flex flex-col">
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
                      {blends.map((blend) => (
                        <SelectItem key={blend.id} value={String(blend.id)}>
                          {blend.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">
                    목표 생산량 (Roasted Weight)
                  </label>
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

                {/* Actual Data Inputs Section */}
                {simulationResult && (
                  <div className="grid grid-cols-2 gap-3 mb-8">
                    <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 flex flex-col items-center justify-center gap-1">
                      <span className="text-xs font-semibold text-slate-500">총 필요 생두량</span>
                      <span className="text-lg font-bold text-slate-700">
                        {formatWeight(simulationResult.totalRequired)} kg
                      </span>
                    </div>
                    <div className="bg-amber-50/60 p-3 rounded-xl border border-amber-100/50 flex flex-col items-center justify-center gap-1">
                      <span className="text-xs font-semibold text-amber-600">예상 손실률</span>
                      <span className="text-lg font-bold text-amber-700">
                        {(simulationResult.avgLossRate * 100).toFixed(1)} %
                      </span>
                    </div>
                  </div>
                )}

                {/* Actual Data Inputs Section */}
                <div className="pt-8 border-t border-slate-100 mt-8 flex-1">
                  <h3 className="text-lg font-bold text-slate-800 mb-6 flex items-center gap-2">
                    <Scale className="w-5 h-5 text-amber-600" />
                    실제 투입 및 결과 입력 (Actual)
                  </h3>

                  {/* 1. Individual Inputs List */}
                  <div className="space-y-4 mb-8">
                    {simulationResult?.details.map((detail) => (
                      <div key={detail.beanId} className="flex items-center justify-between group">
                        <div className="flex flex-col">
                          <span className="text-sm font-bold text-slate-700 group-hover:text-amber-700 transition-colors">
                            {detail.beanName}
                          </span>
                          <span className="text-xs text-slate-400">{detail.origin}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          {/* Loss Rate Input */}
                          <div className="relative w-20">
                            <input
                              type="number"
                              className="w-full h-12 pr-6 text-center text-sm font-semibold text-slate-500 border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500 outline-none hover:border-amber-300 transition-colors bg-slate-50/50"
                              value={actualBeanLossRates[detail.beanId] || ''}
                              onChange={(e) => handleLossRateChange(detail.beanId, e.target.value)}
                              step="0.1"
                            />
                            <span className="absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 text-xs">
                              %
                            </span>
                          </div>

                          {/* Weight Input */}
                          <div className="relative w-36">
                            <input
                              type="number"
                              className="w-full h-12 pr-12 text-right text-lg font-bold text-slate-700 border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none transition-all shadow-sm group-hover:border-amber-300"
                              value={actualBeanInputs[detail.beanId] || ''}
                              onChange={(e) =>
                                setActualBeanInputs((prev) => ({
                                  ...prev,
                                  [detail.beanId]: e.target.value,
                                }))
                              }
                              step="0.01"
                            />
                            <span className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 font-medium text-sm">
                              kg
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Divider */}
                  <div className="h-px bg-slate-100 my-6" />

                  {/* 2. Totals */}
                  <div className="space-y-5">
                    {/* Total Input Summary */}
                    <div className="flex items-center justify-between">
                      <label className="text-sm font-bold text-amber-900 leading-tight">
                        실제 투입 합계 (Total)
                      </label>
                      <div className="w-36 h-12 flex items-center justify-end px-4 bg-amber-50 border border-amber-200 rounded-xl text-lg font-bold text-amber-900 shadow-sm">
                        {formatWeight(Object.values(actualBeanInputs)
                          .reduce((sum, val) => sum + (parseFloat(val) || 0), 0))}
                        <span className="text-sm font-medium ml-1 text-amber-700">kg</span>
                      </div>
                    </div>

                    {/* Total Output Input */}
                    <div className="flex items-center justify-between">
                      <label className="text-sm font-bold text-green-700 leading-tight">
                        실제 생산량 (Total)
                      </label>
                      <div className="relative w-36">
                        <input
                          type="number"
                          className="w-full h-12 pr-12 text-right text-lg font-bold text-green-800 bg-green-50 border border-green-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:bg-white outline-none transition-all shadow-sm placeholder-green-300"
                          placeholder="0.0"
                          value={actualOutputWeight}
                          onChange={(e) => setActualOutputWeight(e.target.value)}
                          step="0.1"
                        />
                        <span className="absolute right-4 top-1/2 -translate-y-1/2 text-green-600 font-medium text-sm">
                          kg
                        </span>
                      </div>
                    </div>

                    {/* Actual Loss Rate */}
                    <div className="mt-6 p-5 bg-white rounded-xl border border-slate-100 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] flex items-center justify-between group hover:border-amber-200 transition-colors">
                      <div className="flex flex-col gap-0.5">
                        <span className="text-sm font-bold text-slate-600">실제 손실률</span>
                        <span className="text-[11px] text-slate-400">투입 대비 생산 손실</span>
                      </div>
                      <span className="text-3xl font-black text-amber-600 tracking-tight">
                        {(Object.values(actualBeanInputs).reduce(
                          (sum, val) => sum + (parseFloat(val) || 0),
                          0
                        ) > 0
                          ? ((Object.values(actualBeanInputs).reduce(
                            (sum, val) => sum + (parseFloat(val) || 0),
                            0
                          ) -
                            (parseFloat(actualOutputWeight) || 0)) /
                            Object.values(actualBeanInputs).reduce(
                              (sum, val) => sum + (parseFloat(val) || 0),
                              0
                            )) *
                          100
                          : 0
                        ).toFixed(1)}
                        <span className="text-lg ml-0.5 font-bold text-amber-400">%</span>
                      </span>
                    </div>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={
                    submitting || !selectedBlendId || targetWeight <= 0 || !actualOutputWeight
                  }
                  className="w-full bg-slate-800 text-white py-3 rounded-lg font-medium hover:bg-slate-900 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 mt-auto"
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
          <section className="lg:col-span-7 h-full flex flex-col">
            {simulationResult ? (
              <>
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mb-3 flex-1 flex flex-col">
                  <div className="p-6 border-b border-slate-100 bg-slate-50">
                    <h2 className="text-lg font-bold flex items-center gap-2 text-slate-800">
                      <Scale className="w-5 h-5 text-blue-600" />
                      예상 투입 명세서 (Expected)
                    </h2>
                  </div>
                  <div className="p-0 flex-1 overflow-auto">
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
                              <span className="block text-xs text-slate-500 font-normal">
                                {detail.origin}
                              </span>
                            </td>
                            <td className="px-6 py-4 text-right">{Math.round(detail.ratio)}%</td>
                            <td className="px-6 py-4 text-right text-slate-500">
                              {detail.lossRate.toFixed(1)}%
                            </td>
                            <td className="px-6 py-4 text-right font-bold text-slate-800 bg-blue-50/50">
                              {formatWeight(detail.requiredAmount)} kg
                            </td>
                            <td
                              className={`px-6 py-4 text-right font-medium ${detail.isStockShort ? 'text-red-600' : 'text-green-600'}`}
                            >
                              {formatWeight(detail.currentStock)} kg
                              {detail.isStockShort && (
                                <span className="block text-[10px] text-red-500 font-bold">
                                  부족!
                                </span>
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
                            {formatWeight(simulationResult.totalRequired)} kg
                          </th>
                          <th className="px-6 py-3 text-right text-slate-500">-</th>
                        </tr>
                      </tfoot>
                    </table>
                  </div>

                  {/* Stock Status Check Banner (Embedded in Card) */}
                  {/* Stock Status Check Banner (Refined UI: Compact & Integrated) */}
                  <div
                    className={`border-t transition-all duration-300 ${simulationResult.details.some(d => d.isStockShort)
                        ? 'bg-red-50/30 border-red-100'
                        : 'bg-green-50/30 border-green-100'
                      }`}
                  >
                    <div className="p-4">
                      {simulationResult.details.some(d => d.isStockShort) ? (
                        <>
                          <div className="flex items-center gap-2 mb-3">
                            <div className="p-1.5 bg-red-100 rounded-lg shrink-0">
                              <AlertTriangle className="w-4 h-4 text-red-600" />
                            </div>
                            <h3 className="font-bold text-sm text-red-900">
                              재고 부족 경고
                            </h3>
                            <div className="h-px flex-1 bg-red-100/50 text-red-100"></div>
                          </div>

                          <div className="max-h-[140px] overflow-y-auto pr-1 space-y-1.5 scrollbar-thin scrollbar-thumb-red-200 scrollbar-track-transparent">
                            {simulationResult.details.filter(d => d.isStockShort).map(d => (
                              <div key={d.beanId} className="flex items-center justify-between bg-white px-3 py-2 rounded-lg border border-red-100 shadow-sm transition-all hover:bg-red-50/50">
                                <div className="flex items-center gap-2 min-w-0">
                                  <div className="w-1.5 h-1.5 rounded-full bg-red-500 shrink-0" />
                                  <span className="font-bold text-slate-700 text-sm truncate">{d.beanName}</span>
                                  <span className="text-xs text-slate-400 shrink-0">({d.origin})</span>
                                </div>
                                <div className="text-right shrink-0 flex items-center gap-2">
                                  <span className="text-xs text-red-500 font-bold">
                                    -{formatWeight(d.requiredAmount - d.currentStock)} kg
                                  </span>
                                  <span className="text-[10px] text-red-300 bg-red-50 px-1.5 py-0.5 rounded border border-red-100">부족</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </>
                      ) : (
                        <div className="flex items-center gap-2 text-green-700/80">
                          <CheckCircle2 className="w-4 h-4 text-green-600" />
                          <p className="text-sm font-medium mt-0.5">
                            현재 보유 중인 생두로 로스팅이 가능합니다.
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Chart Section (Separated) */}
                <div className="mt-3">
                  <BlendRatioChart data={simulationResult.details} />
                </div>
              </>
            ) : (
              <div className="bg-slate-50 border-2 border-dashed border-slate-200 rounded-xl p-12 text-center text-slate-500 h-full flex flex-col items-center justify-center">
                <BeanIcon className="w-12 h-12 mb-4 text-slate-300" />
                <p className="text-lg font-medium">블렌드를 선택하고 목표 생산량을 입력하세요.</p>
                <p className="text-sm">
                  각 생두별 손실률을 고려하여 정확한 투입량을 계산해드립니다.
                </p>
              </div>
            )}
          </section>
        </div>

        <AlertDialog open={dialogConfig.isOpen} onOpenChange={closeDialog}>
          <AlertDialogContent className="bg-white/95 backdrop-blur-xl border border-white/20 ring-1 ring-latte-900/5 shadow-[0_32px_64px_-12px_rgba(80,50,30,0.15)] rounded-[2rem] p-0 max-w-md overflow-hidden outline-none">
            <div className="bg-gradient-to-b from-amber-50/40 to-white p-8">
              <AlertDialogHeader className="space-y-4">
                <AlertDialogTitle className="hidden">
                  {dialogConfig.title}
                </AlertDialogTitle>

                <AlertDialogDescription asChild>
                  <div className="w-full text-latte-700 text-base leading-relaxed">
                    {dialogConfig.description}
                  </div>
                </AlertDialogDescription>
              </AlertDialogHeader>

              <AlertDialogFooter className="mt-8 flex gap-3 sm:space-x-0 w-full">
                {dialogConfig.type === 'confirm' && (
                  <AlertDialogCancel
                    onClick={closeDialog}
                    className="flex-1 border-0 bg-white hover:bg-latte-50 text-latte-500 hover:text-latte-700 rounded-xl py-6 font-bold shadow-sm ring-1 ring-latte-100 transition-all text-base"
                  >
                    취소
                  </AlertDialogCancel>
                )}
                <AlertDialogAction
                  onClick={() => {
                    if (dialogConfig.onConfirm) dialogConfig.onConfirm();
                    closeDialog();
                  }}
                  className={`flex-1 rounded-xl py-6 shadow-lg shadow-amber-900/20 transition-all font-bold text-base ${dialogConfig.type === 'alert'
                    ? 'bg-red-500 hover:bg-red-600 text-white w-full'
                    : 'bg-latte-900 hover:bg-latte-800 text-white'
                    }`}
                >
                  확인
                </AlertDialogAction>
              </AlertDialogFooter>
            </div>
          </AlertDialogContent>
        </AlertDialog>
      </div>
    </div>
  );
}
