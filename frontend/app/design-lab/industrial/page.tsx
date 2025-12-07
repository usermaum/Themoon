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
    Factory
} from 'lucide-react'
import Link from 'next/link'

export default function IndustrialRoasteryPage() {
    return (
        <div className="fixed inset-0 z-[100] flex bg-[#E5E5E5] font-mono text-neutral-900 overflow-hidden">
            {/* Sidebar */}
            <aside className="w-20 lg:w-72 bg-[#1A1A1A] text-neutral-400 flex flex-col border-r border-neutral-800">
                <div className="h-20 flex items-center justify-center lg:justify-start lg:px-6 border-b border-neutral-800">
                    <Link href="/design-lab" className="hover:text-white transition-colors mr-4 lg:mr-0">
                        <ArrowLeft size={20} />
                    </Link>
                    <div className="hidden lg:flex items-center gap-3 ml-4">
                        <Factory className="text-white" />
                        <span className="font-bold text-white tracking-tighter text-xl">THE MOON</span>
                    </div>
                </div>

                <nav className="flex-1 py-8 space-y-1">
                    <NavItem icon={<LayoutDashboard size={20} />} label="DASHBOARD" active />
                    <NavItem icon={<Package size={20} />} label="INVENTORY" />
                    <NavItem icon={<Coffee size={20} />} label="ROASTING" />
                    <NavItem icon={<Settings size={20} />} label="SYSTEM" />
                </nav>

                <div className="p-6 border-t border-neutral-800">
                    <div className="flex items-center gap-4">
                        <div className="w-10 h-10 bg-neutral-800 flex items-center justify-center font-bold text-white border border-neutral-700">
                            PM
                        </div>
                        <div className="hidden lg:block">
                            <p className="text-sm font-bold text-white">OPERATOR</p>
                            <p className="text-xs text-neutral-500">ID: 8821-A</p>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col overflow-hidden relative">

                {/* Header */}
                <header className="h-20 flex items-center justify-between px-8 bg-white border-b-4 border-neutral-900 z-10">
                    <div className="flex items-center gap-4">
                        <h2 className="text-3xl font-black tracking-tighter uppercase">Inventory Control</h2>
                        <span className="px-2 py-1 bg-neutral-900 text-white text-xs font-bold">V.2.0</span>
                    </div>

                    <div className="flex items-center gap-6">
                        <div className="relative">
                            <Search className="w-5 h-5 text-neutral-400 absolute left-3 top-1/2 -translate-y-1/2" />
                            <input
                                type="text"
                                placeholder="SEARCH_DB..."
                                className="pl-10 pr-4 py-2 bg-neutral-100 border-2 border-transparent focus:border-neutral-900 text-sm w-64 placeholder-neutral-400 text-neutral-900 outline-none transition-all font-bold"
                            />
                        </div>
                        <button className="relative p-2 border-2 border-neutral-200 hover:border-neutral-900 transition-colors">
                            <Bell size={20} />
                        </button>
                    </div>
                </header>

                {/* Content Scroll Area */}
                <div className="flex-1 overflow-auto bg-[#F0F0F0] p-8">
                    <div className="max-w-[1600px] mx-auto space-y-8">

                        {/* Stats Row */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <StatCard title="TOTAL_MASS" value="124.5" unit="KG" trend="+12%" />
                            <StatCard title="ACTIVE_JOBS" value="08" unit="BATCHES" trend="RUNNING" />
                            <StatCard title="CRITICAL_STOCK" value="03" unit="ITEMS" trend="ALERT" isWarning />
                        </div>

                        {/* Section Header */}
                        <div className="flex items-center justify-between bg-neutral-900 text-white p-4">
                            <h3 className="text-lg font-bold uppercase tracking-wider">Raw Material Database</h3>
                            <button className="flex items-center gap-2 bg-white text-neutral-900 px-4 py-1 hover:bg-neutral-200 transition-colors font-bold text-sm uppercase">
                                <Plus size={16} />
                                <span>New Entry</span>
                            </button>
                        </div>

                        {/* Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                            <BeanCard
                                code="ETH-YIR-01"
                                name="Ethiopia Yirgacheffe"
                                origin="ETH"
                                roast="LIGHT"
                                stock="12"
                                image="/images/beans/ethiopia.png"
                            />
                            <BeanCard
                                code="COL-SUP-02"
                                name="Colombia Supremo"
                                origin="COL"
                                roast="MEDIUM"
                                stock="45"
                                image="/images/beans/colombia.png"
                            />
                            <BeanCard
                                code="IDN-MAN-03"
                                name="Sumatra Mandheling"
                                origin="IDN"
                                roast="DARK"
                                stock="08"
                                image="/images/beans/sumatra.png"
                            />
                            <BeanCard
                                code="KEN-AA-04"
                                name="Kenya AA"
                                origin="KEN"
                                roast="MED-LGT"
                                stock="22"
                                image="/images/beans/kenya.png"
                            />
                            <BeanCard
                                code="BRA-SAN-05"
                                name="Brazil Santos"
                                origin="BRA"
                                roast="MEDIUM"
                                stock="60"
                                image="/images/beans/brazil.png"
                            />
                            <BeanCard
                                code="GTM-ANT-06"
                                name="Guatemala Antigua"
                                origin="GTM"
                                roast="MEDIUM"
                                stock="15"
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
      flex items-center gap-4 px-6 py-4 cursor-pointer border-l-4 transition-all duration-200
      ${active
                ? 'border-white bg-neutral-800 text-white'
                : 'border-transparent text-neutral-500 hover:bg-neutral-900 hover:text-neutral-300'}
    `}>
            {icon}
            <span className="font-bold tracking-wider hidden lg:block">{label}</span>
        </div>
    )
}

function StatCard({ title, value, unit, trend, isWarning = false }: { title: string, value: string, unit: string, trend: string, isWarning?: boolean }) {
    return (
        <div className="bg-white border-2 border-neutral-200 p-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
            <div className="flex justify-between items-start mb-4">
                <p className="text-xs font-bold text-neutral-500 uppercase">{title}</p>
                <span className={`text-[10px] font-bold px-1 py-0.5 border ${isWarning ? 'border-red-600 text-red-600' : 'border-green-600 text-green-600'}`}>
                    {trend}
                </span>
            </div>
            <div className="flex items-baseline gap-1">
                <h4 className="text-4xl font-black text-neutral-900">{value}</h4>
                <span className="text-sm font-bold text-neutral-400">{unit}</span>
            </div>
        </div>
    )
}

function BeanCard({ code, name, origin, roast, stock, image }: { code: string, name: string, origin: string, roast: string, stock: string, image: string }) {
    return (
        <div className="bg-white border-2 border-neutral-200 group hover:border-neutral-900 transition-colors">
            <div className="h-48 relative overflow-hidden bg-neutral-100 border-b-2 border-neutral-200">
                <img
                    src={image}
                    alt={name}
                    className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-500"
                />
                <div className="absolute top-0 left-0 bg-neutral-900 text-white text-[10px] font-bold px-2 py-1">
                    {code}
                </div>
            </div>
            <div className="p-4">
                <div className="flex justify-between items-start mb-2">
                    <h4 className="font-bold text-lg text-neutral-900 leading-tight uppercase">{name}</h4>
                    <span className="text-xs font-bold border border-neutral-300 px-1">{origin}</span>
                </div>

                <div className="grid grid-cols-2 gap-4 mt-4 pt-4 border-t-2 border-neutral-100">
                    <div>
                        <p className="text-[10px] text-neutral-400 font-bold uppercase">ROAST_LVL</p>
                        <p className="text-sm font-bold text-neutral-800">{roast}</p>
                    </div>
                    <div className="text-right">
                        <p className="text-[10px] text-neutral-400 font-bold uppercase">STOCK_KG</p>
                        <p className="text-sm font-bold text-neutral-800">{stock}</p>
                    </div>
                </div>
            </div>
        </div>
    )
}
