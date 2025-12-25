'use client';

import { useEffect } from 'react';
import { Button } from '@/components/ui/button';
import MascotStatus from '@/components/ui/mascot-status';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error(error);
  }, [error]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-[#F8F5F2] p-4">
      <MascotStatus
        variant="error"
        title="문제가 발생했습니다!"
        description={error.message || '예기치 않은 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'}
        videoClassName="w-64 h-64 border-red-100 shadow-red-100/50"
        action={
          <div className="flex gap-4">
            <Button
              onClick={() => (window.location.href = '/')}
              variant="outline"
              className="bg-white border-latte-200 text-latte-700 hover:bg-latte-50 hover:text-latte-900"
            >
              홈으로 이동
            </Button>
            <Button
              onClick={() => reset()}
              className="bg-red-500 hover:bg-red-600 text-white shadow-lg shadow-red-500/20 border border-transparent"
            >
              다시 시도
            </Button>
          </div>
        }
      />
    </div>
  );
}
