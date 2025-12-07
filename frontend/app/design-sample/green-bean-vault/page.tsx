'use client'

import React from 'react'
import Link from 'next/link'
import { Card, CardContent } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"
import { Badge } from "@/components/ui/Badge"
import { Progress } from "@/components/ui/progress"
import { ArrowLeft, ArrowRight, Package, Map, Database, Leaf, Search, Settings } from 'lucide-react'

// --- Mock Data ---
const inventory = [
    {
        id: 1,
        name: "ETHIOPIA YIRGACHEFFE",
        origin: "Ethiopia, Yirgacheffe region",
        process: "Washed",
        grade: "G2",
        altitude: "1,700-2,200m",
        notes: "Floral, citrus, jasmine, bright acidity",
        stock: 85, // High
        image: "/images/beans/yirgacheffe.png"
    },
    {
        id: 2,
        name: "KENYA AA",
        origin: "Kenya, Central Highlands",
        process: "Fully Washed",
        grade: "AA",
        altitude: "1,600-2,000m",
        notes: "Blackcurrant, tomato, winey, complex, full body",
        stock: 45, // Medium
        image: "/images/beans/kenya.png"
    },
    {
        id: 3,
        name: "COLOMBIA SUPREMO",
        origin: "Colombia, Supremo",
        process: "Washed",
        grade: "Supremo",
        altitude: "1,700-2,200m",
        notes: "Floral, citrus, jasmine, bright acidity",
        stock: 92, // High
        image: "/images/beans/colombia.png"
    },
    {
        id: 4,
        name: "BRAZIL CERRADO",
        origin: "Brazil, Cerrado",
        process: "Fully Washed",
        grade: "NY2",
        altitude: "1,000-2,000m",
        notes: "Blackcurrant, tomato, winey, complex, full body",
        stock: 25, // Medium
        image: "/images/beans/santos.png"
    }
]

// --- Assets as Components ---

// 1. Vintage Logo SVG
const VaultLogo = () => (
    <svg viewBox="0 0 200 200" className="w-full h-full drop-shadow-md">
        {/* Outer Ring */}
        <circle cx="100" cy="100" r="95" fill="#5D4037" stroke="#3E2723" strokeWidth="2" />
        {/* Inner Texture */}
        <circle cx="100" cy="100" r="88" fill="#8D6E63" opacity="0.5" />
        <circle cx="100" cy="100" r="85" fill="none" stroke="#D7CCC8" strokeWidth="1" strokeDasharray="4 2" />

        {/* Text Path Area */}
        <path d="M100 20 C 150 20, 180 60, 180 100 C 180 140, 150 180, 100 180 C 50 180, 20 140, 20 100 C 20 60, 50 20, 100 20" fill="none" id="textCurve" />

        {/* Main Text */}
        <text x="100" y="55" fontSize="14" fontFamily="serif" textAnchor="middle" fill="#EBE5D9" fontWeight="bold" letterSpacing="2">THE GREEN BEAN</text>
        <text x="100" y="160" fontSize="18" fontFamily="serif" textAnchor="middle" fill="#EBE5D9" fontWeight="bold" letterSpacing="4">VAULT</text>

        {/* Center Bean Icon */}
        <g transform="translate(100 105) scale(0.8)">
            <path d="M0 -30 Q 30 -30 30 0 Q 30 30 0 50 Q -30 30 -30 0 Q -30 -30 0 -30 Z" fill="#66BB6A" stroke="#1B5E20" strokeWidth="2" />
            <path d="M-2 50 Q 0 0 15 -25" stroke="#1B5E20" strokeWidth="2" fill="none" />
            {/* Sprout */}
            <path d="M 0 -30 Q -10 -50 -25 -45 Q -10 -40 0 -30" fill="#81C784" />
            <path d="M 0 -30 Q 10 -50 25 -45 Q 10 -40 0 -30" fill="#81C784" />
        </g>
    </svg>
)

// Burlap Texture CSS Pattern
const burlapStyle = {
    backgroundColor: '#C8B096',
    backgroundImage: `
        repeating-linear-gradient(45deg, transparent, transparent 2px, rgba(0,0,0,0.05) 2px, rgba(0,0,0,0.05) 3px),
        repeating-linear-gradient(-45deg, transparent, transparent 2px, rgba(0,0,0,0.05) 2px, rgba(0,0,0,0.05) 3px),
        url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.08'/%3E%3C/svg%3E")
    `
}

// Kraft Paper Texture CSS
const kraftStyle = {
    backgroundColor: '#DFD3C3',
    backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.15'/%3E%3C/svg%3E")`
}

// CSS Filter to simulate Green Beans from Roasted images
const greenBeanFilter = "hue-rotate(85deg) saturate(0.6) brightness(1.1) contrast(0.9)"

export default function GreenBeanVaultPage() {
    return (
        <div className="flex h-screen w-full font-serif overflow-hidden relative bg-[#2C1E1A]">

            {/* Sidebar (Left) */}
            <aside className="w-72 h-full flex flex-col z-20 shadow-[4px_0_15px_rgba(0,0,0,0.5)] relative" style={burlapStyle}>
                {/* Frayed Edge Effect (Right Border) */}
                <div className="absolute right-0 top-0 bottom-0 w-[4px]"
                    style={{
                        background: 'linear-gradient(to right, transparent, rgba(0,0,0,0.2))',
                        maskImage: 'url("data:image/svg+xml,%3Csvg width=\'10\' height=\'20\' viewBox=\'0 0 10 20\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M0 0 L10 10 L0 20 Z\' fill=\'black\'/%3E%3C/svg%3E")',
                        maskSize: '10px 8px'
                    }}>
                </div>

                {/* Logo Area */}
                <div className="h-64 flex items-center justify-center p-6 border-b border-[#5D4037]/20 relative">
                    {/* Stitching effect */}
                    <div className="absolute inset-4 border-2 border-dashed border-[#5D4037]/30 rounded-lg pointer-events-none"></div>
                    <div className="w-40 h-40 transform hover:scale-105 transition-transform duration-500">
                        <VaultLogo />
                    </div>
                </div>

                {/* Navigation */}
                <nav className="flex-1 py-8 px-4 space-y-3">
                    <NavItem icon={<Package size={18} />} label="INBOUND" />
                    <NavItem icon={<Map size={18} />} label="ORIGINS" active={true} />
                    <NavItem icon={<Database size={18} />} label="STOCK" />
                </nav>

                {/* Vertical Text Decoration */}
                <div className="absolute bottom-32 -left-2 text-[#5D4037] opacity-10 font-black text-6xl rotate-[-90deg] origin-bottom-left whitespace-nowrap pointer-events-none select-none tracking-widest">
                    GREEN BEAN
                </div>

                {/* Settings Footer */}
                <div className="p-6 border-t border-[#5D4037]/20">
                    <Button variant="ghost" className="w-full justify-start text-[#5D4037] hover:bg-[#5D4037]/10 uppercase tracking-[0.2em] font-bold text-[10px] h-10">
                        <Settings className="mr-3 h-4 w-4" /> Settings
                    </Button>
                </div>
            </aside>

            {/* Main Content (Right) */}
            <main className="flex-1 flex flex-col relative h-full">

                {/* Back Button (Absolute) */}
                <div className="absolute top-6 right-6 z-50">
                    <Button asChild variant="outline" className="bg-black/20 backdrop-blur-sm border-white/20 text-white hover:bg-white/30 rounded-full px-6">
                        <Link href="/design-sample">
                            Exit <ArrowRight className="ml-2 w-4 h-4" />
                        </Link>
                    </Button>
                </div>

                {/* Hero Section (Top) */}
                <div className="h-[45%] relative w-full bg-[#1a120e] overflow-hidden group">
                    {/* Background Image with Green Filter */}
                    <div className="absolute inset-0">
                        <img
                            src="/images/beans/ethiopia.png"
                            alt="Green Beans Background"
                            className="w-full h-full object-cover opacity-60 scale-105 group-hover:scale-110 transition-transform duration-[20s] ease-linear"
                            style={{ filter: greenBeanFilter }}
                        />
                    </div>

                    {/* Shadow Gradient */}
                    <div className="absolute inset-0 bg-gradient-to-t from-[#2C1E1A] via-[#2C1E1A]/40 to-black/60"></div>

                    {/* Floating Map Cutouts (Simulated with SVGs) */}
                    <div className="absolute top-1/4 left-[15%] animate-pulse-slow hidden lg:block">
                        <svg width="150" height="150" viewBox="0 0 100 100" className="drop-shadow-[0_10px_20px_rgba(0,0,0,0.5)]">
                            <path d="M30,20 L60,10 L70,40 L50,70 L20,60 Z" fill="#EBE5D9" stroke="#D4AF37" strokeWidth="2" opacity="0.9" />
                            <text x="45" y="45" fontSize="8" fill="#3E2723" fontWeight="bold" fontFamily="serif">ETHIOPIA</text>
                        </svg>
                    </div>
                    <div className="absolute bottom-[20%] right-[15%] animate-bounce-slow hidden lg:block">
                        <svg width="140" height="140" viewBox="0 0 100 100" className="drop-shadow-[0_10px_20px_rgba(0,0,0,0.5)]">
                            <path d="M40,20 L80,30 L70,70 L30,60 Z" fill="#EBE5D9" stroke="#D4AF37" strokeWidth="2" opacity="0.9" />
                            <text x="55" y="50" fontSize="8" fill="#3E2723" fontWeight="bold" fontFamily="serif">KENYA</text>
                        </svg>
                    </div>

                    {/* Main Text Content */}
                    <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-8 z-10">
                        <h1 className="text-4xl md:text-6xl text-[#EBE5D9] font-bold max-w-5xl leading-tight drop-shadow-2xl mb-4 font-serif">
                            THE GREEN BEAN VAULT: RAW <br />
                            MATERIAL, FARM-TO-CUP ORIGINS.
                        </h1>
                        <p className="text-[#A1887F] text-sm md:text-base tracking-[0.05em] max-w-xl mb-8 font-sans">
                            Explore our global sourcing of premium, unroasted green coffee beans.
                        </p>
                        <Button className="bg-[#556B2F] hover:bg-[#33691E] text-[#EBE5D9] rounded-full px-10 py-6 text-xs font-bold tracking-[0.2em] border border-[#7CB342]/30 shadow-[0_10px_30px_rgba(85,107,47,0.4)] transition-all hover:scale-105 active:scale-95">
                            EXPLORE ORIGINS
                        </Button>
                    </div>
                </div>

                {/* Inventory Grid (Bottom) */}
                <div className="flex-1 overflow-y-auto" style={kraftStyle}>
                    <div className="max-w-7xl mx-auto h-full flex flex-col p-8 md:p-12">

                        {/* Section Header */}
                        <div className="text-center mb-12 relative">
                            <div className="absolute top-1/2 left-0 right-0 h-px bg-[#5D4037]/20 z-0"></div>
                            <h2 className="text-[#3E2723] text-sm font-bold tracking-[0.25em] uppercase inline-block bg-[#DFD3C3] px-6 py-2 relative z-10 border border-[#5D4037]/10 rounded-full shadow-sm">
                                Current Inventory & Origins
                            </h2>
                        </div>

                        {/* Cards Grid */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 pb-12">
                            {inventory.map((bean) => (
                                <InventoryCard key={bean.id} bean={bean} />
                            ))}
                        </div>

                        {/* Footer Links */}
                        <div className="mt-auto pt-8 border-t border-[#5D4037]/10 flex flex-col md:flex-row justify-between items-center text-[10px] uppercase tracking-[0.15em] text-[#5D4037] font-bold gap-4">
                            <div className="space-x-8">
                                <span className="cursor-pointer hover:text-[#3E2723] transition-colors">About Us</span>
                                <span className="cursor-pointer hover:text-[#3E2723] transition-colors">Sustainability</span>
                                <span className="cursor-pointer hover:text-[#3E2723] transition-colors">Contact</span>
                            </div>
                            <div className="opacity-50">
                                <span>Terms & Conditions • Privacy</span>
                            </div>
                        </div>
                    </div>
                </div>

            </main>
        </div>
    )
}

// --- Sub Components ---

function NavItem({ icon, label, active = false }: { icon: any, label: string, active?: boolean }) {
    return (
        <div className={`
            group flex items-center gap-4 p-3 pl-6 cursor-pointer transition-all relative overflow-hidden rounded-r-full mr-4
            ${active
                ? 'bg-[#EBE5D9] shadow-md translate-x-1'
                : 'hover:bg-[#5D4037]/10 hover:translate-x-1'}
        `}>
            {/* Active Marker */}
            {active && <div className="absolute left-0 top-0 bottom-0 w-1 bg-[#556B2F]"></div>}

            <div className={`${active ? 'text-[#3E2723]' : 'text-[#5D4037] group-hover:text-[#3E2723]'}`}>
                {icon}
            </div>
            <span className={`text-xs font-bold tracking-[0.2em] ${active ? 'text-[#3E2723]' : 'text-[#5D4037] group-hover:text-[#3E2723]'}`}>
                {label}
            </span>
            {active && <Leaf className="ml-auto w-4 h-4 text-[#556B2F] animate-in fade-in slide-in-from-right-2" />}
        </div>
    )
}

function InventoryCard({ bean }: { bean: any }) {
    return (
        <Card className="border border-[#BCAAA4] bg-[#EBE5D9] shadow-lg hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 p-2 flex flex-col md:flex-row gap-0 overflow-hidden group h-full md:h-60 rounded-xl">

            {/* Image Side */}
            <div className="w-full md:w-56 h-48 md:h-full bg-[#1a120e] shrink-0 relative overflow-hidden rounded-lg border border-[#D7CCC8]/50 shadow-inner">
                <img
                    src={bean.image}
                    className="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-110"
                    style={{ filter: greenBeanFilter }}
                    alt={bean.name}
                />
                {/* Vignette */}
                <div className="absolute inset-0 bg-[radial-gradient(circle,transparent_40%,rgba(0,0,0,0.6)_100%)]"></div>

                {/* Badge Overlay */}
                <div className="absolute top-3 left-3">
                    <Badge className="bg-[#F5F5F5]/90 text-[#3E2723] hover:bg-white border-none shadow-sm text-[9px] tracking-widest font-bold px-2 py-1 backdrop-blur-sm">
                        RAW
                    </Badge>
                </div>
            </div>

            {/* Content Side */}
            <div className="flex-1 p-6 flex flex-col justify-between relative">
                {/* Card Texture */}
                <div className="absolute inset-0 opacity-20 pointer-events-none mix-blend-multiply"
                    style={{ backgroundImage: 'url("https://www.transparenttextures.com/patterns/cardboard-flat.png")' }}>
                </div>

                <div>
                    <h3 className="font-serif text-2xl font-bold text-[#3E2723] uppercase tracking-wide mb-1 leading-none drop-shadow-sm">{bean.name}</h3>
                    <div className="flex items-center gap-2 mb-4 pb-2 border-b border-[#D7CCC8]">
                        <span className="w-2 h-2 rounded-full bg-[#556B2F]"></span>
                        <p className="text-[10px] font-bold text-[#8D6E63] uppercase tracking-[0.1em]">
                            {bean.origin}
                        </p>
                    </div>

                    <div className="grid grid-cols-2 gap-x-6 gap-y-3 text-[10px] text-[#5D4037] uppercase tracking-wide font-medium mb-4">
                        <div className="flex flex-col">
                            <span className="text-[#A1887F] text-[8px] mb-0.5">Process</span>
                            <span className="font-bold">{bean.process}</span>
                        </div>
                        <div className="flex flex-col">
                            <span className="text-[#A1887F] text-[8px] mb-0.5">Altitude</span>
                            <span className="font-bold">{bean.altitude}</span>
                        </div>
                        <div className="col-span-2 flex flex-col mt-1 bg-[#fff] p-2 rounded border border-[#e0e0e0] shadow-sm">
                            <span className="text-[#A1887F] text-[8px] mb-0.5">Cupping Notes</span>
                            <span className="normal-case italic font-serif text-xs text-[#3E2723]">{bean.notes}</span>
                        </div>
                    </div>
                </div>

                <div className="space-y-3 relative z-10">
                    <div className="flex justify-between items-end text-[9px] font-bold uppercase tracking-wider text-[#5D4037]">
                        <span>Stock Level</span>
                        <span className={bean.stock > 40 ? "text-[#556B2F]" : "text-[#E65100]"}>{bean.stock > 40 ? 'High' : 'Low'}</span>
                    </div>
                    <Progress value={bean.stock} className="h-1.5 bg-[#D7CCC8]" />

                    <Button className="w-full mt-3 bg-[#8D6E63] hover:bg-[#6D4C41] text-[#EBE5D9] text-[10px] font-bold tracking-[0.25em] py-0 h-9 uppercase shadow-[0_4px_10px_rgba(141,110,99,0.3)] active:translate-y-px transition-all">
                        View Details
                    </Button>
                </div>
            </div>
        </Card>
    )
}
