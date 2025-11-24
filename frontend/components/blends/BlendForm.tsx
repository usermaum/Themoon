'use client'

import { useState, useEffect } from 'react'
import { Bean, BeanAPI, BlendCreateData, Blend } from '@/lib/api'
import Link from 'next/link'

interface BlendFormProps {
    initialData?: Blend
    onSubmit: (data: BlendCreateData) => Promise<void>
    onDelete?: () => Promise<void>
    isSubmitting: boolean
    title: string
    submitLabel: string
}

export default function BlendForm({
    initialData,
    onSubmit,
    onDelete,
    isSubmitting,
    title,
    submitLabel,
}: BlendFormProps) {
    const [beans, setBeans] = useState<Bean[]>([])
    const [loadingBeans, setLoadingBeans] = useState(true)

    // Form State
    const [name, setName] = useState('')
    const [description, setDescription] = useState('')
    const [targetRoastLevel, setTargetRoastLevel] = useState('Medium')
    const [notes, setNotes] = useState('')

    // Recipe State: [{ beanId: string, ratio: string }]
    const [recipe, setRecipe] = useState<{ beanId: string; ratio: string }[]>([
        { beanId: '', ratio: '' },
    ])

    useEffect(() => {
        const fetchBeans = async () => {
            try {
                const data = await BeanAPI.getAll({ size: 100 })
                setBeans(data.items)
            } catch (err) {
                console.error('Failed to fetch beans:', err)
            } finally {
                setLoadingBeans(false)
            }
        }
        fetchBeans()
    }, [])

    useEffect(() => {
        if (initialData) {
            setName(initialData.name)
            setDescription(initialData.description || '')
            setTargetRoastLevel(initialData.target_roast_level || 'Medium')
            setNotes(initialData.notes || '')

            if (initialData.recipe && initialData.recipe.length > 0) {
                setRecipe(
                    initialData.recipe.map((item) => ({
                        beanId: item.bean_id.toString(),
                        ratio: (item.ratio * 100).toString(), // 0.5 -> 50
                    }))
                )
            }
        }
    }, [initialData])

    const handleRecipeChange = (index: number, field: 'beanId' | 'ratio', value: string) => {
        const newRecipe = [...recipe]
        newRecipe[index] = { ...newRecipe[index], [field]: value }
        setRecipe(newRecipe)
    }

    const addBeanRow = () => {
        setRecipe([...recipe, { beanId: '', ratio: '' }])
    }

    const removeBeanRow = (index: number) => {
        if (recipe.length === 1) return
        const newRecipe = recipe.filter((_, i) => i !== index)
        setRecipe(newRecipe)
    }

    const calculateTotalRatio = () => {
        return recipe.reduce((sum, item) => sum + (parseFloat(item.ratio) || 0), 0)
    }

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()

        // Validation
        const totalRatio = calculateTotalRatio()
        if (Math.abs(totalRatio - 100) > 0.1) {
            alert(`비율의 합은 100%가 되어야 합니다. (현재: ${totalRatio}%)`)
            return
        }

        const validRecipe = recipe.map((item) => ({
            bean_id: parseInt(item.beanId),
            ratio: parseFloat(item.ratio) / 100,
        }))

        if (validRecipe.some((item) => isNaN(item.bean_id) || isNaN(item.ratio))) {
            alert('모든 원두와 비율을 올바르게 입력해주세요.')
            return
        }

        onSubmit({
            name,
            description,
            target_roast_level: targetRoastLevel,
            notes,
            recipe: validRecipe,
        })
    }

    if (loadingBeans) {
        return <div className="p-8 text-center">원두 목록을 불러오는 중...</div>
    }

    return (
        <div className="container mx-auto px-4 py-8 max-w-3xl">
            <div className="mb-8 flex justify-between items-start">
                <div>
                    <Link
                        href="/blends"
                        className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 mb-4 inline-block"
                    >
                        ← 목록으로 돌아가기
                    </Link>
                    <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                        {title}
                    </h1>
                </div>
                {onDelete && (
                    <button
                        type="button"
                        onClick={onDelete}
                        className="bg-red-100 text-red-600 px-4 py-2 rounded-lg hover:bg-red-200 transition-colors"
                    >
                        삭제하기
                    </button>
                )}
            </div>

            <form onSubmit={handleSubmit} className="space-y-8 bg-white dark:bg-gray-800 p-6 rounded-lg shadow border border-gray-200 dark:border-gray-700">
                {/* 기본 정보 섹션 */}
                <section className="space-y-4">
                    <h2 className="text-xl font-semibold text-gray-900 dark:text-white border-b pb-2">기본 정보</h2>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            블렌드 이름 *
                        </label>
                        <input
                            type="text"
                            required
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder="예: Summer Breeze Blend"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            설명
                        </label>
                        <input
                            type="text"
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            placeholder="블렌드의 특징을 간단히 설명해주세요"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            목표 로스팅 포인트
                        </label>
                        <select
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                            value={targetRoastLevel}
                            onChange={(e) => setTargetRoastLevel(e.target.value)}
                        >
                            <option value="Light">Light</option>
                            <option value="Medium-Light">Medium-Light</option>
                            <option value="Medium">Medium</option>
                            <option value="Medium-Dark">Medium-Dark</option>
                            <option value="Dark">Dark</option>
                        </select>
                    </div>
                </section>

                {/* 레시피 구성 섹션 */}
                <section className="space-y-4">
                    <div className="flex justify-between items-center border-b pb-2">
                        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">레시피 구성</h2>
                        <span className={`font-bold ${Math.abs(calculateTotalRatio() - 100) < 0.1 ? 'text-green-600' : 'text-red-500'}`}>
                            총 비율: {calculateTotalRatio()}%
                        </span>
                    </div>

                    <div className="space-y-3">
                        {recipe.map((item, index) => (
                            <div key={index} className="flex gap-4 items-start">
                                <div className="flex-grow">
                                    <select
                                        required
                                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                                        value={item.beanId}
                                        onChange={(e) => handleRecipeChange(index, 'beanId', e.target.value)}
                                    >
                                        <option value="">원두 선택</option>
                                        {beans.map((bean) => (
                                            <option key={bean.id} value={bean.id}>
                                                {bean.name} ({bean.origin})
                                            </option>
                                        ))}
                                    </select>
                                </div>
                                <div className="w-32 relative">
                                    <input
                                        type="number"
                                        required
                                        min="0"
                                        max="100"
                                        step="0.1"
                                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent pr-8"
                                        value={item.ratio}
                                        onChange={(e) => handleRecipeChange(index, 'ratio', e.target.value)}
                                        placeholder="비율"
                                    />
                                    <span className="absolute right-3 top-2 text-gray-500">%</span>
                                </div>
                                <button
                                    type="button"
                                    onClick={() => removeBeanRow(index)}
                                    className="px-3 py-2 text-red-500 hover:bg-red-50 rounded-lg border border-red-200"
                                    disabled={recipe.length === 1}
                                >
                                    삭제
                                </button>
                            </div>
                        ))}
                    </div>

                    <button
                        type="button"
                        onClick={addBeanRow}
                        className="w-full py-2 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-indigo-500 hover:text-indigo-500 transition-colors"
                    >
                        + 원두 추가하기
                    </button>
                </section>

                {/* 메모 섹션 */}
                <section className="space-y-4">
                    <h2 className="text-xl font-semibold text-gray-900 dark:text-white border-b pb-2">메모</h2>
                    <textarea
                        rows={3}
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                        value={notes}
                        onChange={(e) => setNotes(e.target.value)}
                        placeholder="추가적인 메모사항을 입력하세요"
                    />
                </section>

                <div className="flex justify-end gap-4 pt-4">
                    <Link
                        href="/blends"
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
