'use client';

import { useState, useEffect } from 'react';
import { useRouter, usePathname, useSearchParams } from 'next/navigation';
import { motion } from 'framer-motion';
import { Bean } from '@/lib/api';
import { useBeans, deleteBean } from '@/hooks';
import Link from 'next/link';
import { useLoading } from '@/components/providers/loading-provider';
import PageHero from '@/components/ui/page-hero';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
  CardDescription,
} from '@/components/ui/card';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Search, Plus, Trash2, Coffee, Edit2, MapPin, Tag, RefreshCw, X } from 'lucide-react';
import { formatCurrency } from '@/lib/utils';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import MascotStatus from '@/components/ui/mascot-status';

// Helper to resolve bean images
const getBeanImage = (bean: Bean) => {
  // ... (This function remains unchanged)
  const nameLower = bean.name.toLowerCase();

  // 1. Blend Beans (Priority Check by Name)
  if (nameLower.includes('full moon') || nameLower.includes('풀문'))
    return '/images/roasted/17_fullmoon_blend.png';
  if (nameLower.includes('new moon') || nameLower.includes('뉴문'))
    return '/images/roasted/18_newmoon_blend.png';
  if (nameLower.includes('eclipse') || nameLower.includes('이클립스'))
    return '/images/roasted/19_eclipse_blend.png';

  // 2. Generic Blend Check
  if (bean.type === 'BLEND_BEAN' || nameLower.includes('blend') || nameLower.includes('블렌드')) {
    // Fallback for generic blend
    return '/images/roasted/17_fullmoon_blend.png';
  }

  // 2. Determine File Type (Green vs Roasted)
  // Check if it's a Roasted Bean based on type or roast_profile
  const isRoasted =
    bean.type === 'ROASTED_BEAN' || (bean.roast_profile && bean.roast_profile !== null);

  let folder = '/images/raw_material/';
  // Use optimized WebP thumbnail for raw materials
  let suffix = '_raw_thumb.webp';

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

  if (nameLower.includes('예가체프') || nameLower.includes('yirgacheffe'))
    idPrefix = '01_yirgacheffe';
  else if (nameLower.includes('모모라') || nameLower.includes('mormora')) idPrefix = '02_mormora';
  else if (nameLower.includes('코케') || nameLower.includes('koke')) idPrefix = '03_koke_honey';
  else if (nameLower.includes('우라가') || nameLower.includes('uraga')) idPrefix = '04_uraga';
  else if (nameLower.includes('시다모') || nameLower.includes('sidamo')) idPrefix = '05_sidamo';
  else if (nameLower.includes('마사이') || nameLower.includes('masai')) idPrefix = '06_masai';
  else if (
    nameLower.includes('키린야가') ||
    nameLower.includes('키리냐가') ||
    nameLower.includes('kirinyaga')
  )
    idPrefix = '07_kirinyaga';
  else if (nameLower.includes('후일라') || nameLower.includes('huila')) idPrefix = '08_huila';
  else if (nameLower.includes('안티구아') || nameLower.includes('antigua')) idPrefix = '09_antigua';
  else if (nameLower.includes('엘탄케') || nameLower.includes('eltanque')) idPrefix = '10_eltanque';
  else if (nameLower.includes('파젠다') || nameLower.includes('fazenda')) idPrefix = '11_fazenda';
  else if (nameLower.includes('산토스') || nameLower.includes('santos')) idPrefix = '12_santos';
  else if (nameLower.includes('디카페') || nameLower.includes('decaf')) {
    if (nameLower.includes('sdm')) idPrefix = '13_decaf_sdm';
    else if (nameLower.includes('sm')) idPrefix = '14_decaf_sm';
    else idPrefix = '15_swiss_water';
  } else if (nameLower.includes('스위스') || nameLower.includes('swiss'))
    idPrefix = '15_swiss_water';
  else if (nameLower.includes('게이샤') || nameLower.includes('geisha')) idPrefix = '16_geisha';

  return `${folder}${idPrefix}${suffix}`;
};

export default function BeanManagementPage() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const { startLoading } = useLoading();

  // URL에서 페이지 번호 가져오기 (기본값 1)
  const page = Number(searchParams.get('page')) || 1;
  const [search, setSearch] = useState('');
  const [activeTab, setActiveTab] = useState('all');
  const [itemToDelete, setItemToDelete] = useState<number | null>(null);

  // 탭 변경 핸들러
  const handleTabChange = (value: string) => {
    setActiveTab(value);
    setPage(1, false);
  };

  // 탭 값에 따른 필터 타입 반환
  const getBeanTypes = () => {
    switch (activeTab) {
      case 'raw':
        return ['GREEN_BEAN'];
      case 'roasted':
        return ['ROASTED_BEAN'];
      case 'blend':
        return ['BLEND_BEAN'];
      default:
        return [];
    }
  };

  // 페이지 변경 핸들러
  const setPage = (newPage: number, withLoading: boolean = true) => {
    if (withLoading) startLoading();
    const params = new URLSearchParams(searchParams.toString());
    params.set('page', newPage.toString());
    router.push(`${pathname}?${params.toString()}`);
  };

  const limit = 12;
  const skip = (page - 1) * limit;

  // SWR 훅 사용 - 자동 재시도, 포커스 시 재검증, 네트워크 복구 시 재갱신
  const {
    beans,
    pages: totalPages,
    isLoading,
    isValidating,
    error,
    refresh,
  } = useBeans({
    skip,
    limit,
    search: search || undefined,
    type: getBeanTypes(),
  });

  const handleDelete = async (e: React.MouseEvent, id: number) => {
    e.preventDefault();
    e.stopPropagation();
    setItemToDelete(id);
  };

  const confirmDelete = async () => {
    if (!itemToDelete) return;

    try {
      await deleteBean(itemToDelete);
      setItemToDelete(null);
    } catch (err) {
      alert('삭제에 실패했습니다.');
    }
  };

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
              className="pl-12 pr-10 bg-white border-latte-200 focus:border-latte-400 h-12 rounded-xl shadow-sm"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            {search && (
              <button
                onClick={() => setSearch('')}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-latte-400 hover:text-latte-600 focus:outline-none"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>

          <Button
            asChild
            className="shadow-lg hover:shadow-xl bg-latte-800 hover:bg-latte-900 gap-2 h-12 px-6 rounded-xl text-lg font-serif"
          >
            <Link href="/beans/new" onClick={startLoading}>
              <Plus className="w-5 h-5" /> 새 원두 등록
            </Link>
          </Button>
        </motion.div>

        <Tabs defaultValue="all" value={activeTab} onValueChange={handleTabChange} className="mb-8">
          <TabsList className="bg-latte-100 p-1 h-12 rounded-xl">
            <TabsTrigger
              value="all"
              className="h-10 rounded-lg px-6 data-[state=active]:bg-white data-[state=active]:text-latte-900 data-[state=active]:shadow-sm"
            >
              전체
            </TabsTrigger>
            <TabsTrigger
              value="raw"
              className="h-10 rounded-lg px-6 data-[state=active]:bg-white data-[state=active]:text-latte-900 data-[state=active]:shadow-sm"
            >
              생두
            </TabsTrigger>
            <TabsTrigger
              value="roasted"
              className="h-10 rounded-lg px-6 data-[state=active]:bg-white data-[state=active]:text-latte-900 data-[state=active]:shadow-sm"
            >
              원두
            </TabsTrigger>
            <TabsTrigger
              value="blend"
              className="h-10 rounded-lg px-6 data-[state=active]:bg-white data-[state=active]:text-latte-900 data-[state=active]:shadow-sm"
            >
              블렌드
            </TabsTrigger>
          </TabsList>
        </Tabs>

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
          <div className="py-12">
            {search ? (
              <MascotStatus
                variant="search"
                title="검색 결과가 없습니다"
                description={`'${search}'에 대한 검색 결과를 찾을 수 없습니다. 다른 검색어를 입력해 보세요.`}
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
            ) : activeTab === 'blend' ? (
              <MascotStatus
                variant="empty"
                title="등록된 블렌드가 없습니다"
                description="새로운 블렌드 레시피를 생성하면 이곳에 표시됩니다."
                action={
                  <Button
                    asChild
                    variant="outline"
                    className="border-latte-400 text-latte-700 hover:bg-latte-50 rounded-full px-8"
                  >
                    <Link href="/roasting/blend" onClick={startLoading}>
                      블렌드 생성 (Pre-Roast)
                    </Link>
                  </Button>
                }
              />
            ) : activeTab === 'roasted' ? (
              <MascotStatus
                variant="empty"
                title="등록된 원두가 없습니다"
                description="로스팅된 싱글 오리진 원두가 없습니다."
                action={
                  <Button
                    asChild
                    variant="outline"
                    className="border-latte-400 text-latte-700 hover:bg-latte-50 rounded-full px-8"
                  >
                    <Link href="/roasting/single-origin" onClick={startLoading}>
                      싱글 오리진 로스팅
                    </Link>
                  </Button>
                }
              />
            ) : (
              <MascotStatus
                variant="empty"
                title="원두 목록이 비어있습니다"
                description="새로운 원두(생두)를 등록하여 컬렉션을 시작해보세요."
                action={
                  <Button
                    asChild
                    variant="outline"
                    className="border-latte-400 text-latte-700 hover:bg-latte-50 rounded-full px-8"
                  >
                    <Link href="/beans/new" onClick={startLoading}>
                      첫 번째 원두 등록하기
                    </Link>
                  </Button>
                }
              />
            )}
          </div>
        ) : (
          <div
            key={activeTab}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 animate-in fade-in slide-in-from-bottom-4 duration-500"
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
                      <Badge
                        variant="secondary"
                        className="bg-white/90 backdrop-blur-sm shadow-sm font-serif border-0"
                      >
                        {bean.roast_profile || bean.grade || 'Raw Bean'}
                      </Badge>
                    </div>
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center p-6">
                      <div className="flex gap-2">
                        <Button
                          asChild
                          size="icon"
                          variant="secondary"
                          className="bg-white/90 hover:bg-white text-latte-800 rounded-full h-10 w-10"
                        >
                          <Link href={`/beans/${bean.id}`} onClick={startLoading}>
                            <Edit2 className="w-4 h-4" />
                          </Link>
                        </Button>
                        <Button
                          size="icon"
                          variant="destructive"
                          className="rounded-full h-10 w-10"
                          onClick={(e) => handleDelete(e, bean.id)}
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                  <CardHeader className="pb-2">
                    <div className="flex justify-between items-start mb-2">
                      <Badge
                        variant="outline"
                        className="border-latte-300 text-latte-600 bg-latte-50/50"
                      >
                        {bean.variety || 'Unknown'}
                      </Badge>
                      <span
                        className={`font-mono font-bold text-sm ${bean.quantity_kg < 5 ? 'text-red-500' : 'text-latte-400'}`}
                      >
                        {bean.quantity_kg.toFixed(1)}kg
                      </span>
                    </div>
                    <CardTitle className="leading-tight group-hover:text-latte-600 transition-colors">
                      <Link
                        href={`/beans/${bean.id}`}
                        onClick={startLoading}
                        className="hover:underline decoration-latte-400 underline-offset-4 block"
                      >
                        <span>{bean.name_ko || bean.name}</span>
                        {bean.name_en && (
                          <span className="block text-xs font-normal text-latte-400 mt-1 font-sans">
                            {bean.name_en}
                          </span>
                        )}
                      </Link>
                    </CardTitle>
                    <CardDescription className="flex items-center gap-1 mt-1 text-latte-500">
                      <MapPin className="w-3 h-3" />{' '}
                      {bean.origin_ko || bean.origin || 'Unknown Origin'}
                    </CardDescription>
                  </CardHeader>
                  <CardFooter className="pt-2 border-t border-latte-50 mt-auto bg-latte-50/30">
                    <div className="w-full flex justify-between items-center text-sm">
                      <span className="text-latte-400">단가 (kg)</span>
                      <span className="font-mono font-bold text-latte-800">
                        ₩{formatCurrency(bean.purchase_price_per_kg)}
                      </span>
                    </div>
                  </CardFooter>
                </Card>
              </motion.div>
            ))}
          </div>
        )}

        {/* Pagination */}
        {/* Pagination */}
        {beans.length > 0 && (
          <div className="mt-12 flex justify-center gap-3">
            <Button
              variant="outline"
              onClick={() => setPage(Math.max(1, page - 1))}
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
              onClick={() => setPage(Math.min(totalPages, page + 1))}
              disabled={page >= totalPages}
              className="bg-white border-latte-200 text-latte-700 hover:bg-latte-50 px-6"
            >
              다음 페이지
            </Button>
          </div>
        )}
      </div>

      <AlertDialog open={!!itemToDelete} onOpenChange={(open) => !open && setItemToDelete(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>원두 삭제 확인</AlertDialogTitle>
            <AlertDialogDescription>
              정말로 이 원두 데이터를 삭제하시겠습니까?
              <br />이 작업은 되돌릴 수 없습니다.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>취소</AlertDialogCancel>
            <AlertDialogAction onClick={confirmDelete} className="bg-red-600 hover:bg-red-700">
              삭제
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
