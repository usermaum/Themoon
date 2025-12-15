'use client'

/**
 * Inventory 관련 SWR 커스텀 훅
 * 
 * 자동 재검증, 에러 재시도, 뮤테이션 기능 제공
 */
import useSWR, { mutate } from 'swr'
import { InventoryLog, InventoryLogCreateData, InventoryLogAPI } from '@/lib/api'

// API 엔드포인트 키
const INVENTORY_KEY = '/api/v1/inventory-logs/'

interface UseInventoryLogsOptions {
    beanId?: number
    limit?: number
}

/**
 * Inventory Log 목록 조회 훅
 */
export function useInventoryLogs(options: UseInventoryLogsOptions = {}) {
    const { beanId, limit = 100 } = options

    // URL 파라미터 생성 (Backend matches page/size)
    const params = new URLSearchParams()

    // limit -> size, page=1 (skip 없음)
    params.set('page', '1')
    params.set('size', String(limit))
    if (beanId) params.set('bean_id', String(beanId))

    const key = `${INVENTORY_KEY}?${params.toString()}`

    const { data, error, isLoading, isValidating } = useSWR<InventoryLog[]>(key)

    return {
        logs: data ?? [],
        isLoading,
        isValidating,
        error,
        refresh: () => mutate(key),
    }
}

/**
 * 특정 Bean의 Inventory Log 조회 훅
 */
export function useInventoryLogsByBean(beanId: number | null) {
    const key = beanId ? `${INVENTORY_KEY}?bean_id=${beanId}` : null

    const { data, error, isLoading } = useSWR<InventoryLog[]>(key)

    return {
        logs: data ?? [],
        isLoading,
        error,
        refresh: () => beanId && mutate(key),
    }
}

/**
 * Inventory Log 생성 함수 (mutation)
 */
export async function createInventoryLog(data: InventoryLogCreateData): Promise<InventoryLog> {
    const result = await InventoryLogAPI.create(data)
    // 캐시 무효화
    await mutate((key) => typeof key === 'string' && key.startsWith(INVENTORY_KEY), undefined, { revalidate: true })
    return result
}

/**
 * Inventory Log 수정 함수 (mutation)
 */
export async function updateInventoryLog(id: number, changeAmount: number, notes?: string): Promise<InventoryLog> {
    const result = await InventoryLogAPI.update(id, changeAmount, notes)
    // 캐시 무효화
    await mutate((key) => typeof key === 'string' && key.startsWith(INVENTORY_KEY), undefined, { revalidate: true })
    return result
}

/**
 * Inventory Log 삭제 함수 (mutation)
 */
export async function deleteInventoryLog(id: number): Promise<void> {
    await InventoryLogAPI.delete(id)
    // 캐시 무효화
    await mutate((key) => typeof key === 'string' && key.startsWith(INVENTORY_KEY), undefined, { revalidate: true })
}

/**
 * 모든 Inventory 캐시 새로고침
 */
export function refreshAllInventory() {
    return mutate((key) => typeof key === 'string' && key.startsWith(INVENTORY_KEY), undefined, { revalidate: true })
}
