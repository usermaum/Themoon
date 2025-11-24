'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { BeanAPI, BeanCreateData } from '@/lib/api'
import BeanForm from '@/components/beans/BeanForm'

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
        <>
            {error && (
                <div className="container mx-auto px-4 mt-8 max-w-2xl">
                    <div className="bg-red-50 text-red-600 p-4 rounded-lg">{error}</div>
                </div>
            )}
            <BeanForm
                onSubmit={handleSubmit}
                isSubmitting={loading}
                title="새 원두 등록"
                submitLabel="원두 등록"
            />
        </>
    )
}
