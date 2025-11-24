'use client'

import { useState, useEffect } from 'react'
import { BeanCreateData, Bean } from '@/lib/api'
import Link from 'next/link'

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
        origin: '',
        variety: '',
        processing_method: '',
        roast_level: 'Medium',
        purchase_date: new Date().toISOString().split('T')[0],
        purchase_price_per_kg: 0,
        quantity_kg: 0,
        notes: '',
    })

    useEffect(() => {
        if (initialData) {
            setFormData({
                name: initialData.name,
                origin: initialData.origin,
                variety: initialData.variety,
                processing_method: initialData.processing_method,
                roast_level: initialData.roast_level,
                purchase_date: initialData.purchase_date,
                purchase_price_per_kg: initialData.purchase_price_per_kg,
                quantity_kg: initialData.quantity_kg,
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
        <div className="container mx-auto px-4 py-8 max-w-2xl">
            <div className="mb-8">
                <Link
                    href="/beans"
                    className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 mb-4 inline-block"
                >
                    ← 목록으로 돌아가기
                </Link>
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                    {title}
                </h1>
            </div>

            <form
                onSubmit={handleSubmit}
                className="space-y-6 bg-white dark:bg-gray-800 p-6 rounded-lg shadow border border-gray-200 dark:border-gray-700"
            >
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="col-span-2">
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            원두명 *
                        </label>
                        <input
                            type="text"
                            name="name"
                            required
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                            value={formData.name}
                            onChange={handleChange}
                            placeholder="직접 입력 (예: 에티오피아 예가체프 G1)"
                            list="bean-names"
                        />
                        <datalist id="bean-names">
                            <option value="에티오피아 예가체프 G1" />
                            <option value="에티오피아 시다모 G2" />
                            <option value="콜롬비아 수프리모" />
                            <option value="과테말라 안티구아" />
                            <option value="브라질 세라도" />
                            <option value="케냐 AA" />
                            <option value="코스타리카 따라주" />
                            <option value="인도네시아 만델링" />
                        </datalist>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            원산지 *
                        </label>
                        <select
                            name="origin"
                            required
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                            value={formData.origin}
                            onChange={handleChange}
                        >
                            <option value="">선택해주세요</option>
                            <option value="Ethiopia">Ethiopia (에티오피아)</option>
                            <option value="Colombia">Colombia (콜롬비아)</option>
                            <option value="Guatemala">Guatemala (과테말라)</option>
                            <option value="Brazil">Brazil (브라질)</option>
                            <option value="Kenya">Kenya (케냐)</option>
                            <option value="Costa Rica">Costa Rica (코스타리카)</option>
                            <option value="Indonesia">Indonesia (인도네시아)</option>
                            <option value="Vietnam">Vietnam (베트남)</option>
                            <option value="Panama">Panama (파나마)</option>
                            <option value="El Salvador">El Salvador (엘살바도르)</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            품종
                        </label>
                        <select
                            name="variety"
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                            value={formData.variety}
                            onChange={handleChange}
                        >
                            <option value="">선택해주세요</option>
                            <option value="Arabica">Arabica (아라비카)</option>
                            <option value="Robusta">Robusta (로부스타)</option>
                            <option value="Typica">Typica (티피카)</option>
                            <option value="Bourbon">Bourbon (버번)</option>
                            <option value="Caturra">Caturra (카투라)</option>
                            <option value="Catuai">Catuai (카투아이)</option>
                            <option value="Geisha">Geisha (게이샤)</option>
                            <option value="Heirloom">Heirloom (에어룸)</option>
                            <option value="SL28">SL28</option>
                            <option value="SL34">SL34</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            가공 방식
                        </label>
                        <select
                            name="processing_method"
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                            value={formData.processing_method}
                            onChange={handleChange}
                        >
                            <option value="">선택해주세요</option>
                            <option value="Washed">Washed (워시드)</option>
                            <option value="Natural">Natural (내추럴)</option>
                            <option value="Honey">Honey (허니)</option>
                            <option value="Pulped Natural">Pulped Natural (펄프드 내추럴)</option>
                            <option value="Anaerobic">Anaerobic (무산소 발효)</option>
                            <option value="Wet Hulled">Wet Hulled (웻 헐링)</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            로스팅 포인트
                        </label>
                        <select
                            name="roast_level"
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                            value={formData.roast_level}
                            onChange={handleChange}
                        >
                            <option value="Light">Light (약배전 - 시나몬)</option>
                            <option value="Medium-Light">Medium-Light (중약배전 - 미디엄/하이)</option>
                            <option value="Medium">Medium (중배전 - 시티)</option>
                            <option value="Medium-Dark">Medium-Dark (중강배전 - 풀시티)</option>
                            <option value="Dark">Dark (강배전 - 프렌치/이탈리안)</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            구매일
                        </label>
                        <input
                            type="date"
                            name="purchase_date"
                            required
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                            value={formData.purchase_date}
                            onChange={handleChange}
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            구매가 (kg당)
                        </label>
                        <input
                            type="number"
                            name="purchase_price_per_kg"
                            required
                            min="0"
                            step="100"
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                            value={formData.purchase_price_per_kg}
                            onChange={handleChange}
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            초기 재고량 (kg)
                        </label>
                        <input
                            type="number"
                            name="quantity_kg"
                            required
                            min="0"
                            step="0.1"
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                            value={formData.quantity_kg}
                            onChange={handleChange}
                        />
                    </div>

                    <div className="col-span-2">
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            메모
                        </label>
                        <textarea
                            name="notes"
                            rows={3}
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                            value={formData.notes}
                            onChange={handleChange}
                        />
                    </div>
                </div>

                <div className="flex justify-end gap-4 mt-8">
                    <Link
                        href="/beans"
                        className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-700"
                    >
                        취소
                    </Link>
                    <button
                        type="submit"
                        disabled={isSubmitting}
                        className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {isSubmitting ? '처리 중...' : submitLabel}
                    </button>
                </div>
            </form>
        </div>
    )
}
