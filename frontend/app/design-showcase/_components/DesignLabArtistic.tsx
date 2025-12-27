'use client';

import React, { useState } from 'react';
import {
    Heart,
    Share2,
    MessageCircle,
    MoreHorizontal,
    Music,
    Image as ImageIcon,
    Mic,
    Coffee,
    ArrowRight,
    Star,
    ArrowLeft,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import Link from 'next/link';

// Configuration for artistic themes
const themes = [
    {
        id: 'bauhaus',
        name: 'Bauhaus',
        description: '기하학적 형태와 원색의 조화',
        bg: 'bg-[#f4f4f0]',
        font: 'font-sans',
    },
    {
        id: 'watercolor',
        name: 'Soft Watercolor',
        description: '물이 번지는 듯한 부드러운 감성',
        bg: 'bg-[#fdfbf7]',
        font: 'font-serif',
    },
    {
        id: 'noir',
        name: 'Cinema Noir',
        description: '빛과 그림자의 극적인 대비',
        bg: 'bg-[#1a1a1a]', // Dark styling handled in component
        font: 'font-sans',
    },
    {
        id: 'collage',
        name: 'Vintage Collage',
        description: '종이를 오려 붙인 듯한 텍스처',
        bg: 'bg-[#efebe0]',
        font: 'font-serif',
    },
    {
        id: 'neon',
        name: 'Neon Pop',
        description: '어둠 속에서 빛나는 네온 사인',
        bg: 'bg-[#0f0f13]',
        font: 'font-sans',
    },
];

export function DesignLabArtistic() {
    const [currentTheme, setCurrentTheme] = useState('bauhaus');

    return (
        <div
            className={`fixed inset-0 z-[100] transition-colors duration-500 p-8 font-sans overflow-auto ${currentTheme === 'noir' || currentTheme === 'neon'
                    ? 'bg-neutral-900 text-white'
                    : 'bg-[#faf9f6] text-neutral-800'
                }`}
        >
            {/* Header / Theme Switcher */}
            <header className="max-w-7xl mx-auto mb-16">
                <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-8">
                    <div>
                        <div className="flex items-center gap-4 mb-4">
                            <Link href="/design-showcase?tab=lab" className="hover:opacity-60 transition-opacity">
                                <ArrowLeft size={32} />
                            </Link>
                            <h1 className="text-4xl md:text-5xl font-bold tracking-tight">
                                Artistic Components
                            </h1>
                        </div>
                        <p
                            className={`text-lg max-w-xl ${currentTheme === 'noir' || currentTheme === 'neon' ? 'text-neutral-400' : 'text-neutral-500'}`}
                        >
                            UI를 넘어 예술적인 경험을 제공하는 컴포넌트 컬렉션입니다.
                            <br />각 테마는 단순한 스타일링을 넘어 독특한 분위기를 자아냅니다.
                        </p>
                    </div>
                </div>

                <div className="flex flex-wrap gap-4 mt-8">
                    {themes.map((theme) => (
                        <button
                            key={theme.id}
                            onClick={() => setCurrentTheme(theme.id)}
                            className={cn(
                                'group relative px-6 py-3 rounded-full text-sm font-medium transition-all duration-300 overflow-hidden',
                                currentTheme === theme.id
                                    ? 'ring-2 ring-offset-4 ring-current'
                                    : 'opacity-60 hover:opacity-100'
                            )}
                        >
                            <span className="relative z-10">{theme.name}</span>
                            {currentTheme === theme.id && (
                                <span
                                    className={`absolute inset-0 opacity-20 ${theme.id === 'bauhaus'
                                            ? 'bg-yellow-400'
                                            : theme.id === 'watercolor'
                                                ? 'bg-blue-300'
                                                : theme.id === 'noir'
                                                    ? 'bg-white'
                                                    : theme.id === 'collage'
                                                        ? 'bg-orange-300'
                                                        : 'bg-purple-500'
                                        }`}
                                ></span>
                            )}
                        </button>
                    ))}
                </div>
            </header>

            {/* Main Showcase Area */}
            <main className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8 items-start">
                {/* 1. Artist Profile Card */}
                <section className="space-y-4">
                    <h2 className="text-sm font-bold uppercase tracking-widest opacity-50 mb-4">
                        01. Profile Card
                    </h2>
                    {currentTheme === 'bauhaus' ? (
                        <ProfileBauhaus />
                    ) : currentTheme === 'watercolor' ? (
                        <ProfileWatercolor />
                    ) : currentTheme === 'noir' ? (
                        <ProfileNoir />
                    ) : currentTheme === 'collage' ? (
                        <ProfileCollage />
                    ) : (
                        <ProfileNeon />
                    )}
                </section>

                {/* 2. Media Player */}
                <section className="space-y-4">
                    <h2 className="text-sm font-bold uppercase tracking-widest opacity-50 mb-4">
                        02. Media Player
                    </h2>
                    {currentTheme === 'bauhaus' ? (
                        <PlayerBauhaus />
                    ) : currentTheme === 'watercolor' ? (
                        <PlayerWatercolor />
                    ) : currentTheme === 'noir' ? (
                        <PlayerNoir />
                    ) : currentTheme === 'collage' ? (
                        <PlayerCollage />
                    ) : (
                        <PlayerNeon />
                    )}
                </section>

                {/* 3. Article / Content Card */}
                <section className="space-y-4">
                    <h2 className="text-sm font-bold uppercase tracking-widest opacity-50 mb-4">
                        03. Content Card
                    </h2>
                    {currentTheme === 'bauhaus' ? (
                        <ContentBauhaus />
                    ) : currentTheme === 'watercolor' ? (
                        <ContentWatercolor />
                    ) : currentTheme === 'noir' ? (
                        <ContentNoir />
                    ) : currentTheme === 'collage' ? (
                        <ContentCollage />
                    ) : (
                        <ContentNeon />
                    )}
                </section>
            </main>
        </div>
    );
}

// ==========================================
// THEME 1: BAUHAUS (Geometric, Primary Colors)
// ==========================================
function ProfileBauhaus() {
    return (
        <div className="bg-[#f0f0f0] p-8 relative overflow-hidden group hover:shadow-xl transition-shadow border-2 border-black">
            {/* Geometric Shapes */}
            <div className="absolute top-0 right-0 w-24 h-24 bg-red-600 rounded-bl-full border-l-2 border-b-2 border-black"></div>
            <div className="absolute bottom-0 left-0 w-16 h-16 bg-blue-600 rounded-tr-full border-t-2 border-r-2 border-black"></div>
            <div className="absolute top-1/2 left-4 w-4 h-4 bg-yellow-400 rounded-full border-2 border-black"></div>

            <div className="relative z-10 flex flex-col items-center">
                <div className="w-24 h-24 bg-white border-2 border-black rounded-full mb-4 flex items-center justify-center overflow-hidden">
                    <img
                        src="/images/beans/ethiopia.png"
                        alt="Profile"
                        className="w-full h-full object-cover grayscale contrast-125"
                    />
                </div>
                <h3 className="text-2xl font-bold text-black tracking-tighter bg-yellow-400 px-2 border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                    MONDRIAN
                </h3>
                <p className="mt-2 text-sm font-bold text-black uppercase tracking-widest">Visual Artist</p>

                <div className="flex gap-4 mt-6">
                    <button className="w-10 h-10 border-2 border-black bg-white flex items-center justify-center hover:bg-black hover:text-white transition-colors shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]">
                        <MessageCircle size={18} />
                    </button>
                    <button className="w-10 h-10 border-2 border-black bg-blue-600 text-white flex items-center justify-center hover:bg-blue-700 transition-colors shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]">
                        <Share2 size={18} />
                    </button>
                </div>
            </div>
        </div>
    );
}

function PlayerBauhaus() {
    return (
        <div className="bg-white border-2 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] relative">
            <div className="absolute -left-2 top-8 w-4 h-16 bg-red-600 border-2 border-black"></div>

            <div className="flex items-center justify-between mb-6">
                <div>
                    <h4 className="font-bold text-lg leading-none">JAZZ NO.1</h4>
                    <p className="text-xs font-bold uppercase mt-1 bg-black text-white inline-block px-1">
                        Ensemble
                    </p>
                </div>
                <Music className="w-8 h-8 text-black" />
            </div>

            <div className="space-y-2 mb-6">
                <div className="h-4 w-full border-2 border-black bg-[#f0f0f0] relative">
                    <div className="absolute top-0 left-0 h-full w-2/3 bg-blue-600 border-r-2 border-black"></div>
                </div>
                <div className="flex justify-between text-xs font-bold font-mono">
                    <span>02:14</span>
                    <span>03:45</span>
                </div>
            </div>

            <div className="flex justify-center gap-6">
                <button className="w-12 h-12 rounded-full border-2 border-black bg-yellow-400 flex items-center justify-center hover:scale-110 transition-transform">
                    <div className="w-0 h-0 border-t-[8px] border-t-transparent border-l-[12px] border-l-black border-b-[8px] border-b-transparent ml-1"></div>
                </button>
            </div>
        </div>
    );
}

function ContentBauhaus() {
    return (
        <div className="border-2 border-black bg-white group hover:-translate-y-2 transition-transform duration-300">
            <div className="h-48 bg-gray-200 border-b-2 border-black relative overflow-hidden">
                <div className="absolute inset-0 bg-[url('/images/hero/beans-hero.png')] bg-cover bg-center grayscale mix-blend-multiply opacity-50"></div>
                <div className="absolute inset-0 bg-gradient-to-tr from-red-600/20 to-blue-600/20"></div>
                <div className="absolute bottom-0 right-0 bg-black text-white px-4 py-2 font-bold text-lg border-t-2 border-l-2 border-black">
                    NEW ARRIVAL
                </div>
            </div>
            <div className="p-6 relative">
                <div className="absolute -top-6 left-6 w-12 h-12 bg-yellow-400 border-2 border-black flex items-center justify-center shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                    <Star size={20} className="fill-black" />
                </div>
                <h3 className="mt-4 text-2xl font-bold leading-tight">Functional Aesthetics</h3>
                <p className="mt-3 text-sm font-medium leading-relaxed border-l-4 border-red-600 pl-4">
                    Form follows function. Minimalism is not a lack of something. It’s simply the perfect
                    amount of something.
                </p>
                <button className="mt-6 flex items-center gap-2 text-sm font-bold hover:bg-black hover:text-white px-3 py-1 transition-colors border-2 border-transparent hover:border-black">
                    READ MORE <ArrowRight size={16} />
                </button>
            </div>
        </div>
    );
}

// ==========================================
// THEME 2: WATERCOLOR (Soft, Fluid, Serif)
// ==========================================
function ProfileWatercolor() {
    return (
        <div className="bg-white/50 backdrop-blur-sm p-8 rounded-[3rem] shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)] border border-white/60 relative overflow-hidden text-center font-serif">
            {/* Water Stains */}
            <div className="absolute top-[-50px] left-[-50px] w-48 h-48 bg-blue-100 rounded-full mix-blend-multiply filter blur-3xl opacity-50"></div>
            <div className="absolute bottom-[-30px] right-[-30px] w-40 h-40 bg-purple-100 rounded-full mix-blend-multiply filter blur-3xl opacity-50"></div>

            <div className="relative z-10 flex flex-col items-center">
                <div className="w-28 h-28 rounded-full p-1 bg-gradient-to-br from-blue-200 to-purple-200 mb-4">
                    <img
                        src="/images/beans/ethiopia.png"
                        alt="Profile"
                        className="w-full h-full rounded-full object-cover border-4 border-white"
                    />
                </div>
                <h3 className="text-2xl text-slate-700 font-medium italic">Claude Monet</h3>
                <p className="text-sm text-slate-500 mt-1">Impressionist Painter</p>

                <div className="flex gap-4 mt-8">
                    <button className="px-6 py-2 rounded-full bg-blue-50 text-blue-800 text-sm hover:bg-blue-100 transition-colors">
                        Follow
                    </button>
                    <button className="px-6 py-2 rounded-full bg-white border border-slate-200 text-slate-600 text-sm hover:bg-slate-50 transition-colors">
                        Message
                    </button>
                </div>
            </div>
        </div>
    );
}

function PlayerWatercolor() {
    return (
        <div className="font-serif bg-white/80 backdrop-blur-md rounded-[2rem] p-6 shadow-sm border border-white/50 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-pink-50 via-white to-blue-50 opacity-50"></div>

            <div className="relative z-10">
                <div className="w-full aspect-square rounded-2xl bg-indigo-50 mb-6 overflow-hidden shadow-inner flex items-center justify-center">
                    <Music size={48} className="text-indigo-200 opacity-50" />
                </div>

                <h4 className="text-xl text-slate-800">Clair de Lune</h4>
                <p className="text-sm text-slate-500 italic mb-6">Claude Debussy</p>

                <div className="relative h-1 bg-slate-100 rounded-full mb-8 overflow-hidden">
                    <div className="absolute top-0 left-0 h-full w-1/3 bg-gradient-to-r from-blue-300 to-purple-300 rounded-full"></div>
                </div>

                <div className="flex justify-between items-center px-4">
                    <button className="text-slate-400 hover:text-slate-600">
                        <Star size={20} />
                    </button>
                    <button className="w-14 h-14 rounded-full bg-slate-800 text-white flex items-center justify-center shadow-lg hover:bg-slate-700 transition-colors">
                        <div className="w-0 h-0 border-t-[6px] border-t-transparent border-l-[10px] border-l-white border-b-[6px] border-b-transparent ml-1"></div>
                    </button>
                    <button className="text-slate-400 hover:text-slate-600">
                        <MoreHorizontal size={20} />
                    </button>
                </div>
            </div>
        </div>
    );
}

function ContentWatercolor() {
    return (
        <div className="group font-serif relative">
            <div className="absolute -inset-2 bg-gradient-to-r from-blue-100 to-purple-100 rounded-2xl blur-lg opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
            <div className="relative bg-white rounded-xl p-6 shadow-sm border border-slate-100">
                <div className="flex gap-4 items-start mb-4">
                    <span className="text-4xl text-blue-200">"</span>
                </div>
                <p className="text-lg text-slate-700 leading-relaxed italic mb-6">
                    Color is my day-long obsession, joy and torment. To me, color is a vital energy that must
                    be expressed.
                </p>
                <div className="flex items-center gap-3 border-t border-slate-100 pt-4">
                    <div className="w-10 h-10 rounded-full bg-slate-100 overflow-hidden">
                        <img src="/images/hero/beans-hero.png" className="w-full h-full object-cover" />
                    </div>
                    <div>
                        <div className="text-sm font-bold text-slate-800">Water Lilies</div>
                        <div className="text-xs text-slate-500">Exhibit 24</div>
                    </div>
                    <button className="ml-auto text-slate-400 hover:text-pink-400 transition-colors">
                        <Heart size={18} />
                    </button>
                </div>
            </div>
        </div>
    );
}

// ==========================================
// THEME 3: CINEMA NOIR (High Contrast, Dark)
// ==========================================
function ProfileNoir() {
    return (
        <div className="bg-black text-white p-0 relative group overflow-hidden border border-neutral-800">
            <div className="absolute inset-0 bg-[url('/images/hero/beans-hero.png')] bg-cover bg-center opacity-30 grayscale contrast-150"></div>
            <div className="absolute inset-0 bg-gradient-to-t from-black via-black/80 to-transparent"></div>

            <div className="relative z-10 p-8 flex flex-col items-start min-h-[300px] justify-end">
                <h3 className="text-4xl font-bold font-serif tracking-tighter mb-1">THE DETECTIVE</h3>
                <div className="h-0.5 w-12 bg-white mb-4"></div>
                <p className="text-neutral-400 text-sm max-w-xs leading-relaxed mb-6">
                    Shadows tell more stories than light. In the city of smoke, everyone has a secret.
                </p>
                <button className="border border-white px-6 py-2 text-xs tracking-[0.2em] hover:bg-white hover:text-black transition-colors uppercase">
                    Investigate
                </button>
            </div>
        </div>
    );
}

function PlayerNoir() {
    return (
        <div className="bg-neutral-900 border border-neutral-800 p-8 flex flex-col items-center justify-center relative">
            <div className="w-48 h-48 rounded-full border border-neutral-800 relative flex items-center justify-center group cursor-pointer mb-8">
                {/* Vinyl Effect */}
                <div className="absolute inset-1 rounded-full border border-neutral-800 opacity-50 group-hover:animate-spin-slow duration-[10s]"></div>
                <div className="absolute inset-8 rounded-full border border-neutral-800 opacity-50 group-hover:animate-spin-slow duration-[10s] delay-75"></div>
                <div className="absolute inset-16 rounded-full border border-neutral-800 opacity-50 group-hover:animate-spin-slow duration-[10s] delay-150"></div>

                <div className="w-16 h-16 rounded-full bg-white flex items-center justify-center z-10">
                    <div className="w-2 h-2 rounded-full bg-black"></div>
                </div>
            </div>

            <div className="w-full space-y-4">
                <div className="flex justify-between items-end border-b border-neutral-800 pb-2">
                    <span className="text-xs text-neutral-500 uppercase tracking-widest">Now Playing</span>
                    <span className="font-serif italic text-lg">Midnight Rain</span>
                </div>
                <div className="flex justify-between items-center pt-2">
                    <button className="text-neutral-500 hover:text-white transition-colors">PREV</button>
                    <button className="w-10 h-10 bg-white text-black rounded-full flex items-center justify-center hover:bg-neutral-200">
                        <div className="w-3 h-3 bg-black"></div>
                    </button>
                    <button className="text-neutral-500 hover:text-white transition-colors">NEXT</button>
                </div>
            </div>
        </div>
    );
}

function ContentNoir() {
    return (
        <div className="bg-black border border-neutral-700 p-1">
            <div className="border border-neutral-800 p-6 flex flex-col h-full bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-neutral-800 via-black to-black">
                <div className="mb-6 self-start px-2 py-1 bg-white text-black text-[10px] font-bold uppercase tracking-wider">
                    Classified
                </div>
                <h3 className="text-2xl font-serif text-white mb-4 leading-snug">
                    The Case of the
                    <br />
                    Missing Roast
                </h3>
                <p className="text-neutral-500 text-sm mb-8 flex-1">
                    Evidence suggests it wasn't an accident. The beans were green when they entered the
                    warehouse...
                </p>
                <div className="flex items-center gap-4 text-xs text-neutral-400 uppercase tracking-wider border-t border-neutral-900 pt-4 mt-auto">
                    <span>Dec 06, 1954</span>
                    <span className="w-1 h-1 bg-neutral-600 rounded-full"></span>
                    <span>File #892</span>
                </div>
            </div>
        </div>
    );
}

// ==========================================
// THEME 4 & 5 Placeholders (To keep it concise but expandable)
// ==========================================

function ProfileCollage() {
    return (
        <div className="bg-[#f2e6d6] p-4 rotate-1 shadow-lg relative max-w-sm mx-auto">
            {/* Tape Effect */}
            <div className="absolute -top-3 left-1/2 -translate-x-1/2 w-24 h-8 bg-white/40 rotate-2 backdrop-blur-sm z-10 shadow-sm border border-white/20"></div>

            <div className="bg-[url('https://www.transparenttextures.com/patterns/paper.png')] p-6 border-4 border-white shadow-inner flex flex-col items-center">
                <div className="w-32 h-32 bg-gray-300 mb-4 overflow-hidden grayscale contrast-125 sepia relative">
                    <img src="/images/beans/ethiopia.png" className="w-full h-full object-cover" />
                    <div className="absolute top-0 left-0 w-full h-full bg-red-500/20 mix-blend-overlay"></div>
                </div>
                <h3 className="font-serif text-3xl text-[#2c2c2c] bg-white px-2 -rotate-2 shadow-sm font-bold">
                    The Collector
                </h3>
                <p className="mt-2 font-mono text-xs text-gray-500 text-center uppercase tracking-widest border-t border-b border-gray-400 py-1 w-full">
                    Est. 2024
                </p>
            </div>
            <div className="absolute -bottom-4 -right-4 bg-orange-500 text-white font-bold rounded-full w-12 h-12 flex items-center justify-center rotate-12 shadow-md text-xs border-2 border-white">
                NEW
            </div>
        </div>
    );
}

function PlayerCollage() {
    return (
        <div className="bg-[#4a4a4a] p-1 shadow-lg -rotate-1 relative">
            <div className="absolute -top-2 -right-2 w-8 h-24 bg-yellow-200/50 -rotate-45 z-10"></div>

            <div className="bg-[#e8e8e8] p-6 h-full flex items-center gap-4 relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-full bg-[url('https://www.transparenttextures.com/patterns/dust.png')] opacity-20 pointer-events-none"></div>

                <div className="w-20 h-20 bg-black flex-shrink-0 border-4 border-white shadow-md relative">
                    <div className="absolute inset-0 bg-red-500 mix-blend-screen opacity-50"></div>
                    <div className="w-full h-full flex items-center justify-center text-white font-mono text-2xl">
                        A
                    </div>
                </div>

                <div className="flex-1 z-10">
                    <div className="bg-black text-white inline-block px-1 font-mono text-xs mb-1">SIDE A</div>
                    <h4 className="font-serif font-bold text-xl leading-none">Retro Vibes</h4>
                    <div className="w-full h-2 bg-gray-300 mt-3 rounded-full overflow-hidden border border-gray-400">
                        <div className="w-1/2 h-full bg-[repeating-linear-gradient(45deg,#000,#000_2px,#fff_2px,#fff_4px)]"></div>
                    </div>
                </div>
            </div>
        </div>
    );
}

function ContentCollage() {
    return (
        <div className="relative p-4">
            <div className="absolute inset-0 bg-blue-100 rotate-2 rounded-lg"></div>
            <div className="absolute inset-0 bg-white -rotate-1 rounded-lg border border-gray-200 shadow-sm"></div>

            <div className="relative z-10 p-4">
                <div className="flex gap-2 mb-4 bg-yellow-100 p-2 -ml-6 w-[110%] shadow-sm rotate-1">
                    <Star size={16} className="text-orange-500 fill-orange-500" />
                    <span className="font-mono text-xs font-bold text-orange-800 uppercase">
                        Featured Story
                    </span>
                </div>

                <h3 className="font-serif text-2xl mb-2">Memory Fragments</h3>
                <p className="font-sans text-sm text-gray-600 leading-relaxed mb-4">
                    "We do not remember days, we remember moments."
                </p>
                <div className="flex gap-2">
                    <span className="px-2 py-0.5 bg-gray-200 text-xs font-mono">#art</span>
                    <span className="px-2 py-0.5 bg-gray-200 text-xs font-mono">#life</span>
                </div>
            </div>
        </div>
    );
}

// Minimal placeholder for Neon to prevent error if selected (full implementation would be similar)
function ProfileNeon() {
    return (
        <div className="p-8 border border-purple-500/50 bg-black shadow-[0_0_20px_rgba(168,85,247,0.2)] rounded-lg text-center">
            <div className="w-24 h-24 rounded-full border-2 border-cyan-400 mx-auto mb-4 shadow-[0_0_15px_rgba(34,211,238,0.5)] bg-gray-900"></div>
            <h3 className="text-white font-bold text-xl tracking-wider shadow-cyan-500 drop-shadow-[0_0_5px_rgba(255,255,255,0.5)]">
                CYBER
            </h3>
            <p className="text-purple-400 text-xs mt-2 uppercase tracking-[0.2em] animate-pulse">
                Punk 2077
            </p>
        </div>
    );
}
function PlayerNeon() {
    return (
        <div className="p-6 border border-pink-500/50 bg-black/80 rounded-lg flex items-center justify-between">
            <div className="text-cyan-400 font-mono">03:24</div>
            <div className="h-1 bg-gray-800 flex-1 mx-4 relative overflow-hidden">
                <div className="absolute left-0 top-0 h-full w-1/2 bg-pink-500 shadow-[0_0_10px_#ec4899]"></div>
            </div>
            <Music className="text-pink-500 drop-shadow-[0_0_5px_rgba(236,72,153,1)]" />
        </div>
    );
}
function ContentNeon() {
    return (
        <div className="p-6 border border-blue-500/30 bg-gray-900/50 rounded-lg relative overflow-hidden group">
            <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <h3 className="text-white text-lg font-bold">Neon Lights</h3>
            <p className="text-gray-400 text-sm mt-2">The city never sleeps, and neither do we.</p>
        </div>
    );
}
