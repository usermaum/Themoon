import type { Metadata, Viewport } from 'next';
import { Inter, Playfair_Display } from 'next/font/google';
import './globals.css';
import AppLayout from '@/components/layouts/AppLayout';

import { cookies } from 'next/headers';
import { SWRProvider } from '@/lib/swr-config';
import NextTopLoader from 'nextjs-toploader';
import { Toaster } from '@/components/ui/toaster';
import { LoadingProvider } from '@/components/providers/loading-provider';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });
const playfair = Playfair_Display({ subsets: ['latin'], variable: '--font-playfair' });

export const viewport: Viewport = {
  themeColor: '#FFF8F0',
};

export const metadata: Metadata = {
  title: 'The Moon Drip Bar',
  description: 'Premium Roasting Management System',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const cookieStore = cookies();
  const sidebarState = cookieStore.get('sidebar:state');

  return (
    <html lang="ko">
      <body
        className={`${inter.variable} ${playfair.variable} font-sans min-h-screen bg-latte-50 text-latte-800`}
      >
        <NextTopLoader
          color="#D97706"
          initialPosition={0.08}
          crawlSpeed={200}
          height={3}
          crawl={true}
          showSpinner={false}
          easing="ease"
          speed={200}
          shadow="0 0 10px #D97706,0 0 5px #D97706"
        />
        <LoadingProvider>
          <AppLayout initialSidebarState={sidebarState?.value === 'true'}>
            <SWRProvider>
              <div className="flex flex-col min-h-screen">
                {children}
                <div className="flex-grow" />
              </div>
              <Toaster />
            </SWRProvider>
          </AppLayout>
        </LoadingProvider>
      </body>
    </html>
  );
}
