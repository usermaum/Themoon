'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { BlendAPI, Bean, BeanAPI, BlendCreateData, BlendRecipeItem } from '@/lib/api'
import PageHero from '@/components/ui/PageHero'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Card, CardContent } from '@/components/ui/Card'
import { Plus, Coffee, Trash2, Hexagon, Save, ArrowLeft } from 'lucide-react'

export default function NewBlendPage() {
    const router = useRouter()
    const [loading, setLoading] = useState(false)
    const [submitting, setSubmitting] = useState(false)

    // Form State
    const [name, setName] = useState('')
    const [description, setDescription] = useState('')
    const [targetRoastLevel, setTargetRoastLevel] = useState('')
    const [notes, setNotes] = useState('')
    const [recipeItems, setRecipeItems] = useState<{ beanId: string, percent: string }[]>([])

    // Data State
    const [availableBeans, setAvailableBeans] = useState<Bean[]>([])

    useEffect(() => {
        const fetchBeans = async () => {
            try {
                const data = await BeanAPI.getAll({ limit: 100 })
                // BeanListResponse { items: Bean[], ... }
                setAvailableBeans(data.items)
            } catch (err) {
                console.error('Failed to fetch beans', err)
            }
        }
        fetchBeans()
    }, [])

    const addRecipeItem = () => {
        setRecipeItems([...recipeItems, { beanId: '', percent: '' }])
    }

    const removeRecipeItem = (index: number) => {
        const newItems = [...recipeItems]
        newItems.splice(index, 1)
        setRecipeItems(newItems)
    }

    const updateRecipeItem = (index: number, field: 'beanId' | 'percent', value: string) => {
        const newItems = [...recipeItems]
        newItems[index] = { ...newItems[index], [field]: value }
        setRecipeItems(newItems)
    }

    const totalPercent = recipeItems.reduce((sum, item) => sum + (parseFloat(item.percent) || 0), 0)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (recipeItems.length === 0) {
            alert('최소 하나 이상의 원두를 추가해주세요.')
            return
        }
        if (Math.abs(totalPercent - 100) > 0.1) {
            alert(`비율의 합은 100%여야 합니다. (현재: ${totalPercent}%)`)
            return
        }

        try {
            setSubmitting(true)

            const recipe: BlendRecipeItem[] = recipeItems.map(item => ({
                bean_id: parseInt(item.beanId),
                ratio: parseFloat(item.percent) / 100.0
            }))

            const blendData: BlendCreateData = {
                name,
                description,
                target_roast_level: targetRoastLevel,
                notes,
                recipe
            }

            await BlendAPI.create(blendData)
            router.push('/blends')
        } catch (err) {
            console.error('Failed to create blend', err)
            alert('블렌드 생성에 실패했습니다.')
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <div className="min-h-screen">
            <PageHero
                title="Create New Blend"
                description="새로운 블렌딩 레시피를 설계합니다."
                icon={<Hexagon />}
                image="/images/hero/beans-hero.png"
                className="mb-8"
            />

            <div className="container mx-auto px-4 py-8 max-w-3xl">
                <Button variant="ghost" onClick={() => router.back()} className="mb-6 pl-0 hover:bg-transparent hover:text-latte-800">
                    <ArrowLeft className="w-4 h-4 mr-2" /> 목록으로 돌아가기
                </Button>

                <Card className="border-latte-200 shadow-lg">
                    <CardContent className="p-8">
                        <form onSubmit={handleSubmit} className="space-y-8">
                            {/* 기본 정보 */}
                            <div className="space-y-4">
                                <h3 className="text-lg font-serif font-bold text-latte-800 border-b border-latte-100 pb-2">기본 정보</h3>
                                <div className="grid gap-4">
                                    <div className="grid gap-2">
                                        <label className="text-sm font-medium text-latte-600">블렌드 이름 *</label>
                                        <Input
                                            required
                                            value={name}
                                            onChange={(e) => setName(e.target.value)}
                                            placeholder="예: 문라이트 블렌드"
                                            className="bg-latte-50/50"
                                        />
                                    </div>
                                    <div className="grid gap-2">
                                        <label className="text-sm font-medium text-latte-600">설명</label>
                                        <Input
                                            value={description}
                                            onChange={(e) => setDescription(e.target.value)}
                                            placeholder="맛과 향에 대한 간단한 설명"
                                            className="bg-latte-50/50"
                                        />
                                    </div>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="grid gap-2">
                                            <label className="text-sm font-medium text-latte-600">목표 로스팅 포인트</label>
                                            <Input
                                                value={targetRoastLevel}
                                                onChange={(e) => setTargetRoastLevel(e.target.value)}
                                                placeholder="예: Medium Dark"
                                                className="bg-latte-50/50"
                                            />
                                        </div>
                                        <div className="grid gap-2">
                                            <label className="text-sm font-medium text-latte-600">참고 노트</label>
                                            <Input
                                                value={notes}
                                                onChange={(e) => setNotes(e.target.value)}
                                                placeholder="추가 메모"
                                                className="bg-latte-50/50"
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* 레시피 구성 */}
                            <div className="space-y-4">
                                <div className="flex justify-between items-end border-b border-latte-100 pb-2">
                                    <h3 className="text-lg font-serif font-bold text-latte-800">레시피 구성</h3>
                                    <span className={`text-sm font-bold ${totalPercent === 100 ? 'text-green-600' : 'text-red-500'}`}>
                                        총 합계: {totalPercent}%
                                    </span>
                                </div>

                                <div className="space-y-3">
                                    {recipeItems.map((item, index) => (
                                        <div key={index} className="flex gap-3 items-end p-4 bg-latte-50 rounded-xl relative group">
                                            <div className="flex-1">
                                                <label className="text-xs text-latte-500 mb-1 block">원두 선택</label>
                                                <select
                                                    className="w-full h-10 rounded-md border border-latte-200 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-latte-400 focus:border-transparent bg-white"
                                                    value={item.beanId}
                                                    onChange={(e) => updateRecipeItem(index, 'beanId', e.target.value)}
                                                    required
                                                >
                                                    <option value="">원두를 선택하세요</option>
                                                    {availableBeans.map(bean => (
                                                        <option key={bean.id} value={bean.id}>
                                                            {bean.name} ({bean.origin}) - ₩{bean.purchase_price_per_kg?.toLocaleString()}/kg
                                                        </option>
                                                    ))}
                                                </select>
                                            </div>
                                            <div className="w-24">
                                                <label className="text-xs text-latte-500 mb-1 block">비율 (%)</label>
                                                <div className="relative">
                                                    <Input
                                                        type="number"
                                                        value={item.percent}
                                                        onChange={(e) => updateRecipeItem(index, 'percent', e.target.value)}
                                                        className="pr-6 bg-white"
                                                        placeholder="0"
                                                        min="0"
                                                        max="100"
                                                        required
                                                    />
                                                    <span className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-latte-400">%</span>
                                                </div>
                                            </div>
                                            <Button
                                                type="button"
                                                variant="destructive"
                                                size="icon"
                                                onClick={() => removeRecipeItem(index)}
                                                className="mb-[1px]"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </Button>
                                        </div>
                                    ))}

                                    <Button
                                        type="button"
                                        variant="outline"
                                        className="w-full border-dashed border-2 border-latte-200 text-latte-500 hover:border-latte-400 hover:text-latte-700 hover:bg-latte-50"
                                        onClick={addRecipeItem}
                                    >
                                        <Plus className="w-4 h-4 mr-2" /> 원두 추가하기
                                    </Button>
                                </div>
                            </div>

                            <div className="pt-6 border-t border-latte-100 flex justify-end gap-3">
                                <Button type="button" variant="ghost" onClick={() => router.back()}>
                                    취소
                                </Button>
                                <Button
                                    type="submit"
                                    className="bg-latte-800 hover:bg-latte-900 text-white min-w-[120px]"
                                    disabled={submitting}
                                >
                                    {submitting ? '저장 중...' : (
                                        <>
                                            <Save className="w-4 h-4 mr-2" /> 저장하기
                                        </>
                                    )}
                                </Button>
                            </div>
                        </form>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
