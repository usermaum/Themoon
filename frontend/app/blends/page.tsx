'use client'

import { useState, useEffect } from 'react'
import { Blend, BlendAPI, Bean, BeanAPI } from '@/lib/api'
import Link from 'next/link'
import PageHero from '@/components/ui/PageHero'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Badge } from '@/components/ui/Badge'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/Card'
import { Search, Plus, Trash2, Edit2, Hexagon, PieChart } from 'lucide-react'

// 블렌드 리스트 메인 페이지
export default function BlendManagementPage() {
    const [blends, setBlends] = useState<Blend[]>([])
    const [beans, setBeans] = useState<Bean[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [page, setPage] = useState(1)
    const [totalPages, setTotalPages] = useState(1)
    const [search, setSearch] = useState('')

    // 원두 정보 캐싱 (ID로 이름 찾기 위함)
    const fetchBeans = async () => {
        try {
            // 모든 원두를 가져옵니다 (최적화 필요 시 변경)
            const data = await BeanAPI.getAll({ limit: 100 })
            if (Array.isArray(data)) {
                setBeans(data)
            } else if ((data as any).items) {
                setBeans((data as any).items)
            }
        } catch (err) {
            console.error('Failed to fetch beans:', err)
        }
    }

    const fetchBlends = async () => {
        try {
            setLoading(true)
            const limit = 12
            const skip = (page - 1) * limit

            const data = await BlendAPI.getAll({
                skip,
                limit,
                search: search || undefined,
            })

            if (Array.isArray(data)) {
                setBlends(data)
                setTotalPages(data.length < limit ? page : page + 1)
            } else if ((data as any).items) {
                setBlends((data as any).items)
                setTotalPages((data as any).pages)
            }
            setError(null)
        } catch (err) {
            console.error('Failed to fetch blends:', err)
            setError('블렌드 목록을 불러오는데 실패했습니다.')
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchBeans()
        fetchBlends()
    }, [page, search])

    const handleDelete = async (id: number) => {
        if (!confirm('정말로 이 블렌드 레시피를 삭제하시겠습니까?')) return

        try {
            await BlendAPI.delete(id)
            fetchBlends()
        } catch (err) {
            alert('삭제에 실패했습니다.')
        }
    }

    const getBeanName = (id: number) => {
        const bean = beans.find(b => b.id === id)
        return bean ? bean.name : `Unknown Bean (${id})`
    }

    return (
        <div className="min-h-screen">
            <PageHero
                title="Blend Recipes"
                description="나만의 커피 경험을 위한 블렌딩 레시피를 관리하세요."
                icon={<Hexagon />}
                image="/images/hero/beans-hero.png" // 블렌드용 이미지 있으면 교체 추천
                className="mb-8"
            />

            <div className="container mx-auto px-4 py-8">
                <div className="flex flex-col md:flex-row justify-between items-center mb-10 gap-4">
                    <div className="w-full md:w-96 relative">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-latte-400" />
                        <Input
                            type="text"
                            placeholder="블렌드 이름 검색..."
                            className="pl-12 bg-white border-latte-200 focus:border-latte-400 h-12 rounded-xl shadow-sm"
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>

                    <Button asChild className="shadow-lg hover:shadow-xl bg-latte-800 hover:bg-latte-900 gap-2 h-12 px-6 rounded-xl text-lg font-serif">
                        <Link href="/blends/new">
                            <Plus className="w-5 h-5" /> 새 블렌드 생성
                        </Link>
                    </Button>
                </div>

                {error && (
                    <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-200 mb-6 flex items-center gap-2">
                        <span>⚠️</span> {error}
                    </div>
                )}

                {loading ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {[1, 2, 3].map((n) => (
                            <div key={n} className="h-64 bg-latte-50 rounded-[2rem] animate-pulse"></div>
                        ))}
                    </div>
                ) : !blends || blends.length === 0 ? (
                    <div className="text-center py-24 bg-white rounded-[2rem] shadow-sm border border-latte-200">
                        <div className="bg-latte-100 w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6">
                            <Hexagon className="w-10 h-10 text-latte-400" />
                        </div>
                        <h3 className="text-2xl font-serif font-bold text-latte-800 mb-2">등록된 블렌드가 없습니다</h3>
                        <p className="text-latte-500 mb-8">새로운 블렌드 레시피를 만들어보세요.</p>
                        <Button asChild variant="outline" className="border-latte-400 text-latte-700 hover:bg-latte-50">
                            <Link href="/blends/new">
                                첫 블렌드 만들기
                            </Link>
                        </Button>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {blends.map((blend) => (
                            <Card key={blend.id} className="group overflow-hidden border-latte-200 hover:border-latte-400 hover:shadow-xl transition-all duration-300 flex flex-col">
                                <CardHeader className="bg-latte-50/50 pb-4">
                                    <div className="flex justify-between items-start mb-2">
                                        <Badge variant="outline" className="bg-white border-latte-300 text-latte-600">
                                            {blend.target_roast_level || 'Custom Roast'}
                                        </Badge>
                                        <div className="flex gap-1">
                                            <Button asChild size="icon" variant="ghost" className="h-8 w-8 hover:bg-white text-latte-500">
                                                <Link href={`/blends/${blend.id}`}>
                                                    <Edit2 className="w-4 h-4" />
                                                </Link>
                                            </Button>
                                            <Button
                                                size="icon"
                                                variant="ghost"
                                                className="h-8 w-8 hover:bg-red-50 text-latte-500 hover:text-red-500"
                                                onClick={() => handleDelete(blend.id)}
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </Button>
                                        </div>
                                    </div>
                                    <CardTitle className="text-xl font-serif text-latte-900">
                                        {blend.name}
                                    </CardTitle>
                                    <CardDescription className="line-clamp-2 mt-1">
                                        {blend.description}
                                    </CardDescription>
                                </CardHeader>
                                <CardContent className="pt-6 flex-grow">
                                    <div className="space-y-3">
                                        <div className="flex items-center gap-2 text-sm font-semibold text-latte-700 mb-2">
                                            <PieChart className="w-4 h-4" />
                                            <span>블렌딩 비율</span>
                                        </div>
                                        {blend.recipe.map((item, idx) => (
                                            <div key={idx} className="flex justify-between items-center text-sm">
                                                <span className="text-latte-600 truncate flex-1 pr-2">
                                                    {getBeanName(item.bean_id)}
                                                </span>
                                                <div className="flex items-center gap-2 min-w-[3rem] justify-end">
                                                    <div className="h-2 rounded-full bg-latte-200 w-16 overflow-hidden">
                                                        <div
                                                            className="h-full bg-latte-600"
                                                            style={{ width: `${item.ratio * 100}%` }}
                                                        />
                                                    </div>
                                                    <span className="font-mono font-bold text-latte-800">
                                                        {Math.round(item.ratio * 100)}%
                                                    </span>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </CardContent>
                                <CardFooter className="bg-latte-50/30 border-t border-latte-100 pt-4 text-xs text-latte-400 flex justify-between">
                                    <span>Created: {new Date(blend.created_at).toLocaleDateString()}</span>
                                    <span>{blend.recipe.length} Origins</span>
                                </CardFooter>
                            </Card>
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}
