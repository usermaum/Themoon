'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Blend, Bean } from '@/lib/api';
import { useBlends, useBeans, deleteBlend } from '@/hooks';
import Link from 'next/link';
import PageHero from '@/components/ui/page-hero';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Search, Plus, Trash2, Edit2, Hexagon, PieChart, Layers, RefreshCw } from 'lucide-react';
import { useLoading } from '@/components/providers/loading-provider';
import MascotStatus from '@/components/ui/mascot-status';

// 블렌드 리스트 메인 페이지
export default function BlendManagementPage() {
  const { startLoading } = useLoading();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');

  const limit = 12;
  const skip = (page - 1) * limit;

  // SWR 훅 사용 - 자동 재시도, 포커스 시 재검증, 네트워크 복구 시 재갱신
  const { blends, isLoading, isValidating, error, refresh } = useBlends({
    skip,
    limit,
    search: search || undefined,
  });

  // 원두 이름 조회를 위한 훅
  const { beans } = useBeans({ limit: 300 });

  const handleDelete = async (id: number) => {
    if (!confirm('정말로 이 블렌드 레시피를 삭제하시겠습니까?')) return;

    try {
      await deleteBlend(id);
      // SWR이 자동으로 캐시를 무효화하고 새로고침
    } catch (err) {
      alert('삭제에 실패했습니다.');
    }
  };

  const getBeanName = (id: number) => {
    const bean = beans.find((b) => b.id === id);
    return bean ? bean.name : `Unknown Bean (${id})`;
  };

  return (
    <div className="min-h-screen">
      <PageHero
        title="Blend Recipes"
        description="나만의 커피 경험을 위한 블렌딩 레시피를 관리하세요."
        icon={<Layers />}
        image="/images/hero/beans-hero.png" // 블렌드용 이미지 있으면 교체 추천
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
              placeholder="블렌드 이름 검색..."
              className="pl-12 pr-10 bg-white border-latte-200 focus:border-latte-400 h-12 rounded-xl shadow-sm"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            {search && (
              <button
                onClick={() => setSearch('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 p-1.5 text-latte-400 hover:text-latte-600 hover:bg-latte-50 rounded-full transition-all"
              >
                <span className="sr-only">Clear search</span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="w-4 h-4"
                >
                  <path d="M18 6 6 18" />
                  <path d="m6 6 12 12" />
                </svg>
              </button>
            )}
          </div>

          <Button
            asChild
            className="shadow-lg hover:shadow-xl bg-latte-800 hover:bg-latte-900 gap-2 h-12 px-6 rounded-xl text-lg font-serif"
          >
            <Link href="/blends/new" onClick={startLoading}>
              <Plus className="w-5 h-5" /> 새 블렌드 생성
            </Link>
          </Button>
        </motion.div>

        {error && (
          <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-200 mb-6 flex items-center gap-2">
            <span>⚠️</span> 블렌드 목록을 불러오는데 실패했습니다.
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

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[1, 2, 3].map((n) => (
              <div key={n} className="h-64 bg-latte-50 rounded-[2rem] animate-pulse"></div>
            ))}
          </div>
        ) : !blends || blends.length === 0 ? (
          <div className="py-12">
            {search ? (
              <MascotStatus
                variant="search"
                title="검색 결과가 없습니다"
                description={`'${search}'에 대한 검색 결과가 없습니다.\n다른 검색어로 시도해보시거나 검색을 초기화해보세요.`}
                action={
                  <Button
                    variant="outline"
                    onClick={() => setSearch('')}
                    className="border-latte-400 text-latte-700 hover:bg-latte-50 rounded-full px-8"
                  >
                    검색 초기화
                  </Button>
                }
              />
            ) : (
              <MascotStatus
                variant="empty"
                title="등록된 블렌드가 없습니다"
                description="나만의 시그니처 블렌드 레시피를 만들어보세요."
                action={
                  <Button
                    asChild
                    variant="outline"
                    className="border-latte-400 text-latte-700 hover:bg-latte-50 rounded-full px-8"
                  >
                    <Link href="/blends/new" onClick={startLoading}>
                      첫 블렌드 만들기
                    </Link>
                  </Button>
                }
              />
            )}
          </div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
          >
            {blends.map((blend, index) => {
              // 이미지 선택 로직
              let imageSrc = '/images/blends/new-moon.png'; // default
              const nameLower = blend.name.toLowerCase();

              if (nameLower.includes('full') || nameLower.includes('풀문')) {
                imageSrc = '/images/blends/full-moon.png';
              } else if (nameLower.includes('eclipse') || nameLower.includes('이클립스')) {
                imageSrc = '/images/blends/eclipse-moon.png';
              }

              return (
                <motion.div
                  key={blend.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: index * 0.05 }}
                >
                  <Card className="group overflow-hidden border-latte-200 hover:border-latte-400 hover:shadow-xl transition-all duration-300 flex flex-col rounded-[1.5rem] h-full">
                    {/* 이미지 영역 */}
                    <div className="relative h-48 w-full overflow-hidden bg-latte-100">
                      <div
                        className="absolute inset-0 bg-cover bg-center transition-transform duration-700 group-hover:scale-110"
                        style={{ backgroundImage: `url(${imageSrc})` }}
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />

                      {/* 오버레이 뱃지 & 액션 */}
                      <div className="absolute top-4 left-4">
                        <Badge className="bg-white/90 text-latte-900 font-serif backdrop-blur-sm border-0">
                          {blend.target_roast_level || 'Custom Roast'}
                        </Badge>
                      </div>
                      <div className="absolute top-4 right-4 flex gap-1 opacity-100 md:opacity-0 group-hover:opacity-100 transition-opacity">
                        <Button
                          asChild
                          size="icon"
                          variant="secondary"
                          className="h-8 w-8 bg-white/90 hover:bg-white text-latte-800 rounded-full shadow-lg"
                        >
                          <Link href={`/blends/${blend.id}`} onClick={startLoading}>
                            <Edit2 className="w-4 h-4" />
                          </Link>
                        </Button>
                        <Button
                          size="icon"
                          variant="destructive"
                          className="h-8 w-8 bg-red-500/90 hover:bg-red-600 rounded-full shadow-lg"
                          onClick={() => handleDelete(blend.id)}
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>

                      <div className="absolute bottom-4 left-4 right-4 text-white">
                        <h3 className="text-xl font-serif font-bold tracking-tight mb-1 drop-shadow-md">
                          {blend.name}
                        </h3>
                        <p className="text-xs text-white/80 line-clamp-1 drop-shadow-sm">
                          {blend.description}
                        </p>
                      </div>
                    </div>

                    {/* 상세 정보 (비율 그래프) */}
                    <CardContent className="pt-6 flex-grow">
                      <div className="space-y-4">
                        <div className="space-y-3">
                          {blend.recipe.map((item, idx) => (
                            <div key={idx} className="space-y-1">
                              <div className="flex justify-between items-center text-xs text-latte-600">
                                <span className="truncate pr-2 font-medium">
                                  {getBeanName(item.bean_id)}
                                </span>
                                <span className="font-bold text-latte-800">
                                  {Math.round(item.ratio * 100)}%
                                </span>
                              </div>
                              <div className="h-1.5 rounded-full bg-latte-100 w-full overflow-hidden">
                                <motion.div
                                  initial={{ width: 0 }}
                                  animate={{ width: `${item.ratio * 100}%` }}
                                  transition={{ duration: 1, delay: 0.5 + idx * 0.1 }}
                                  className={`h-full rounded-full ${idx % 2 === 0 ? 'bg-latte-600' : 'bg-latte-400'}`}
                                />
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </CardContent>

                    <CardFooter className="bg-latte-50/50 border-t border-latte-100 py-3 px-6 text-[10px] font-medium text-latte-400 flex justify-between uppercase tracking-wider">
                      <span>Since {new Date(blend.created_at).getFullYear()}</span>
                      <span>{blend.recipe.length} Origins</span>
                    </CardFooter>
                  </Card>
                </motion.div>
              );
            })}
          </motion.div>
        )}
      </div>
    </div>
  );
}
