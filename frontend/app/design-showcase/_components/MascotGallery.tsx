'use client';

import { motion } from 'framer-motion';
import MascotStatus from '@/components/ui/mascot-status';
import { RotateCcw, Cat } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function MascotGallery() {
    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1,
                delayChildren: 0.2,
            },
        },
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: {
            opacity: 1,
            y: 0,
            transition: {
                duration: 0.5,
            },
        },
    };

    return (
        <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="space-y-12"
        >
            <motion.section variants={itemVariants}>
                <h2 className="text-3xl font-serif font-bold text-latte-900 mb-6 flex items-center gap-3">
                    <Cat className="w-8 h-8 text-latte-600" />
                    핵심 상태 표현 (Core Expressions)
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <motion.div variants={itemVariants}>
                        <MascotStatus
                            variant="empty"
                            title="데이터가 비어있을 때 (empty)"
                            description="목록에 아무것도 없을 때 나타나는 기본 상태입니다."
                            action={
                                <Button className="bg-latte-900 rounded-full px-8">새 항목 추가</Button>
                            }
                        />
                    </motion.div>

                    <motion.div variants={itemVariants}>
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
                    </motion.div>

                    <motion.div variants={itemVariants}>
                        <MascotStatus
                            variant="sleep"
                            title="대기 중이거나 평화로울 때 (sleep)"
                            description="이력이 없거나 로딩을 기다릴 때 조용히 자고 있는 냥이입니다."
                        />
                    </motion.div>

                    <motion.div variants={itemVariants}>
                        <MascotStatus
                            variant="error"
                            title="에러가 발생했을 때 (error)"
                            description="무언가 잘못되었을 때 나타나는 역동적인 냥이입니다."
                            action={
                                <Button variant="destructive" className="rounded-full px-8">다시 시도</Button>
                            }
                        />
                    </motion.div>
                </div>
            </motion.section>

            <motion.section variants={itemVariants} className="pt-8 border-t border-latte-200">
                <h2 className="text-3xl font-serif font-bold text-latte-900 mb-6 flex items-center gap-3">
                    특수 페이지 (Special Pages)
                </h2>
                <div className="max-w-2xl mx-auto">
                    <MascotStatus
                        variant="not-found"
                        title="404 - 길을 잃었을 때 (not-found)"
                        description="페이지를 찾을 수 없을 때 전용 페이지에서 사용되는 스타일입니다."
                    />
                </div>
            </motion.section>
        </motion.div>
    );
}
