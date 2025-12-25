'use client';

/**
 * Bean 관련 SWR 커스텀 훅
 *
 * 자동 재검증, 에러 재시도, 뮤테이션 기능 제공
 */
import useSWR, { mutate } from 'swr';
import { Bean, BeanCreateData, BeanListResponse, BeanAPI } from '@/lib/api';

// API 엔드포인트 키
const BEANS_KEY = '/api/v1/beans/';

interface UseBeansOptions {
  skip?: number;
  limit?: number;
  search?: string;
  type?: string[];
}

/**
 * Bean 목록 조회 훅
 */
export function useBeans(options: UseBeansOptions = {}) {
  const { skip = 0, limit = 100, search, type } = options;

  // URL 파라미터 생성
  // URL 파라미터 생성 (Backend matches page/size, not skip/limit)
  const params = new URLSearchParams();

  // skip/limit -> page/size 변환
  const page = Math.floor(skip / limit) + 1;
  const size = limit;

  params.set('page', String(page));
  params.set('size', String(size));
  if (search) params.set('search', search);
  if (type && type.length > 0) {
    type.forEach((t) => params.append('type', t));
  }

  const key = `${BEANS_KEY}?${params.toString()}`;

  const { data, error, isLoading, isValidating } = useSWR<BeanListResponse>(key);

  return {
    beans: data?.items ?? [],
    total: data?.total ?? 0,
    page: data?.page ?? 1,
    pages: data?.pages ?? 1,
    isLoading,
    isValidating, // 백그라운드 재검증 중
    error,
    // 수동 새로고침
    refresh: () => mutate(key),
  };
}

/**
 * 단일 Bean 조회 훅
 */
export function useBean(id: number | null) {
  const key = id ? `/api/v1/beans/${id}` : null;

  const { data, error, isLoading } = useSWR<Bean>(key);

  return {
    bean: data,
    isLoading,
    error,
    refresh: () => id && mutate(key),
  };
}

/**
 * Bean 생성 함수 (mutation)
 */
export async function createBean(data: BeanCreateData): Promise<Bean> {
  const result = await BeanAPI.create(data);
  // 목록 캐시 무효화
  await mutate((key) => typeof key === 'string' && key.startsWith(BEANS_KEY), undefined, {
    revalidate: true,
  });
  return result;
}

/**
 * Bean 수정 함수 (mutation)
 */
export async function updateBean(id: number, data: Partial<BeanCreateData>): Promise<Bean> {
  const result = await BeanAPI.update(id, data);
  // 목록 및 상세 캐시 무효화
  await mutate((key) => typeof key === 'string' && key.startsWith(BEANS_KEY), undefined, {
    revalidate: true,
  });
  await mutate(`/api/v1/beans/${id}`);
  return result;
}

/**
 * Bean 삭제 함수 (mutation)
 */
export async function deleteBean(id: number): Promise<void> {
  await BeanAPI.delete(id);
  // 목록 캐시 무효화
  await mutate((key) => typeof key === 'string' && key.startsWith(BEANS_KEY), undefined, {
    revalidate: true,
  });
}

/**
 * 모든 Bean 캐시 새로고침
 */
export function refreshAllBeans() {
  return mutate((key) => typeof key === 'string' && key.startsWith(BEANS_KEY), undefined, {
    revalidate: true,
  });
}
