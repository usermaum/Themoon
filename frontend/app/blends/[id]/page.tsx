'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { BlendAPI, BlendCreateData, Blend } from '@/lib/api'
import BlendForm from '@/components/blends/BlendForm'

export default function EditBlendPage({ params }: { params: { id: string } }) {
    const router = useRouter()
    const [blend, setBlend] = useState<Blend | undefined>(undefined)
    const [loading, setLoading] = useState(true)
    const [submitting, setSubmitting] = useState(false)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchBlend = async () => {
            try {
                const data = await BlendAPI.getOne(parseInt(params.id))
                setBlend(data)
            } catch (err) {
                console.error('Failed to fetch blend:', err)
                setError('블렌드 정보를 불러오는데 실패했습니다.')
            } finally {
                setLoading(false)
            }
        }
        fetchBlend()
    }, [params.id])

    const handleSubmit = async (data: BlendCreateData) => {
        setSubmitting(true)
        setError(null)

        try {
            await BlendAPI.update(parseInt(params.id), data)
            router.push('/blends')
        } catch (err) {
            console.error('Failed to update blend:', err)
            setError('블렌드 수정에 실패했습니다.')
            setSubmitting(false)
        }
    }

    const handleDelete = async () => {
        if (!confirm('정말로 이 블렌드 레시피를 삭제하시겠습니까?')) return

        try {
            await BlendAPI.delete(parseInt(params.id))
            router.push('/blends')
        } catch (err) {
            console.error('Failed to delete blend:', err)
            alert('삭제에 실패했습니다.')
        }
    }

    if (loading) {
        return (
            <div className="container mx-auto px-4 py-12 text-center text-gray-500">
                데이터를 불러오는 중입니다...
            </div>
        )
    }

    if (!blend) {
        return (
            <div className="container mx-auto px-4 py-12 text-center text-red-500">
                블렌드 정보를 찾을 수 없습니다.
            </div>
        )
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
                initialData={blend}
                onSubmit={handleSubmit}
                onDelete={handleDelete}
                isSubmitting={submitting}
                title="블렌드 레시피 수정"
                submitLabel="수정 완료"
            />
        </>
    )
}
