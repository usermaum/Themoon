'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  LayoutDashboard,
  Coffee,
  Package,
  Settings,
  LogOut,
  Menu,
  Search,
  Bell,
  User,
  ChevronRight,
  Leaf,
  Droplets,
  Wind,
  Sun,
  Cloud,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

// --- Mock Data ---
const menuItems = [
  { icon: LayoutDashboard, label: 'Dashboard', active: true },
  { icon: Coffee, label: 'Beans', active: false },
  { icon: Package, label: 'Inventory', active: false },
  { icon: Settings, label: 'Settings', active: false },
];

// --- Sidebar Components for each Concept ---

// 1. Morning Breeze (Linear Minimalist)
const SidebarOne = () => (
  <div className="h-full w-64 bg-white border-r border-slate-100 flex flex-col font-sans">
    <div className="p-6 flex items-center gap-2 border-b border-slate-50">
      <div className="w-8 h-8 bg-slate-900 rounded-lg flex items-center justify-center text-white">
        <Wind size={16} />
      </div>
      <span className="font-bold text-slate-900 tracking-tight">Breeze</span>
    </div>
    <div className="flex-1 px-4 py-8 space-y-1">
      {menuItems.map((item) => (
        <button
          key={item.label}
          className={cn(
            'w-full flex items-center gap-3 px-4 py-2.5 rounded-md text-sm transition-all',
            item.active
              ? 'bg-slate-50 text-slate-900 font-medium shadow-sm ring-1 ring-slate-200'
              : 'text-slate-500 hover:text-slate-900 hover:bg-slate-50'
          )}
        >
          <item.icon size={18} className={cn(item.active ? 'text-slate-900' : 'text-slate-400')} />
          {item.label}
        </button>
      ))}
    </div>
    <div className="p-4 border-t border-slate-50">
      <div className="flex items-center gap-3 px-4 py-3 rounded-xl bg-slate-50">
        <div className="w-8 h-8 rounded-full bg-slate-200" />
        <div className="flex-1">
          <div className="text-sm font-medium text-slate-900">Barista</div>
          <div className="text-xs text-slate-500">Moon Cafe</div>
        </div>
      </div>
    </div>
  </div>
);

// 2. Minty Fresh (Floating & Glass)
const SidebarTwo = () => (
  <div className="h-full w-full bg-teal-50/30 p-4 flex items-center justify-center">
    <div className="h-[95%] w-64 rounded-3xl bg-white/80 backdrop-blur-xl shadow-xl shadow-teal-100/50 border border-white/50 flex flex-col overflow-hidden">
      <div className="p-8 text-center">
        <div className="w-12 h-12 bg-teal-100 text-teal-600 rounded-2xl mx-auto flex items-center justify-center mb-4">
          <Leaf size={24} />
        </div>
        <h3 className="font-bold text-teal-950">Mint UI</h3>
      </div>
      <div className="flex-1 px-4 space-y-2">
        {menuItems.map((item) => (
          <button
            key={item.label}
            className={cn(
              'w-full flex items-center gap-4 px-6 py-3.5 rounded-2xl text-sm transition-all duration-300',
              item.active
                ? 'bg-teal-500 text-white shadow-lg shadow-teal-200'
                : 'text-slate-500 hover:bg-teal-50 hover:text-teal-700'
            )}
          >
            <item.icon size={20} />
            {item.label}
          </button>
        ))}
      </div>
    </div>
  </div>
);

// 3. Ocean Spray (Gradient Sidebar)
const SidebarThree = () => (
  <div className="h-full w-64 bg-gradient-to-b from-sky-50 to-white border-r border-sky-100 flex flex-col">
    <div className="p-6">
      <h3 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-sky-600 to-blue-600 flex items-center gap-2">
        <Droplets className="text-sky-500" size={20} />
        Ocean
      </h3>
    </div>
    <div className="flex-1 px-3 py-4 space-y-1">
      <div className="text-xs font-bold text-sky-400/80 px-4 mb-2 uppercase tracking-wider">
        Menu
      </div>
      {menuItems.map((item) => (
        <button
          key={item.label}
          className={cn(
            'w-full flex items-center justify-between px-4 py-3 rounded-xl text-sm transition-all group',
            item.active
              ? 'bg-white text-sky-600 shadow-sm border border-sky-100'
              : 'text-slate-500 hover:bg-sky-50/50 hover:text-sky-600'
          )}
        >
          <div className="flex items-center gap-3">
            <item.icon
              size={18}
              className={cn(
                'transition-colors',
                item.active ? 'text-sky-500' : 'text-slate-400 group-hover:text-sky-400'
              )}
            />
            {item.label}
          </div>
          {item.active && <div className="w-1.5 h-1.5 rounded-full bg-sky-500" />}
        </button>
      ))}
    </div>
  </div>
);

// 4. Citrus Zest (Dark & Pop)
const SidebarFour = () => (
  <div className="h-full w-20 bg-stone-900 flex flex-col items-center py-6 gap-8">
    <div className="w-10 h-10 bg-lime-400 rounded-full flex items-center justify-center text-stone-900 shadow-[0_0_15px_rgba(163,230,53,0.4)]">
      <Sun size={20} strokeWidth={3} />
    </div>

    <div className="flex-1 flex flex-col gap-4 w-full px-3">
      {menuItems.map((item) => (
        <button
          key={item.label}
          className={cn(
            'w-full aspect-square rounded-2xl flex items-center justify-center transition-all duration-300 relative group',
            item.active
              ? 'bg-white/10 text-lime-400'
              : 'text-stone-500 hover:bg-white/5 hover:text-lime-200'
          )}
        >
          <item.icon size={22} />
          {/* Tooltip hint */}
          <span className="absolute left-full ml-4 px-2 py-1 bg-stone-800 text-lime-400 text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
            {item.label}
          </span>
          {item.active && (
            <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-lime-400 rounded-r-full" />
          )}
        </button>
      ))}
    </div>

    <button className="w-10 h-10 rounded-full bg-stone-800 flex items-center justify-center text-stone-400 hover:text-white transition-colors">
      <LogOut size={18} />
    </button>
  </div>
);

// 5. Soft Cloud (Neumorphic Lite)
const SidebarFive = () => (
  <div className="h-full w-64 bg-[#F2F4F8] flex flex-col border-r border-white">
    <div className="p-8 flex items-center gap-3">
      <div className="p-2 bg-white rounded-xl shadow-sm text-indigo-500">
        <Cloud size={20} />
      </div>
      <span className="font-bold text-slate-700 text-lg">Cloud</span>
    </div>

    <div className="flex-1 px-6 space-y-4">
      {menuItems.map((item) => (
        <button
          key={item.label}
          className={cn(
            'w-full flex items-center gap-4 px-5 py-4 rounded-2xl text-sm transition-all duration-300',
            item.active
              ? 'bg-white text-indigo-600 shadow-[4px_4px_10px_rgba(0,0,0,0.03),-4px_-4px_10px_rgba(255,255,255,1)]'
              : 'text-slate-500 hover:text-slate-700 hover:bg-white/50'
          )}
        >
          <item.icon size={18} className={item.active ? 'text-indigo-500' : 'opacity-50'} />
          {item.label}
        </button>
      ))}
    </div>

    <div className="p-6">
      <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl p-4 text-white shadow-lg shadow-indigo-200">
        <p className="text-xs font-medium opacity-80 mb-1">Upgrade Plan</p>
        <p className="text-sm font-bold mb-3">Get Pro Features</p>
        <div className="h-1 bg-white/20 rounded-full overflow-hidden">
          <div className="h-full w-3/4 bg-white rounded-full" />
        </div>
      </div>
    </div>
  </div>
);

export default function SidebarConceptsPage() {
  const [selectedTheme, setSelectedTheme] = useState('breeze');

  return (
    <div className="min-h-screen bg-white font-sans">
      {/* Header */}
      <div className="border-b sticky top-0 bg-white/80 backdrop-blur-md z-10 px-8 py-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Sidebar Collection</h1>
          <p className="text-slate-500 text-sm">
            Next.js & Shadcn Compatible • Simple & Refreshing
          </p>
        </div>
        <Button asChild variant="outline">
          <Link href="/">Back to Home</Link>
        </Button>
      </div>

      <div className="p-8 grid grid-cols-1 xl:grid-cols-2 gap-8">
        {/* 1. Morning Breeze */}
        <div className="rounded-xl border border-slate-200 bg-slate-50 h-[600px] overflow-hidden flex shadow-sm hover:shadow-md transition-shadow">
          <SidebarOne />
          <div className="flex-1 p-8 flex flex-col">
            <div className="flex justify-between items-center mb-8">
              <div>
                <h2 className="text-xl font-bold text-slate-900">Morning Breeze</h2>
                <p className="text-slate-500 text-sm">Linear • Minimalist • Crisp</p>
              </div>
              <Button variant="ghost" size="icon">
                <Menu />
              </Button>
            </div>
            <div className="flex-1 bg-white rounded-lg border border-slate-200 border-dashed flex items-center justify-center text-slate-300">
              Main Content Area
            </div>
          </div>
        </div>

        {/* 2. Minty Fresh */}
        <div className="rounded-xl border border-teal-100 bg-teal-50/50 h-[600px] overflow-hidden flex relative shadow-sm hover:shadow-md transition-shadow">
          <div className="w-80 h-full">
            <SidebarTwo />
          </div>
          <div className="flex-1 p-8 pl-0 flex flex-col relative z-10">
            <div className="mb-8 pt-4">
              <h2 className="text-xl font-bold text-teal-900">Minty Fresh</h2>
              <p className="text-teal-600/70 text-sm">Glassmorphism • Floating • Soft</p>
            </div>
            <div className="flex-1 bg-white/60 backdrop-blur-md rounded-2xl shadow-sm flex items-center justify-center text-teal-300">
              Main Content Area
            </div>
          </div>
          {/* Background blob */}
          <div className="absolute -top-20 -right-20 w-96 h-96 bg-teal-200/30 rounded-full blur-3xl pointer-events-none" />
        </div>

        {/* 3. Ocean Spray */}
        <div className="rounded-xl border border-sky-100 bg-white h-[600px] overflow-hidden flex shadow-sm hover:shadow-md transition-shadow">
          <SidebarThree />
          <div className="flex-1 bg-slate-50 p-8 flex flex-col">
            <div className="flex justify-between items-center mb-8 bg-white p-4 rounded-xl shadow-sm border border-sky-50">
              <div>
                <h2 className="text-xl font-bold text-slate-900">Ocean Spray</h2>
                <p className="text-sky-500 text-sm font-medium">Gradient • Airy • Blue</p>
              </div>
              <div className="flex gap-2">
                <div className="w-8 h-8 rounded-full bg-sky-100" />
                <div className="w-8 h-8 rounded-full bg-sky-50" />
              </div>
            </div>
            <div className="flex-1 bg-white rounded-xl shadow-sm flex items-center justify-center text-sky-200">
              Content
            </div>
          </div>
        </div>

        {/* 4. Citrus Zest */}
        <div className="rounded-xl border border-stone-200 bg-white h-[600px] overflow-hidden flex shadow-sm hover:shadow-md transition-shadow">
          <SidebarFour />
          <div className="flex-1 bg-stone-50 p-8 flex flex-col">
            <div className="mb-8">
              <h2 className="text-xl font-bold text-stone-900">Citrus Zest</h2>
              <p className="text-lime-600 text-sm font-medium">
                Dark Sidebar • Pop Color • Icon-only
              </p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="h-32 bg-white rounded-2xl shadow-sm" />
              <div className="h-32 bg-white rounded-2xl shadow-sm" />
              <div className="h-64 bg-stone-900 rounded-2xl shadow-sm col-span-2 text-lime-400 p-6">
                Dark Mode Content Area
              </div>
            </div>
          </div>
        </div>

        {/* 5. Soft Cloud */}
        <div className="rounded-xl border border-slate-200 bg-[#F2F4F8] h-[600px] overflow-hidden flex shadow-sm hover:shadow-md transition-shadow">
          <SidebarFive />
          <div className="flex-1 p-8 flex flex-col">
            <div className="mb-8 flex justify-between items-center">
              <div>
                <h2 className="text-xl font-bold text-slate-700">Soft Cloud</h2>
                <p className="text-slate-400 text-sm">Neumorphic Lite • Comfortable • Seamless</p>
              </div>
              <Button className="bg-indigo-500 hover:bg-indigo-600 rounded-xl shadow-lg shadow-indigo-200 text-white border-0">
                Action
              </Button>
            </div>
            <div className="flex-1 bg-white rounded-3xl shadow-[inset_0_2px_4px_rgba(0,0,0,0.05)] border border-slate-100 flex items-center justify-center text-slate-300">
              Inner Content
            </div>
          </div>
        </div>
      </div>

      <div className="text-center py-12 bg-slate-50 border-t">
        <h3 className="text-2xl font-bold text-slate-900 mb-4">어떤 스타일이 마음에 드시나요?</h3>
        <p className="text-slate-600 mb-8">
          선택하신 사이드바 디자인을 현재 프로젝트의 <code>Sidebar.tsx</code>에 바로 적용해드릴 수
          있습니다.
        </p>
      </div>
    </div>
  );
}
