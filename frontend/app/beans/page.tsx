'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Bean } from '@/lib/api'
import { useBeans, deleteBean } from '@/hooks'
import Link from 'next/link'
import PageHero from '@/components/ui/page-hero'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardFooter, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Search, Plus, Trash2, Coffee, Edit2, MapPin, Tag, RefreshCw } from 'lucide-react'

// Helper to resolve bean images
const getBeanImage = (bean: Bean) => {
    const nameLower = bean.name.toLowerCase();

    // 1. Blend Beans
    // Note: Blends are stored in /images/roasted/
    if (bean.type === 'BLEND_BEAN' || nameLower.includes('blend') || nameLower.includes('블렌드')) {
        if (nameLower.includes('full moon') || nameLower.includes('풀문')) return '/images/roasted/17_fullmoon_blend.png';
        if (nameLower.includes('new moon') || nameLower.includes('뉴문')) return '/images/roasted/18_newmoon_blend.png';
        if (nameLower.includes('eclipse') || nameLower.includes('이클립스')) return '/images/roasted/19_eclipse_blend.png';
        // Fallback for generic blend
        return '/images/roasted/17_fullmoon_blend.png';
    }

    // 2. Determine File Type (Green vs Roasted)
    // Check if it's a Roasted Bean based on type or roast_profile
    const isRoasted = bean.type === 'ROASTED_BEAN' || (bean.roast_profile && bean.roast_profile !== null);

    let folder = '/images/raw_material/';
    let suffix = '_raw.png';

    if (isRoasted) {
        folder = '/images/roasted/';
        // Map Roast Profile to suffix
        // LIGHT, MEDIUM -> _light.png
        // DARK -> _dark.png
        const profile = bean.roast_profile || 'LIGHT';
        suffix = profile === 'DARK' ? '_dark.png' : '_light.png';
    }

    // 3. Determine Bean Identity (Prefix)
    let idPrefix = '01_yirgacheffe'; // Default

    if (nameLower.includes('예가체프') || nameLower.includes('yirgacheffe')) idPrefix = '01_yirgacheffe';
    else if (nameLower.includes('모모라') || nameLower.includes('mormora')) idPrefix = '02_mormora';
    else if (nameLower.includes('코케') || nameLower.includes('koke')) idPrefix = '03_koke_honey';
    else if (nameLower.includes('우라가') || nameLower.includes('uraga')) idPrefix = '04_uraga';
    else if (nameLower.includes('시다모') || nameLower.includes('sidamo')) idPrefix = '05_sidamo';
    else if (nameLower.includes('마사이') || nameLower.includes('masai')) idPrefix = '06_masai';
    else if (nameLower.includes('키린야가') || nameLower.includes('키리냐가') || nameLower.includes('kirinyaga')) idPrefix = '07_kirinyaga';
    else if (nameLower.includes('후일라') || nameLower.includes('huila')) idPrefix = '08_huila';
    else if (nameLower.includes('안티구아') || nameLower.includes('antigua')) idPrefix = '09_antigua';
    else if (nameLower.includes('엘탄케') || nameLower.includes('eltanque')) idPrefix = '10_eltanque';
    else if (nameLower.includes('파젠다') || nameLower.includes('fazenda')) idPrefix = '11_fazenda';
    else if (nameLower.includes('산토스') || nameLower.includes('santos')) idPrefix = '12_santos';
    else if (nameLower.includes('디카페') || nameLower.includes('decaf')) {
        if (nameLower.includes('sdm')) idPrefix = '13_decaf_sdm';
        else if (nameLower.includes('sm')) idPrefix = '14_decaf_sm';
        else idPrefix = '15_swiss_water';
    }
    else if (nameLower.includes('스위스') || nameLower.includes('swiss')) idPrefix = '15_swiss_water';
    else if (nameLower.includes('게이샤') || nameLower.includes('geisha')) idPrefix = '16_geisha';

    return `${folder}${idPrefix}${suffix}`;
}


export default function BeanManagementPage() {
    const [page, setPage] = useState(1)
    const [search, setSearch] = useState('')

    const limit = 12
    const skip = (page - 1) * limit

    // SWR 훅 사용 - 자동 재시도, 포커스 시 재검증, 네트워크 복구 시 재갱신
    const { beans, pages: totalPages, isLoading, isValidating, error, refresh } = useBeans({
        skip,
        limit,
        search: search || undefined,
    })

    const handleDelete = async (id: number) => {
        if (!confirm('정말로 이 원두를 삭제하시겠습니까?')) return

        try {
            await deleteBean(id)
            // SWR이 자동으로 캐시를 무효화하고 새로고침
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
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.2 }}
                    className="flex flex-col md:flex-row justify-between items-center mb-10 gap-4"
                >
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
                </motion.div>

                {/* Error Message */}
                {error && (
                    <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-200 mb-6 flex items-center gap-2">
                        <span>⚠️</span> 원두 목록을 불러오는데 실패했습니다.
                        <Button variant="ghost" size="sm" onClick={refresh} className="ml-auto">
                            <RefreshCw className="w-4 h-4 mr-1" /> 다시 시도
                        </Button>
                    </div>
                )}

                {/* 백그라운드 재검증 중 표시 */}
                {isValidating && !isLoading && (
                    <div className="flex items-center gap-2 text-latte-500 mb-4">
                        <RefreshCw className="w-4 h-4 animate-spin" />
                        <span className="text-sm">데이터 동기화 중...</span>
                    </div>
                )}

                {/* Bean Collection Grid */}
                {isLoading ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                        {[1, 2, 3, 4].map((n) => (
                            <div key={n} className="h-96 bg-latte-50 rounded-[1em] animate-pulse"></div>
                        ))}
                    </div>
                ) : !beans || beans.length === 0 ? (
                    <div className="text-center py-24 bg-white rounded-[1em] shadow-sm border border-latte-200">
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
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.3 }}
                        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8"
                    >
                        {beans.map((bean, index) => (
                            <motion.div
                                key={bean.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.4, delay: index * 0.05 }}
                            >
                                <Card className="group overflow-hidden border-latte-200 hover:border-latte-400 hover:shadow-xl transition-all duration-300 h-full">
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
                            </motion.div>
                        ))}
                    </motion.div>
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
