'use client'

import React from 'react'
import Link from 'next/link'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Coffee, Cake, ShoppingBag, ArrowLeft } from 'lucide-react'

export default function TabsSamplePage() {
    return (
        <div className="min-h-screen bg-latte-50 p-8 md:p-12 font-sans flex flex-col items-center justify-center gap-12 relative">

            {/* Back Navigation */}
            <div className="absolute top-4 left-4 z-50">
                <Button asChild variant="ghost" className="text-latte-600 hover:text-latte-900 hover:bg-latte-100/50 transition-colors">
                    <Link href="/design-sample">
                        <ArrowLeft className="mr-2 h-4 w-4" /> Back to Gallery
                    </Link>
                </Button>
            </div>

            <div className="text-center space-y-2 pt-8">
                <h1 className="font-serif text-4xl text-latte-900 font-bold">Menu Categories</h1>
                <p className="text-latte-600">Switch between brew and sweet delights.</p>
            </div>

            <div className="w-full max-w-3xl">

                {/* Custom Styled Tabs */}
                <Tabs defaultValue="coffee" className="w-full">

                    <div className="flex justify-center mb-8">
                        <TabsList className="bg-latte-200/50 p-1 rounded-full border border-latte-200 shadow-sm relative overflow-hidden">
                            <TabsTrigger
                                value="coffee"
                                className="rounded-full px-8 py-2.5 text-sm font-medium transition-all data-[state=active]:bg-white data-[state=active]:text-latte-900 data-[state=active]:shadow-md text-latte-600 hover:text-latte-800"
                            >
                                <Coffee className="w-4 h-4 mr-2" /> Coffee
                            </TabsTrigger>
                            <TabsTrigger
                                value="dessert"
                                className="rounded-full px-8 py-2.5 text-sm font-medium transition-all data-[state=active]:bg-white data-[state=active]:text-latte-900 data-[state=active]:shadow-md text-latte-600 hover:text-latte-800"
                            >
                                <Cake className="w-4 h-4 mr-2" /> Dessert
                            </TabsTrigger>
                            <TabsTrigger
                                value="beans"
                                className="rounded-full px-8 py-2.5 text-sm font-medium transition-all data-[state=active]:bg-white data-[state=active]:text-latte-900 data-[state=active]:shadow-md text-latte-600 hover:text-latte-800"
                            >
                                <ShoppingBag className="w-4 h-4 mr-2" /> Beans
                            </TabsTrigger>
                        </TabsList>
                    </div>

                    {/* Content 1: Coffee */}
                    <TabsContent value="coffee" className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <MenuItem
                                title="Signature Latte"
                                desc="Rich espresso with velvety steamed milk."
                                price="5.5"
                                tags={['Hot', 'Iced']}
                            />
                            <MenuItem
                                title="Cold Brew"
                                desc="Slow-steeped for 12 hours, smooth finish."
                                price="6.0"
                                tags={['Iced Only']}
                            />
                        </div>
                    </TabsContent>

                    {/* Content 2: Dessert */}
                    <TabsContent value="dessert" className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <MenuItem
                                title="Tiramisu"
                                desc="Espresso-soaked ladyfingers with mascarpone."
                                price="7.5"
                                tags={['Contains Dairy']}
                            />
                            <MenuItem
                                title="Croissant"
                                desc="Buttery, flaky, and freshly baked."
                                price="4.0"
                                tags={['Bakery']}
                            />
                        </div>
                    </TabsContent>

                    {/* Content 3: Beans */}
                    <TabsContent value="beans" className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <Card className="bg-white border-latte-100">
                            <CardHeader>
                                <CardTitle className="font-serif text-latte-900">Weekly Subscription</CardTitle>
                                <CardDescription>Get fresh beans delivered to your door.</CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <p className="text-latte-700 text-sm leading-relaxed">
                                    Choose your roast preference and frequency. We curate the best beans from around the world just for you.
                                </p>
                            </CardContent>
                            <CardFooter>
                                <Button className="w-full bg-latte-800 hover:bg-latte-900">Subscribe Now</Button>
                            </CardFooter>
                        </Card>
                    </TabsContent>
                </Tabs>
            </div>
        </div>
    )
}

function MenuItem({ title, desc, price, tags }: { title: string, desc: string, price: string, tags: string[] }) {
    return (
        <Card className="border border-latte-100 bg-white hover:border-latte-300 transition-colors shadow-sm hover:shadow-md cursor-pointer group">
            <CardHeader className="pb-3">
                <div className="flex justify-between items-start">
                    <CardTitle className="text-lg font-serif text-latte-900 group-hover:text-latte-600 transition-colors">{title}</CardTitle>
                    <span className="font-mono text-latte-700 font-bold">${price}</span>
                </div>
                <CardDescription className="text-latte-500 line-clamp-2">{desc}</CardDescription>
            </CardHeader>
            <CardFooter className="pt-0">
                <div className="flex gap-2">
                    {tags.map(tag => (
                        <span key={tag} className="text-[10px] bg-latte-50 text-latte-600 px-2 py-1 rounded-full uppercase tracking-wide font-medium">
                            {tag}
                        </span>
                    ))}
                </div>
            </CardFooter>
        </Card>
    )
}
