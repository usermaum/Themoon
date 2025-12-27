'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Bean, InventoryLog, InventoryLogAPI, DashboardAPI } from '@/lib/api';
import Link from 'next/link';
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import Hero from '@/components/home/Hero';
import { ErrorState, LoadingSkeleton } from '@/components/ui/error-state';
import { Coffee, Layers, Package, AlertTriangle, ArrowRight } from 'lucide-react';

export default function HomePage() {
  const [stats, setStats] = useState<{
    total_beans: number;
    total_blends: number;
    total_stock_kg: number;
    low_stock_beans: Bean[];
    low_stock_count: number;
  } | null>(null);

  const [recentLogs, setRecentLogs] = useState<InventoryLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<any>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [statsData, logsData] = await Promise.all([
        DashboardAPI.getStats(),
        InventoryLogAPI.getAll({ limit: 10 }),
      ]);

      setStats(statsData);
      setRecentLogs(Array.isArray(logsData?.items) ? logsData.items : []);
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // stats가 없으면 0으로 처리 (로딩 중 또는 에러)
  const totalBeans = stats?.total_beans || 0;
  const totalBlends = stats?.total_blends || 0;
  const totalStock = stats?.total_stock_kg || 0;
  const lowStockBeans = stats?.low_stock_beans || [];

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
                    <p className="text-latte-500 text-sm font-medium">보유 생두</p>
                    <p className="text-3xl font-bold text-latte-900 mt-1">{totalBeans}</p>
                  </div>
                  <Coffee className="w-10 h-10 text-latte-300" />
                </CardContent>
              </Card>

              <Card className="hover:border-latte-400">
                <CardContent className="p-6 flex items-center justify-between">
                  <div>
                    <p className="text-latte-500 text-sm font-medium">블렌드 레시피</p>
                    <p className="text-3xl font-bold text-latte-900 mt-1">{totalBlends}</p>
                  </div>
                  <Layers className="w-10 h-10 text-latte-300" />
                </CardContent>
              </Card>

              <Card className="hover:border-latte-400">
                <CardContent className="p-6 flex items-center justify-between">
                  <div>
                    <p className="text-latte-500 text-sm font-medium">총 재고량</p>
                    <p className="text-3xl font-bold text-latte-900 mt-1">
                      {totalStock.toFixed(1)} <span className="text-lg text-latte-400">kg</span>
                    </p>
                  </div>
                  <Package className="w-10 h-10 text-latte-300" />
                </CardContent>
              </Card>

              <Card
                className={`hover:border-red-300 ${lowStockBeans.length > 0 ? 'border-red-200 bg-red-50/50' : ''}`}
              >
                <CardContent className="p-6 flex items-center justify-between">
                  <div>
                    <p className="text-red-600/80 text-sm font-medium">재고 부족</p>
                    <p className="text-3xl font-bold text-red-600 mt-1">
                      {stats?.low_stock_count || 0}
                    </p>
                  </div>
                  <AlertTriangle className="w-10 h-10 text-red-300" />
                </CardContent>
              </Card>
            </motion.div>

            {/* 재고 부족 알림 (Red Theme - Polished) */}
            {lowStockBeans.length > 0 && (
              <motion.section
                initial={{ opacity: 0, scale: 0.98 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.4, delay: 0.2 }}
                className="mb-8"
              >
                <div className="bg-[#FFFBF5] rounded-[2.5rem] border-2 border-dashed border-red-200 p-8 shadow-xl relative overflow-visible">
                  {/* Top Pin Decoration (Punch Hole) */}
                  <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 w-8 h-8 rounded-full bg-red-50 shadow-sm z-20 border-4 border-red-100 flex items-center justify-center">
                    <div className="w-2 h-2 rounded-full bg-red-200 shadow-inner"></div>
                  </div>

                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8 border-b-2 border-dashed border-red-100 pb-6">
                    <div>
                      <h2 className="text-3xl font-serif font-bold text-red-900 mb-1 flex items-center gap-3">
                        <AlertTriangle className="w-8 h-8 text-red-500 animate-pulse" />
                        STOCK ALERT
                      </h2>
                      <p className="text-red-700/60 font-mono text-xs font-bold tracking-widest uppercase">
                        System Critical Warning
                      </p>
                    </div>
                    <Badge className="bg-red-600 hover:bg-red-700 text-white px-4 py-1.5 rounded-full text-sm font-bold shadow-lg border-none animate-bounce md:animate-none">
                      {lowStockBeans.length} Items Short!
                    </Badge>
                  </div>

                  <div className="space-y-6">
                    <div className="bg-red-50/80 p-5 rounded-2xl border border-red-100/50 backdrop-blur-sm shadow-inner flex items-start gap-4">
                      <div className="bg-white p-2 rounded-xl shadow-sm border border-red-100">
                        <span className="text-2xl">💡</span>
                      </div>
                      <div>
                        <p className="text-red-900 font-bold text-lg leading-snug">
                          재고 부족 품목이 감지되었습니다.
                        </p>
                        <p className="text-red-800/70 text-sm font-medium mt-1">
                          원활한 로스팅 작업을 위해 다음 품목의 재고를 확인하고 보충해주시기 바랍니다.
                        </p>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                      {lowStockBeans.map((bean) => (
                        <div
                          key={bean.id}
                          className="bg-white rounded-2xl p-5 flex flex-col gap-3 shadow-md border border-red-100/30 hover:border-red-300 transition-all hover:-translate-y-1.5 hover:shadow-xl group relative overflow-hidden"
                        >
                          <div className="absolute top-0 right-0 w-16 h-16 bg-red-50/50 rounded-bl-[2rem] -mr-4 -mt-4 transition-colors group-hover:bg-red-100/50" />

                          <div className="flex justify-between items-start relative z-10">
                            <span className="text-red-900 font-bold text-xl group-hover:text-red-700 transition-colors line-clamp-1">
                              {bean.name_ko || bean.name}
                            </span>
                          </div>

                          <div className="flex items-center gap-2 relative z-10">
                            <Badge variant="outline" className="text-[10px] font-bold border-red-200 text-red-800 py-0 h-5">
                              {bean.origin_ko || bean.origin}
                            </Badge>
                          </div>

                          <div className="flex justify-between items-end mt-2 pt-3 border-t border-red-50 relative z-10">
                            <span className="text-latte-400 text-xs font-bold uppercase tracking-tighter">Current Stock</span>
                            <span className="text-red-600 font-mono font-black text-2xl bg-red-50/50 px-3 py-1 rounded-xl shadow-sm border border-red-100/50">
                              {bean.quantity_kg.toFixed(1)}<span className="text-sm ml-0.5">kg</span>
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="mt-10 pt-6 border-t-2 border-dashed border-red-100/50 flex flex-col sm:flex-row justify-between items-center gap-4">
                    <span className="text-red-800/30 text-[10px] font-mono select-none tracking-widest order-2 sm:order-1">
                      SR_LOG_SEC_404_STOCK_LVL_CRITICAL
                    </span>
                    <Button variant="ghost" asChild className="text-red-700 hover:text-red-900 hover:bg-red-50 p-0 px-6 h-12 rounded-2xl font-black text-lg transition-all order-1 sm:order-2">
                      <Link href="/inventory" className="flex items-center gap-3">
                        재고 관리로 이동
                        <ArrowRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
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
              <div className="bg-white rounded-[1em] shadow-sm overflow-hidden border border-latte-200">
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
                          품목
                        </th>
                        <th className="px-6 py-4 text-left text-xs font-semibold text-latte-500 uppercase tracking-wider">
                          유형
                        </th>
                        <th className="px-6 py-4 text-left text-xs font-semibold text-latte-500 uppercase tracking-wider">
                          수량
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-latte-100 bg-white">
                      {recentLogs.map((log) => (
                        <tr key={log.id} className="hover:bg-latte-50/30 transition-colors">
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-latte-700">
                            {new Date(log.created_at).toLocaleString('ko-KR')}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-latte-900 font-medium">
                            {log.bean?.name_ko || log.bean?.name || '-'}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <Badge
                              variant={log.change_amount >= 0 ? 'default' : 'destructive'}
                              className={
                                log.change_amount >= 0 ? 'bg-green-600 hover:bg-green-700' : ''
                              }
                            >
                              {log.change_amount >= 0 ? '입고' : '출고'}
                            </Badge>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-mono text-latte-900 font-bold">
                            {log.change_amount > 0 ? '+' : ''}
                            {log.change_amount.toFixed(1)} kg
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
              <h2 className="text-2xl font-serif font-bold text-latte-900 mb-4">빠른 작업</h2>
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
                        <Layers className="w-5 h-5 text-latte-400 group-hover:text-latte-600 transition-colors" />
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
  );
}
