'use client'

import { useState, useEffect } from 'react'
import { Blend, BlendAPI } from '@/lib/api'
import Card from '@/components/ui/Card'
import Link from 'next/link'
import PageHero from '@/components/ui/PageHero'

export default function BlendsPage() {
    const [blends, setBlends] = useState<Blend[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchBlends = async () => {
            try {
                const data = await BlendAPI.getAll({})
                setBlends(data)
            } catch (err) {
                console.error('Failed to fetch blends:', err)
                setError('블렌드 목록을 불러오는데 실패했습니다.')
            } finally {
                setLoading(false)
            }
        }
        fetchBlends()
    }, [])

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <PageHero
                title="블렌드 레시피"
                description="나만의 커피 블렌드 레시피를 만들고 관리하세요"
                icon="🎨"
                backgroundImage="/blends_background.png"
            />

            <div className="container mx-auto px-4 py-8">
                <div className="flex justify-end mb-6">
                    <Link
                        href="/blends/new"
                        className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors duration-200 flex items-center gap-2"
                    >
                        <span>+ 새 블렌드 등록</span>
                    </Link>
                </div>

                {error && (
                    <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-6">
                        {error}
                    </div>
                )}

                {loading ? (
                    <div className="text-center py-12 text-gray-500">
                        데이터를 불러오는 중입니다...
                    </div>
                ) : blends.length === 0 ? (
                    <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                        <p className="text-gray-500 dark:text-gray-400 mb-4">
                            등록된 블렌드 레시피가 없습니다.
                        </p>
                        <Link
                            href="/blends/new"
                            className="text-indigo-600 hover:text-indigo-800 font-medium"
                        >
                            첫 번째 블렌드를 만들어보세요!
                        </Link>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {blends.map((blend) => (
                            <Card
                                key={blend.id}
                                title={blend.name}
                                description={blend.description || '설명 없음'}
                                tags={[blend.target_roast_level || 'Roast Level 미지정']}
                                href={`/blends/${blend.id}`}
                                actionText="레시피 보기"
                            />
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}
