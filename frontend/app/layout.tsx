import type { Metadata, Viewport } from 'next'
import { Inter, Playfair_Display } from 'next/font/google'
import './globals.css'
import AppLayout from '@/components/layout/AppLayout'
import Footer from '@/components/layout/Footer'
import { cookies } from 'next/headers'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const playfair = Playfair_Display({ subsets: ['latin'], variable: '--font-playfair' })

export const viewport: Viewport = {
  themeColor: '#FFF8F0',
}

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
      <body className={`${inter.variable} ${playfair.variable} font-sans min-h-screen bg-latte-50 text-latte-800`}>
        <AppLayout initialSidebarState={sidebarState?.value === 'true'}>
          <div className="flex flex-col min-h-screen">
            <div className="flex-1">
              {children}
            </div>
            <Footer />
          </div>
        </AppLayout>
      </body>
    </html>
  )
}
