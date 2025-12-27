'use client';

import MascotStatus from '@/components/ui/mascot-status';
import { Button } from '@/components/ui/button';
import { RefreshCcw } from 'lucide-react';

export default function GlobalError({
    error,
    reset,
}: {
    error: Error & { digest?: string };
    reset: () => void;
}) {
    return (
        <html>
            <body>
                <div className="flex min-h-screen items-center justify-center bg-latte-25 p-4">
                    <MascotStatus
                        variant="error"
                        title="시스템 치명적 오류"
                        description={error.message || "로딩 중 치명적인 오류가 발생했습니다."}
                        action={
                            <Button
                                onClick={() => reset()}
                                variant="default"
                                className="rounded-full px-8 bg-red-600 hover:bg-red-700 text-white"
                            >
                                <div className="flex items-center gap-2">
                                    <RefreshCcw className="w-4 h-4" />
                                    다시 시도하기
                                </div>
                            </Button>
                        }
                    />
                </div>
            </body>
        </html>
    );
}
