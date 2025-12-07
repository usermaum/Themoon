'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { BeanAPI, BeanCreateData, Bean } from '@/lib/api'
import BeanForm from '@/components/beans/BeanForm'
import PageHero from '@/components/ui/PageHero'
import { Edit2 } from 'lucide-react'

export default function EditBeanPage({ params }: { params: { id: string } }) {
    const router = useRouter()
    const [bean, setBean] = useState<Bean | undefined>(undefined)
    const [loading, setLoading] = useState(true)
    const [submitting, setSubmitting] = useState(false)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchBean = async () => {
            try {
                const data = await BeanAPI.getOne(parseInt(params.id))
                setBean(data)
            } catch (err) {
                console.error('Failed to fetch bean:', err)
                setError('원두 정보를 불러오는데 실패했습니다.')
            } finally {
                setLoading(false)
            }
        }

        fetchBean()
    }, [params.id])

    const handleSubmit = async (data: BeanCreateData) => {
        setSubmitting(true)
        setError(null)

        try {
            await BeanAPI.update(parseInt(params.id), data)
            router.push('/beans')
        } catch (err) {
            console.error('Failed to update bean:', err)
            setError('원두 수정에 실패했습니다. 입력 값을 확인해주세요.')
            setSubmitting(false)
        }
    }

    if (loading) {
        return (
            <div className="container mx-auto px-4 py-12 text-center text-gray-500">
                데이터를 불러오는 중입니다...
            </div>
        )
    }

    if (!bean) {
        return (
            <div className="container mx-auto px-4 py-12 text-center text-red-500">
                원두 정보를 찾을 수 없습니다.
            </div>
        )
    }

    return (
        <div className="min-h-screen">
            <PageHero
                title="원두 정보 수정"
                description="등록된 원두의 상세 정보를 수정하고 관리합니다."
                icon={<Edit2 />}
                image="/images/hero/bean_edit_hero.png"
                className="mb-8 min-h-[280px]"
            />

            {error && (
                <div className="container mx-auto px-4 mt-8 max-w-2xl">
                    <div className="bg-red-50 text-red-600 p-4 rounded-lg">{error}</div>
                </div>
            )}
            <BeanForm
                initialData={bean}
                onSubmit={handleSubmit}
                isSubmitting={submitting}
                title="원두 정보 수정"
                submitLabel="수정 완료"
            />
        </div>
    )
}
