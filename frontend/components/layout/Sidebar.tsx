'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
    Home,
    Coffee,
    Layers,
    Package,
    Settings,
    User,
    PanelLeft
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
        { name: 'Blends', href: '/blends', icon: Layers },
        { name: 'Inventory', href: '/inventory', icon: Package },
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
                    className="fixed inset-0 bg-black/50 z-[90] lg:hidden"
                    onClick={onToggle}
                />
            )}

            {/* Sidebar */}
            <aside
                className={`
                    fixed top-0 left-0 h-screen bg-white dark:bg-gray-900
                    border-r border-gray-200 dark:border-gray-800
                    transition-all duration-300 ease-in-out z-[100]
                    flex flex-col
                    ${isOpen ? 'w-64' : 'w-[70px]'}
                `}
                style={{ overflow: 'visible' }}
            >
                {/* Header / Logo Area */}
                <div className={`
                    h-16 flex items-center 
                    ${isOpen ? 'justify-between px-4' : 'justify-center'} 
                    border-b border-gray-200 dark:border-gray-800
                `}>
                    {isOpen ? (
                        <>
                            <Link href="/" className="flex items-center gap-2 overflow-hidden">
                                <span className="text-2xl flex-shrink-0">☕</span>
                                <span className="font-bold text-xl tracking-tight text-gray-900 dark:text-white whitespace-nowrap">
                                    The Moon
                                </span>
                            </Link>
                            <div className="relative group">
                                <button
                                    onClick={onToggle}
                                    className="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500 transition-colors"
                                    aria-label="Collapse sidebar"
                                >
                                    <PanelLeft className="w-5 h-5" />
                                </button>
                                <div className="absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-1 bg-gray-900 dark:bg-gray-700 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-[200]">
                                    사이드바 접기
                                </div>
                            </div>
                        </>
                    ) : (
                        <div className="relative group">
                            <button
                                onClick={onToggle}
                                className="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500 transition-colors"
                                aria-label="Expand sidebar"
                            >
                                <PanelLeft className="w-5 h-5" />
                            </button>
                            <div className="absolute left-full ml-2 top-1/2 -translate-y-1/2 px-2 py-1 bg-gray-900 dark:bg-gray-700 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-[200]">
                                사이드바 펼치기
                            </div>
                        </div>
                    )}
                </div>

                {/* Navigation Links */}
                <div className="flex-1 py-4 overflow-y-auto scrollbar-hide">
                    <ul className="space-y-2 px-3">
                        {navItems.map((item) => {
                            const Icon = item.icon
                            const active = isActive(item.href)

                            return (
                                <li key={item.name}>
                                    <div className="relative group">
                                        <Link
                                            href={item.href}
                                            className={`
                                                flex items-center
                                                ${isOpen ? 'gap-3 px-3' : 'justify-center'}
                                                py-2.5 rounded-lg
                                                transition-all duration-200
                                                ${active
                                                    ? 'bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-400'
                                                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                                                }
                                            `}
                                        >
                                            <Icon className="w-5 h-5 flex-shrink-0" />
                                            {isOpen && (
                                                <span className="font-medium whitespace-nowrap">
                                                    {item.name}
                                                </span>
                                            )}
                                        </Link>
                                        {!isOpen && (
                                            <div className="absolute left-full ml-2 top-1/2 -translate-y-1/2 px-2 py-1 bg-gray-900 dark:bg-gray-700 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-[200]">
                                                {item.name}
                                            </div>
                                        )}
                                    </div>
                                </li>
                            )
                        })}
                    </ul>
                </div>

                {/* User Profile Area */}
                <div className="border-t border-gray-200 dark:border-gray-800 p-3" style={{ overflow: 'visible' }}>
                    <div className="relative group">
                        <button
                            className={`
                                w-full flex items-center
                                ${isOpen ? 'gap-3 px-3' : 'justify-center'}
                                py-2.5 rounded-lg
                                text-gray-700 dark:text-gray-300
                                hover:bg-gray-100 dark:hover:bg-gray-800
                                transition-all duration-200
                            `}
                        >
                            <Settings className="w-5 h-5 flex-shrink-0" />
                            {isOpen && <span className="font-medium">Settings</span>}
                        </button>
                        {!isOpen && (
                            <div className="absolute left-full ml-2 top-1/2 -translate-y-1/2 px-2 py-1 bg-gray-900 dark:bg-gray-700 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-[200]">
                                Settings
                            </div>
                        )}
                    </div>

                    <div
                        className={`
                            flex items-center 
                            ${isOpen ? 'gap-3 px-3' : 'justify-center'} 
                            py-2.5 mt-1 rounded-lg
                            hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer
                            transition-all duration-200
                        `}
                    >
                        <div className="w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center flex-shrink-0">
                            <User className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                        </div>
                        {isOpen && (
                            <div className="overflow-hidden">
                                <p className="text-sm font-medium text-gray-900 dark:text-white truncate">User</p>
                                <p className="text-xs text-gray-500 dark:text-gray-400 truncate">user@themoon.com</p>
                            </div>
                        )}
                    </div>
                </div>
            </aside>
        </>
    )
}
