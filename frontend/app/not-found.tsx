'use client';

import Link from 'next/link';
import MascotStatus from '@/components/ui/mascot-status';
import { Button } from '@/components/ui/button';
import { Home } from 'lucide-react';

export default function NotFound() {
    return (
        <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-gradient-to-br from-latte-50 via-latte-100 to-latte-200 p-4">
            {/* Floating Coffee Beans Background */}
            <div className="absolute inset-0 overflow-hidden">
                {/* Coffee Bean 1 - Large, slow orbit */}
                <div className="absolute left-[10%] top-[20%] h-16 w-16 animate-float-slow opacity-20">
                    <div className="h-full w-full rounded-full bg-gradient-to-br from-latte-600 to-latte-700 shadow-lg" />
                </div>

                {/* Coffee Bean 2 - Medium, medium orbit */}
                <div className="absolute right-[15%] top-[30%] h-12 w-12 animate-float-medium opacity-25">
                    <div className="h-full w-full rounded-full bg-gradient-to-br from-latte-500 to-latte-600 shadow-md" />
                </div>

                {/* Coffee Bean 3 - Small, fast orbit */}
                <div className="absolute left-[20%] bottom-[25%] h-8 w-8 animate-float-fast opacity-30">
                    <div className="h-full w-full rounded-full bg-gradient-to-br from-latte-400 to-latte-500 shadow-sm" />
                </div>

                {/* Coffee Bean 4 - Tiny, very slow */}
                <div className="absolute right-[25%] bottom-[35%] h-6 w-6 animate-float-slow opacity-15" style={{ animationDelay: '2s' }}>
                    <div className="h-full w-full rounded-full bg-gradient-to-br from-latte-600 to-latte-700" />
                </div>

                {/* Coffee Bean 5 - Medium, reverse orbit */}
                <div className="absolute left-[70%] top-[60%] h-10 w-10 animate-float-reverse opacity-20">
                    <div className="h-full w-full rounded-full bg-gradient-to-br from-latte-500 to-latte-600 shadow-md" />
                </div>

                {/* Coffee Bean 6 - Large, gentle float */}
                <div className="absolute right-[5%] bottom-[15%] h-14 w-14 animate-float-medium opacity-18" style={{ animationDelay: '4s' }}>
                    <div className="h-full w-full rounded-full bg-gradient-to-br from-latte-600 to-latte-700 shadow-lg" />
                </div>

                {/* Atmospheric Gradient Overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-latte-100/50 via-transparent to-latte-50/30" />
            </div>

            {/* Main Content */}
            <div className="relative z-10">
                <MascotStatus
                    variant="not-found"
                    title="페이지를 찾을 수 없습니다"
                    description="요청하신 페이지가 존재하지 않거나 이동되었을 수 있습니다. 주소를 다시 확인해주세요."
                    videoClassName="w-80 h-80 drop-shadow-2xl"
                    action={
                        <Button
                            asChild
                            variant="outline"
                            className="rounded-full px-8 shadow-lg backdrop-blur-sm hover:shadow-xl transition-all duration-300 hover:scale-105"
                        >
                            <Link href="/" className="flex items-center gap-2">
                                <Home className="w-4 h-4" />
                                홈으로 돌아가기
                            </Link>
                        </Button>
                    }
                />
            </div>
        </div>
    );
}
