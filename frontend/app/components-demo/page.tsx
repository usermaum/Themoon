'use client'

import React from 'react'
import PageHero from '@/components/ui/PageHero'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Badge } from '@/components/ui/Badge'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/Card'
import { Label } from '@/components/ui/Label'
import { Textarea } from '@/components/ui/Textarea'
import { Coffee, Palette, Package, Plus, Trash2, Edit2, Search, Check, Mail, ArrowRight } from 'lucide-react'

export default function ComponentsDemoPage() {
    return (
        <div className="min-h-screen pb-20">
            <PageHero
                title="Design System"
                description="Cafe Latte Art 테마 디자인 시스템 컴포넌트 가이드"
                icon={<Palette />}
                image="/images/hero/home-hero.png"
                className="mb-12"
            />

            <div className="container mx-auto px-4 space-y-20">

                {/* 1. Typography & Colors */}
                <section className="space-y-6">
                    <h2 className="text-3xl font-serif font-bold text-latte-900 border-b border-latte-200 pb-4">
                        1. Colors & Typography
                    </h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <Card>
                            <CardHeader>
                                <CardTitle>Color Palette (Latte)</CardTitle>
                                <CardDescription>따뜻한 커피 톤의 메인 컬러 팔레트입니다.</CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-2">
                                <div className="flex items-center gap-4"><div className="w-16 h-16 rounded-lg bg-latte-50 shadow-sm border border-latte-100"></div> <span className="font-mono">latte-50 (Background)</span></div>
                                <div className="flex items-center gap-4"><div className="w-16 h-16 rounded-lg bg-latte-100"></div> <span className="font-mono">latte-100 (Secondary BG)</span></div>
                                <div className="flex items-center gap-4"><div className="w-16 h-16 rounded-lg bg-latte-200"></div> <span className="font-mono">latte-200 (Border)</span></div>
                                <div className="flex items-center gap-4"><div className="w-16 h-16 rounded-lg bg-latte-400"></div> <span className="font-mono">latte-400 (Accent)</span></div>
                                <div className="flex items-center gap-4"><div className="w-16 h-16 rounded-lg bg-latte-600"></div> <span className="font-mono">latte-600 (Text Muted)</span></div>
                                <div className="flex items-center gap-4"><div className="w-16 h-16 rounded-lg bg-latte-800"></div> <span className="font-mono">latte-800 (Primary)</span></div>
                                <div className="flex items-center gap-4"><div className="w-16 h-16 rounded-lg bg-latte-900"></div> <span className="font-mono">latte-900 (Text Main)</span></div>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <CardTitle>Typography</CardTitle>
                                <CardDescription>Playfair Display (Serif) & Inter (Sans)</CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                <div>
                                    <h1 className="text-4xl font-serif font-bold text-latte-900">Heading 1 (Serif)</h1>
                                    <p className="text-sm text-latte-500">Playfair Display / Bold / 4xl</p>
                                </div>
                                <div>
                                    <h2 className="text-3xl font-serif font-bold text-latte-900">Heading 2 (Serif)</h2>
                                    <p className="text-sm text-latte-500">Playfair Display / Bold / 3xl</p>
                                </div>
                                <div>
                                    <h3 className="text-2xl font-bold text-latte-900">Heading 3 (Sans)</h3>
                                    <p className="text-sm text-latte-500">Inter / Bold / 2xl</p>
                                </div>
                                <div>
                                    <p className="text-base text-latte-700 leading-relaxed">
                                        Body text example. The quick brown fox jumps over the lazy dog.
                                        본문 텍스트 예시입니다. 가독성을 위해 적절한 줄간격과 색상을 사용합니다.
                                    </p>
                                    <p className="text-sm text-latte-500 mt-1">Inter / Regular / base</p>
                                </div>
                            </CardContent>
                        </Card>
                    </div>
                </section>

                {/* 2. Buttons */}
                <section className="space-y-6">
                    <h2 className="text-3xl font-serif font-bold text-latte-900 border-b border-latte-200 pb-4">
                        2. Buttons
                    </h2>
                    <Card>
                        <CardContent className="p-8 space-y-8">
                            <div className="flex flex-wrap gap-4 items-center">
                                <Button>Default Button</Button>
                                <Button variant="secondary">Secondary</Button>
                                <Button variant="outline">Outline</Button>
                                <Button variant="ghost">Ghost</Button>
                                <Button variant="destructive">Destructive</Button>
                                <Button variant="link">Link Style</Button>
                            </div>

                            <div className="flex flex-wrap gap-4 items-center">
                                <Button size="lg">Large Button</Button>
                                <Button>Default Size</Button>
                                <Button size="sm">Small</Button>
                                <Button size="icon"><Plus className="w-4 h-4" /></Button>
                            </div>

                            <div className="flex flex-wrap gap-4 items-center">
                                <Button className="bg-latte-800"><Coffee className="mr-2 w-4 h-4" /> With Icon</Button>
                                <Button variant="outline"><Trash2 className="mr-2 w-4 h-4" /> Delete</Button>
                                <Button variant="secondary">Next Step <ArrowRight className="ml-2 w-4 h-4" /></Button>
                            </div>

                            <div className="flex flex-wrap gap-4 items-center">
                                <Button disabled>Disabled</Button>
                                <Button disabled variant="secondary">Disabled</Button>
                                <Button disabled variant="outline">Disabled</Button>
                            </div>
                        </CardContent>
                    </Card>
                </section>

                {/* 3. Badges */}
                <section className="space-y-6">
                    <h2 className="text-3xl font-serif font-bold text-latte-900 border-b border-latte-200 pb-4">
                        3. Badges
                    </h2>
                    <Card>
                        <CardContent className="p-8 flex flex-wrap gap-4">
                            <Badge>Default Badge</Badge>
                            <Badge variant="secondary">Secondary</Badge>
                            <Badge variant="outline">Outline</Badge>
                            <Badge variant="destructive">Destructive</Badge>
                            <Badge className="bg-blob-orange text-latte-900 hover:bg-blob-orange/80">Custom (Orange)</Badge>
                            <Badge className="bg-blob-green text-latte-900 hover:bg-blob-green/80">Custom (Green)</Badge>
                        </CardContent>
                    </Card>
                </section>

                {/* 4. Inputs & Forms */}
                <section className="space-y-6">
                    <h2 className="text-3xl font-serif font-bold text-latte-900 border-b border-latte-200 pb-4">
                        4. Inputs & Forms
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <Card>
                            <CardHeader>
                                <CardTitle>Input Fields</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="space-y-2">
                                    <Label htmlFor="email">Email</Label>
                                    <div className="relative">
                                        <Search className="absolute left-3 top-3 h-4 w-4 text-latte-400" />
                                        <Input id="search" placeholder="Search..." className="pl-9" />
                                    </div>
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="username">Username</Label>
                                    <Input id="username" placeholder="Enter username" />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="disabled">Disabled Input</Label>
                                    <Input id="disabled" disabled placeholder="Cannot type here" />
                                </div>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <CardTitle>Text Area & Select</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="space-y-2">
                                    <Label htmlFor="message">Message</Label>
                                    <Textarea id="message" placeholder="Type your message here..." />
                                </div>
                            </CardContent>
                        </Card>
                    </div>
                </section>

                {/* 5. Cards */}
                <section className="space-y-6">
                    <h2 className="text-3xl font-serif font-bold text-latte-900 border-b border-latte-200 pb-4">
                        5. Cards
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <Card className="hover:shadow-lg transition-all duration-300">
                            <CardHeader>
                                <CardTitle>Interactive Card</CardTitle>
                                <CardDescription>Hover me to see the effect</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <p>Cards have a subtle border and shadow in the Latte theme. This one elevates on hover.</p>
                            </CardContent>
                            <CardFooter>
                                <Button className="w-full">Action</Button>
                            </CardFooter>
                        </Card>

                        <Card className="bg-latte-900 text-white border-none">
                            <CardHeader>
                                <CardTitle className="text-white">Dark Card</CardTitle>
                                <CardDescription className="text-latte-200">Used for emphasis</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <p>Some components can be inverted for dark styling within the light theme.</p>
                            </CardContent>
                            <CardFooter>
                                <Button variant="secondary" className="w-full">Action</Button>
                            </CardFooter>
                        </Card>

                        <Card>
                            <div className="h-40 bg-latte-200 flex items-center justify-center">
                                <Coffee className="w-12 h-12 text-latte-400" />
                            </div>
                            <CardHeader>
                                <CardTitle>Image Card</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p>Cards can contain images or media areas at the top.</p>
                            </CardContent>
                        </Card>
                    </div>
                </section>

            </div>
        </div>
    )
}
