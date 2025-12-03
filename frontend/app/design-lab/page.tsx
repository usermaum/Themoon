'use client'

import React from 'react'
import Link from 'next/link'
import { Coffee, ArrowRight } from 'lucide-react'

export default function DesignLabPage() {
    const demos = [
        {
            id: 'classic',
            name: 'Classic Espresso',
            description: 'Warm, traditional, paper textures, rich browns. The current default.',
            href: '/design-lab/classic',
            color: 'bg-[#2C1810] text-[#F5EBE0]'
        },
        {
            id: 'modern',
            name: 'Modern Cold Brew',
            description: 'Sleek dark mode, glassmorphism, neon amber accents. Tech-focused.',
            href: '/design-lab/modern',
            color: 'bg-slate-900 text-amber-400'
        },
        {
            id: 'organic',
            name: 'Organic Raw Bean',
            description: 'Light, airy, nature-inspired, soft greens and beiges. Serif typography.',
            href: '/design-lab/organic',
            color: 'bg-[#E3D5CA] text-[#4A3728]'
        },
        {
            id: 'industrial',
            name: 'Industrial Roastery',
            description: 'Technical, grayscale, bold type, metallic accents. Factory vibes.',
            href: '/design-lab/industrial',
            color: 'bg-neutral-200 text-neutral-900'
        },
        {
            id: 'artistic',
            name: 'Cafe Latte Art',
            description: 'Soft curves, fluid layout, pastel tones, artistic and playful.',
            href: '/design-lab/artistic',
            color: 'bg-[#F5EBE0] text-[#8D7B68]'
        }
    ]

    return (
        <div className="min-h-screen bg-coffee-50 flex items-center justify-center p-8 font-sans">
            <div className="max-w-4xl w-full">
                <div className="text-center mb-12 space-y-4">
                    <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-coffee-900 text-coffee-50 mb-4 shadow-xl">
                        <Coffee size={32} />
                    </div>
                    <h1 className="text-5xl font-bold text-coffee-900 tracking-tight">The Moon Design Lab</h1>
                    <p className="text-xl text-coffee-600 max-w-2xl mx-auto">
                        Explore 5 distinct design directions for the Roasting Management System.
                        Select a concept to view the interactive demo.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {demos.map((demo) => (
                        <Link key={demo.id} href={demo.href} className="group">
                            <div className={`h-full p-8 rounded-2xl shadow-lg transition-all duration-300 transform group-hover:-translate-y-2 group-hover:shadow-2xl ${demo.color} relative overflow-hidden`}>
                                <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                                    <Coffee size={100} />
                                </div>
                                <div className="relative z-10 flex flex-col h-full">
                                    <h3 className="text-2xl font-bold mb-3">{demo.name}</h3>
                                    <p className="text-sm opacity-80 mb-8 leading-relaxed flex-1">
                                        {demo.description}
                                    </p>
                                    <div className="flex items-center font-medium text-sm uppercase tracking-wider">
                                        View Demo <ArrowRight size={16} className="ml-2 group-hover:translate-x-1 transition-transform" />
                                    </div>
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>
            </div>
        </div>
    )
}
