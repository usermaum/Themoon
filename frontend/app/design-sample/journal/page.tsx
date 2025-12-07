'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Slider } from '@/components/ui/slider'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { ArrowLeft, Save, Coffee } from 'lucide-react'

export default function RoastingJournalPage() {
    return (
        <div className="min-h-screen bg-[#FDFBF7] p-8 md:p-12 font-sans relative flex justify-center">
            {/* Background Texture */}
            <div className="absolute inset-0 opacity-[0.03] pointer-events-none" style={{ backgroundImage: 'url("https://www.transparenttextures.com/patterns/paper.png")' }}></div>

            {/* Back Nav */}
            <div className="absolute top-4 left-4 z-50">
                <Button asChild variant="ghost" className="text-latte-600 hover:text-latte-900 hover:bg-latte-100/50 transition-colors">
                    <Link href="/design-sample">
                        <ArrowLeft className="mr-2 h-4 w-4" /> Back to Gallery
                    </Link>
                </Button>
            </div>

            <Card className="w-full max-w-2xl bg-white border border-latte-200 shadow-2xl relative z-10">
                <CardHeader className="bg-latte-50/50 border-b border-latte-100 pt-10 pb-6 text-center space-y-2">
                    <div className="mx-auto w-12 h-12 bg-latte-900 text-white rounded-full flex items-center justify-center mb-2 shadow-lg">
                        <Coffee size={24} />
                    </div>
                    <CardTitle className="font-serif text-3xl text-latte-900">Cupping Journal</CardTitle>
                    <CardDescription className="text-latte-500">Record the sensory details of today's roast.</CardDescription>
                </CardHeader>

                <CardContent className="p-8 space-y-8">
                    {/* Basic Info */}
                    <div className="grid grid-cols-2 gap-6">
                        <div className="space-y-2">
                            <Label htmlFor="bean-name" className="text-xs font-bold uppercase tracking-wider text-latte-400">Bean Name</Label>
                            <Input id="bean-name" placeholder="e.g. Kenya AA Top" className="border-latte-200 focus-visible:ring-latte-400 bg-latte-50/30 font-medium text-latte-800" />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="roast-date" className="text-xs font-bold uppercase tracking-wider text-latte-400">Roast Date</Label>
                            <Input id="roast-date" type="date" className="border-latte-200 focus-visible:ring-latte-400 bg-latte-50/30 text-latte-600" />
                        </div>
                    </div>

                    {/* Taste Profile Sliders */}
                    <div className="space-y-6 pt-4 border-t border-latte-50">
                        <Label className="text-lg font-serif text-latte-800">Flavor Profile</Label>

                        <TasteSlider label="Acidity" left="Flat" right="Bright" defaultValue={[60]} />
                        <TasteSlider label="Body" left="Light" right="Heavy" defaultValue={[40]} />
                        <TasteSlider label="Sweetness" left="Dry" right="Syrupy" defaultValue={[75]} />
                        <TasteSlider label="Balance" left="Wild" right="Structured" defaultValue={[50]} />
                    </div>

                    {/* Notes */}
                    <div className="space-y-2">
                        <Label htmlFor="notes" className="text-xs font-bold uppercase tracking-wider text-latte-400">Tasting Notes</Label>
                        <Textarea
                            id="notes"
                            placeholder="Describe the aroma, flavor, and finish..."
                            className="min-h-[120px] border-latte-200 focus-visible:ring-latte-400 bg-yellow-50/20 text-latte-700 leading-relaxed resize-none"
                        />
                    </div>
                </CardContent>

                <CardFooter className="bg-latte-50 border-t border-latte-100 p-6 flex justify-between items-center">
                    <span className="text-xs text-latte-400 italic">Draft saved 2 mins ago</span>
                    <Button className="bg-latte-900 hover:bg-latte-800 text-white min-w-[140px]">
                        <Save className="mr-2 h-4 w-4" /> Save Log
                    </Button>
                </CardFooter>
            </Card>
        </div>
    )
}

function TasteSlider({ label, left, right, defaultValue }: { label: string, left: string, right: string, defaultValue: number[] }) {
    return (
        <div className="space-y-3">
            <div className="flex justify-between items-end">
                <span className="text-sm font-bold text-latte-700">{label}</span>
            </div>
            <Slider defaultValue={defaultValue} max={100} step={1} className="" />
            <div className="flex justify-between text-[10px] text-latte-400 uppercase font-medium tracking-wide">
                <span>{left}</span>
                <span>{right}</span>
            </div>
        </div>
    )
}
