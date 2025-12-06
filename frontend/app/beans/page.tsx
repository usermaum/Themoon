'use client'

import { useState, useEffect } from 'react'
import { Bean, BeanAPI } from '@/lib/api'
import Link from 'next/link'
import PageHero from '@/components/ui/PageHero'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Badge } from '@/components/ui/Badge'
import { Search, Plus, Trash2, Coffee } from 'lucide-react'

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
            const data = await BeanAPI.getAll({
                page,
                size: 10,
                search: search || undefined,
            })
            setBeans(data.items)
            setTotalPages(data.pages)
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
                title="원두 관리"
                description="다양한 원산지의 원두를 관리하고 품질을 추적하세요"
                icon={<Coffee />}
                className="mb-8"
            />

            <div className="container mx-auto px-4 py-8">
                <div className="flex flex-col md:flex-row justify-between items-center mb-8 gap-4">
                    <div className="w-full md:w-96 relative">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-latte-400" />
                        <Input
                            type="text"
                            placeholder="원두명, 원산지, 품종 검색..."
                            className="pl-12 bg-white border-latte-200 focus:border-latte-400"
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>

                    <Button asChild className="shadow-lg hover:shadow-xl bg-latte-800 hover:bg-latte-900 gap-2">
                        <Link href="/beans/new">
                            <Plus className="w-4 h-4" /> 새 원두 등록
                        </Link>
                    </Button>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-200 mb-6 flex items-center gap-2">
                        <span>⚠️</span> {error}
                    </div>
                )}

                {/* Bean List Table */}
                <div className="bg-white rounded-[2rem] shadow-sm overflow-hidden border border-latte-200">
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-latte-100">
                            <thead className="bg-latte-50/50">
                                <tr>
                                    <th className="px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">
                                        원두명
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">
                                        원산지/품종
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">
                                        로스팅 포인트
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">
                                        재고 (kg)
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">
                                        구매가 (kg)
                                    </th>
                                    <th className="px-6 py-4 text-right text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">
                                        관리
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-latte-100">
                                {loading ? (
                                    <tr>
                                        <td colSpan={6} className="px-6 py-12 text-center text-latte-400 animate-pulse">
                                            데이터를 불러오는 중입니다...
                                        </td>
                                    </tr>
                                ) : !beans || beans.length === 0 ? (
                                    <tr>
                                        <td colSpan={6} className="px-6 py-12 text-center text-latte-500">
                                            등록된 원두가 없습니다.
                                        </td>
                                    </tr>
                                ) : (
                                    beans.map((bean) => (
                                        <tr key={bean.id} className="hover:bg-latte-50/30 transition-colors group">
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <Link href={`/beans/${bean.id}`} className="text-base font-bold text-latte-900 override:text-latte-900 group-hover:text-latte-700 transition-colors">
                                                    {bean.name}
                                                </Link>
                                                <div className="text-xs text-latte-400 mt-1">
                                                    {bean.created_at && new Date(bean.created_at).toLocaleDateString()}
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <div className="text-sm font-medium text-latte-800">
                                                    {bean.origin}
                                                </div>
                                                <div className="text-sm text-latte-500">{bean.variety}</div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <Badge variant="outline" className="border-latte-300 text-latte-700 bg-latte-50">
                                                    {bean.roast_level}
                                                </Badge>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <div className={`text-sm font-bold ${bean.quantity_kg < 5 ? 'text-red-600' : 'text-latte-800'}`}>
                                                    {bean.quantity_kg.toFixed(2)} kg
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-latte-500 font-mono">
                                                ₩{bean.purchase_price_per_kg?.toLocaleString() || '0'}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    onClick={() => handleDelete(bean.id)}
                                                    className="text-latte-400 hover:text-red-600 hover:bg-red-50"
                                                >
                                                    <Trash2 className="w-4 h-4" />
                                                </Button>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Pagination */}
                <div className="mt-8 flex justify-center gap-2">
                    <Button
                        variant="outline"
                        onClick={() => setPage((p) => Math.max(1, p - 1))}
                        disabled={page === 1}
                        className="bg-white border-latte-200 text-latte-700 hover:bg-latte-50"
                    >
                        이전
                    </Button>
                    <span className="px-4 py-2 text-latte-600 font-medium flex items-center">
                        {page} / {totalPages || 1}
                    </span>
                    <Button
                        variant="outline"
                        onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                        disabled={page >= totalPages}
                        className="bg-white border-latte-200 text-latte-700 hover:bg-latte-50"
                    >
                        다음
                    </Button>
                </div>
            </div>
        </div>
    )
}
