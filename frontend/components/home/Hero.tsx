'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'

export default function Hero() {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6 }}
            className="relative w-full min-h-[400px] flex items-center overflow-hidden bg-latte-900 text-white shadow-md transition-transform hover:shadow-lg mb-8"
        >
            {/* Background Image */}
            <motion.div
                initial={{ scale: 1.1, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
                className="absolute inset-0"
            >
                <img
                    className="w-full h-full object-cover opacity-90 transition-transform duration-700 hover:scale-105"
                    src="/images/hero/home-hero.png"
                    alt="Hand drip coffee brewing"
                />
                <div className="absolute inset-0 bg-latte-900/50 backdrop-blur-[2px]"></div>
            </motion.div>

            {/* Content */}
            <div className="relative z-10 container mx-auto px-6 py-20 flex flex-col md:flex-row items-center gap-10 justify-center h-full">
                <div className="flex-1 text-center md:text-left max-w-3xl">
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                        className="font-serif text-5xl md:text-6xl font-bold mb-6 tracking-tight text-white drop-shadow-lg"
                    >
                        The Moon <span className="text-latte-200">Drip Bar</span>
                    </motion.h1>
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.35 }}
                        className="text-xl md:text-2xl text-latte-100 leading-relaxed drop-shadow-md font-light"
                    >
                        프리미엄 로스팅 관리 시스템에 오신 것을 환영합니다.
                        <br />
                        원두 재고부터 블렌딩 레시피까지, 모든 과정을 체계적으로 관리하세요.
                    </motion.p>
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.5 }}
                        className="mt-10 flex gap-4 justify-center md:justify-start"
                    >
                        <Button asChild size="lg" className="text-lg">
                            <Link href="/beans">
                                원두 관리 시작하기
                            </Link>
                        </Button>
                        <Button asChild variant="outline" size="lg" className="text-lg bg-white/10 border-white/30 text-white hover:bg-white/20 hover:text-white backdrop-blur-md">
                            <Link href="/blends">
                                블렌드 레시피 보기
                            </Link>
                        </Button>
                    </motion.div>
                </div>
            </div>
        </motion.div>
    )
}
