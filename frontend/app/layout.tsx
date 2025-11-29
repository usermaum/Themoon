import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import AppLayout from '@/components/layout/AppLayout'
import Footer from '@/components/layout/Footer'
import { cookies } from 'next/headers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'The Moon Drip Bar',
  description: 'Premium Roasting Management System',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const cookieStore = cookies()
  const sidebarState = cookieStore.get('sidebar:state')

  return (
    <html lang="ko">
      <body className={`${inter.className} min-h-screen bg-gray-50 dark:bg-gray-900`}>
        <AppLayout initialSidebarState={sidebarState?.value === 'true'}>
          {children}
          <Footer />
        </AppLayout>
      </body>
    </html>
  )
}
