'use client'

import AppLayout from '@/components/layout/AppLayout'
import Footer from '@/components/layout/Footer'

interface ClientLayoutProps {
    children: React.ReactNode
    initialSidebarState: boolean
}

export default function ClientLayout({ children, initialSidebarState }: ClientLayoutProps) {
    return (
        <AppLayout initialSidebarState={initialSidebarState}>
            {children}
            <Footer />
        </AppLayout>
    )
}
