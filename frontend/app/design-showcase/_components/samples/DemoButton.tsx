'use client';

import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Coffee, ArrowRight, ShoppingBag, Plus, Sparkles, Mail, ArrowLeft } from 'lucide-react';

export function DemoButton() {
    return (
        <div className="min-h-screen bg-latte-50 p-12 font-sans flex flex-col items-center justify-center gap-16 relative">
            {/* Back Navigation */}
            <div className="absolute top-4 left-4 z-50">
                <Button
                    asChild
                    variant="ghost"
                    className="text-latte-600 hover:text-latte-900 hover:bg-latte-100/50 transition-colors"
                >
                    <Link href="/design-showcase?tab=samples">
                        <ArrowLeft className="mr-2 h-4 w-4" /> Back to Gallery
                    </Link>
                </Button>
            </div>

            <div className="text-center space-y-4 pt-8">
                <h1 className="font-serif text-4xl text-latte-900 font-bold">The Art of Buttons</h1>
                <p className="text-latte-600">Cafe Latte Theme Interactive Elements</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12 w-full max-w-5xl">
                {/* 1. Primary Actions */}
                <div className="space-y-6 flex flex-col items-center p-8 bg-white rounded-[2rem] shadow-sm border border-latte-100">
                    <h2 className="font-serif text-xl text-latte-800 mb-2">Espresso Shots</h2>

                    <Button className="w-full bg-latte-900 hover:bg-latte-800 text-latte-50 shadow-lg shadow-latte-900/20 rounded-full h-12 text-lg">
                        Brew Coffee
                    </Button>

                    <Button className="w-full bg-latte-600 hover:bg-latte-500 text-white rounded-xl h-11">
                        <ShoppingBag className="mr-2 h-4 w-4" /> Add to Cart
                    </Button>

                    <Button className="w-full bg-gradient-to-r from-latte-400 to-latte-300 hover:from-latte-500 hover:to-latte-400 text-latte-900 font-bold rounded-lg border border-latte-200/50">
                        <Sparkles className="mr-2 h-4 w-4" /> Special Blend
                    </Button>
                </div>

                {/* 2. Secondary & Outline */}
                <div className="space-y-6 flex flex-col items-center p-8 bg-latte-100/50 rounded-[2rem] border border-latte-200">
                    <h2 className="font-serif text-xl text-latte-800 mb-2">Milk Foam</h2>

                    <Button
                        variant="outline"
                        className="w-full border-2 border-latte-800 text-latte-900 hover:bg-latte-800 hover:text-white rounded-full h-12 font-bold tracking-wide"
                    >
                        VIEW MENU
                    </Button>

                    <Button
                        variant="outline"
                        className="w-full border-latte-300 text-latte-700 hover:bg-white hover:border-latte-400 bg-white/50 rounded-xl dashed border-2"
                    >
                        Customize Order
                    </Button>

                    <Button
                        variant="secondary"
                        className="w-full bg-white text-latte-800 hover:bg-latte-50 shadow-sm border border-latte-100"
                    >
                        Read More <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                </div>

                {/* 3. Minimal & Icon */}
                <div className="space-y-6 flex flex-col items-center p-8">
                    <h2 className="font-serif text-xl text-latte-800 mb-2">Latte Art</h2>

                    <div className="flex gap-4">
                        <Button
                            size="icon"
                            className="rounded-full w-14 h-14 bg-latte-800 hover:bg-latte-700 shadow-xl shadow-latte-400/50 text-latte-100"
                        >
                            <Plus className="h-6 w-6" />
                        </Button>
                        <Button
                            size="icon"
                            variant="outline"
                            className="rounded-full w-14 h-14 border-2 border-latte-300 text-latte-600 hover:border-latte-500 hover:bg-latte-50"
                        >
                            <Coffee className="h-6 w-6" />
                        </Button>
                    </div>

                    <Button
                        variant="ghost"
                        className="text-latte-600 hover:text-latte-900 hover:bg-latte-100/50 -ml-2"
                    >
                        Skip for now
                    </Button>

                    <Button className="w-full bg-black text-white rounded-none border-b-4 border-latte-500 hover:border-latte-400 hover:translate-y-[2px] transition-all">
                        <Mail className="mr-2 h-4 w-4" /> Subscribe
                    </Button>
                </div>
            </div>
        </div>
    );
}
