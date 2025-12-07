'use client'

import React from 'react'
import Link from 'next/link'
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { Button } from '@/components/ui/Button'
import { Card, CardContent } from '@/components/ui/Card'
import { Trash2, ShoppingBag, LogOut, CheckCircle2, ArrowLeft } from 'lucide-react'

export default function AlertDialogSamplePage() {
    return (
        <div className="min-h-screen bg-latte-50 p-12 font-sans flex flex-col items-center justify-center gap-16 relative">

            {/* Back Navigation */}
            <div className="absolute top-4 left-4 z-50">
                <Button asChild variant="ghost" className="text-latte-600 hover:text-latte-900 hover:bg-latte-100/50 transition-colors">
                    <Link href="/design-sample">
                        <ArrowLeft className="mr-2 h-4 w-4" /> Back to Gallery
                    </Link>
                </Button>
            </div>

            <div className="text-center space-y-4 pt-8">
                <h1 className="font-serif text-4xl text-latte-900 font-bold">Important Decisions</h1>
                <p className="text-latte-600">User confirmations styled with warmth.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full max-w-5xl">

                {/* 1. Destructive Action */}
                <Card className="bg-white border-latte-100 flex flex-col items-center justify-center text-center p-6 shadow-sm">
                    <CardContent className="space-y-6 pt-6">
                        <div className="w-16 h-16 bg-red-50 text-red-500 rounded-full flex items-center justify-center mx-auto">
                            <Trash2 size={32} />
                        </div>
                        <div>
                            <h3 className="font-bold text-latte-900 mb-1">Delete Recipe</h3>
                            <p className="text-sm text-latte-500">Remove 'My Morning Blend'?</p>
                        </div>

                        <AlertDialog>
                            <AlertDialogTrigger asChild>
                                <Button variant="destructive" className="w-full">Delete Item</Button>
                            </AlertDialogTrigger>
                            <AlertDialogContent className="bg-white border-latte-200 rounded-[2rem] shadow-2xl">
                                <AlertDialogHeader>
                                    <AlertDialogTitle className="font-serif text-2xl text-latte-900">Are you absolutely sure?</AlertDialogTitle>
                                    <AlertDialogDescription className="text-latte-600">
                                        This action cannot be undone. This will permanently delete your
                                        blending recipe from our servers.
                                    </AlertDialogDescription>
                                </AlertDialogHeader>
                                <AlertDialogFooter className="gap-2 sm:gap-0">
                                    <AlertDialogCancel className="rounded-xl border-latte-200 text-latte-700 hover:bg-latte-50 mt-0">Cancel</AlertDialogCancel>
                                    <AlertDialogAction className="bg-red-600 hover:bg-red-700 rounded-xl text-white">Delete Recipe</AlertDialogAction>
                                </AlertDialogFooter>
                            </AlertDialogContent>
                        </AlertDialog>
                    </CardContent>
                </Card>

                {/* 2. Transaction Confirmation */}
                <Card className="bg-white border-latte-100 flex flex-col items-center justify-center text-center p-6 shadow-sm">
                    <CardContent className="space-y-6 pt-6">
                        <div className="w-16 h-16 bg-latte-100 text-latte-700 rounded-full flex items-center justify-center mx-auto">
                            <ShoppingBag size={32} />
                        </div>
                        <div>
                            <h3 className="font-bold text-latte-900 mb-1">Checkout</h3>
                            <p className="text-sm text-latte-500">Total: ₩ 45,000</p>
                        </div>

                        <AlertDialog>
                            <AlertDialogTrigger asChild>
                                <Button className="w-full bg-latte-800 text-latte-50 hover:bg-latte-900">Proceed to Payment</Button>
                            </AlertDialogTrigger>
                            <AlertDialogContent className="bg-[#FFF8F0] border-latte-200 rounded-[2rem] shadow-2xl">
                                <AlertDialogHeader className="items-center text-center">
                                    <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-4">
                                        <CheckCircle2 className="text-green-600" size={24} />
                                    </div>
                                    <AlertDialogTitle className="font-serif text-2xl text-latte-900">Confirm Purchase</AlertDialogTitle>
                                    <AlertDialogDescription className="text-latte-700">
                                        You are about to purchase <strong>3 items</strong> from your cart.
                                        Proceed with the detailed transaction?
                                    </AlertDialogDescription>
                                </AlertDialogHeader>
                                <AlertDialogFooter className="sm:justify-center gap-4 mt-4">
                                    <AlertDialogCancel className="rounded-full border-none bg-transparent hover:bg-latte-200/50 text-latte-600 w-auto px-6">Modify Cart</AlertDialogCancel>
                                    <AlertDialogAction className="rounded-full bg-latte-900 hover:bg-black w-auto px-8">Confirm Payment</AlertDialogAction>
                                </AlertDialogFooter>
                            </AlertDialogContent>
                        </AlertDialog>
                    </CardContent>
                </Card>

                {/* 3. Session Info */}
                <Card className="bg-white border-latte-100 flex flex-col items-center justify-center text-center p-6 shadow-sm">
                    <CardContent className="space-y-6 pt-6">
                        <div className="w-16 h-16 bg-gray-100 text-gray-500 rounded-full flex items-center justify-center mx-auto">
                            <LogOut size={32} />
                        </div>
                        <div>
                            <h3 className="font-bold text-latte-900 mb-1">Sign Out</h3>
                            <p className="text-sm text-latte-500">End your current session</p>
                        </div>

                        <AlertDialog>
                            <AlertDialogTrigger asChild>
                                <Button variant="outline" className="w-full border-latte-200 text-latte-600">Log Out</Button>
                            </AlertDialogTrigger>
                            <AlertDialogContent className="bg-white border-latte-100 rounded-[1rem] shadow-xl max-w-sm">
                                <AlertDialogHeader>
                                    <AlertDialogTitle className="text-lg font-bold text-gray-900">Signing out?</AlertDialogTitle>
                                    <AlertDialogDescription className="text-gray-500 text-sm">
                                        We'll save your current progress automatically.
                                    </AlertDialogDescription>
                                </AlertDialogHeader>
                                <AlertDialogFooter>
                                    <AlertDialogCancel className="h-9 text-xs">Stay</AlertDialogCancel>
                                    <AlertDialogAction className="h-9 text-xs bg-gray-900 text-white">Sign Out</AlertDialogAction>
                                </AlertDialogFooter>
                            </AlertDialogContent>
                        </AlertDialog>
                    </CardContent>
                </Card>

            </div>
        </div>
    )
}
