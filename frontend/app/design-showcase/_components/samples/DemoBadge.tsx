'use client';

import React from 'react';
import Link from 'next/link';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Leaf, Flame, Droplets, Star, ArrowLeft } from 'lucide-react';

export function DemoBadge() {
    return (
        <div className="min-h-screen bg-[#FDFBF7] p-12 font-sans flex flex-col items-center justify-center gap-12 relative">
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

            <div className="text-center space-y-2 pt-8">
                <h1 className="font-serif text-4xl text-latte-900 font-bold">Coffee Tags & Badges</h1>
                <p className="text-latte-500 italic">Small details, rich flavor.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-4xl">
                {/* 1. Roast Levels */}
                <Card className="bg-white border-latte-100 shadow-sm">
                    <CardContent className="p-8 space-y-6">
                        <h3 className="font-serif text-xl text-latte-800 border-b border-latte-100 pb-2 mb-4">
                            Roast Levels
                        </h3>

                        <div className="flex flex-wrap gap-3 items-center">
                            <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-200 border-yellow-200 px-3 py-1 text-sm font-medium rounded-full">
                                <Leaf className="w-3 h-3 mr-1" /> Light
                            </Badge>
                            <Badge className="bg-orange-100 text-orange-800 hover:bg-orange-200 border-orange-200 px-3 py-1 text-sm font-medium rounded-full">
                                <Flame className="w-3 h-3 mr-1" /> Medium
                            </Badge>
                            <Badge className="bg-stone-800 text-stone-100 hover:bg-black border-stone-700 px-3 py-1 text-sm font-medium rounded-full">
                                <Droplets className="w-3 h-3 mr-1" /> Dark
                            </Badge>
                        </div>
                        <p className="text-xs text-latte-400">Standard roast classification tags.</p>
                    </CardContent>
                </Card>

                {/* 2. Flavor Notes (Pill Style) */}
                <Card className="bg-latte-50 border-none shadow-inner">
                    <CardContent className="p-8 space-y-6">
                        <h3 className="font-serif text-xl text-latte-800 border-b border-latte-200/50 pb-2 mb-4">
                            Flavor Notes
                        </h3>

                        <div className="flex flex-wrap gap-2">
                            <Badge
                                variant="outline"
                                className="border-latte-400 text-latte-700 bg-white hover:bg-latte-100 rounded-lg px-3"
                            >
                                Chocolate
                            </Badge>
                            <Badge
                                variant="outline"
                                className="border-latte-400 text-latte-700 bg-white hover:bg-latte-100 rounded-lg px-3"
                            >
                                Nutty
                            </Badge>
                            <Badge
                                variant="outline"
                                className="border-pink-300 text-pink-700 bg-white hover:bg-pink-50 rounded-lg px-3"
                            >
                                Berry
                            </Badge>
                            <Badge
                                variant="outline"
                                className="border-orange-300 text-orange-700 bg-white hover:bg-orange-50 rounded-lg px-3"
                            >
                                Citrus
                            </Badge>
                        </div>
                    </CardContent>
                </Card>

                {/* 3. Status Indicators */}
                <Card className="bg-white border-latte-100 shadow-md transform rotate-1">
                    <CardContent className="p-8 space-y-6">
                        <h3 className="font-serif text-xl text-latte-800 mb-4">Inventory Status</h3>

                        <div className="space-y-3">
                            <div className="flex justify-between items-center">
                                <span className="text-latte-600">Ethiopia Yirgacheffe</span>
                                <Badge className="bg-green-100 text-green-700 hover:bg-green-100 shadow-none">
                                    In Stock
                                </Badge>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="text-latte-600">Kenya AA</span>
                                <Badge className="bg-red-50 text-red-600 hover:bg-red-50 border border-red-100 shadow-none">
                                    Low Stock
                                </Badge>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="text-latte-600">Guatemala Antigua</span>
                                <Badge variant="secondary" className="bg-gray-100 text-gray-500">
                                    Out of Stock
                                </Badge>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                {/* 4. Special Tags */}
                <Card className="bg-gradient-to-br from-latte-800 to-latte-900 border-none text-white overflow-hidden relative">
                    <div className="absolute top-0 right-0 w-24 h-24 bg-latte-700 rounded-bl-full opacity-50"></div>
                    <CardContent className="p-8 space-y-6 relative z-10">
                        <h3 className="font-serif text-xl text-latte-100 mb-4">Premium Selection</h3>

                        <div className="flex flex-wrap gap-3">
                            <Badge className="bg-gradient-to-r from-yellow-400 to-yellow-600 text-white border-none shadow-lg px-4 py-1">
                                <Star className="w-3 h-3 mr-1 fill-white" /> Signature
                            </Badge>
                            <Badge className="bg-transparent border border-white/30 text-latte-100 hover:bg-white/10 backdrop-blur-sm">
                                Limited Edition
                            </Badge>
                            <Badge className="bg-latte-500/50 text-latte-50 hover:bg-latte-500/70 border-none">
                                New Arrival
                            </Badge>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
