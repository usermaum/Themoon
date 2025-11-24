'use client'

import { useState, useEffect } from 'react'
import { Bean, BeanAPI } from '@/lib/api'
import Link from 'next/link'
import PageHero from '@/components/ui/PageHero'

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
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <PageHero
                title="원두 관리"
                description="다양한 원산지의 원두를 관리하고 품질을 추적하세요"
                icon="☕"
                backgroundImage="https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&w=1920&q=80"
            />

            <div className="container mx-auto px-4 py-8">
                <div className="flex justify-between items-center mb-6">
                    <div>
                        <Link
                            href="/beans/new"
                            className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors duration-200 flex items-center gap-2"
                        >
                            <span>+ 새 원두 등록</span>
                        </Link>
                    </div>
                </div>

                {/* Search & Filter */}
                <div className="mb-6 bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
                    <input
                        type="text"
                        placeholder="원두명, 원산지, 품종 검색..."
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-transparent"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                </div>

                {/* Error Message */}
                {error && (
                    <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-6">
                        {error}
                    </div>
                )}

                {/* Bean List Table */}
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden border border-gray-200 dark:border-gray-700">
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                            <thead className="bg-gray-50 dark:bg-gray-900">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                        원두명
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                        원산지/품종
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                        로스팅 포인트
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                        재고 (kg)
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                        구매가 (kg)
                                    </th>
                                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                        관리
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                                {loading ? (
                                    <tr>
                                        <td colSpan={6} className="px-6 py-12 text-center text-gray-500">
                                            데이터를 불러오는 중입니다...
                                        </td>
                                    </tr>
                                ) : !beans || beans.length === 0 ? (
                                    <tr>
                                        <td colSpan={6} className="px-6 py-12 text-center text-gray-500">
                                            등록된 원두가 없습니다.
                                        </td>
                                    </tr>
                                ) : (
                                    beans.map((bean) => (
                                        <tr key={bean.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <Link href={`/beans/${bean.id}`} className="text-sm font-medium text-indigo-600 hover:text-indigo-900 dark:text-indigo-400">
                                                    {bean.name}
                                                </Link>
                                                <div className="text-xs text-gray-500">
                                                    {bean.created_at && new Date(bean.created_at).toLocaleDateString()}
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <div className="text-sm text-gray-900 dark:text-white">
                                                    {bean.origin}
                                                </div>
                                                <div className="text-sm text-gray-500">{bean.variety}</div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-200">
                                                    {bean.roast_level}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <div className={`text-sm font-medium ${bean.quantity_kg < 5 ? 'text-red-600' : 'text-gray-900 dark:text-white'}`}>
                                                    {bean.quantity_kg.toFixed(2)} kg
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                ₩{bean.purchase_price_per_kg?.toLocaleString() || '0'}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                                <button
                                                    onClick={() => handleDelete(bean.id)}
                                                    className="text-red-600 hover:text-red-900"
                                                >
                                                    삭제
                                                </button>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Pagination */}
                <div className="mt-6 flex justify-center gap-2">
                    <button
                        onClick={() => setPage((p) => Math.max(1, p - 1))}
                        disabled={page === 1}
                        className="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:border-gray-600 dark:hover:bg-gray-700"
                    >
                        이전
                    </button>
                    <span className="px-4 py-2 text-gray-600 dark:text-gray-300">
                        {page} / {totalPages || 1}
                    </span>
                    <button
                        onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                        disabled={page >= totalPages}
                        className="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:border-gray-600 dark:hover:bg-gray-700"
                    >
                        다음
                    </button>
                </div>
            </div>
        </div>
    )
}
