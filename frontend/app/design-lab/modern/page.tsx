'use client'

import React from 'react'
import {
    Coffee,
    LayoutDashboard,
    Package,
    Settings,
    Search,
    Bell,
    MoreVertical,
    Plus,
    ArrowLeft,
    Zap
} from 'lucide-react'
import Link from 'next/link'

export default function ModernColdBrewPage() {
    return (
        <div className="fixed inset-0 z-[100] flex bg-slate-950 font-sans text-slate-100 overflow-hidden selection:bg-amber-500/30">
            {/* Sidebar */}
            <aside className="w-20 lg:w-64 bg-slate-900/50 backdrop-blur-xl border-r border-slate-800 flex flex-col transition-all duration-300">
                <div className="p-6 flex items-center gap-4">
                    <Link href="/design-lab" className="hover:bg-slate-800 p-1 rounded transition-colors">
                        <ArrowLeft size={20} className="text-slate-400" />
                    </Link>
                    <div className="w-10 h-10 bg-gradient-to-br from-amber-500 to-orange-600 rounded-xl flex items-center justify-center shadow-lg shadow-orange-500/20">
                        <Coffee className="w-6 h-6 text-white" />
                    </div>
                    <div className="hidden lg:block">
                        <h1 className="font-bold text-lg tracking-tight text-white">The Moon</h1>
                        <p className="text-[10px] text-amber-500 font-bold uppercase tracking-[0.2em]">Cold Brew</p>
                    </div>
                </div>

                <nav className="flex-1 px-4 py-6 space-y-2">
                    <NavItem icon={<LayoutDashboard size={20} />} label="Dashboard" active />
                    <NavItem icon={<Package size={20} />} label="Inventory" />
                    <NavItem icon={<Coffee size={20} />} label="Roasting" />
                    <NavItem icon={<Settings size={20} />} label="Settings" />
                </nav>

                <div className="p-4 border-t border-slate-800/50">
                    <div className="flex items-center gap-3 p-2 rounded-xl hover:bg-slate-800/50 transition-colors cursor-pointer group">
                        <div className="w-10 h-10 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center group-hover:border-amber-500/50 transition-colors">
                            <span className="text-xs font-bold text-amber-500">PM</span>
                        </div>
                        <div className="hidden lg:block flex-1">
                            <p className="text-sm font-medium text-slate-200">Pmaum</p>
                            <p className="text-xs text-slate-500">Head Barista</p>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col overflow-hidden relative bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-slate-900 via-slate-950 to-black">

                {/* Header */}
                <header className="h-20 flex items-center justify-between px-8 sticky top-0 z-10">
                    <div className="flex items-center gap-4">
                        <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">Inventory</h2>
                    </div>

                    <div className="flex items-center gap-6">
                        <div className="relative group">
                            <Search className="w-5 h-5 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2 group-focus-within:text-amber-500 transition-colors" />
                            <input
                                type="text"
                                placeholder="Search beans..."
                                className="pl-10 pr-4 py-2.5 rounded-xl bg-slate-900/50 border border-slate-800 focus:border-amber-500/50 focus:ring-2 focus:ring-amber-500/20 text-sm w-64 placeholder-slate-600 text-slate-200 transition-all outline-none"
                            />
                        </div>
                        <button className="relative p-2.5 text-slate-400 hover:bg-slate-800 rounded-xl transition-colors">
                            <Bell size={20} />
                            <span className="absolute top-2 right-2 w-2 h-2 bg-amber-500 rounded-full shadow-[0_0_10px_rgba(245,158,11,0.5)]"></span>
                        </button>
                    </div>
                </header>

                {/* Content Scroll Area */}
                <div className="flex-1 overflow-auto p-8">
                    <div className="max-w-7xl mx-auto space-y-10">

                        {/* Stats Row */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <StatCard title="Total Beans" value="124 kg" trend="+12%" icon={<Package className="text-amber-500" />} />
                            <StatCard title="Active Roasts" value="8 Batches" trend="Processing" icon={<Zap className="text-blue-500" />} />
                            <StatCard title="Low Stock" value="3 Items" trend="Warning" isWarning icon={<Coffee className="text-red-500" />} />
                        </div>

                        {/* Section Header */}
                        <div className="flex items-center justify-between">
                            <h3 className="text-xl font-bold text-slate-200 tracking-wide">Recent Beans</h3>
                            <button className="flex items-center gap-2 bg-amber-600 hover:bg-amber-500 text-white px-5 py-2.5 rounded-xl transition-all shadow-lg shadow-amber-900/20 hover:shadow-amber-600/20">
                                <Plus size={18} />
                                <span className="font-medium">Add Bean</span>
                            </button>
                        </div>

                        {/* Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                            <BeanCard
                                name="Ethiopia Yirgacheffe"
                                origin="Ethiopia"
                                roast="Light Roast"
                                notes="Floral, Citrus"
                                stock="12kg"
                                image="/images/beans/ethiopia.png"
                            />
                            <BeanCard
                                name="Colombia Supremo"
                                origin="Colombia"
                                roast="Medium Roast"
                                notes="Caramel, Nutty"
                                stock="45kg"
                                image="/images/beans/colombia.png"
                            />
                            <BeanCard
                                name="Sumatra Mandheling"
                                origin="Indonesia"
                                roast="Dark Roast"
                                notes="Earthy, Spicy"
                                stock="8kg"
                                image="/images/beans/sumatra.png"
                            />
                            <BeanCard
                                name="Kenya AA"
                                origin="Kenya"
                                roast="Medium-Light"
                                notes="Berry, Wine"
                                stock="22kg"
                                image="/images/beans/kenya.png"
                            />
                            <BeanCard
                                name="Brazil Santos"
                                origin="Brazil"
                                roast="Medium Roast"
                                notes="Chocolate"
                                stock="60kg"
                                image="/images/beans/brazil.png"
                            />
                            <BeanCard
                                name="Guatemala Antigua"
                                origin="Guatemala"
                                roast="Medium Roast"
                                notes="Spicy, Smoky"
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
      flex items-center gap-4 px-4 py-3.5 rounded-xl cursor-pointer transition-all duration-300 group
      ${active
                ? 'bg-gradient-to-r from-amber-500/10 to-transparent text-amber-500 border-l-2 border-amber-500'
                : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'}
    `}>
            {React.cloneElement(icon as React.ReactElement<any>, {
                className: `transition-colors ${active ? 'text-amber-500' : 'group-hover:text-slate-200'}`
            })}
            <span className="font-medium hidden lg:block">{label}</span>
        </div>
    )
}

function StatCard({ title, value, trend, isWarning = false, icon }: { title: string, value: string, trend: string, isWarning?: boolean, icon: React.ReactNode }) {
    return (
        <div className="bg-slate-900/40 backdrop-blur-md p-6 rounded-2xl border border-slate-800 hover:border-slate-700 transition-all group">
            <div className="flex justify-between items-start mb-4">
                <div className="p-3 rounded-xl bg-slate-800/50 group-hover:bg-slate-800 transition-colors">
                    {icon}
                </div>
                <span className={`text-xs font-bold px-2 py-1 rounded-lg ${isWarning ? 'bg-red-500/10 text-red-500' : 'bg-green-500/10 text-green-500'}`}>
                    {trend}
                </span>
            </div>
            <div>
                <p className="text-slate-500 text-sm font-medium mb-1">{title}</p>
                <h4 className="text-3xl font-bold text-white tracking-tight">{value}</h4>
            </div>
        </div>
    )
}

function BeanCard({ name, origin, roast, notes, stock, image }: { name: string, origin: string, roast: string, notes: string, stock: string, image: string }) {
    return (
        <div className="bg-slate-900/40 backdrop-blur-sm rounded-2xl overflow-hidden border border-slate-800 group hover:border-amber-500/30 hover:shadow-[0_0_30px_rgba(245,158,11,0.1)] transition-all duration-500">
            <div className="h-56 relative overflow-hidden">
                <img
                    src={image}
                    alt={name}
                    className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 opacity-80 group-hover:opacity-100"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/50 to-transparent"></div>
                <div className="absolute top-4 right-4">
                    <button className="p-2 rounded-full bg-black/20 backdrop-blur-md text-white/70 hover:bg-amber-500 hover:text-white transition-all">
                        <MoreVertical size={16} />
                    </button>
                </div>
                <div className="absolute bottom-4 left-4 right-4">
                    <span className="inline-block px-2 py-1 rounded-md bg-amber-500/20 text-amber-400 text-xs font-bold mb-2 border border-amber-500/20 backdrop-blur-md">
                        {origin}
                    </span>
                    <h4 className="font-bold text-lg text-white leading-tight mb-1">{name}</h4>
                    <p className="text-xs text-slate-400">{roast}</p>
                </div>
            </div>
            <div className="p-5">
                <div className="space-y-4">
                    <div className="flex items-center gap-2 text-sm text-slate-300">
                        <div className="w-1.5 h-1.5 rounded-full bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.8)]"></div>
                        {notes}
                    </div>
                    <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
                        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Stock Level</span>
                        <span className="font-mono font-bold text-amber-400">{stock}</span>
                    </div>
                </div>
            </div>
        </div>
    )
}
