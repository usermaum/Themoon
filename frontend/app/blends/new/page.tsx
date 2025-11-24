'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { BlendAPI, BlendCreateData } from '@/lib/api'
import BlendForm from '@/components/blends/BlendForm'

export default function NewBlendPage() {
    const router = useRouter()
    const [submitting, setSubmitting] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const handleSubmit = async (data: BlendCreateData) => {
        setSubmitting(true)
        setError(null)

        try {
            await BlendAPI.create(data)
            router.push('/blends')
        } catch (err) {
            console.error('Failed to create blend:', err)
            setError('블렌드 레시피 등록에 실패했습니다.')
            setSubmitting(false)
        }
    }

    return (
        <>
            {error && (
                <div className="container mx-auto px-4 mt-8 max-w-3xl">
                    <div className="bg-red-50 text-red-600 p-4 rounded-lg border border-red-200">
                        {error}
                    </div>
                </div>
            )}
            <BlendForm
                onSubmit={handleSubmit}
                isSubmitting={submitting}
                title="새 블렌드 레시피 등록"
                submitLabel="블렌드 저장"
            />
        </>
    )
}
