'use client'

import React from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card'
import { Switch } from '@/components/ui/switch'
import { Button } from '@/components/ui/Button'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Label } from '@/components/ui/Label'
import { ArrowLeft, Bell, Moon, Volume2, Shield, CreditCard, Smartphone } from 'lucide-react'

export default function SettingsPage() {
    return (
        <div className="min-h-screen bg-latte-50 p-8 md:p-12 font-sans relative">
            {/* Back Nav */}
            <div className="absolute top-4 left-4 z-50">
                <Button asChild variant="ghost" className="text-latte-600 hover:text-latte-900 hover:bg-latte-100/50 transition-colors">
                    <Link href="/design-sample">
                        <ArrowLeft className="mr-2 h-4 w-4" /> Back to Gallery
                    </Link>
                </Button>
            </div>

            <main className="max-w-2xl mx-auto space-y-8 pt-8">
                <div className="text-center mb-8">
                    <Avatar className="w-24 h-24 mx-auto mb-4 border-4 border-white shadow-lg">
                        <AvatarImage src="/images/avatar-placeholder.png" />
                        <AvatarFallback className="bg-latte-800 text-white text-2xl font-serif">JD</AvatarFallback>
                    </Avatar>
                    <h1 className="font-serif text-3xl font-bold text-latte-900">John Doe</h1>
                    <p className="text-latte-500">Premium Member since 2023</p>
                </div>

                {/* Group 1: Preferences */}
                <Card className="bg-white border-latte-100 shadow-sm overflow-hidden">
                    <CardHeader className="bg-latte-50/50 border-b border-latte-100 pb-4">
                        <CardTitle className="text-lg font-bold text-latte-800">App Preferences</CardTitle>
                        <CardDescription>Customize your brewing experience.</CardDescription>
                    </CardHeader>
                    <CardContent className="p-0">
                        <div className="divide-y divide-latte-50">
                            <SettingItem
                                icon={Bell}
                                title="Push Notifications"
                                desc="Get alerted when your roast is ready."
                                defaultChecked={true}
                            />
                            <SettingItem
                                icon={Moon}
                                title="Dark Mode"
                                desc="Easier on the eyes for night roasting."
                                defaultChecked={false}
                            />
                            <SettingItem
                                icon={Volume2}
                                title="Sound Effects"
                                desc="Timer alerts and interaction sounds."
                                defaultChecked={true}
                            />
                        </div>
                    </CardContent>
                </Card>

                {/* Group 2: Account */}
                <Card className="bg-white border-latte-100 shadow-sm overflow-hidden">
                    <CardHeader className="bg-latte-50/50 border-b border-latte-100 pb-4">
                        <CardTitle className="text-lg font-bold text-latte-800">Privacy & Security</CardTitle>
                    </CardHeader>
                    <CardContent className="p-0">
                        <div className="divide-y divide-latte-50">
                            <SettingItem
                                icon={Shield}
                                title="2-Factor Authentication"
                                desc="Secure your account with an extra layer."
                                defaultChecked={true}
                            />
                            <SettingItem
                                icon={Smartphone}
                                title="Device Sync"
                                desc="Sync recipes across all logged devices."
                                defaultChecked={true}
                            />
                        </div>
                    </CardContent>
                </Card>

                <div className="flex justify-center pt-4">
                    <Button variant="outline" className="text-red-500 hover:text-red-600 hover:bg-red-50 border-red-100">
                        Log Out of All Devices
                    </Button>
                </div>
            </main>
        </div>
    )
}

function SettingItem({ icon: Icon, title, desc, defaultChecked }: { icon: any, title: string, desc: string, defaultChecked: boolean }) {
    return (
        <div className="flex items-center justify-between p-6 hover:bg-latte-50/30 transition-colors">
            <div className="flex items-start gap-4">
                <div className="p-2 bg-latte-50 rounded-lg text-latte-600">
                    <Icon size={20} />
                </div>
                <div>
                    <Label className="text-base font-bold text-latte-900 block mb-1">{title}</Label>
                    <span className="text-sm text-latte-500 leading-tight">{desc}</span>
                </div>
            </div>
            <Switch defaultChecked={defaultChecked} className="data-[state=checked]:bg-latte-800" />
        </div>
    )
}
