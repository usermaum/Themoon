/**
 * API 에러 상태 표시 컴포넌트
 *
 * Render.com 슬립 모드, 네트워크 에러 등에 대한 친화적인 UI 제공
 */
import { AlertTriangle, RefreshCw, WifiOff, Clock } from 'lucide-react'
import { Button } from './button'

interface ErrorStateProps {
  error?: any
  onRetry?: () => void
  message?: string
  type?: 'network' | 'timeout' | 'server' | 'unknown'
}

export function ErrorState({ error, onRetry, message, type }: ErrorStateProps) {
  // 에러 타입 자동 감지
  const errorType = type || detectErrorType(error)

  const config = getErrorConfig(errorType)

  return (
    <div className="flex flex-col items-center justify-center py-12 px-4">
      <div className="w-16 h-16 rounded-full bg-red-50 flex items-center justify-center mb-4">
        {config.icon}
      </div>

      <h3 className="text-lg font-semibold text-latte-900 mb-2">
        {config.title}
      </h3>

      <p className="text-sm text-latte-600 text-center max-w-md mb-6">
        {message || config.message}
      </p>

      {onRetry && (
        <Button
          onClick={onRetry}
          variant="outline"
          className="gap-2"
        >
          <RefreshCw className="w-4 h-4" />
          다시 시도
        </Button>
      )}

      {errorType === 'timeout' && (
        <p className="text-xs text-latte-500 mt-4 text-center max-w-md">
          💡 팁: 서버가 절전 모드에서 깨어나는 중일 수 있습니다.
          잠시 후 자동으로 재시도됩니다.
        </p>
      )}
    </div>
  )
}

// 에러 타입 감지
function detectErrorType(error: any): 'network' | 'timeout' | 'server' | 'unknown' {
  if (!error) return 'unknown'

  // 네트워크 에러
  if (error.message?.includes('Network Error') || error.code === 'ERR_NETWORK') {
    return 'network'
  }

  // 타임아웃
  if (error.message?.includes('timeout') || error.code === 'ECONNABORTED') {
    return 'timeout'
  }

  // 5xx 서버 에러
  if (error.response?.status >= 500) {
    return 'server'
  }

  return 'unknown'
}

// 에러 타입별 설정
function getErrorConfig(type: string) {
  const configs = {
    network: {
      icon: <WifiOff className="w-8 h-8 text-red-500" />,
      title: '네트워크 연결 실패',
      message: '인터넷 연결을 확인해주세요. 연결이 복구되면 자동으로 재시도됩니다.',
    },
    timeout: {
      icon: <Clock className="w-8 h-8 text-amber-500" />,
      title: '서버 응답 대기 중',
      message: '서버가 응답하는 데 시간이 걸리고 있습니다. 자동으로 재시도 중입니다.',
    },
    server: {
      icon: <AlertTriangle className="w-8 h-8 text-red-500" />,
      title: '서버 오류',
      message: '서버에서 오류가 발생했습니다. 잠시 후 다시 시도해주세요.',
    },
    unknown: {
      icon: <AlertTriangle className="w-8 h-8 text-latte-400" />,
      title: '오류가 발생했습니다',
      message: '데이터를 불러올 수 없습니다. 다시 시도해주세요.',
    },
  }

  return configs[type as keyof typeof configs] || configs.unknown
}

// 로딩 스켈레톤 컴포넌트
export function LoadingSkeleton({ count = 3 }: { count?: number }) {
  return (
    <div className="space-y-4">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="animate-pulse">
          <div className="h-24 bg-latte-100 rounded-2xl"></div>
        </div>
      ))}
    </div>
  )
}

// 빈 상태 컴포넌트
export function EmptyState({ message = '데이터가 없습니다', icon }: { message?: string, icon?: React.ReactNode }) {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4">
      <div className="w-16 h-16 rounded-full bg-latte-100 flex items-center justify-center mb-4">
        {icon || <AlertTriangle className="w-8 h-8 text-latte-400" />}
      </div>
      <p className="text-sm text-latte-600 text-center">{message}</p>
    </div>
  )
}
