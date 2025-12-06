'use client'

import React from 'react'
import Link from 'next/link'
import { ArrowRight, Coffee, Check } from 'lucide-react'
import { cn } from '@/lib/utils'

// Theme Data Configuration
const themes = [
    {
        id: 'midnight',
        name: 'Midnight Espresso',
        description: '깊고 진한 에스프레소의 풍미, 프리미엄 다크 모드',
        colors: {
            bg: '#1A120B',
            card: '#3C2A21',
            text: '#E5E5CB',
            primary: '#D5CEA3', // Gold
            accent: '#D5CEA3'
        },
        font: 'font-serif', // Playfair
        vibe: 'Premium, Dark, Serious',
    },
    {
        id: 'paper',
        name: 'Paper Filter',
        description: '핸드 드립의 깔끔함, 여백이 살아있는 미니멀리즘',
        colors: {
            bg: '#FFFFFF',
            card: '#F8F9FA',
            text: '#111111',
            primary: '#111111',
            accent: '#CD853F' // Amber
        },
        font: 'font-sans', // Inter
        vibe: 'Clean, Minimal, Modern',
    },
    {
        id: 'origin',
        name: 'Origin Earth',
        description: '커피나무가 자라는 떼루아, 내추럴 & 오가닉',
        colors: {
            bg: '#F0EBE3', // Kraft
            card: '#E4D1B9', // Clay
            text: '#282A24',
            primary: '#5F8D4E', // Leaf Green
            accent: '#A4BE7B'
        },
        font: 'font-serif', // Lora-like
        vibe: 'Natural, Organic, Warm',
    },
    {
        id: 'vintage',
        name: 'Vintage Roastery',
        description: '달그락거리는 로스터기, 구리와 나무의 질감',
        colors: {
            bg: '#2C3333', // Slate
            card: '#2E4F4F', // Wood
            text: '#EFFFFD',
            primary: '#D77353', // Copper
            accent: '#D77353'
        },
        font: 'font-mono', // Slab-like
        vibe: 'Industrial, Retro, Analog',
    },
    {
        id: 'cherry',
        name: 'Coffee Cherry',
        description: '원두 이전에 과일이었다, 화려하고 산미 넘치는 스타일',
        colors: {
            bg: '#FFF5E4', // Cream
            card: '#FFFFFF',
            text: '#3d3042',
            primary: '#FF6969', // Cherry Red
            accent: '#FFE569' // Yellow
        },
        font: 'font-sans', // Poppins-like
        vibe: 'Pop, Fruity, Energetic',
    },
]

export default function DesignConceptsPage() {
    return (
        <div className="min-h-screen bg-gray-50 pb-20 font-sans">
            {/* Header */}
            <div className="bg-white border-b border-gray-200 py-12 px-4 shadow-sm">
                <div className="max-w-5xl mx-auto text-center">
                    <h1 className="text-4xl font-serif font-bold text-gray-900 mb-4">
                        Design Theme Concepts
                    </h1>
                    <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                        Moon Drip Bar의 새로운 얼굴을 선택해주세요. <br />
                        각 테마는 고유한 커피의 맛과 향을 시각적으로 표현하고 있습니다.
                    </p>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 py-12 space-y-24">
                {themes.map((theme, index) => (
                    <section key={theme.id} className="scroll-mt-20">
                        <div className="flex flex-col lg:flex-row gap-12 items-start">
                            {/* Description Side */}
                            <div className="lg:w-1/3 pt-4">
                                <span className="inline-block px-3 py-1 rounded-full text-sm font-bold bg-gray-900 text-white mb-4">
                                    Option {index + 1}
                                </span>
                                <h2 className="text-4xl font-bold mb-2 text-gray-900">{theme.name}</h2>
                                <p className="text-lg text-gray-600 mb-6">{theme.description}</p>

                                <div className="flex flex-wrap gap-2 mb-8">
                                    {theme.vibe.split(', ').map(v => (
                                        <span key={v} className="px-3 py-1 bg-gray-100 text-gray-600 rounded-lg text-sm font-medium">
                                            #{v}
                                        </span>
                                    ))}
                                </div>

                                <div className="space-y-3">
                                    <div className="flex items-center gap-3">
                                        <div className="w-12 h-12 rounded-full shadow-sm border" style={{ backgroundColor: theme.colors.bg }}></div>
                                        <span className="text-sm text-gray-500">Background</span>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <div className="w-12 h-12 rounded-full shadow-sm border" style={{ backgroundColor: theme.colors.primary }}></div>
                                        <span className="text-sm text-gray-500">Primary / Accent</span>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <div className="w-12 h-12 rounded-full shadow-sm border" style={{ backgroundColor: theme.colors.card }}></div>
                                        <span className="text-sm text-gray-500">Surface / Card</span>
                                    </div>
                                </div>
                            </div>

                            {/* Live Preview Side - Simulated Window */}
                            <div className="lg:w-2/3 w-full rounded-2xl overflow-hidden shadow-2xl border border-gray-200 transition-transform hover:scale-[1.01] duration-500">
                                {/* Browser Mockup Header */}
                                <div className="bg-gray-100 border-b border-gray-200 px-4 py-3 flex items-center gap-2">
                                    <div className="flex gap-1.5">
                                        <div className="w-3 h-3 rounded-full bg-red-400"></div>
                                        <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
                                        <div className="w-3 h-3 rounded-full bg-green-400"></div>
                                    </div>
                                    <div className="ml-4 bg-white rounded-md px-3 py-1 text-xs text-gray-400 flex-1 text-center font-mono">
                                        themoon-drip-bar.com/{theme.id}
                                    </div>
                                </div>

                                {/* Simulated UI Content */}
                                <div
                                    className={`p-8 md:p-12 min-h-[500px] flex flex-col ${theme.font}`}
                                    style={{ backgroundColor: theme.colors.bg, color: theme.colors.text }}
                                >
                                    {/* Navigation Mockup */}
                                    <div className="flex justify-between items-center mb-16 opacity-80">
                                        <div className="text-xl font-bold tracking-tight">The Moon.</div>
                                        <div className="flex gap-6 text-sm font-medium">
                                            <span>Beans</span>
                                            <span>Blends</span>
                                            <span>Inventory</span>
                                        </div>
                                    </div>

                                    {/* Hero Content */}
                                    <div className="max-w-xl">
                                        <span
                                            className="inline-block px-3 py-1 rounded-full text-xs font-bold mb-6 tracking-wide uppercase"
                                            style={{
                                                backgroundColor: theme.colors.primary,
                                                color: theme.id === 'paper' || theme.id === 'cherry' || theme.id === 'origin' ? '#fff' : theme.colors.bg
                                            }}
                                        >
                                            Premium Coffee
                                        </span>
                                        <h3 className="text-5xl md:text-6xl font-bold leading-tight mb-6">
                                            The Perfect <br />
                                            <span style={{ color: theme.colors.accent }}>Roast & Brew.</span>
                                        </h3>
                                        <p className="text-lg opacity-80 mb-10 leading-relaxed max-w-md">
                                            최고의 원두 품질을 관리하고, 당신만의 완벽한 블렌딩 레시피를 만들어보세요.
                                        </p>
                                        <div className="flex gap-4">
                                            <button
                                                className="px-8 py-4 rounded-lg font-bold text-sm transition-opacity hover:opacity-90 shadow-lg"
                                                style={{
                                                    backgroundColor: theme.colors.primary,
                                                    color: theme.id === 'paper' || theme.id === 'cherry' ? '#fff' : theme.colors.bg
                                                }}
                                            >
                                                Get Started
                                            </button>
                                            <button
                                                className="px-8 py-4 rounded-lg font-bold text-sm border-2 backdrop-blur-sm"
                                                style={{ borderColor: theme.colors.primary, color: theme.colors.text }}
                                            >
                                                Learn More
                                            </button>
                                        </div>
                                    </div>

                                    {/* Floating Card Mockup */}
                                    <div className="mt-auto self-end w-full max-w-sm">
                                        <div
                                            className="p-6 rounded-xl shadow-xl flex gap-4 items-center"
                                            style={{ backgroundColor: theme.colors.card }}
                                        >
                                            <div
                                                className="w-16 h-16 rounded-lg flex items-center justify-center shrink-0"
                                                style={{
                                                    backgroundColor: theme.colors.bg,
                                                    color: theme.colors.accent
                                                }}
                                            >
                                                <Coffee size={28} />
                                            </div>
                                            <div>
                                                <div className="font-bold text-lg mb-1">Ethiopia Yirgacheffe</div>
                                                <div className="text-sm opacity-70">Washed • Light Roast</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>
                ))}
            </div>

            {/* CTA */}
            <div className="mt-20 py-20 bg-gray-900 text-white text-center">
                <h2 className="text-3xl font-serif font-bold mb-6">마음에 드는 테마가 있으신가요?</h2>
                <p className="text-gray-400 mb-8 max-w-xl mx-auto">
                    선택하신 테마 번호나 이름을 알려주시면, <br />
                    해당 디자인 시스템으로 전체 앱을 즉시 재구축해드립니다.
                </p>
                <div className="flex gap-4 justify-center">
                    <Link href="/" className="px-8 py-3 bg-white text-gray-900 rounded-full font-bold hover:bg-gray-100 transition-colors">
                        현재 테마 유지하기
                    </Link>
                </div>
            </div>
        </div>
    )
}
