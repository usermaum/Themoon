'use client'

import { useState, useEffect } from 'react'
import { Bean, BeanAPI } from '@/lib/api'
import Link from 'next/link'
import PageHero from '@/components/ui/PageHero'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Badge } from '@/components/ui/Badge'
import { Card, CardContent, CardFooter, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card'
import { Search, Plus, Trash2, Coffee, Edit2, MapPin, Tag } from 'lucide-react'

// Helper to resolve bean images
const getBeanImage = (bean: Bean) => {
    const nameLower = bean.name.toLowerCase();
    const originLower = (bean.origin || '').toLowerCase();

    // Mapping logic based on available images
    if (nameLower.includes('ethiopia') || originLower.includes('ethiopia')) return '/images/beans/ethiopia.png';
    if (nameLower.includes('colombia') || originLower.includes('colombia')) return '/images/beans/colombia.png';
    if (nameLower.includes('brazil') || originLower.includes('brazil')) return '/images/beans/brazil.png';
    if (nameLower.includes('guatemala') || originLower.includes('guatemala')) return '/images/beans/guatemala.png';
    if (nameLower.includes('kenya') || originLower.includes('kenya')) return '/images/beans/kenya.png';
    if (nameLower.includes('geisha') || originLower.includes('geisha')) return '/images/beans/geisha.png';
    if (nameLower.includes('santos') || originLower.includes('santos')) return '/images/beans/santos.png';
    if (nameLower.includes('yirgacheffe') || originLower.includes('yirgacheffe')) return '/images/beans/yirgacheffe.png';
    if (nameLower.includes('sidamo') || originLower.includes('sidamo')) return '/images/beans/sidamo.png';
    if (nameLower.includes('sumatra') || originLower.includes('sumatra')) return '/images/beans/sumatra.png';
    if (nameLower.includes('decaf') || originLower.includes('decaf')) return '/images/beans/decaf-sm.png';

    // Default placeholder if no match
    return '/images/beans/placeholder.png';
}

export default function BeanManagementPage() {
    const [beans, setBeans] = useState<Bean[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [page, setPage] = useState(1)
    const [totalPages, setTotalPages] = useState(1)
    const [search, setSearch] = useState('')

    const fetchBeans = async () => {
        try {
            setLoading(true)
            // 백엔드가 현재 skip, limit을 지원하지만 search는 지원 여부 불확실
            // 페이지네이션 계산: page 1 -> skip 0, page 2 -> skip 12
            const limit = 12
            const skip = (page - 1) * limit

            const data = await BeanAPI.getAll({
                skip,
                limit,
                search: search || undefined,
            })

            // 백엔드 응답이 배열인 경우 (현재 상태)
            if (Array.isArray(data)) {
                setBeans(data)
                // 전체 개수를 알 수 없으므로, 데이터가 limit보다 적으면 마지막 페이지로 간주
                setTotalPages(data.length < limit ? page : page + 1)
            }
            // 백엔드 응답이 페이지네이션 객체인 경우 (향후 대응)
            else if ((data as any).items) {
                setBeans((data as any).items)
                setTotalPages((data as any).pages)
            }

            setError(null)
        } catch (err) {
            console.error('Failed to fetch beans:', err)
            setError('원두 목록을 불러오는데 실패했습니다.')
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchBeans()
    }, [page, search])

    const handleDelete = async (id: number) => {
        if (!confirm('정말로 이 원두를 삭제하시겠습니까?')) return

        try {
            await BeanAPI.delete(id)
            fetchBeans()
        } catch (err) {
            alert('삭제에 실패했습니다.')
        }
    }

    return (
        <div className="min-h-screen">
            <PageHero
                title="Bean Collection"
                description="The Moon Drip Bar의 엄선된 원두 컬렉션을 관리하세요."
                icon={<Coffee />}
                image="/images/hero/beans-hero.png"
                className="mb-8"
            />

            <div className="container mx-auto px-4 py-8">
                <div className="flex flex-col md:flex-row justify-between items-center mb-10 gap-4">
                    <div className="w-full md:w-96 relative">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-latte-400" />
                        <Input
                            type="text"
                            placeholder="원두명, 원산지, 품종 검색..."
                            className="pl-12 bg-white border-latte-200 focus:border-latte-400 h-12 rounded-xl shadow-sm"
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>

                    <Button asChild className="shadow-lg hover:shadow-xl bg-latte-800 hover:bg-latte-900 gap-2 h-12 px-6 rounded-xl text-lg font-serif">
                        <Link href="/beans/new">
                            <Plus className="w-5 h-5" /> 새 원두 등록
                        </Link>
                    </Button>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-200 mb-6 flex items-center gap-2">
                        <span>⚠️</span> {error}
                    </div>
                )}

                {/* Bean Collection Grid */}
                {loading ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                        {[1, 2, 3, 4].map((n) => (
                            <div key={n} className="h-96 bg-latte-50 rounded-[2rem] animate-pulse"></div>
                        ))}
                    </div>
                ) : !beans || beans.length === 0 ? (
                    <div className="text-center py-24 bg-white rounded-[2rem] shadow-sm border border-latte-200">
                        <div className="bg-latte-100 w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6">
                            <Coffee className="w-10 h-10 text-latte-400" />
                        </div>
                        <h3 className="text-2xl font-serif font-bold text-latte-800 mb-2">등록된 원두가 없습니다</h3>
                        <p className="text-latte-500 mb-8">새로운 원두를 등록하여 컬렉션을 시작해보세요.</p>
                        <Button asChild variant="outline" className="border-latte-400 text-latte-700 hover:bg-latte-50">
                            <Link href="/beans/new">
                                첫 번째 원두 등록하기
                            </Link>
                        </Button>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                        {beans.map((bean) => (
                            <Card key={bean.id} className="group overflow-hidden border-latte-200 hover:border-latte-400 hover:shadow-xl transition-all duration-300">
                                <div className="h-64 relative overflow-hidden bg-latte-100">
                                    <img
                                        src={getBeanImage(bean)}
                                        alt={bean.name}
                                        className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                                    />
                                    <div className="absolute top-4 left-4">
                                        <Badge variant="secondary" className="bg-white/90 backdrop-blur-sm shadow-sm font-serif border-0">
                                            {bean.roast_profile || bean.grade || 'Raw Bean'}
                                        </Badge>
                                    </div>
                                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center p-6">
                                        <div className="flex gap-2">
                                            <Button asChild size="icon" variant="secondary" className="bg-white/90 hover:bg-white text-latte-800 rounded-full h-10 w-10">
                                                <Link href={`/beans/${bean.id}`}>
                                                    <Edit2 className="w-4 h-4" />
                                                </Link>
                                            </Button>
                                            <Button
                                                size="icon"
                                                variant="destructive"
                                                className="rounded-full h-10 w-10"
                                                onClick={() => handleDelete(bean.id)}
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </Button>
                                        </div>
                                    </div>
                                </div>
                                <CardHeader className="pb-2">
                                    <div className="flex justify-between items-start mb-2">
                                        <Badge variant="outline" className="border-latte-300 text-latte-600 bg-latte-50/50">
                                            {bean.variety || 'Unknown'}
                                        </Badge>
                                        <span className={`font-mono font-bold text-sm ${bean.quantity_kg < 5 ? 'text-red-500' : 'text-latte-400'}`}>
                                            {bean.quantity_kg.toFixed(1)}kg
                                        </span>
                                    </div>
                                    <CardTitle className="leading-tight group-hover:text-latte-600 transition-colors">
                                        <Link href={`/beans/${bean.id}`} className="hover:underline decoration-latte-400 underline-offset-4">
                                            {bean.name}
                                        </Link>
                                    </CardTitle>
                                    <CardDescription className="flex items-center gap-1 mt-1 text-latte-500">
                                        <MapPin className="w-3 h-3" /> {bean.origin}
                                    </CardDescription>
                                </CardHeader>
                                <CardFooter className="pt-2 border-t border-latte-50 mt-auto bg-latte-50/30">
                                    <div className="w-full flex justify-between items-center text-sm">
                                        <span className="text-latte-400">단가 (kg)</span>
                                        <span className="font-mono font-bold text-latte-800">
                                            ₩{bean.purchase_price_per_kg?.toLocaleString() || '0'}
                                        </span>
                                    </div>
                                </CardFooter>
                            </Card>
                        ))}
                    </div>
                )}

                {/* Pagination */}
                <div className="mt-12 flex justify-center gap-3">
                    <Button
                        variant="outline"
                        onClick={() => setPage((p) => Math.max(1, p - 1))}
                        disabled={page === 1}
                        className="bg-white border-latte-200 text-latte-700 hover:bg-latte-50 px-6"
                    >
                        이전 페이지
                    </Button>
                    <span className="px-6 py-2 bg-white border border-latte-200 rounded-lg text-latte-800 font-bold flex items-center shadow-sm">
                        {page} / {totalPages || 1}
                    </span>
                    <Button
                        variant="outline"
                        onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                        disabled={page >= totalPages}
                        className="bg-white border-latte-200 text-latte-700 hover:bg-latte-50 px-6"
                    >
                        다음 페이지
                    </Button>
                </div>
            </div>
        </div>
    )
}
