'use client'

import { useState, useEffect } from 'react'
import { BeanCreateData, Bean } from '@/lib/api'
import Link from 'next/link'
import {
    TextInput,
    NumberInput,
    Textarea,
    Button,
    Group,
    Paper,
    Title,
    Text
} from '@mantine/core'
import { ArrowLeft } from 'lucide-react'

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
    const [name, setName] = useState('')
    const [origin, setOrigin] = useState('')
    const [variety, setVariety] = useState('')
    const [processingMethod, setProcessingMethod] = useState('')
    const [roastLevel, setRoastLevel] = useState('Medium')
    const [purchaseDate, setPurchaseDate] = useState(new Date().toISOString().split('T')[0])
    const [purchasePrice, setPurchasePrice] = useState<number | string>(0)
    const [quantity, setQuantity] = useState<number | string>(0)
    const [notes, setNotes] = useState('')

    useEffect(() => {
        if (initialData) {
            setName(initialData.name)
            setOrigin(initialData.origin)
            setVariety(initialData.variety)
            setProcessingMethod(initialData.processing_method)
            setRoastLevel(initialData.roast_level)
            setPurchaseDate(new Date(initialData.purchase_date).toISOString().split('T')[0])
            setPurchasePrice(initialData.purchase_price_per_kg)
            setQuantity(initialData.quantity_kg)
            setNotes(initialData.notes || '')
        }
    }, [initialData])

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        console.log("Submitting form..."); // Debug log

        const price = typeof purchasePrice === 'number' ? purchasePrice : parseFloat(purchasePrice as string) || 0
        const qty = typeof quantity === 'number' ? quantity : parseFloat(quantity as string) || 0

        onSubmit({
            name,
            origin: origin,
            variety: variety,
            processing_method: processingMethod,
            roast_level: roastLevel,
            purchase_date: purchaseDate,
            purchase_price_per_kg: price,
            quantity_kg: qty,
            notes
        })
    }

    return (
        <div className="container mx-auto px-4 py-8 max-w-2xl">
            <div className="mb-8">
                <Button
                    component={Link}
                    href="/beans"
                    variant="subtle"
                    color="gray"
                    leftSection={<ArrowLeft size={16} />}
                    mb="md"
                >
                    목록으로 돌아가기
                </Button>
                <Title order={2}>{title}</Title>
            </div>

            <Paper p="xl" radius="md" shadow="sm" withBorder>
                <form onSubmit={handleSubmit}>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="col-span-2">
                            <label className="block text-sm font-medium mb-1">원두명 *</label>
                            <input
                                name="name"
                                required
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                                placeholder="예: 에티오피아 예가체프 G1"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">원산지 *</label>
                            <select
                                name="origin"
                                required
                                value={origin}
                                onChange={(e) => setOrigin(e.target.value)}
                                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
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
                            <label className="block text-sm font-medium mb-1">품종</label>
                            <select
                                name="variety"
                                value={variety}
                                onChange={(e) => setVariety(e.target.value)}
                                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
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
                            <label className="block text-sm font-medium mb-1">가공 방식</label>
                            <select
                                name="processingMethod"
                                value={processingMethod}
                                onChange={(e) => setProcessingMethod(e.target.value)}
                                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
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
                            <label className="block text-sm font-medium mb-1">로스팅 포인트</label>
                            <select
                                name="roastLevel"
                                value={roastLevel}
                                onChange={(e) => setRoastLevel(e.target.value)}
                                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
                            >
                                <option value="Green">Green (생두)</option>
                                <option value="Light">Light (약배전 - 시나몬)</option>
                                <option value="Medium-Light">Medium-Light (중약배전 - 미디엄/하이)</option>
                                <option value="Medium">Medium (중배전 - 시티)</option>
                                <option value="Medium-Dark">Medium-Dark (중강배전 - 풀시티)</option>
                                <option value="Dark">Dark (강배전 - 프렌치/이탈리안)</option>
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">구매일 *</label>
                            <input
                                type="date"
                                name="purchaseDate"
                                required
                                value={purchaseDate}
                                onChange={(e) => setPurchaseDate(e.target.value)}
                                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">구매가 (kg당) *</label>
                            <input
                                type="number"
                                name="purchasePrice"
                                required
                                min="0"
                                step="100"
                                value={purchasePrice}
                                onChange={(e) => setPurchasePrice(e.target.value)}
                                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">초기 재고량 (kg) *</label>
                            <input
                                type="number"
                                name="quantity"
                                required
                                min="0"
                                step="0.1"
                                value={quantity}
                                onChange={(e) => setQuantity(e.target.value)}
                                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            />
                        </div>

                        <div className="col-span-2">
                            <label className="block text-sm font-medium mb-1">메모</label>
                            <textarea
                                name="notes"
                                rows={3}
                                value={notes}
                                onChange={(e) => setNotes(e.target.value)}
                                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            />
                        </div>
                    </div>

                    <Group justify="flex-end" mt="xl">
                        <Button
                            component={Link}
                            href="/beans"
                            variant="default"
                        >
                            취소
                        </Button>
                        <button
                            type="submit"
                            style={{
                                backgroundColor: '#f97316',
                                color: 'white',
                                padding: '8px 16px',
                                borderRadius: '4px',
                                border: 'none',
                                cursor: 'pointer'
                            }}
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? '처리 중...' : submitLabel}
                        </button>
                    </Group>
                </form>
            </Paper>
        </div>
    )
}
