'use client'

import React from 'react'
import {
    Coffee,
    LayoutDashboard,
    Package,
    Settings,
    Search,
    Bell,
    Menu,
    MoreVertical,
    Plus
} from 'lucide-react'

export default function DesignDemoPage() {
    return (
        <div className="fixed inset-0 z-[100] flex bg-coffee-50 font-sans text-coffee-900 overflow-hidden">
            {/* Sidebar */}
            <aside className="w-64 bg-coffee-900 text-coffee-100 flex flex-col shadow-2xl">
                <div className="p-6 flex items-center gap-3">
                    <div className="w-10 h-10 bg-coffee-600 rounded-full flex items-center justify-center shadow-inner">
                        <Coffee className="w-6 h-6 text-coffee-100" />
                    </div>
                    <div>
                        <h1 className="font-bold text-lg tracking-wide text-coffee-50">The Moon</h1>
                        <p className="text-xs text-coffee-300 uppercase tracking-widest">Drip Bar</p>
                    </div>
                </div>

                <nav className="flex-1 px-4 py-6 space-y-2">
                    <NavItem icon={<LayoutDashboard size={20} />} label="Dashboard" active />
                    <NavItem icon={<Package size={20} />} label="Inventory" />
                    <NavItem icon={<Coffee size={20} />} label="Roasting" />
                    <NavItem icon={<Settings size={20} />} label="Settings" />
                </nav>

                <div className="p-4 border-t border-coffee-800">
                    <div className="flex items-center gap-3 p-2 rounded-lg hover:bg-coffee-800 transition-colors cursor-pointer">
                        <div className="w-8 h-8 rounded-full bg-coffee-700 flex items-center justify-center">
                            <span className="text-xs font-bold">PM</span>
                        </div>
                        <div className="flex-1">
                            <p className="text-sm font-medium">Pmaum</p>
                            <p className="text-xs text-coffee-400">Barista</p>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col overflow-hidden relative">
                {/* Background Texture Overlay */}
                <div className="absolute inset-0 pointer-events-none opacity-[0.03]"
                    style={{ backgroundImage: 'url("https://www.transparenttextures.com/patterns/paper.png")' }}>
                </div>

                {/* Header */}
                <header className="h-16 bg-white/80 backdrop-blur-sm border-b border-coffee-100 flex items-center justify-between px-8 sticky top-0 z-10">
                    <div className="flex items-center gap-4 text-coffee-700">
                        <h2 className="text-xl font-semibold">Inventory Management</h2>
                    </div>

                    <div className="flex items-center gap-6">
                        <div className="relative">
                            <Search className="w-5 h-5 text-coffee-400 absolute left-3 top-1/2 -translate-y-1/2" />
                            <input
                                type="text"
                                placeholder="Search beans..."
                                className="pl-10 pr-4 py-2 rounded-full bg-coffee-50 border-none focus:ring-2 focus:ring-coffee-200 text-sm w-64 placeholder-coffee-300 text-coffee-800"
                            />
                        </div>
                        <button className="relative p-2 text-coffee-600 hover:bg-coffee-50 rounded-full transition-colors">
                            <Bell size={20} />
                            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
                        </button>
                    </div>
                </header>

                {/* Content Scroll Area */}
                <div className="flex-1 overflow-auto p-8">
                    <div className="max-w-7xl mx-auto space-y-8">

                        {/* Stats Row */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <StatCard title="Total Beans" value="124 kg" trend="+12%" />
                            <StatCard title="Active Roasts" value="8 Batches" trend="In Progress" />
                            <StatCard title="Low Stock" value="3 Items" trend="Action Needed" isWarning />
                        </div>

                        {/* Section Header */}
                        <div className="flex items-center justify-between">
                            <h3 className="text-2xl font-bold text-coffee-900">Recent Beans</h3>
                            <button className="flex items-center gap-2 bg-coffee-600 text-white px-4 py-2 rounded-lg hover:bg-coffee-700 transition-colors shadow-lg shadow-coffee-200/50">
                                <Plus size={18} />
                                <span>Add New Bean</span>
                            </button>
                        </div>

                        {/* Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                            <BeanCard
                                name="Ethiopia Yirgacheffe"
                                origin="Ethiopia"
                                roast="Light Roast"
                                notes="Floral, Citrus, Tea-like"
                                stock="12kg"
                                image="/images/beans/ethiopia.png"
                            />
                            <BeanCard
                                name="Colombia Supremo"
                                origin="Colombia"
                                roast="Medium Roast"
                                notes="Caramel, Nutty, Balanced"
                                stock="45kg"
                                image="/images/beans/colombia.png"
                            />
                            <BeanCard
                                name="Sumatra Mandheling"
                                origin="Indonesia"
                                roast="Dark Roast"
                                notes="Earthy, Spicy, Full Body"
                                stock="8kg"
                                image="/images/beans/sumatra.png"
                            />
                            <BeanCard
                                name="Kenya AA"
                                origin="Kenya"
                                roast="Medium-Light"
                                notes="Berry, Wine, Bright"
                                stock="22kg"
                                image="/images/beans/kenya.png"
                            />
                            <BeanCard
                                name="Brazil Santos"
                                origin="Brazil"
                                roast="Medium Roast"
                                notes="Chocolate, Smooth"
                                stock="60kg"
                                image="/images/beans/brazil.png"
                            />
                            <BeanCard
                                name="Guatemala Antigua"
                                origin="Guatemala"
                                roast="Medium Roast"
                                notes="Spicy, Smoky, Cocoa"
                                stock="15kg"
                                image="/images/beans/guatemala.png"
                            />
                        </div>
                    </div>
                </div>
            </main>
        </div>
    )
}

function NavItem({ icon, label, active = false }: { icon: React.ReactNode, label: string, active?: boolean }) {
    return (
        <div className={`
      flex items-center gap-3 px-4 py-3 rounded-lg cursor-pointer transition-all duration-200
      ${active
                ? 'bg-coffee-800 text-coffee-50 shadow-md border-l-4 border-coffee-400'
                : 'text-coffee-300 hover:bg-coffee-800/50 hover:text-coffee-100'}
    `}>
            {icon}
            <span className="font-medium">{label}</span>
        </div>
    )
}

function StatCard({ title, value, trend, isWarning = false }: { title: string, value: string, trend: string, isWarning?: boolean }) {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-coffee-100 hover:shadow-md transition-shadow">
            <p className="text-sm text-coffee-500 font-medium uppercase tracking-wider">{title}</p>
            <div className="mt-2 flex items-end justify-between">
                <h4 className="text-3xl font-bold text-coffee-900">{value}</h4>
                <span className={`text-sm font-medium px-2 py-1 rounded-full ${isWarning ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                    {trend}
                </span>
            </div>
        </div>
    )
}

function BeanCard({ name, origin, roast, notes, stock, image }: { name: string, origin: string, roast: string, notes: string, stock: string, image: string }) {
    return (
        <div className="bg-white rounded-xl overflow-hidden shadow-sm border border-coffee-100 group hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
            <div className="h-48 relative overflow-hidden bg-coffee-100">
                <img
                    src={image}
                    alt={name}
                    className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-60"></div>
                <div className="absolute bottom-3 left-4">
                    <span className="bg-white/90 backdrop-blur-sm px-2 py-1 rounded text-xs font-bold text-coffee-800 shadow-sm">
                        {origin}
                    </span>
                </div>
            </div>
            <div className="p-5">
                <div className="flex justify-between items-start mb-2">
                    <h4 className="font-bold text-lg text-coffee-900 leading-tight group-hover:text-coffee-600 transition-colors">{name}</h4>
                    <button className="text-coffee-300 hover:text-coffee-600">
                        <MoreVertical size={18} />
                    </button>
                </div>
                <p className="text-xs font-medium text-coffee-500 mb-4 uppercase tracking-wide">{roast}</p>

                <div className="space-y-3">
                    <div className="flex items-center gap-2 text-sm text-coffee-700">
                        <span className="w-1.5 h-1.5 rounded-full bg-coffee-400"></span>
                        {notes}
                    </div>
                    <div className="pt-3 border-t border-coffee-50 flex items-center justify-between">
                        <span className="text-sm text-coffee-400">Stock</span>
                        <span className="font-bold text-coffee-800">{stock}</span>
                    </div>
                </div>
            </div>
        </div>
    )
}
