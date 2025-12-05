import type { Metadata } from 'next'
import { Inter, Playfair_Display } from 'next/font/google'
import './globals.css'
import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';
import { Notifications } from '@mantine/notifications';
import { ColorSchemeScript, MantineProvider, createTheme } from '@mantine/core'
import { MainShell } from '@/components/layout/MainShell'
import { cookies } from 'next/headers'
import { LanguageProvider } from '@/lib/i18n/LanguageContext'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const playfair = Playfair_Display({ subsets: ['latin'], variable: '--font-playfair' })

import { theme } from '@/theme'

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
  // const sidebarState = cookieStore.get('sidebar:state') // Mantine handles state internally or via other means if needed

  return (
    <html lang="ko">
      <head>
        <ColorSchemeScript />
      </head>
      <body className={`${inter.className} ${playfair.variable} min-h-screen bg-[#FFF8F0] dark:bg-zinc-900`}>
        <MantineProvider theme={theme}>
          <Notifications />
          <LanguageProvider>
            <MainShell>
              {children}
            </MainShell>
          </LanguageProvider>
        </MantineProvider>
      </body>
    </html>
  )
}
