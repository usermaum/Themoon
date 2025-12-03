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
    Palette
} from 'lucide-react'
import Link from 'next/link'

export default function ArtisticLattePage() {
    return (
        <div className="fixed inset-0 z-[100] flex bg-[#FFF8F0] font-sans text-[#4A403A] overflow-hidden">
            {/* Sidebar */}
            <aside className="w-24 lg:w-80 bg-white/50 backdrop-blur-xl border-r border-[#E6D5C3] flex flex-col">
                <div className="h-32 flex flex-col items-center justify-center border-b border-[#E6D5C3] relative overflow-hidden">
                    <div className="absolute -top-10 -left-10 w-32 h-32 bg-[#FFD6BA] rounded-full blur-2xl opacity-50"></div>
                    <div className="absolute -bottom-10 -right-10 w-32 h-32 bg-[#C3E2DD] rounded-full blur-2xl opacity-50"></div>

                    <Link href="/design-lab" className="absolute top-4 left-4 hover:bg-[#FFF8F0] p-2 rounded-full transition-colors z-10">
                        <ArrowLeft size={20} className="text-[#8D7B68]" />
                    </Link>

                    <div className="relative z-10 text-center">
                        <h1 className="font-serif text-3xl text-[#4A403A]">The Moon</h1>
                        <p className="text-xs text-[#8D7B68] tracking-[0.2em] uppercase mt-1">Artisan Coffee</p>
                    </div>
                </div>

                <nav className="flex-1 px-6 py-8 space-y-4">
                    <NavItem icon={<LayoutDashboard size={24} />} label="Dashboard" active />
                    <NavItem icon={<Package size={24} />} label="Inventory" />
                    <NavItem icon={<Coffee size={24} />} label="Roasting" />
                    <NavItem icon={<Settings size={24} />} label="Studio" />
                </nav>

                <div className="p-8">
                    <div className="bg-white/80 p-4 rounded-2xl shadow-sm flex items-center gap-4">
                        <div className="w-12 h-12 rounded-full bg-gradient-to-tr from-[#FFD6BA] to-[#C3E2DD] p-0.5">
                            <div className="w-full h-full bg-white rounded-full flex items-center justify-center">
                                <span className="font-serif text-[#4A403A]">PM</span>
                            </div>
                        </div>
                        <div>
                            <p className="font-serif text-[#4A403A]">Pmaum</p>
                            <p className="text-xs text-[#8D7B68]">Curator</p>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col overflow-hidden relative">
                <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-[#FFD6BA] rounded-full blur-[100px] opacity-20 pointer-events-none"></div>
                <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-[#C3E2DD] rounded-full blur-[100px] opacity-20 pointer-events-none"></div>

                {/* Header */}
                <header className="h-24 flex items-center justify-between px-12 z-10">
                    <div>
                        <h2 className="text-4xl font-serif text-[#4A403A]">Bean Collection</h2>
                    </div>

                    <div className="flex items-center gap-6">
                        <div className="relative group">
                            <Search className="w-6 h-6 text-[#8D7B68] absolute left-4 top-1/2 -translate-y-1/2" />
                            <input
                                type="text"
                                placeholder="Search..."
                                className="pl-12 pr-6 py-3 bg-white/50 rounded-full border border-transparent focus:bg-white focus:shadow-lg focus:border-[#E6D5C3] text-sm w-72 placeholder-[#B0A69D] text-[#4A403A] outline-none transition-all"
                            />
                        </div>
                        <button className="p-3 bg-white/50 hover:bg-white rounded-full transition-all hover:shadow-md text-[#4A403A]">
                            <Bell size={24} />
                        </button>
                    </div>
                </header>

                {/* Content Scroll Area */}
                <div className="flex-1 overflow-auto px-12 pb-12">
                    <div className="max-w-[1800px] mx-auto space-y-12">

                        {/* Stats Row */}
                        <div className="flex gap-8 overflow-x-auto pb-4 scrollbar-hide">
                            <StatCard title="Total Beans" value="124 kg" color="bg-[#FFD6BA]" />
                            <StatCard title="Roasting" value="8 Batches" color="bg-[#C3E2DD]" />
                            <StatCard title="Low Stock" value="3 Items" color="bg-[#E6D5C3]" />
                        </div>

                        {/* Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-8">
                            <BeanCard
                                name="Ethiopia Yirgacheffe"
                                origin="Ethiopia"
                                roast="Light Roast"
                                notes="Floral, Citrus"
                                stock="12kg"
                                image="/images/beans/ethiopia.png"
                                accent="bg-[#FFD6BA]"
                            />
                            <BeanCard
                                name="Colombia Supremo"
                                origin="Colombia"
                                roast="Medium Roast"
                                notes="Caramel, Nutty"
                                stock="45kg"
                                image="/images/beans/colombia.png"
                                accent="bg-[#C3E2DD]"
                            />
                            <BeanCard
                                name="Sumatra Mandheling"
                                origin="Indonesia"
                                roast="Dark Roast"
                                notes="Earthy, Spicy"
                                stock="8kg"
                                image="/images/beans/sumatra.png"
                                accent="bg-[#E6D5C3]"
                            />
                            <BeanCard
                                name="Kenya AA"
                                origin="Kenya"
                                roast="Medium-Light"
                                notes="Berry, Wine"
                                stock="22kg"
                                image="/images/beans/kenya.png"
                                accent="bg-[#FFD6BA]"
                            />
                            <BeanCard
                                name="Brazil Santos"
                                origin="Brazil"
                                roast="Medium Roast"
                                notes="Chocolate"
                                stock="60kg"
                                image="/images/beans/brazil.png"
                                accent="bg-[#C3E2DD]"
                            />
                            <BeanCard
                                name="Guatemala Antigua"
                                origin="Guatemala"
                                roast="Medium Roast"
                                notes="Spicy, Smoky"
                                stock="15kg"
                                image="/images/beans/guatemala.png"
                                accent="bg-[#E6D5C3]"
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
      flex items-center gap-4 px-6 py-4 rounded-2xl cursor-pointer transition-all duration-300
      ${active
                ? 'bg-white shadow-md text-[#4A403A]'
                : 'text-[#8D7B68] hover:bg-white/50 hover:text-[#4A403A]'}
    `}>
            {icon}
            <span className="font-medium text-lg hidden lg:block">{label}</span>
        </div>
    )
}

function StatCard({ title, value, color }: { title: string, value: string, color: string }) {
    return (
        <div className={`min-w-[250px] p-8 rounded-[2rem] ${color}/30 backdrop-blur-sm flex flex-col justify-between h-40 transition-transform hover:-translate-y-1 cursor-default`}>
            <p className="text-[#8D7B68] font-medium">{title}</p>
            <h4 className="text-4xl font-serif text-[#4A403A]">{value}</h4>
        </div>
    )
}

function BeanCard({ name, origin, roast, notes, stock, image, accent }: { name: string, origin: string, roast: string, notes: string, stock: string, image: string, accent: string }) {
    return (
        <div className="bg-white rounded-[2.5rem] p-4 shadow-sm hover:shadow-xl transition-all duration-500 group">
            <div className="relative aspect-square rounded-[2rem] overflow-hidden mb-6">
                <img
                    src={image}
                    alt={name}
                    className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                />
                <div className={`absolute inset-0 ${accent} mix-blend-multiply opacity-20 group-hover:opacity-0 transition-opacity duration-500`}></div>
                <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-md px-4 py-2 rounded-full text-sm font-medium text-[#4A403A]">
                    {origin}
                </div>
            </div>
            <div className="px-4 pb-4">
                <h4 className="font-serif text-2xl text-[#4A403A] mb-2">{name}</h4>
                <div className="flex flex-wrap gap-2 mb-6">
                    <span className={`px-3 py-1 rounded-full text-xs ${accent} text-[#4A403A]`}>{roast}</span>
                    <span className="px-3 py-1 rounded-full text-xs bg-[#F5F5F5] text-[#8D7B68]">{notes}</span>
                </div>
                <div className="flex items-center justify-between">
                    <span className="text-[#B0A69D] text-sm">In Stock</span>
                    <span className="font-serif text-xl text-[#4A403A]">{stock}</span>
                </div>
            </div>
        </div>
    )
}
