'use client';

import React from 'react';
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
    Leaf,
} from 'lucide-react';
import Link from 'next/link';

export function DesignLabOrganic() {
    return (
        <div className="fixed inset-0 z-[100] flex bg-[#F0EBE5] font-serif text-[#5D5C56] overflow-hidden">
            {/* Sidebar */}
            <aside className="w-64 bg-[#E6E1DB] flex flex-col border-r border-[#D8D3CD]">
                <div className="p-8 flex items-center gap-3">
                    <Link
                        href="/design-showcase?tab=lab"
                        className="hover:bg-[#D8D3CD] p-2 rounded-full transition-colors"
                    >
                        <ArrowLeft size={20} className="text-[#8C8B85]" />
                    </Link>
                    <div className="w-10 h-10 bg-[#7A9A7E] rounded-full flex items-center justify-center text-[#F0EBE5]">
                        <Leaf size={20} />
                    </div>
                    <div>
                        <h1 className="font-medium text-xl tracking-wide text-[#4A4945]">The Moon</h1>
                        <p className="text-xs text-[#8C8B85] italic">Organic Roastery</p>
                    </div>
                </div>

                <nav className="flex-1 px-6 py-4 space-y-4">
                    <NavItem icon={<LayoutDashboard size={20} />} label="Dashboard" active />
                    <NavItem icon={<Package size={20} />} label="Inventory" />
                    <NavItem icon={<Coffee size={20} />} label="Roasting" />
                    <NavItem icon={<Settings size={20} />} label="Settings" />
                </nav>

                <div className="p-6 border-t border-[#D8D3CD]">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-[#D8D3CD] flex items-center justify-center">
                            <span className="text-sm font-serif text-[#5D5C56]">PM</span>
                        </div>
                        <div>
                            <p className="text-sm font-medium text-[#4A4945]">Pmaum</p>
                            <p className="text-xs text-[#8C8B85]">Head Roaster</p>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col overflow-hidden relative">
                {/* Header */}
                <header className="h-24 flex items-center justify-between px-10 sticky top-0 z-10 bg-[#F0EBE5]/90 backdrop-blur-sm">
                    <div>
                        <h2 className="text-3xl italic text-[#4A4945]">Inventory</h2>
                        <p className="text-sm text-[#8C8B85] mt-1 font-sans">Manage your raw beans and stock</p>
                    </div>

                    <div className="flex items-center gap-6">
                        <div className="relative">
                            <Search className="w-5 h-5 text-[#8C8B85] absolute left-3 top-1/2 -translate-y-1/2" />
                            <input
                                type="text"
                                placeholder="Search collection..."
                                className="pl-10 pr-4 py-2 bg-transparent border-b border-[#8C8B85] focus:border-[#4A4945] text-sm w-64 placeholder-[#A8A7A1] text-[#4A4945] outline-none font-sans transition-colors"
                            />
                        </div>
                        <button className="relative p-2 text-[#5D5C56] hover:bg-[#E6E1DB] rounded-full transition-colors">
                            <Bell size={20} />
                            <span className="absolute top-2 right-2 w-1.5 h-1.5 bg-[#C75C5C] rounded-full"></span>
                        </button>
                    </div>
                </header>

                {/* Content Scroll Area */}
                <div className="flex-1 overflow-auto p-10 font-sans">
                    <div className="max-w-7xl mx-auto space-y-12">
                        {/* Stats Row */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                            <StatCard title="Total Stock" value="124 kg" sub="Raw Beans" />
                            <StatCard title="Active Batches" value="8" sub="In Roaster" />
                            <StatCard title="Low Inventory" value="3" sub="Needs Restock" isWarning />
                        </div>

                        {/* Section Header */}
                        <div className="flex items-center justify-between border-b border-[#D8D3CD] pb-4">
                            <h3 className="text-xl font-serif text-[#4A4945]">Bean Collection</h3>
                            <button className="flex items-center gap-2 text-[#4A4945] hover:text-[#7A9A7E] transition-colors">
                                <Plus size={18} />
                                <span className="text-sm uppercase tracking-widest">Add New</span>
                            </button>
                        </div>

                        {/* Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-x-8 gap-y-12">
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
    );
}

function NavItem({
    icon,
    label,
    active = false,
}: {
    icon: React.ReactNode;
    label: string;
    active?: boolean;
}) {
    return (
        <div
            className={`
      flex items-center gap-4 px-4 py-2 rounded-full cursor-pointer transition-all duration-300
      ${active ? 'bg-[#7A9A7E] text-[#F0EBE5]' : 'text-[#8C8B85] hover:text-[#4A4945]'}
    `}
        >
            {icon}
            <span className="font-sans text-sm tracking-wide">{label}</span>
        </div>
    );
}

function StatCard({
    title,
    value,
    sub,
    isWarning = false,
}: {
    title: string;
    value: string;
    sub: string;
    isWarning?: boolean;
}) {
    return (
        <div className="bg-[#E6E1DB]/50 p-6 rounded-3xl">
            <p className="text-xs text-[#8C8B85] uppercase tracking-widest mb-2">{title}</p>
            <div className="flex items-baseline gap-2">
                <h4 className="text-4xl font-serif text-[#4A4945]">{value}</h4>
                <span className={`text-xs font-sans ${isWarning ? 'text-[#C75C5C]' : 'text-[#7A9A7E]'}`}>
                    {sub}
                </span>
            </div>
        </div>
    );
}

function BeanCard({
    name,
    origin,
    roast,
    notes,
    stock,
    image,
}: {
    name: string;
    origin: string;
    roast: string;
    notes: string;
    stock: string;
    image: string;
}) {
    return (
        <div className="group cursor-pointer">
            <div className="aspect-[4/5] relative overflow-hidden rounded-t-[100px] rounded-b-2xl mb-4 bg-[#E6E1DB]">
                <img
                    src={image}
                    alt={name}
                    className="w-full h-full object-cover opacity-90 group-hover:scale-105 transition-transform duration-700 ease-out"
                />
                <div className="absolute top-4 right-4 bg-[#F0EBE5]/80 backdrop-blur-sm px-3 py-1 rounded-full text-xs font-sans text-[#4A4945]">
                    {origin}
                </div>
            </div>
            <div className="px-2">
                <h4 className="font-serif text-xl text-[#4A4945] mb-1 group-hover:text-[#7A9A7E] transition-colors">
                    {name}
                </h4>
                <p className="text-xs text-[#8C8B85] uppercase tracking-widest mb-3">{roast}</p>
                <div className="flex justify-between items-end border-t border-[#D8D3CD] pt-3">
                    <p className="text-sm text-[#5D5C56] italic">{notes}</p>
                    <p className="font-sans font-medium text-[#4A4945]">{stock}</p>
                </div>
            </div>
        </div>
    );
}
