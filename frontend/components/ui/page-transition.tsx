'use client';

import { useEffect, useState } from 'react';
import { usePathname, useSearchParams } from 'next/navigation';
import LoadingState from '@/components/ui/loading-state';
import { motion, AnimatePresence } from 'framer-motion';

export default function PageTransition() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // 경로가 바뀌면 로딩 시작
    setIsLoading(true);

    // 짧은 지연 후 로딩 종료 (데이터 페칭 완료 시점과 맞추는 것이 이상적이나,
    // Next.js App Router는 페이지 로드 완료 이벤트를 완벽히 제공하지 않으므로
    // 시각적 피드백을 위한 최소 시간을 보장)
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 500); // 0.5초 최소 노출

    return () => clearTimeout(timer);
  }, [pathname, searchParams]);

  return (
    <AnimatePresence>
      {isLoading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          className="fixed inset-0 z-50 flex items-center justify-center bg-white/80 backdrop-blur-sm"
        >
          <LoadingState message="페이지 이동 중..." />
        </motion.div>
      )}
    </AnimatePresence>
  );
}
