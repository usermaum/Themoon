'use client'

import React from 'react'
import Link from 'next/link'
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { ArrowLeft, Coffee, Facebook, Instagram, Twitter } from 'lucide-react'

export default function AuthPage() {
    return (
        <div className="min-h-screen grid grid-cols-1 lg:grid-cols-2 font-sans bg-white">
            {/* Back Nav */}
            <div className="absolute top-4 left-4 z-50 lg:text-white">
                <Button asChild variant="ghost" className="hover:bg-white/20 transition-colors">
                    <Link href="/design-sample">
                        <ArrowLeft className="mr-2 h-4 w-4" /> Back to Gallery
                    </Link>
                </Button>
            </div>

            {/* Left: Banner */}
            <div className="hidden lg:flex flex-col justify-between p-12 bg-latte-900 text-white relative overflow-hidden">
                <div className="absolute inset-0 bg-[url('/images/beans/ethiopia.png')] bg-cover opacity-20 mix-blend-overlay"></div>
                <div className="relative z-10">
                    <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center text-latte-900 mb-8">
                        <Coffee size={24} />
                    </div>
                    <h1 className="font-serif text-5xl font-bold leading-tight mb-4">
                        Brewing<br />Community
                    </h1>
                    <p className="text-latte-200 text-lg max-w-md">
                        Join 15,000+ coffee lovers tracking their daily roasts and sharing recipes.
                    </p>
                </div>
                <div className="relative z-10 text-latte-400 text-sm">
                    © 2024 The Moon Roastery. All rights reserved.
                </div>
            </div>

            {/* Right: Form */}
            <div className="flex items-center justify-center p-8 lg:p-24 bg-latte-50">
                <Card className="w-full max-w-md border-none shadow-xl bg-white/80 backdrop-blur-sm">
                    <CardContent className="p-8 space-y-8">
                        <div className="text-center space-y-2">
                            <h2 className="text-2xl font-bold text-latte-900">Welcome Back</h2>
                            <p className="text-latte-500">Enter your credentials to access your lab.</p>
                        </div>

                        <div className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="email">Email</Label>
                                <Input id="email" type="email" placeholder="barista@themoon.com" className="bg-white border-latte-200" />
                            </div>
                            <div className="space-y-2">
                                <div className="flex justify-between items-center">
                                    <Label htmlFor="password">Password</Label>
                                    <span className="text-xs text-latte-600 hover:underline cursor-pointer">Forgot password?</span>
                                </div>
                                <Input id="password" type="password" className="bg-white border-latte-200" />
                            </div>

                            <div className="flex items-center space-x-2">
                                <Checkbox id="remember" className="border-latte-300 text-latte-900 data-[state=checked]:bg-latte-900 data-[state=checked]:border-latte-900" />
                                <label
                                    htmlFor="remember"
                                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-latte-600"
                                >
                                    Remember me for 30 days
                                </label>
                            </div>
                        </div>

                        <Button className="w-full bg-latte-900 hover:bg-latte-800 text-white h-11 text-base">Sign In</Button>

                        <div className="relative">
                            <div className="absolute inset-0 flex items-center">
                                <span className="w-full border-t border-latte-200" />
                            </div>
                            <div className="relative flex justify-center text-xs uppercase">
                                <span className="bg-white px-2 text-latte-400">Or continue with</span>
                            </div>
                        </div>

                        <div className="flex gap-4 justify-center">
                            <Button variant="outline" size="icon" className="rounded-full border-latte-200 text-latte-600 hover:bg-latte-50"><Instagram size={18} /></Button>
                            <Button variant="outline" size="icon" className="rounded-full border-latte-200 text-latte-600 hover:bg-latte-50"><Facebook size={18} /></Button>
                            <Button variant="outline" size="icon" className="rounded-full border-latte-200 text-latte-600 hover:bg-latte-50"><Twitter size={18} /></Button>
                        </div>

                        <p className="text-center text-sm text-latte-500">
                            Don't have an account? <span className="text-latte-900 font-bold hover:underline cursor-pointer">Sign up</span>
                        </p>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
