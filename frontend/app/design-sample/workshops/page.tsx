'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { Calendar } from "@/components/ui/calendar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { ArrowLeft, Clock, MapPin, Users } from 'lucide-react'

export default function WorkshopsPage() {
    const [date, setDate] = useState<Date | undefined>(new Date())

    return (
        <div className="min-h-screen bg-[#FFF8F0] px-4 py-8 md:p-12 font-sans relative">
            {/* Back Nav */}
            <div className="absolute top-4 left-4 z-50">
                <Button asChild variant="ghost" className="text-latte-600 hover:text-latte-900 hover:bg-latte-100/50 transition-colors">
                    <Link href="/design-sample">
                        <ArrowLeft className="mr-2 h-4 w-4" /> Back to Gallery
                    </Link>
                </Button>
            </div>

            <div className="max-w-6xl mx-auto pt-12 grid grid-cols-1 lg:grid-cols-12 gap-12">

                {/* Left: Calender Selection */}
                <div className="lg:col-span-4 space-y-8">
                    <div>
                        <h1 className="font-serif text-4xl text-latte-900 font-bold mb-2">Barista Class</h1>
                        <p className="text-latte-600">Select a date to book your session.</p>
                    </div>

                    <Card className="border-none shadow-xl bg-white">
                        <CardContent className="p-4 flex justify-center">
                            <Calendar
                                mode="single"
                                selected={date}
                                onSelect={setDate}
                                className="rounded-md border-none"
                            />
                        </CardContent>
                    </Card>

                    <Card className="bg-latte-900 text-latte-100 border-none relative overflow-hidden">
                        <div className="absolute top-0 right-0 w-32 h-32 bg-latte-800 rounded-bl-full opacity-50"></div>
                        <CardHeader>
                            <CardTitle className="font-serif">Master Class</CardTitle>
                            <CardDescription className="text-latte-300">Level up your pouring skills.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="flex -space-x-3 mb-4">
                                <Avatar className="border-2 border-latte-900"><AvatarImage src="/images/avatar-1.png" /><AvatarFallback>A</AvatarFallback></Avatar>
                                <Avatar className="border-2 border-latte-900"><AvatarImage src="/images/avatar-2.png" /><AvatarFallback>B</AvatarFallback></Avatar>
                                <Avatar className="border-2 border-latte-900"><AvatarImage src="/images/avatar-3.png" /><AvatarFallback>C</AvatarFallback></Avatar>
                                <div className="w-10 h-10 rounded-full bg-latte-800 flex items-center justify-center text-xs border-2 border-latte-900">+12</div>
                            </div>
                            <Button variant="outline" className="w-full border-latte-700 text-white hover:bg-latte-800 hover:text-white">View Curriculum</Button>
                        </CardContent>
                    </Card>
                </div>

                {/* Right: Available Sessions */}
                <div className="lg:col-span-8 space-y-6">
                    <h2 className="font-serif text-2xl text-latte-800 mb-6 flex items-center gap-2">
                        Available Sessions <Badge variant="secondary" className="bg-latte-200 text-latte-800">3 Spots Left</Badge>
                    </h2>

                    {/* Session Card 1 */}
                    <Card className="bg-white border-latte-100 hover:border-latte-300 transition-colors group cursor-pointer">
                        <div className="flex flex-col md:flex-row">
                            <div className="w-full md:w-48 bg-latte-100 relative min-h-[160px]">
                                <img src="/images/beans/ethiopia.png" className="w-full h-full object-cover mix-blend-multiply opacity-80" />
                                <div className="absolute top-4 left-4 bg-white/90 px-3 py-1 rounded-full text-xs font-bold text-latte-900">
                                    10:00 AM
                                </div>
                            </div>
                            <div className="flex-1 p-6 flex flex-col justify-between">
                                <div>
                                    <h3 className="font-serif text-xl font-bold text-latte-900 group-hover:text-latte-700 transition-colors">Latte Art Basics</h3>
                                    <p className="text-latte-500 text-sm mt-2 line-clamp-2">
                                        Perfect for beginners. Learn the mechanics of steaming milk and pouring hearts.
                                    </p>
                                </div>
                                <div className="flex items-center gap-6 mt-6 text-sm text-latte-600 font-medium">
                                    <span className="flex items-center gap-2"><Clock size={16} /> 2h 30m</span>
                                    <span className="flex items-center gap-2"><MapPin size={16} /> Studio A</span>
                                    <span className="flex items-center gap-2"><Users size={16} /> Max 6</span>
                                    <div className="flex-1 text-right font-bold text-lg text-latte-900">₩ 80,000</div>
                                </div>
                            </div>
                        </div>
                    </Card>

                    {/* Session Card 2 */}
                    <Card className="bg-white border-latte-100 hover:border-latte-300 transition-colors group cursor-pointer opacity-70">
                        <div className="flex flex-col md:flex-row">
                            <div className="w-full md:w-48 bg-latte-50 relative min-h-[160px]">
                                <div className="flex items-center justify-center h-full text-latte-400 font-serif italic">Sold Out</div>
                            </div>
                            <div className="flex-1 p-6 flex flex-col justify-between">
                                <div>
                                    <h3 className="font-serif text-xl font-bold text-gray-500">Sensory Cupping</h3>
                                    <p className="text-gray-400 text-sm mt-2">
                                        Advanced palate training with Q-Grader Instructor.
                                    </p>
                                </div>
                                <Button disabled variant="secondary" className="mt-4 w-fit">Join Waitlist</Button>
                            </div>
                        </div>
                    </Card>

                </div>
            </div>
        </div>
    )
}
