'use client'

import { useState, useEffect } from 'react'
import { Blend, BlendAPI } from '@/lib/api'
import {
    Card,
    CardHeader,
    CardTitle,
    CardDescription,
    CardContent,
    CardFooter
} from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import Link from 'next/link'
import PageHero from '@/components/ui/PageHero'
import { Palette, Plus, ArrowRight } from 'lucide-react'

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
        <div className="min-h-screen">
            <PageHero
                title="블렌드 레시피"
                description="나만의 커피 블렌드 레시피를 만들고 관리하세요"
                icon={<Palette />}
                className="mb-8"
            />

            <div className="container mx-auto px-4 py-8">
                <div className="flex justify-end mb-8">
                    <Button asChild className="gap-2 shadow-lg hover:shadow-xl bg-latte-800 hover:bg-latte-900">
                        <Link href="/blends/new">
                            <Plus className="w-4 h-4" /> 새 블렌드 등록
                        </Link>
                    </Button>
                </div>

                {error && (
                    <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-200 mb-6 flex items-center gap-2">
                        <span>⚠️</span> {error}
                    </div>
                )}

                {loading ? (
                    <div className="text-center py-20">
                        <div className="text-latte-400 animate-pulse">데이터를 불러오는 중입니다...</div>
                    </div>
                ) : blends.length === 0 ? (
                    <div className="text-center py-20 bg-white rounded-[2rem] border border-latte-200 shadow-sm">
                        <Palette className="w-16 h-16 text-latte-200 mx-auto mb-4" />
                        <p className="text-latte-500 mb-6 text-lg">
                            등록된 블렌드 레시피가 없습니다.
                        </p>
                        <Button asChild variant="outline" className="border-latte-400 text-latte-700">
                            <Link href="/blends/new">
                                첫 번째 블렌드를 만들어보세요!
                            </Link>
                        </Button>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {blends.map((blend) => (
                            <Card key={blend.id} className="group border-latte-200 hover:border-latte-400 h-full flex flex-col">
                                <div className="h-48 bg-latte-100 relative overflow-hidden">
                                    {/* Placeholder Pattern */}
                                    <div className="absolute inset-0 opacity-10 flex items-center justify-center">
                                        <Palette className="w-24 h-24 text-latte-900" />
                                    </div>
                                    <div className="absolute top-4 left-4">
                                        <Badge variant="secondary" className="bg-white/80 backdrop-blur-sm border-0 font-serif">
                                            {blend.target_roast_level || 'Roast Level 미지정'}
                                        </Badge>
                                    </div>
                                </div>
                                <CardHeader>
                                    <CardTitle className="group-hover:text-latte-600 transition-colors">
                                        {blend.name}
                                    </CardTitle>
                                    <CardDescription className="line-clamp-2 mt-2">
                                        {blend.description || '설명 없음'}
                                    </CardDescription>
                                </CardHeader>
                                <CardFooter className="mt-auto pt-4 border-t border-latte-100">
                                    <Button asChild variant="ghost" className="w-full justify-between hover:bg-latte-50 text-latte-600 hover:text-latte-900 group/btn">
                                        <Link href={`/blends/${blend.id}`}>
                                            레시피 보기
                                            <ArrowRight className="w-4 h-4 group-hover/btn:translate-x-1 transition-transform" />
                                        </Link>
                                    </Button>
                                </CardFooter>
                            </Card>
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}
