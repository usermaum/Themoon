'use client';

import { useEffect } from 'react';
import MascotStatus from '@/components/ui/mascot-status';
import { Button } from '@/components/ui/button';
import { RefreshCcw } from 'lucide-react';

export default function Error({
    error,
    reset,
}: {
    error: Error & { digest?: string };
    reset: () => void;
}) {
    useEffect(() => {
        console.error('Root Layer Error:', error);
    }, [error]);

    return (
        <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-gradient-to-br from-red-50 via-latte-50 to-latte-100 p-4">
            {/* Floating Coffee Beans Background (Chaos Mode) */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
                {/* Bean 1 - Fast Reverse */}
                <div className="absolute left-[15%] top-[15%] h-14 w-14 animate-float-reverse opacity-20">
                    <div className="h-full w-full rounded-full bg-gradient-to-br from-red-200 to-latte-400 shadow-lg" />
                </div>

                {/* Bean 2 - Fast */}
                <div className="absolute right-[20%] top-[40%] h-10 w-10 animate-float-fast opacity-25">
                    <div className="h-full w-full rounded-full bg-gradient-to-br from-latte-400 to-latte-600 shadow-md" />
                </div>

                {/* Bean 3 - Medium Reverse */}
                <div className="absolute left-[30%] bottom-[20%] h-16 w-16 animate-float-reverse opacity-15" style={{ animationDelay: '1s' }}>
                    <div className="h-full w-full rounded-full bg-gradient-to-br from-red-300 to-latte-500 shadow-lg" />
                </div>

                {/* Bean 4 - Tiny Fast */}
                <div className="absolute right-[10%] bottom-[30%] h-6 w-6 animate-float-fast opacity-30" style={{ animationDelay: '0.5s' }}>
                    <div className="h-full w-full rounded-full bg-gradient-to-br from-latte-500 to-latte-700" />
                </div>

                {/* Atmospheric Overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-red-50/20 via-transparent to-transparent" />
            </div>

            <div className="relative z-10 scale-110">
                <MascotStatus
                    variant="error"
                    title="시스템 오류가 발생했습니다"
                    description={error.message || "원두가 쏟아진 것 같습니다. 잠시 후 다시 시도해주시겠어요?"}
                    videoClassName="w-80 h-80 drop-shadow-2xl grayscale-[0.2]"
                    action={
                        <Button
                            onClick={() => reset()}
                            variant="default"
                            className="rounded-full px-8 bg-red-600 hover:bg-red-700 text-white shadow-lg hover:shadow-red-200 hover:scale-105 transition-all duration-300"
                        >
                            <div className="flex items-center gap-2">
                                <RefreshCcw className="w-4 h-4 animate-spin-slow" />
                                시스템 재시도
                            </div>
                        </Button>
                    }
                />
            </div>
        </div>
    );
}
