'use client'

import { useState, useEffect } from 'react'
import Sidebar from './Sidebar'

interface AppLayoutProps {
    children: React.ReactNode
    initialSidebarState?: boolean
}

export default function AppLayout({ children, initialSidebarState = true }: AppLayoutProps) {
    // Initialize sidebar state from prop
    const [isSidebarOpen, setIsSidebarOpen] = useState(initialSidebarState)

    useEffect(() => {
        // Only add resize listener if we want responsive behavior
        // But if we want to persist user choice, we should be careful about overriding it.
        // Let's keep the mobile check: if screen is small, always close.
        const handleResize = () => {
            if (window.innerWidth < 1024) {
                setIsSidebarOpen(false)
            }
            // If >= 1024, we don't necessarily force open, we respect the user's choice (or initial state).
            // However, if we just resized from mobile to desktop, maybe we should restore?
            // For now, let's just handle the mobile closing case to prevent broken layout.
        }

        // Check on mount (in case of hydration mismatch or just initial check)
        handleResize()

        window.addEventListener('resize', handleResize)
        return () => window.removeEventListener('resize', handleResize)
    }, [])

    const toggleSidebar = () => {
        const newState = !isSidebarOpen
        setIsSidebarOpen(newState)
        // Set cookie
        document.cookie = `sidebar:state=${newState}; path=/; max-age=31536000` // 1 year
    }

    return (
        <div className="flex h-screen overflow-hidden">
            <Sidebar isOpen={isSidebarOpen} onToggle={toggleSidebar} />

            <main
                className={`
                    flex-1 overflow-auto scrollbar-thin
                    transition-all duration-300 ease-in-out
                    ${isSidebarOpen ? 'lg:ml-64' : 'lg:ml-16'}
                    relative z-0
                `}
            >
                {/* Mobile menu button */}
                <div className="lg:hidden fixed top-4 left-4 z-30">
                    <button
                        onClick={toggleSidebar}
                        className="p-2 rounded-lg bg-white dark:bg-gray-800 shadow-lg border border-gray-200 dark:border-gray-700"
                        aria-label="Toggle menu"
                    >
                        <svg
                            className="w-6 h-6 text-gray-600 dark:text-gray-300"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M4 6h16M4 12h16M4 18h16"
                            />
                        </svg>
                    </button>
                </div>

                <div className="pt-4 lg:pt-0">
                    {children}
                </div>
            </main>
        </div>
    )
}
