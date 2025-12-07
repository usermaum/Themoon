'use client'

import { motion } from 'framer-motion'
import PageHero from '@/components/ui/PageHero'
import { Flame, Layers, ArrowRight } from 'lucide-react'
import Link from 'next/link'

export default function RoastingMainPage() {
    return (
        <div className="min-h-screen bg-[#FDFBF7] flex flex-col">
            <PageHero
                title="Roasting Management"
                description="로스팅 작업을 수행합니다. 싱글 오리진 또는 블렌드 로스팅을 선택하세요."
                icon={<Flame />}
                image="/images/hero/roasting-hero.png"
            />

            {/* 카드 영역 - 히어로와 푸터 사이에서 수직 중앙 정렬 */}
            <div className="flex-1 flex items-center justify-center py-12">
                <div className="container mx-auto px-6 max-w-4xl">
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.3 }}
                        className="grid grid-cols-1 md:grid-cols-2 gap-8"
                    >
                        {/* 싱글 오리진 로스팅 카드 */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.4, delay: 0.1 }}
                        >
                            <Link href="/roasting/single-origin" className="group relative flex flex-col items-center bg-white rounded-[2rem] shadow-lg overflow-hidden transition-all duration-300 hover:shadow-2xl hover:-translate-y-2 h-full">
                                {/* 상단 이미지 */}
                                <div
                                    className="w-full h-48 bg-cover bg-center transition-transform duration-700 group-hover:scale-105"
                                    style={{ backgroundImage: "url('/images/raw_material/01_yirgacheffe_raw.png')" }}
                                >
                                    <div className="w-full h-full bg-black/10 group-hover:bg-transparent transition-colors duration-300" />
                                </div>

                                {/* 플로팅 타이틀 박스 */}
                                <div className="relative -mt-10 bg-white rounded-[1.5rem] shadow-lg px-6 py-5 w-[85%] text-center border border-latte-50 z-10 group-hover:border-latte-200 transition-colors">
                                    <h2 className="font-serif text-2xl font-bold text-latte-900 mb-1">Single Origin</h2>
                                    <p className="text-[10px] font-bold tracking-[0.2em] text-latte-400 uppercase">Roasting Process</p>
                                </div>

                                {/* 설명 및 버튼 */}
                                <div className="flex-1 px-6 pt-4 pb-8 flex flex-col items-center text-center">
                                    <p className="text-latte-600 leading-relaxed mb-6 text-sm font-light">
                                        단일 생두를 로스팅하여 원두 재고로 등록합니다.<br />
                                        로스팅 프로필과 손실률을 정밀하게 관리하세요.
                                    </p>
                                    <div className="bg-latte-800 text-white px-6 py-2.5 rounded-full font-serif text-base shadow-md group-hover:bg-latte-900 group-hover:scale-105 transition-all flex items-center gap-2">
                                        Start Roasting <ArrowRight className="w-3.5 h-3.5" />
                                    </div>
                                </div>
                            </Link>
                        </motion.div>

                        {/* 블렌드 로스팅 카드 */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.4, delay: 0.2 }}
                        >
                            <Link href="/roasting/blend" className="group relative flex flex-col items-center bg-white rounded-[2rem] shadow-lg overflow-hidden transition-all duration-300 hover:shadow-2xl hover:-translate-y-2 h-full">
                                {/* 상단 이미지 */}
                                <div
                                    className="w-full h-48 bg-cover bg-center transition-transform duration-700 group-hover:scale-105"
                                    style={{ backgroundImage: "url('/images/hero/blends-hero.png')" }}
                                >
                                    <div className="w-full h-full bg-black/10 group-hover:bg-transparent transition-colors duration-300" />
                                </div>

                                {/* 플로팅 타이틀 박스 */}
                                <div className="relative -mt-10 bg-white rounded-[1.5rem] shadow-lg px-6 py-5 w-[85%] text-center border border-latte-50 z-10 group-hover:border-latte-200 transition-colors">
                                    <h2 className="font-serif text-2xl font-bold text-latte-900 mb-1">Pre-Roast Blend</h2>
                                    <p className="text-[10px] font-bold tracking-[0.2em] text-latte-400 uppercase">Blending Simulator</p>
                                </div>

                                {/* 설명 및 버튼 */}
                                <div className="flex-1 px-6 pt-4 pb-8 flex flex-col items-center text-center">
                                    <p className="text-latte-600 leading-relaxed mb-6 text-sm font-light">
                                        여러 생두를 섞어서 로스팅하는 블렌딩 작업입니다.<br />
                                        레시피 비율에 따른 생두 필요량을 자동 계산합니다.
                                    </p>
                                    <div className="bg-latte-800 text-white px-6 py-2.5 rounded-full font-serif text-base shadow-md group-hover:bg-latte-900 group-hover:scale-105 transition-all flex items-center gap-2">
                                        Start Blending <ArrowRight className="w-3.5 h-3.5" />
                                    </div>
                                </div>
                            </Link>
                        </motion.div>
                    </motion.div>
                </div>
            </div>
        </div>
    )
}
