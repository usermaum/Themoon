'use client'

import React from 'react'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Badge } from '@/components/ui/Badge'
import {
    Card,
    CardHeader,
    CardTitle,
    CardDescription,
    CardContent,
    CardFooter
} from '@/components/ui/Card'
import { Coffee, Search, Bell, Plus, Trash2, Edit2 } from 'lucide-react'

export default function ComponentsDemoPage() {
    return (
        <div className="p-8 space-y-12 max-w-6xl mx-auto">
            <div className="space-y-4">
                <h1 className="text-4xl font-bold text-coffee-900">Design System Components</h1>
                <p className="text-coffee-600 text-lg">A collection of reusable components designed for The Moon Drip Bar.</p>
            </div>

            {/* Buttons Section */}
            <section className="space-y-6">
                <h2 className="text-2xl font-semibold text-coffee-800 border-b border-coffee-200 pb-2">Buttons</h2>
                <div className="flex flex-wrap gap-4 items-center">
                    <Button>Default Button</Button>
                    <Button variant="secondary">Secondary</Button>
                    <Button variant="outline">Outline</Button>
                    <Button variant="ghost">Ghost</Button>
                    <Button variant="destructive">Destructive</Button>
                    <Button variant="link">Link Button</Button>
                </div>
                <div className="flex flex-wrap gap-4 items-center">
                    <Button size="sm">Small</Button>
                    <Button size="default">Default</Button>
                    <Button size="lg">Large</Button>
                    <Button size="icon"><Plus className="w-4 h-4" /></Button>
                </div>
                <div className="flex flex-wrap gap-4 items-center">
                    <Button className="gap-2">
                        <Coffee className="w-4 h-4" />
                        With Icon
                    </Button>
                    <Button variant="outline" className="gap-2">
                        <Trash2 className="w-4 h-4" />
                        Delete
                    </Button>
                </div>
            </section>

            {/* Badges Section */}
            <section className="space-y-6">
                <h2 className="text-2xl font-semibold text-coffee-800 border-b border-coffee-200 pb-2">Badges</h2>
                <div className="flex flex-wrap gap-4">
                    <Badge>Default Badge</Badge>
                    <Badge variant="secondary">Secondary</Badge>
                    <Badge variant="outline">Outline</Badge>
                    <Badge variant="destructive">Destructive</Badge>
                </div>
            </section>

            {/* Inputs Section */}
            <section className="space-y-6">
                <h2 className="text-2xl font-semibold text-coffee-800 border-b border-coffee-200 pb-2">Inputs</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl">
                    <div className="space-y-2">
                        <label className="text-sm font-medium text-coffee-700">Default Input</label>
                        <Input placeholder="Type something..." />
                    </div>
                    <div className="space-y-2">
                        <label className="text-sm font-medium text-coffee-700">Disabled Input</label>
                        <Input disabled placeholder="Cannot type here" />
                    </div>
                    <div className="space-y-2">
                        <label className="text-sm font-medium text-coffee-700">With Icon (Simulated)</label>
                        <div className="relative">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-coffee-400" />
                            <Input className="pl-9" placeholder="Search..." />
                        </div>
                    </div>
                </div>
            </section>

            {/* Cards Section */}
            <section className="space-y-6">
                <h2 className="text-2xl font-semibold text-coffee-800 border-b border-coffee-200 pb-2">Cards</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Card Title</CardTitle>
                            <CardDescription>Card Description goes here.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <p className="text-coffee-700">This is the main content of the card. It has a white background and a subtle shadow.</p>
                        </CardContent>
                        <CardFooter>
                            <Button className="w-full">Action</Button>
                        </CardFooter>
                    </Card>

                    <Card>
                        <div className="h-32 bg-coffee-100 relative">
                            <div className="absolute inset-0 flex items-center justify-center text-coffee-300">
                                <Coffee className="w-12 h-12" />
                            </div>
                        </div>
                        <CardHeader>
                            <CardTitle>Product Card</CardTitle>
                            <CardDescription>Coffee Bean</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="flex justify-between items-center mb-2">
                                <Badge variant="secondary">Light Roast</Badge>
                                <span className="font-bold text-coffee-900">$18.00</span>
                            </div>
                            <p className="text-sm text-coffee-600">Notes of jasmine, citrus, and bergamot.</p>
                        </CardContent>
                        <CardFooter className="gap-2">
                            <Button variant="outline" className="flex-1">Details</Button>
                            <Button className="flex-1">Add</Button>
                        </CardFooter>
                    </Card>

                    <Card className="bg-coffee-900 text-coffee-50 border-coffee-800">
                        <CardHeader>
                            <CardTitle className="text-coffee-50">Dark Card</CardTitle>
                            <CardDescription className="text-coffee-300">For special emphasis</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <p className="text-coffee-200">This card uses the dark theme colors directly via className overrides.</p>
                        </CardContent>
                        <CardFooter>
                            <Button variant="secondary" className="w-full">Dark Action</Button>
                        </CardFooter>
                    </Card>
                </div>
            </section>
        </div>
    )
}
