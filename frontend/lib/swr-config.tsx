'use client';

/**
 * SWR 전역 설정
 *
 * API 연결 복구 시 자동 재검증, 에러 재시도 등 설정
 */
import { SWRConfig } from 'swr';
import { ReactNode } from 'react';
import api from '@/lib/api';

// SWR용 axios fetcher
export const fetcher = async (url: string) => {
  const response = await api.get(url);
  return response.data;
};

interface SWRProviderProps {
  children: ReactNode;
}

export function SWRProvider({ children }: SWRProviderProps) {
  return (
    <SWRConfig
      value={{
        fetcher,
        // 에러 발생 시 재시도 설정 (Render.com 슬립 모드 대응)
        errorRetryCount: 5, // 최대 5번 재시도
        errorRetryInterval: 5000, // 5초 간격으로 재시도

        // 지수 백오프: 5초 → 10초 → 20초 → 40초 → 60초
        shouldRetryOnError: (error) => {
          // 4xx 클라이언트 에러는 재시도 안함 (400, 401, 403, 404 등)
          if (
            error?.response?.status &&
            error.response.status >= 400 &&
            error.response.status < 500
          ) {
            return false;
          }
          // 5xx 서버 에러, 타임아웃, 네트워크 에러는 재시도
          return true;
        },

        onErrorRetry: (error, key, config, revalidate, { retryCount }) => {
          // 최대 재시도 횟수 초과
          if (retryCount >= 5) return;

          // 4xx 에러는 재시도 안함
          if (
            error?.response?.status &&
            error.response.status >= 400 &&
            error.response.status < 500
          ) {
            return;
          }

          // 지수 백오프: 5초 * 2^(retryCount)
          const timeout = Math.min(5000 * Math.pow(2, retryCount), 60000); // 최대 60초

          console.log(`[SWR Retry ${retryCount + 1}/5] ${key} in ${timeout}ms`);

          setTimeout(() => revalidate({ retryCount }), timeout);
        },

        // 자동 재검증 설정
        revalidateOnFocus: true, // 탭 포커스 시 재검증
        revalidateOnReconnect: true, // 네트워크 복구 시 재검증
        revalidateIfStale: true, // Stale 데이터일 때 재검증

        // 중복 요청 방지 (2초 내 동일 요청 무시)
        dedupingInterval: 2000,

        // 포커스 감지 간격 (5초)
        focusThrottleInterval: 5000,

        // 에러 핸들링
        onError: (error, key) => {
          console.error(`[SWR Error] ${key}:`, error?.message || error);

          // 프로덕션에서는 에러 로깅 서비스로 전송 가능
          // e.g., Sentry, LogRocket 등
        },
      }}
    >
      {children}
    </SWRConfig>
  );
}
