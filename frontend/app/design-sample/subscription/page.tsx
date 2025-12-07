'use client'

import React from 'react'
import Link from 'next/link'
import { Progress } from "@/components/ui/progress"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/Label"
import { Button } from "@/components/ui/Button"
import { Card } from "@/components/ui/Card"
import { ArrowLeft, Check, Package, Coffee, Truck } from 'lucide-react'

export default function SubscriptionPage() {
    return (
        <div className="min-h-screen bg-white font-sans relative flex flex-col">
            {/* Nav */}
            <div className="p-4 flex items-center justify-between border-b border-latte-100">
                <Button asChild variant="ghost" className="text-latte-600 hover:text-latte-900">
                    <Link href="/design-sample">
                        <ArrowLeft className="mr-2 h-4 w-4" /> Exit
                    </Link>
                </Button>
                <span className="font-serif font-bold text-latte-900">Bean Box Builder</span>
                <div className="w-24"></div>
            </div>

            <main className="flex-1 max-w-3xl mx-auto w-full p-8 md:p-12">

                {/* Progress */}
                <div className="mb-12">
                    <div className="flex justify-between text-sm font-bold text-latte-400 mb-4 uppercase tracking-wider">
                        <span className="text-latte-900">Preference</span>
                        <span>Frequency</span>
                        <span>Summary</span>
                    </div>
                    <Progress value={33} className="h-2 bg-latte-100" />
                </div>

                <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <div className="text-center mb-10">
                        <h1 className="font-serif text-3xl font-bold text-latte-900 mb-3">How do you brew?</h1>
                        <p className="text-latte-500">We'll curate the perfect roast based on your equipment.</p>
                    </div>

                    <RadioGroup defaultValue="drip" className="grid grid-cols-1 md:grid-cols-2 gap-4">

                        <Label htmlFor="drip" className="cursor-pointer [&:has([data-state=checked])]:border-latte-800 [&:has([data-state=checked])]:bg-latte-50">
                            <Card className="border-2 border-latte-100 shadow-sm hover:border-latte-300 transition-all p-6 flex items-start gap-4 h-full">
                                <RadioGroupItem value="drip" id="drip" className="mt-1" />
                                <div>
                                    <div className="font-bold text-lg text-latte-900 mb-1">Drip / Pour Over</div>
                                    <p className="text-sm text-latte-500">Paper filters, Chemex, V60. We'll send medium-light roasts.</p>
                                </div>
                            </Card>
                        </Label>

                        <Label htmlFor="espresso" className="cursor-pointer [&:has([data-state=checked])]:border-latte-800 [&:has([data-state=checked])]:bg-latte-50">
                            <Card className="border-2 border-latte-100 shadow-sm hover:border-latte-300 transition-all p-6 flex items-start gap-4 h-full">
                                <RadioGroupItem value="espresso" id="espresso" className="mt-1" />
                                <div>
                                    <div className="font-bold text-lg text-latte-900 mb-1">Espresso Machine</div>
                                    <p className="text-sm text-latte-500">High pressure extraction. We'll send developed medium-dark roasts.</p>
                                </div>
                            </Card>
                        </Label>

                        <Label htmlFor="french" className="cursor-pointer [&:has([data-state=checked])]:border-latte-800 [&:has([data-state=checked])]:bg-latte-50">
                            <Card className="border-2 border-latte-100 shadow-sm hover:border-latte-300 transition-all p-6 flex items-start gap-4 h-full">
                                <RadioGroupItem value="french" id="french" className="mt-1" />
                                <div>
                                    <div className="font-bold text-lg text-latte-900 mb-1">French Press</div>
                                    <p className="text-sm text-latte-500">Immersion brewing. Perfect for rich, full-bodied beans.</p>
                                </div>
                            </Card>
                        </Label>

                        <Label htmlFor="pods" className="cursor-pointer [&:has([data-state=checked])]:border-latte-800 [&:has([data-state=checked])]:bg-latte-50 opacity-60">
                            <Card className="border-2 border-latte-100 shadow-sm p-6 flex items-start gap-4 h-full bg-gray-50">
                                <RadioGroupItem value="pods" id="pods" className="mt-1" disabled />
                                <div>
                                    <div className="font-bold text-lg text-gray-400 mb-1">Pod Machine</div>
                                    <p className="text-sm text-gray-400">Not currently available.</p>
                                </div>
                            </Card>
                        </Label>
                    </RadioGroup>
                </div>

                <div className="mt-12 flex justify-between items-center">
                    <Button variant="ghost" className="text-latte-400">Skip Customization</Button>
                    <Button className="pl-8 pr-8 bg-latte-900 hover:bg-latte-800 h-12 rounded-full text-lg">
                        Next Step <Check className="ml-2 w-5 h-5" />
                    </Button>
                </div>
            </main>
        </div>
    )
}
