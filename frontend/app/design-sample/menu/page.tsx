'use client'

import React from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { Badge } from '@/components/ui/Badge'
import { ArrowLeft, Info, Plus } from 'lucide-react'

export default function MenuPage() {
    return (
        <div className="min-h-screen bg-[#FFF8F0] p-8 font-sans relative">
            {/* Back Nav */}
            <div className="absolute top-4 left-4 z-50">
                <Button asChild variant="ghost" className="text-latte-600 hover:text-latte-900 hover:bg-latte-100/50 transition-colors">
                    <Link href="/design-sample">
                        <ArrowLeft className="mr-2 h-4 w-4" /> Back to Gallery
                    </Link>
                </Button>
            </div>

            <div className="max-w-5xl mx-auto pt-16 pb-20">
                <div className="text-center mb-16">
                    <span className="text-xs font-bold text-latte-500 uppercase tracking-[0.3em] mb-2 block">Premium Selection</span>
                    <h1 className="font-serif text-5xl font-bold text-latte-900 mb-6">Seasonal Menu</h1>
                    <div className="w-24 h-1 bg-latte-300 mx-auto rounded-full"></div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <MenuItem
                        name="Honey Cold Brew"
                        price="6.5"
                        image="/images/beans/colombia.png" // Using placeholder beans image for demo
                        desc="Slow-steeped brew infused with organic wildflower honey and a splash of oat milk."
                        calories="120"
                        caffeine="High"
                    />
                    <MenuItem
                        name="Matcha Latte"
                        price="5.5"
                        image="/images/beans/brazil.png"
                        desc="Ceremonial grade matcha whisked to perfection with silky steamed milk."
                        calories="180"
                        caffeine="Medium"
                    />
                    <MenuItem
                        name="Espresso Tonic"
                        price="6.0"
                        image="/images/beans/ethiopia.png"
                        desc="Double shot of espresso over ice and premium tonic water, garnished with rosemary."
                        calories="45"
                        caffeine="High"
                    />
                    <MenuItem
                        name="Caramel Macchiato"
                        price="5.8"
                        image="/images/beans/guatemala.png"
                        desc="Vanilla syrup, steamed milk, espresso, and caramel drizzle."
                        calories="250"
                        caffeine="Medium"
                    />
                    <MenuItem
                        name="Flat White"
                        price="5.0"
                        image="/images/beans/kenya.png"
                        desc="Espresso with micro-foam. Smooth texture, strong coffee flavor."
                        calories="110"
                        caffeine="High"
                    />
                    <MenuItem
                        name="Affogato"
                        price="7.0"
                        image="/images/beans/sumatra.png"
                        desc="A scoop of vanilla bean gelato drowned in a hot shot of espresso."
                        calories="190"
                        caffeine="Medium"
                    />
                </div>
            </div>
        </div>
    )
}

function MenuItem({ name, price, image, desc, calories, caffeine }: { name: string, price: string, image: string, desc: string, calories: string, caffeine: string }) {
    return (
        <Card className="bg-white border-none shadow-lg hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 overflow-hidden group">
            <div className="h-48 relative overflow-hidden bg-latte-100">
                <img src={image} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 mix-blend-multiply opacity-80" />
                <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-md px-3 py-1 rounded-full text-sm font-bold text-latte-900 shadow-sm">
                    ${price}
                </div>
            </div>

            <div className="p-6">
                <div className="flex justify-between items-start mb-2">
                    <h3 className="font-serif text-xl font-bold text-latte-900">{name}</h3>

                    {/* Info Popover */}
                    <Popover>
                        <PopoverTrigger asChild>
                            <Button size="icon" variant="ghost" className="h-6 w-6 text-latte-400 hover:text-latte-600">
                                <Info size={16} />
                            </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-64 bg-latte-900 text-latte-50 border-none shadow-xl">
                            <div className="space-y-2">
                                <h4 className="font-bold text-sm border-b border-latte-700 pb-1 mb-2">Nutritional Info</h4>
                                <div className="flex justify-between text-xs">
                                    <span className="text-latte-300">Calories</span>
                                    <span>{calories} kcal</span>
                                </div>
                                <div className="flex justify-between text-xs">
                                    <span className="text-latte-300">Caffeine</span>
                                    <span>{caffeine}</span>
                                </div>
                                <div className="flex justify-between text-xs">
                                    <span className="text-latte-300">Allergens</span>
                                    <span>Milk, Soy</span>
                                </div>
                            </div>
                        </PopoverContent>
                    </Popover>
                </div>

                <p className="text-sm text-latte-500 leading-relaxed mb-6 h-12 line-clamp-2">
                    {desc}
                </p>

                <Button className="w-full bg-latte-100 text-latte-900 hover:bg-latte-200 border border-latte-200 shadow-none font-bold group/btn">
                    <Plus size={16} className="mr-2 group-hover/btn:rotate-90 transition-transform" /> Add to Order
                </Button>
            </div>
        </Card>
    )
}
