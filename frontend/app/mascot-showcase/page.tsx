'use client';

import MascotStatus from '@/components/ui/mascot-status';
import PageHero from '@/components/ui/page-hero';
import { Coffee, RotateCcw } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function MascotDebugPage() {
    return (
        <div className="min-h-screen bg-latte-50/50 pb-20">
            <PageHero
                title="Design System: Mascot"
                description="The emotional interface layer of The Moon Roastery."
                icon={<Coffee />}
                image="/images/hero/settings-hero.png"
                className="mb-12"
            />

            <div className="container mx-auto px-4 space-y-16">
                <section>
                    <h2 className="text-xl font-serif font-bold text-latte-400 mb-8 uppercase tracking-widest text-center">
                        Core Expressions
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <MascotStatus
                            variant="empty"
                            title="데이터가 비어있을 때 (empty)"
                            description="목록에 아무것도 없을 때 나타나는 기본 상태입니다."
                            action={
                                <Button className="bg-latte-900 rounded-full px-8">새 항목 추가</Button>
                            }
                        />

                        <MascotStatus
                            variant="search"
                            title="검색 결과가 없을 때 (search)"
                            description="열심히 찾아봤지만 찾을 수 없을 때의 모습입니다."
                            action={
                                <Button variant="outline" className="border-latte-400 rounded-full px-8">
                                    <RotateCcw className="w-4 h-4 mr-2" /> 검색 초기화
                                </Button>
                            }
                        />

                        <MascotStatus
                            variant="sleep"
                            title="대기 중이거나 평화로울 때 (sleep)"
                            description="이력이 없거나 로딩을 기다릴 때 조용히 자고 있는 냥이입니다."
                        />

                        <MascotStatus
                            variant="error"
                            title="에러가 발생했을 때 (error)"
                            description="무언가 잘못되었을 때 나타나는 역동적인 냥이입니다."
                            action={
                                <Button variant="destructive" className="rounded-full px-8">다시 시도</Button>
                            }
                        />
                    </div>
                </section>

                <section className="pt-8 border-t border-latte-200">
                    <h2 className="text-xl font-serif font-bold text-latte-400 mb-8 uppercase tracking-widest text-center">
                        Special Pages
                    </h2>
                    <div className="max-w-2xl mx-auto">
                        <MascotStatus
                            variant="not-found"
                            title="404 - 길을 잃었을 때 (not-found)"
                            description="페이지를 찾을 수 없을 때 전용 페이지에서 사용되는 스타일입니다."
                        />
                    </div>
                </section>
            </div>
        </div>
    );
}
