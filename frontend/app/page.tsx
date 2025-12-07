'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Bean, BeanAPI, Blend, BlendAPI, InventoryLog, InventoryLogAPI } from '@/lib/api'
import Link from 'next/link'
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import Hero from '@/components/home/Hero'
import { ErrorState, LoadingSkeleton } from '@/components/ui/error-state'
import { Coffee, Palette, Package, AlertTriangle, ArrowRight } from 'lucide-react'

export default function HomePage() {
  const [beans, setBeans] = useState<Bean[]>([])
  const [blends, setBlends] = useState<Blend[]>([])
  const [recentLogs, setRecentLogs] = useState<InventoryLog[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<any>(null)

  const fetchData = async () => {
    try {
      setLoading(true)
      setError(null)
      const [beansData, blendsData, logsData] = await Promise.all([
        BeanAPI.getAll({ limit: 100 }),
        BlendAPI.getAll({ limit: 100 }),
        InventoryLogAPI.getAll({ limit: 10 }),
      ])

      setBeans(beansData.items || [])
      setBlends(blendsData || [])
      setRecentLogs(logsData || [])
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err)
      setError(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  const lowStockBeans = beans.filter((bean) => bean.quantity_kg < 5)
  const totalStock = beans.reduce((sum, bean) => sum + bean.quantity_kg, 0)

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <Hero />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <LoadingSkeleton count={4} />
        ) : error ? (
          <ErrorState error={error} onRetry={fetchData} />
        ) : (
          <>
            {/* 통계 카드 섹션 */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.1 }}
              className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8"
            >
              <Card className="hover:border-latte-400">
                <CardContent className="p-6 flex items-center justify-between">
                  <div>
                    <p className="text-latte-500 text-sm font-medium">전체 원두</p>
                    <p className="text-3xl font-bold text-latte-900 mt-1">{beans.length}</p>
                  </div>
                  <Coffee className="w-10 h-10 text-latte-300" />
                </CardContent>
              </Card>

              <Card className="hover:border-latte-400">
                <CardContent className="p-6 flex items-center justify-between">
                  <div>
                    <p className="text-latte-500 text-sm font-medium">블렌드 레시피</p>
                    <p className="text-3xl font-bold text-latte-900 mt-1">{blends.length}</p>
                  </div>
                  <Palette className="w-10 h-10 text-latte-300" />
                </CardContent>
              </Card>

              <Card className="hover:border-latte-400">
                <CardContent className="p-6 flex items-center justify-between">
                  <div>
                    <p className="text-latte-500 text-sm font-medium">총 재고량</p>
                    <p className="text-3xl font-bold text-latte-900 mt-1">{totalStock.toFixed(1)} <span className="text-lg text-latte-400">kg</span></p>
                  </div>
                  <Package className="w-10 h-10 text-latte-300" />
                </CardContent>
              </Card>

              <Card className={`hover:border-red-300 ${lowStockBeans.length > 0 ? 'border-red-200 bg-red-50/50' : ''}`}>
                <CardContent className="p-6 flex items-center justify-between">
                  <div>
                    <p className="text-red-600/80 text-sm font-medium">재고 부족</p>
                    <p className="text-3xl font-bold text-red-600 mt-1">{lowStockBeans.length}</p>
                  </div>
                  <AlertTriangle className="w-10 h-10 text-red-300" />
                </CardContent>
              </Card>
            </motion.div>

            {/* 재고 부족 알림 */}
            {lowStockBeans.length > 0 && (
              <motion.section
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.2 }}
                className="mb-8"
              >
                <h2 className="text-2xl font-serif font-bold text-latte-900 mb-4 flex items-center gap-2">
                  <AlertTriangle className="w-6 h-6 text-red-500" />
                  재고 부족 알림
                </h2>
                <div className="bg-white rounded-[2rem] border border-red-200 p-6 shadow-sm">
                  <ul className="space-y-3">
                    {lowStockBeans.map((bean) => (
                      <li key={bean.id} className="flex justify-between items-center bg-red-50/50 p-3 rounded-xl">
                        <span className="text-latte-800 font-medium flex items-center gap-2">
                          <span className="w-2 h-2 rounded-full bg-red-400"></span>
                          {bean.name} <span className="text-latte-500 text-sm">({bean.origin})</span>
                        </span>
                        <span className="text-red-600 font-bold bg-white px-3 py-1 rounded-full shadow-sm">
                          {bean.quantity_kg.toFixed(1)} kg
                        </span>
                      </li>
                    ))}
                  </ul>
                  <div className="mt-4 text-right">
                    <Button variant="link" asChild className="text-red-600 hover:text-red-700 p-0">
                      <Link href="/inventory" className="flex items-center gap-1">
                        재고 관리로 이동 <ArrowRight className="w-4 h-4" />
                      </Link>
                    </Button>
                  </div>
                </div>
              </motion.section>
            )}

            {/* 최근 활동 */}
            <motion.section
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.3 }}
              className="mb-8"
            >
              <h2 className="text-2xl font-serif font-bold text-latte-900 mb-4">
                최근 입출고 내역
              </h2>
              <div className="bg-white rounded-[2rem] shadow-sm overflow-hidden border border-latte-200">
                {recentLogs.length === 0 ? (
                  <p className="p-8 text-center text-latte-500">최근 활동이 없습니다.</p>
                ) : (
                  <table className="min-w-full divide-y divide-latte-100">
                    <thead className="bg-latte-50/50">
                      <tr>
                        <th className="px-6 py-4 text-left text-xs font-semibold text-latte-500 uppercase tracking-wider">
                          날짜
                        </th>
                        <th className="px-6 py-4 text-left text-xs font-semibold text-latte-500 uppercase tracking-wider">
                          유형
                        </th>
                        <th className="px-6 py-4 text-left text-xs font-semibold text-latte-500 uppercase tracking-wider">
                          수량
                        </th>
                        <th className="px-6 py-4 text-left text-xs font-semibold text-latte-500 uppercase tracking-wider">
                          사유
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-latte-100 bg-white">
                      {recentLogs.map((log) => (
                        <tr key={log.id} className="hover:bg-latte-50/30 transition-colors">
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-latte-700">
                            {new Date(log.created_at).toLocaleString('ko-KR')}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <Badge variant={log.change_amount >= 0 ? 'default' : 'destructive'}
                              className={log.change_amount >= 0 ? 'bg-green-600 hover:bg-green-700' : ''}>
                              {log.change_amount >= 0 ? '입고' : '출고'}
                            </Badge>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-mono text-latte-900 font-bold">
                            {log.change_amount > 0 ? '+' : ''}{log.change_amount.toFixed(1)} kg
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-latte-500">
                            {log.notes || '-'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </motion.section>

            {/* 빠른 링크 */}
            <motion.section
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.4 }}
            >
              <h2 className="text-2xl font-serif font-bold text-latte-900 mb-4">
                빠른 작업
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Link href="/beans" className="block h-full">
                  <Card className="h-full hover:border-latte-400 group cursor-pointer border-latte-200">
                    <CardHeader>
                      <CardTitle className="flex justify-between items-center">
                        원두 관리
                        <Coffee className="w-5 h-5 text-latte-400 group-hover:text-latte-600 transition-colors" />
                      </CardTitle>
                      <CardDescription>새로운 원두를 등록하고 관리합니다.</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex gap-2">
                        <Badge variant="secondary">CRUD</Badge>
                        <Badge variant="secondary">Beans</Badge>
                      </div>
                    </CardContent>
                  </Card>
                </Link>

                <Link href="/blends" className="block h-full">
                  <Card className="h-full hover:border-latte-400 group cursor-pointer border-latte-200">
                    <CardHeader>
                      <CardTitle className="flex justify-between items-center">
                        블렌드 레시피
                        <Palette className="w-5 h-5 text-latte-400 group-hover:text-latte-600 transition-colors" />
                      </CardTitle>
                      <CardDescription>나만의 커피 블렌드를 만듭니다.</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex gap-2">
                        <Badge variant="secondary">Recipe</Badge>
                        <Badge variant="secondary">Blends</Badge>
                      </div>
                    </CardContent>
                  </Card>
                </Link>

                <Link href="/inventory" className="block h-full">
                  <Card className="h-full hover:border-latte-400 group cursor-pointer border-latte-200">
                    <CardHeader>
                      <CardTitle className="flex justify-between items-center">
                        재고 관리
                        <Package className="w-5 h-5 text-latte-400 group-hover:text-latte-600 transition-colors" />
                      </CardTitle>
                      <CardDescription>입출고 및 재고 현황을 확인합니다.</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex gap-2">
                        <Badge variant="secondary">Inventory</Badge>
                        <Badge variant="secondary">Stock</Badge>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              </div>
            </motion.section>
          </>
        )}
      </div>
    </div>
  )
}
