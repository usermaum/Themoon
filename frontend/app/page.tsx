'use client'

import { useState, useEffect } from 'react'
import { Bean, BeanAPI, Blend, BlendAPI, InventoryLog, InventoryLogAPI } from '@/lib/api'
import Link from 'next/link'
import Card from '@/components/ui/Card'
import Hero from '@/components/home/Hero'

export default function HomePage() {
  const [beans, setBeans] = useState<Bean[]>([])
  const [blends, setBlends] = useState<Blend[]>([])
  const [recentLogs, setRecentLogs] = useState<InventoryLog[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const [beansData, blendsData, logsData] = await Promise.all([
          BeanAPI.getAll({ size: 100 }),
          BlendAPI.getAll({ limit: 100 }),
          InventoryLogAPI.getAll({ limit: 10 }),
        ])

        setBeans(beansData.items || [])
        setBlends(blendsData || [])
        setRecentLogs(logsData || [])
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const lowStockBeans = beans.filter((bean) => bean.quantity_kg < 5)
  const totalStock = beans.reduce((sum, bean) => sum + bean.quantity_kg, 0)

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Hero Section */}
      <Hero />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="text-center py-12 text-gray-500">
            데이터를 불러오는 중입니다...
          </div>
        ) : (
          <>
            {/* 통계 카드 섹션 */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-500 dark:text-gray-400 text-sm font-medium">전체 원두</p>
                    <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{beans.length}</p>
                  </div>
                  <div className="text-4xl">☕</div>
                </div>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-500 dark:text-gray-400 text-sm font-medium">블렌드 레시피</p>
                    <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{blends.length}</p>
                  </div>
                  <div className="text-4xl">🎨</div>
                </div>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-500 dark:text-gray-400 text-sm font-medium">총 재고량</p>
                    <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{totalStock.toFixed(1)} kg</p>
                  </div>
                  <div className="text-4xl">📦</div>
                </div>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-red-200 dark:border-red-700">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-red-600 dark:text-red-400 text-sm font-medium">재고 부족</p>
                    <p className="text-3xl font-bold text-red-600 dark:text-red-400 mt-1">{lowStockBeans.length}</p>
                  </div>
                  <div className="text-4xl">⚠️</div>
                </div>
              </div>
            </div>

            {/* 재고 부족 알림 */}
            {lowStockBeans.length > 0 && (
              <section className="mb-8">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                  재고 부족 알림
                </h2>
                <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                  <ul className="space-y-2">
                    {lowStockBeans.map((bean) => (
                      <li key={bean.id} className="flex justify-between items-center">
                        <span className="text-gray-900 dark:text-white font-medium">
                          {bean.name} ({bean.origin})
                        </span>
                        <span className="text-red-600 dark:text-red-400 font-semibold">
                          {bean.quantity_kg.toFixed(1)} kg
                        </span>
                      </li>
                    ))}
                  </ul>
                  <Link
                    href="/inventory"
                    className="mt-4 inline-block text-indigo-600 dark:text-indigo-400 hover:underline"
                  >
                    재고 관리로 이동 →
                  </Link>
                </div>
              </section>
            )}

            {/* 최근 활동 */}
            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                최근 입출고 내역
              </h2>
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden border border-gray-200 dark:border-gray-700">
                {recentLogs.length === 0 ? (
                  <p className="p-6 text-center text-gray-500">최근 활동이 없습니다.</p>
                ) : (
                  <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                    <thead className="bg-gray-50 dark:bg-gray-900">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                          날짜
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                          유형
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                          수량
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                          사유
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                      {recentLogs.map((log) => (
                        <tr key={log.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                            {new Date(log.created_at).toLocaleString('ko-KR')}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`px-2 py-1 text-xs font-semibold rounded-full ${log.transaction_type === 'IN'
                              ? 'bg-green-100 text-green-800'
                              : 'bg-red-100 text-red-800'
                              }`}>
                              {log.transaction_type === 'IN' ? '입고' : '출고'}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                            {log.quantity_change > 0 ? '+' : ''}{log.quantity_change.toFixed(1)} kg
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                            {log.reason || '-'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </section>

            {/* 빠른 링크 */}
            <section>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                빠른 작업
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card
                  title="원두 관리"
                  description="새로운 원두를 등록하거나 기존 원두 정보를 관리합니다."
                  tags={['CRUD', 'Beans']}
                  href="/beans"
                  actionText="관리하기"
                />
                <Card
                  title="블렌드 레시피"
                  description="나만의 커피 블렌드 레시피를 만들고 관리합니다."
                  tags={['Recipe', 'Blends']}
                  href="/blends"
                  actionText="관리하기"
                />
                <Card
                  title="재고 관리"
                  description="원두의 입고/출고를 처리하고 재고 현황을 확인합니다."
                  tags={['Inventory', 'Stock']}
                  href="/inventory"
                  actionText="관리하기"
                />
              </div>
            </section>
          </>
        )}
      </div>
    </div>
  )
}
