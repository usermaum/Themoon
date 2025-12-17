'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
    Home,
    Coffee,
    Flame,
    Layers,
    Package,
    Settings,
    User,
    PanelLeft,
    LogOut,
    Sparkles,
    FileInput
} from 'lucide-react'

interface SidebarProps {
    isOpen: boolean
    onToggle: () => void
}

export default function Sidebar({ isOpen, onToggle }: SidebarProps) {
    const pathname = usePathname()

    const navItems = [
        { name: 'Home', href: '/', icon: Home },
        { name: 'Beans', href: '/beans', icon: Coffee },
        { name: 'Roasting', href: '/roasting', icon: Flame },
        { name: 'Blends', href: '/blends', icon: Layers },
        { name: 'Inventory', href: '/inventory', icon: Package },
        { name: 'Inbound', href: '/inventory/inbound', icon: FileInput },
        { name: 'Design Demo', href: '/design-showcase', icon: Sparkles },
    ]

    const isActive = (href: string) => {
        if (href === '/') {
            return pathname === '/'
        }
        return pathname.startsWith(href)
    }

    return (
        <>
            {/* Backdrop for mobile */}
            {isOpen && (
                <div
                    className="fixed inset-0 bg-black/20 backdrop-blur-sm z-[90] lg:hidden"
                    onClick={onToggle}
                />
            )}

            {/* Sidebar */}
            <aside
                className={`
                    fixed top-0 left-0 h-screen 
                    bg-white backdrop-blur-xl
                    ${isOpen ? 'border-r border-latte-200 shadow-[0_4px_30px_rgba(0,0,0,0.03)]' : 'lg:border-r lg:border-latte-200/50'}
                    transition-all duration-500 cubic-bezier(0.4, 0, 0.2, 1) z-[100]
                    flex flex-col
                    ${isOpen ? 'w-64 translate-x-0' : 'w-64 -translate-x-full lg:translate-x-0 lg:w-[80px]'}
                `}
            >
                {/* Header / Logo Area */}
                <div className={`
                    h-24 flex items-center relative overflow-hidden
                    ${isOpen ? 'px-6' : 'justify-center'} 
                    border-b border-latte-200/50
                `}>
                    {/* Header Background Blobs */}
                    {isOpen && (
                        <>
                            <div className="absolute -top-10 -left-10 w-32 h-32 bg-blob-orange/50 rounded-full blur-2xl opacity-50"></div>
                            <div className="absolute -bottom-10 -right-10 w-32 h-32 bg-blob-green/50 rounded-full blur-2xl opacity-50"></div>
                        </>
                    )}

                    {isOpen ? (
                        <div className="flex items-center justify-between w-full relative z-10">
                            <Link href="/" className="flex flex-col">
                                <h1 className="font-serif text-3xl font-bold text-latte-900 tracking-tighter leading-none">The Moon</h1>
                                <p className="text-xs font-bold text-latte-600 tracking-[0.3em] uppercase ml-1">Drip Bar</p>
                            </Link>
                            <button
                                onClick={onToggle}
                                className="p-2 rounded-full hover:bg-white/50 text-latte-500 transition-colors"
                            >
                                <PanelLeft className="w-5 h-5" />
                            </button>
                        </div>
                    ) : (
                        <button
                            onClick={onToggle}
                            className="relative z-10 p-3 rounded-full hover:bg-white/50 text-latte-600 transition-colors"
                        >
                            <PanelLeft className="w-6 h-6" />
                        </button>
                    )}
                </div>

                {/* Navigation Links */}
                <div className="flex-1 py-8 px-4 space-y-2">
                    {navItems.map((item) => {
                        const Icon = item.icon
                        const active = isActive(item.href)

                        return (
                            <div key={item.name} className="relative group">
                                <Link
                                    href={item.href}
                                    className={`
                                        flex items-center
                                        ${isOpen ? 'gap-4 px-4' : 'justify-center'}
                                        py-3 rounded-2xl
                                        transition-all duration-300
                                        ${active
                                            ? 'bg-white shadow-md text-latte-800'
                                            : 'text-latte-600 hover:bg-latte-100 hover:text-latte-800'
                                        }
                                    `}
                                >
                                    <Icon className={`flex-shrink-0 ${active ? 'w-5 h-5' : 'w-5 h-5 opacity-80'}`} />
                                    {isOpen && (
                                        <span className={`font-medium ${active ? 'font-serif' : 'font-sans'}`}>
                                            {item.name}
                                        </span>
                                    )}
                                </Link>
                                {!isOpen && (
                                    <div className="absolute left-full ml-4 top-1/2 -translate-y-1/2 px-3 py-1.5 bg-latte-800 text-latte-50 text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-[200] shadow-xl">
                                        {item.name}
                                    </div>
                                )}
                            </div>
                        )
                    })}
                </div>

                {/* User Profile Area */}
                <div className="p-6 border-t border-latte-200/50">
                    <div className={`
                        bg-white/80 rounded-2xl shadow-sm transition-all duration-300 group cursor-pointer
                        ${isOpen ? 'p-3 flex items-center gap-3' : 'p-2 flex justify-center aspect-square items-center'}
                    `}>
                        <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-blob-orange to-blob-green p-0.5 flex-shrink-0">
                            <div className="w-full h-full bg-white rounded-full flex items-center justify-center">
                                <User className="w-5 h-5 text-latte-800" />
                            </div>
                        </div>

                        {isOpen && (
                            <div className="overflow-hidden flex-1">
                                <p className="font-serif text-sm text-latte-800 truncate">Pmaum</p>
                                <p className="text-xs text-latte-500 truncate">Curator</p>
                            </div>
                        )}

                        {isOpen && (
                            <LogOut className="w-4 h-4 text-latte-400 group-hover:text-latte-600 transition-colors" />
                        )}
                    </div>
                </div>
            </aside>
        </>
    )
}
