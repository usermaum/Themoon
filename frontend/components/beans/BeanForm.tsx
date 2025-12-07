'use client'

import { useState, useEffect } from 'react'
import { BeanCreateData, Bean, BeanAPI } from '@/lib/api'
import Link from 'next/link'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Textarea } from '@/components/ui/Textarea'
import { Label } from '@/components/ui/Label'
import { Card, CardContent } from '@/components/ui/Card'
import { ArrowLeft, Check, Coffee } from 'lucide-react'

interface BeanFormProps {
    initialData?: Bean
    onSubmit: (data: BeanCreateData) => Promise<void>
    isSubmitting: boolean
    title: string
    submitLabel: string
}

export default function BeanForm({
    initialData,
    onSubmit,
    isSubmitting,
    title,
    submitLabel,
}: BeanFormProps) {
    const [formData, setFormData] = useState<BeanCreateData>({
        name: '',
        type: 'GREEN_BEAN', // Default type
        origin: '',
        variety: '',
        processing_method: '',
        roast_level: 'Medium',
        purchase_date: new Date().toISOString().split('T')[0],
        purchase_price_per_kg: 0,
        quantity_kg: 0,
        notes: '',
    })

    // 데이터베이스에서 가져온 고유 옵션들
    const [varietyOptions, setVarietyOptions] = useState<string[]>([])
    const [originOptions, setOriginOptions] = useState<string[]>([])
    const [processingOptions, setProcessingOptions] = useState<string[]>([])

    // DB에서 기존 원두 정보를 가져와 고유 값 추출
    useEffect(() => {
        const fetchOptions = async () => {
            try {
                const response = await BeanAPI.getAll({ limit: 100 })
                const beans = response.items || response

                // 고유 값 추출 (빈 값 제외, 정렬)
                const varieties = Array.from(new Set(beans.map((b: Bean) => b.variety).filter((v): v is string => !!v))).sort()
                const origins = Array.from(new Set(beans.map((b: Bean) => b.origin).filter((v): v is string => !!v))).sort()
                const processings = Array.from(new Set(beans.map((b: Bean) => b.processing_method).filter((v): v is string => !!v))).sort()

                setVarietyOptions(varieties)
                setOriginOptions(origins)
                setProcessingOptions(processings)
            } catch (err) {
                console.error('Failed to fetch bean options:', err)
            }
        }
        fetchOptions()
    }, [])

    useEffect(() => {
        if (initialData) {
            setFormData({
                name: initialData.name,
                type: initialData.type,
                origin: initialData.origin,
                variety: initialData.variety,
                processing_method: initialData.processing_method,
                roast_level: initialData.roast_level,
                purchase_date: initialData.purchase_date,
                purchase_price_per_kg: initialData.purchase_price_per_kg,
                quantity_kg: parseFloat(initialData.quantity_kg.toFixed(2)),
                notes: initialData.notes || '',
            })
        }
    }, [initialData])

    const handleChange = (
        e: React.ChangeEvent<
            HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
        >
    ) => {
        const { name, value } = e.target
        setFormData((prev) => ({
            ...prev,
            [name]:
                name === 'purchase_price_per_kg' || name === 'quantity_kg'
                    ? parseFloat(value) || 0
                    : value,
        }))
    }

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        onSubmit(formData)
    }

    return (
        <div className="container mx-auto px-4 py-4 max-w-4xl">
            <div className="mb-8 flex items-center justify-between">
                <Link
                    href="/beans"
                    className="flex items-center gap-2 text-latte-600 hover:text-latte-900 font-bold transition-colors"
                >
                    <ArrowLeft className="w-5 h-5" />
                    이전으로
                </Link>
            </div>

            <Card className="border-latte-100 shadow-lg rounded-[1em]">
                <CardContent className="p-8">
                    <form onSubmit={handleSubmit} className="space-y-8">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            {/* 기본 정보 섹션 */}
                            <div className="col-span-2 space-y-4">
                                <h3 className="text-lg font-serif font-bold text-latte-800 border-b border-latte-100 pb-2 flex items-center gap-2">
                                    <Coffee className="w-5 h-5 text-latte-400" /> 기본 정보
                                </h3>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div className="space-y-2 col-span-2 md:col-span-1">
                                        <Label htmlFor="name">원두명 *</Label>
                                        <Input
                                            id="name"
                                            name="name"
                                            required
                                            value={formData.name}
                                            onChange={handleChange}
                                            placeholder="예: 에티오피아 예가체프 G1"
                                            list="bean-names"
                                            className="bg-latte-50/50"
                                        />
                                        <datalist id="bean-names">
                                            <option value="에티오피아 예가체프 G1" />
                                            <option value="에티오피아 시다모 G2" />
                                            <option value="콜롬비아 수프리모" />
                                            <option value="과테말라 안티구아" />
                                            <option value="브라질 세라도" />
                                            <option value="케냐 AA" />
                                        </datalist>
                                    </div>

                                    <div className="space-y-2 col-span-2 md:col-span-1">
                                        <Label htmlFor="origin">원산지 *</Label>
                                        <div className="relative">
                                            <select
                                                id="origin"
                                                name="origin"
                                                required
                                                className="flex h-10 w-full rounded-md border border-input bg-latte-50/50 px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 appearance-none"
                                                value={formData.origin}
                                                onChange={handleChange}
                                            >
                                                <option value="">원산지 선택</option>
                                                {originOptions.map(origin => (
                                                    <option key={origin} value={origin}>{origin}</option>
                                                ))}
                                            </select>
                                            <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-latte-500">
                                                <svg className="h-4 w-4 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" /></svg>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* 상세 정보 섹션 */}
                            <div className="col-span-2 space-y-4">
                                <h3 className="text-lg font-serif font-bold text-latte-800 border-b border-latte-100 pb-2">상세 정보</h3>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div className="space-y-2">
                                        <Label htmlFor="variety">품종</Label>
                                        <div className="relative">
                                            <select
                                                id="variety"
                                                name="variety"
                                                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 appearance-none bg-white"
                                                value={formData.variety}
                                                onChange={handleChange}
                                            >
                                                <option value="">품종 선택</option>
                                                {varietyOptions.map(variety => (
                                                    <option key={variety} value={variety}>{variety}</option>
                                                ))}
                                            </select>
                                            <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-latte-500">
                                                <svg className="h-4 w-4 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" /></svg>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="processing_method">가공 방식</Label>
                                        <div className="relative">
                                            <select
                                                id="processing_method"
                                                name="processing_method"
                                                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 appearance-none bg-white"
                                                value={formData.processing_method}
                                                onChange={handleChange}
                                            >
                                                <option value="">가공 방식 선택</option>
                                                {processingOptions.map(method => (
                                                    <option key={method} value={method}>{method}</option>
                                                ))}
                                            </select>
                                            <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-latte-500">
                                                <svg className="h-4 w-4 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" /></svg>
                                            </div>
                                        </div>
                                    </div>

                                    {/* 로스팅 포인트 선택 섹션 삭제됨 */}
                                </div>
                            </div>

                            {/* 재고 및 구매 정보 섹션 */}
                            <div className="col-span-2 space-y-4">
                                <h3 className="text-lg font-serif font-bold text-latte-800 border-b border-latte-100 pb-2">재고 및 구매</h3>

                                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                    <div className="space-y-2">
                                        <Label htmlFor="purchase_date">구매일</Label>
                                        <Input
                                            id="purchase_date"
                                            type="date"
                                            name="purchase_date"
                                            required
                                            value={formData.purchase_date}
                                            onChange={handleChange}
                                            className="bg-white"
                                        />
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="purchase_price_per_kg">구매가 (kg당)</Label>
                                        <Input
                                            id="purchase_price_per_kg"
                                            type="number"
                                            name="purchase_price_per_kg"
                                            required
                                            min="0"
                                            step="100"
                                            value={formData.purchase_price_per_kg}
                                            onChange={handleChange}
                                            className="font-mono bg-white"
                                        />
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="quantity_kg">초기 재고량 (kg)</Label>
                                        <Input
                                            id="quantity_kg"
                                            type="number"
                                            name="quantity_kg"
                                            required
                                            min="0"
                                            step="0.1"
                                            value={formData.quantity_kg}
                                            onChange={handleChange}
                                            className="font-mono bg-white"
                                        />
                                    </div>
                                </div>
                            </div>

                            <div className="col-span-2 space-y-2">
                                <Label htmlFor="notes">메모</Label>
                                <Textarea
                                    id="notes"
                                    name="notes"
                                    rows={3}
                                    value={formData.notes}
                                    onChange={handleChange}
                                    placeholder="특이사항이나 노트가 있다면 기록해주세요."
                                    className="bg-white resize-none"
                                />
                            </div>
                        </div>

                        <div className="flex justify-end gap-4 pt-4 border-t border-latte-100">
                            <Button
                                type="button"
                                variant="outline"
                                asChild
                                className="px-6"
                            >
                                <Link href="/beans">이전으로</Link>
                            </Button>
                            <Button
                                type="submit"
                                disabled={isSubmitting}
                                className="px-8 bg-latte-800 hover:bg-latte-900 text-white"
                            >
                                {isSubmitting ? '처리 중...' : (
                                    <>
                                        <Check className="w-4 h-4 mr-2" />
                                        {submitLabel}
                                    </>
                                )}
                            </Button>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}
