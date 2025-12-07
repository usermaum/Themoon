'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { BeanAPI, BeanCreateData } from '@/lib/api'
import BeanForm from '@/components/beans/BeanForm'
import PageHero from '@/components/ui/PageHero'
import { Coffee } from 'lucide-react'

export default function NewBeanPage() {
    const router = useRouter()
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const handleSubmit = async (data: BeanCreateData) => {
        setLoading(true)
        setError(null)

        try {
            await BeanAPI.create(data)
            router.push('/beans')
        } catch (err) {
            console.error('Failed to create bean:', err)
            setError('원두 등록에 실패했습니다. 입력 값을 확인해주세요.')
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen pb-12">
            <PageHero
                title="새 원두 등록"
                description="새로운 원두 정보를 입력하여 컬렉션에 추가하세요."
                icon={<Coffee />}
                image="/images/hero/beans-hero.png" // Using bean hero image
                className="mb-8"
            />

            {error && (
                <div className="container mx-auto px-4 mb-6 max-w-4xl">
                    <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-200 flex items-center gap-2">
                        <span>⚠️</span> {error}
                    </div>
                </div>
            )}

            <BeanForm
                onSubmit={handleSubmit}
                isSubmitting={loading}
                title="원두 정보 입력"
                submitLabel="원두 등록 완료"
            />
        </div>
    )
}
