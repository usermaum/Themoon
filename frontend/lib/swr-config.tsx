'use client'

/**
 * SWR 전역 설정
 * 
 * API 연결 복구 시 자동 재검증, 에러 재시도 등 설정
 */
import { SWRConfig } from 'swr'
import { ReactNode } from 'react'
import api from '@/lib/api'

// SWR용 axios fetcher
export const fetcher = async (url: string) => {
    const response = await api.get(url)
    return response.data
}

interface SWRProviderProps {
    children: ReactNode
}

export function SWRProvider({ children }: SWRProviderProps) {
    return (
        <SWRConfig
            value={{
                fetcher,
                // 에러 발생 시 재시도 설정
                errorRetryCount: 3,           // 최대 3번 재시도
                errorRetryInterval: 3000,     // 3초 간격으로 재시도

                // 자동 재검증 설정
                revalidateOnFocus: true,      // 탭 포커스 시 재검증
                revalidateOnReconnect: true,  // 네트워크 복구 시 재검증
                revalidateIfStale: true,      // Stale 데이터일 때 재검증

                // 중복 요청 방지 (2초 내 동일 요청 무시)
                dedupingInterval: 2000,

                // 포커스 감지 간격 (5초)
                focusThrottleInterval: 5000,

                // 에러 핸들링
                onError: (error, key) => {
                    console.error(`[SWR Error] ${key}:`, error?.message || error)
                },
            }}
        >
            {children}
        </SWRConfig>
    )
}
