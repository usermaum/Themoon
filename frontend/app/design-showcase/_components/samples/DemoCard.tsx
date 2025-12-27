'use client';

import React from 'react';
import Link from 'next/link';
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Coffee, Heart, Share2, ArrowLeft } from 'lucide-react';

export function DemoCard() {
    return (
        <div className="min-h-screen bg-latte-50 p-8 font-sans flex items-center justify-center relative">
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

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto pt-12">
                {/* 1. The Classic Latte Card */}
                <Card className="border-none shadow-xl bg-white/80 backdrop-blur-sm overflow-hidden group">
                    <div className="h-48 overflow-hidden relative">
                        <div className="absolute inset-0 bg-latte-900/10 group-hover:bg-transparent transition-colors duration-500 z-10"></div>
                        <img
                            src="/images/beans/ethiopia.png"
                            alt="Latte Art"
                            className="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700"
                        />
                    </div>
                    <CardHeader className="relative z-20 -mt-8 mx-4 bg-white rounded-xl shadow-sm text-center pb-2">
                        <CardTitle className="font-serif text-2xl text-latte-900">Ethiopia Sidamo</CardTitle>
                        <CardDescription className="text-latte-600 font-medium tracking-wide text-xs uppercase mt-1">
                            Light Roast • Floral
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="text-center pt-4 text-latte-700 leading-relaxed px-8">
                        <p>은은한 꽃향기와 레몬의 산미가 조화로운 에티오피아의 대표적인 커피입니다.</p>
                    </CardContent>
                    <CardFooter className="justify-center pb-8">
                        <Button className="rounded-full px-8 bg-latte-800 hover:bg-latte-900 text-white shadow-lg shadow-latte-200">
                            Taste Note <Coffee className="ml-2 w-4 h-4" />
                        </Button>
                    </CardFooter>
                </Card>

                {/* 2. The Dark Espresso Card */}
                <Card className="bg-latte-900 text-latte-50 border-latte-800 relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-32 h-32 bg-latte-800 rounded-bl-full opacity-20"></div>
                    <div className="absolute bottom-0 left-0 w-24 h-24 bg-latte-800 rounded-tr-full opacity-20"></div>

                    <CardHeader>
                        <div className="w-12 h-1 bg-latte-400 mb-4"></div>
                        <CardTitle className="font-serif text-3xl text-latte-50 tracking-tight">
                            Espresso
                            <br />
                            Romano
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="relative z-10 space-y-4">
                        <div className="flex items-center gap-4 text-sm text-latte-200">
                            <span className="flex items-center gap-1">
                                <div className="w-2 h-2 rounded-full bg-latte-400"></div> Intense
                            </span>
                            <span className="flex items-center gap-1">
                                <div className="w-2 h-2 rounded-full bg-latte-400"></div> Citrusy
                            </span>
                        </div>
                        <p className="text-latte-300 leading-loose text-sm">
                            강렬한 에스프레소 샷에 레몬조각을 곁들여 상큼함을 더한 이탈리아 정통 스타일.
                        </p>
                    </CardContent>
                    <CardFooter className="flex justify-between items-center border-t border-latte-800 pt-6 mt-4">
                        <span className="font-serif text-2xl text-latte-400">₩ 4,500</span>
                        <Button
                            variant="outline"
                            className="border-latte-600 text-latte-200 hover:bg-latte-800 hover:text-white"
                        >
                            Order
                        </Button>
                    </CardFooter>
                </Card>

                {/* 3. The Paper Menu Card */}
                <Card className="bg-[#fcf8f5] border-2 border-dashed border-latte-300 shadow-none relative">
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 w-4 h-4 rounded-full bg-latte-200 border border-latte-300 shadow-inner"></div>
                    <CardHeader className="text-center pt-8">
                        <CardTitle className="font-serif italic text-3xl text-latte-800 decoration-latte-300 decoration-2 underline underline-offset-4">
                            Today's Pick
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="flex justify-between items-baseline border-b border-latte-200 border-dotted pb-2">
                            <span className="font-bold text-latte-800">Hand Drip</span>
                            <span className="font-mono text-latte-500">₩ 6.0</span>
                        </div>
                        <div className="flex justify-between items-baseline border-b border-latte-200 border-dotted pb-2">
                            <span className="font-bold text-latte-800">Cold Brew</span>
                            <span className="font-mono text-latte-500">₩ 5.5</span>
                        </div>
                        <div className="flex justify-between items-baseline border-b border-latte-200 border-dotted pb-2">
                            <span className="font-bold text-latte-800">Affogato</span>
                            <span className="font-mono text-latte-500">₩ 7.0</span>
                        </div>
                    </CardContent>
                    <CardFooter className="justify-center gap-4 text-latte-400">
                        <Heart className="w-5 h-5 hover:fill-latte-400 hover:text-latte-400 transition-colors cursor-pointer" />
                        <Share2 className="w-5 h-5 hover:text-latte-600 transition-colors cursor-pointer" />
                    </CardFooter>
                </Card>
            </div>
        </div>
    );
}
