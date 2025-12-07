'use client'

import React from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import {
    ArrowRight,
    Layout,
    MousePointerClick,
    Tag,
    SquareStack,
    AlertTriangle,
    Coffee,
    LayoutDashboard,
    BookOpen,
    Map,
    Settings,
    Utensils,
    CalendarDays,
    PackageCheck,
    ScrollText,
    Users,
    LockKeyhole
} from 'lucide-react'

// Section 1: Components
const components = [
    {
        title: "Card",
        desc: "Product displays, menu items, and rich content containers.",
        href: "/design-sample/card",
        icon: Layout,
        preview: "Latte, Espresso, Paper Menu Styles",
        color: "text-amber-700 bg-amber-50"
    },
    {
        title: "Button",
        desc: "Interactive elements for actions, navigation, and triggers.",
        href: "/design-sample/button",
        icon: MousePointerClick,
        preview: "Primary, Secondary, Icon Buttons",
        color: "text-blue-700 bg-blue-50"
    },
    {
        title: "Badge",
        desc: "Status indicators, labels, and categorization tags.",
        href: "/design-sample/badge",
        icon: Tag,
        preview: "Roast Level, Flavors, Stock Status",
        color: "text-green-700 bg-green-50"
    },
    {
        title: "Tabs",
        desc: "Content organization and switching between different views.",
        href: "/design-sample/tabs",
        icon: SquareStack,
        preview: "Menu Categories, Subscriptions",
        color: "text-purple-700 bg-purple-50"
    },
    {
        title: "Alert Dialog",
        desc: "Modal dialogs for important confirmations and warnings.",
        href: "/design-sample/alert-dialog",
        icon: AlertTriangle,
        preview: "Delete, Checkout, Logout Confirmations",
        color: "text-red-700 bg-red-50"
    }
]

// Section 2: Scenarios (Original)
const scenarios = [
    {
        title: "Dashboard",
        desc: "Barista morning overview with stats and switches.",
        href: "/design-sample/dashboard",
        icon: LayoutDashboard,
        preview: "Stats, Switch, Avatar, Notifications",
        color: "text-orange-700 bg-orange-50"
    },
    {
        title: "Roast Journal",
        desc: "Detailed input form for cupping notes.",
        href: "/design-sample/journal",
        icon: BookOpen,
        preview: "Slider, Input, Textarea, Form Layout",
        color: "text-stone-700 bg-stone-50"
    },
    {
        title: "Bean Origins",
        desc: "Storytelling page with expandable details.",
        href: "/design-sample/origins",
        icon: Map,
        preview: "Accordion, Split Layout, Hero Image",
        color: "text-emerald-700 bg-emerald-50"
    },
    {
        title: "Settings",
        desc: "User preferences and account management.",
        href: "/design-sample/settings",
        icon: Settings,
        preview: "Switch, Avatar, List Groups",
        color: "text-slate-700 bg-slate-50"
    },
    {
        title: "Seasonal Menu",
        desc: "Visual menu grid with detailed popovers.",
        href: "/design-sample/menu",
        icon: Utensils,
        preview: "Popover, Grid, Rich Cards",
        color: "text-pink-700 bg-pink-50"
    }
]

// Section 3: New Scenarios (Extended)
const extended = [
    {
        title: "Workshops",
        desc: "Class booking system with calendar integration.",
        href: "/design-sample/workshops",
        icon: CalendarDays,
        preview: "Calendar, Grid Layout, Booking Status",
        color: "text-indigo-700 bg-indigo-50"
    },
    {
        title: "Subscription",
        desc: "Multi-step wizard for building custom bean orders.",
        href: "/design-sample/subscription",
        icon: PackageCheck,
        preview: "Progress, Radio Group, Wizard Flow",
        color: "text-cyan-700 bg-cyan-50"
    },
    {
        title: "Order History",
        desc: "Data tables for managing coffee orders and invoices.",
        href: "/design-sample/orders",
        icon: ScrollText,
        preview: "Table, Filters, Badge, Select",
        color: "text-gray-700 bg-gray-50"
    },
    {
        title: "Guest Book",
        desc: "Community reviews in a masonry layout.",
        href: "/design-sample/reviews",
        icon: Users,
        preview: "Masonry Cards, Avatar, Ratings",
        color: "text-yellow-700 bg-yellow-50"
    },
    {
        title: "Member Login",
        desc: "Aesthetic authentication page split layout.",
        href: "/design-sample/auth",
        icon: LockKeyhole,
        preview: "Form, Checkbox, Split Screen",
        color: "text-rose-700 bg-rose-50"
    },
    {
        title: "The Green Bean Vault",
        desc: "Concept page for raw material inventory.",
        href: "/design-sample/green-bean-vault",
        icon: Map,
        preview: "Texture Sidebar, Hero Overlay, Inventory Cards",
        color: "text-emerald-800 bg-emerald-100"
    }
]

export default function DesignSampleIndexPage() {
    return (
        <div className="min-h-screen bg-[#FFF8F0] p-8 md:p-12 font-sans">
            <div className="max-w-6xl mx-auto space-y-16">

                {/* Header */}
                <header className="text-center space-y-4">
                    <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-latte-900 text-latte-50 mb-4 shadow-lg">
                        <Coffee size={32} />
                    </div>
                    <h1 className="font-serif text-5xl font-bold text-latte-900">Design System</h1>
                    <p className="text-lg text-latte-600 max-w-2xl mx-auto">
                        Cafe Latte Art Theme Gallery<br />
                        <span className="text-sm opacity-70">A complete collection of components and real-world scenarios.</span>
                    </p>
                </header>

                {/* Section 1: Components */}
                <section>
                    <div className="flex items-center gap-4 mb-8">
                        <div className="h-px flex-1 bg-latte-200"></div>
                        <h2 className="text-xl font-bold text-latte-400 uppercase tracking-widest">Base Components</h2>
                        <div className="h-px flex-1 bg-latte-200"></div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {components.map((sample) => (
                            <SampleCard key={sample.title} sample={sample} />
                        ))}
                    </div>
                </section>

                {/* Section 2: Scenarios */}
                <section>
                    <div className="flex items-center gap-4 mb-8">
                        <div className="h-px flex-1 bg-latte-200"></div>
                        <h2 className="text-xl font-bold text-latte-400 uppercase tracking-widest">Core Scenarios</h2>
                        <div className="h-px flex-1 bg-latte-200"></div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {scenarios.map((sample) => (
                            <SampleCard key={sample.title} sample={sample} />
                        ))}
                    </div>
                </section>

                {/* Section 3: Extended Scenarios */}
                <section>
                    <div className="flex items-center gap-4 mb-8">
                        <div className="h-px flex-1 bg-latte-200"></div>
                        <h2 className="text-xl font-bold text-latte-400 uppercase tracking-widest">Extended Features</h2>
                        <div className="h-px flex-1 bg-latte-200"></div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {extended.map((sample) => (
                            <SampleCard key={sample.title} sample={sample} />
                        ))}
                    </div>
                </section>

                {/* Footer Info */}
                <div className="text-center pt-8 border-t border-latte-200">
                    <p className="text-latte-400 text-sm font-mono">
                        Designed with Shadcn UI & Tailwind CSS<br />
                        Theme: Cafe Latte Art
                    </p>
                </div>
            </div>
        </div>
    )
}

function SampleCard({ sample }: { sample: any }) {
    return (
        <Link href={sample.href} className="group">
            <Card className="h-full border-latte-200 hover:border-latte-400 hover:shadow-xl transition-all duration-300 bg-white overflow-hidden relative">
                <div className={`absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity ${sample.color} rounded-bl-[2rem]`}>
                    <sample.icon size={64} />
                </div>
                <CardHeader>
                    <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${sample.color}`}>
                        <sample.icon size={24} />
                    </div>
                    <CardTitle className="font-serif text-2xl text-latte-900 group-hover:text-latte-700 transition-colors">
                        {sample.title}
                    </CardTitle>
                    <CardDescription className="text-latte-500 text-sm min-h-[40px]">
                        {sample.desc}
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="flex flex-wrap gap-2">
                        {sample.preview.split(', ').map((tag: string) => (
                            <Badge key={tag} variant="secondary" className="bg-latte-50 text-latte-600 font-normal border border-latte-100">
                                {tag}
                            </Badge>
                        ))}
                    </div>
                </CardContent>
                <CardFooter className="pt-2">
                    <Button variant="ghost" className="p-0 text-latte-600 hover:text-latte-900 hover:bg-transparent group-hover:translate-x-2 transition-all">
                        View Demo <ArrowRight className="ml-2 w-4 h-4" />
                    </Button>
                </CardFooter>
            </Card>
        </Link>
    )
}
