'use client'

/**
 * Blend 관련 SWR 커스텀 훅
 * 
 * 자동 재검증, 에러 재시도, 뮤테이션 기능 제공
 */
import useSWR, { mutate } from 'swr'
import { Blend, BlendCreateData, BlendAPI } from '@/lib/api'

// API 엔드포인트 키
const BLENDS_KEY = '/api/v1/blends/'

interface UseBlendsOptions {
    skip?: number
    limit?: number
    search?: string
}

/**
 * Blend 목록 조회 훅
 */
export function useBlends(options: UseBlendsOptions = {}) {
    const { skip = 0, limit = 100, search } = options

    // URL 파라미터 생성
    const params = new URLSearchParams()
    params.set('skip', String(skip))
    params.set('limit', String(limit))
    if (search) params.set('search', search)

    const key = `${BLENDS_KEY}?${params.toString()}`

    const { data, error, isLoading, isValidating } = useSWR<Blend[]>(key)

    return {
        blends: data ?? [],
        isLoading,
        isValidating, // 백그라운드 재검증 중
        error,
        // 수동 새로고침
        refresh: () => mutate(key),
    }
}

/**
 * 단일 Blend 조회 훅
 */
export function useBlend(id: number | null) {
    const key = id ? `/api/v1/blends/${id}` : null

    const { data, error, isLoading } = useSWR<Blend>(key)

    return {
        blend: data,
        isLoading,
        error,
        refresh: () => id && mutate(key),
    }
}

/**
 * Blend 생성 함수 (mutation)
 */
export async function createBlend(data: BlendCreateData): Promise<Blend> {
    const result = await BlendAPI.create(data)
    // 목록 캐시 무효화
    await mutate((key) => typeof key === 'string' && key.startsWith(BLENDS_KEY), undefined, { revalidate: true })
    return result
}

/**
 * Blend 수정 함수 (mutation)
 */
export async function updateBlend(id: number, data: Partial<BlendCreateData>): Promise<Blend> {
    const result = await BlendAPI.update(id, data)
    // 목록 및 상세 캐시 무효화
    await mutate((key) => typeof key === 'string' && key.startsWith(BLENDS_KEY), undefined, { revalidate: true })
    await mutate(`/api/v1/blends/${id}`)
    return result
}

/**
 * Blend 삭제 함수 (mutation)
 */
export async function deleteBlend(id: number): Promise<void> {
    await BlendAPI.delete(id)
    // 목록 캐시 무효화
    await mutate((key) => typeof key === 'string' && key.startsWith(BLENDS_KEY), undefined, { revalidate: true })
}

/**
 * 모든 Blend 캐시 새로고침
 */
export function refreshAllBlends() {
    return mutate((key) => typeof key === 'string' && key.startsWith(BLENDS_KEY), undefined, { revalidate: true })
}
