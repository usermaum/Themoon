'use client';

import { useState, useEffect } from 'react';
import Sidebar from './Sidebar';
import Footer from './Footer';

interface AppLayoutProps {
  children: React.ReactNode;
  initialSidebarState?: boolean;
}

export default function AppLayout({ children, initialSidebarState = true }: AppLayoutProps) {
  // Initialize sidebar state from prop
  const [isSidebarOpen, setIsSidebarOpen] = useState(initialSidebarState);

  const updateSidebarWidth = (open: boolean) => {
    const width = window.innerWidth < 1024 ? '0px' : open ? '256px' : '80px';
    document.documentElement.style.setProperty('--sidebar-width', width);
  };

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 1024) {
        setIsSidebarOpen(false);
        updateSidebarWidth(false);
      } else {
        updateSidebarWidth(isSidebarOpen);
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [isSidebarOpen]);

  const toggleSidebar = () => {
    const newState = !isSidebarOpen;
    setIsSidebarOpen(newState);
    updateSidebarWidth(newState);
    document.cookie = `sidebar:state=${newState}; path=/; max-age=31536000`;
  };

  // Use 0px as default for SSR to avoid ReferenceError
  const sidebarWidth =
    typeof window !== 'undefined'
      ? window.innerWidth < 1024
        ? '0px'
        : isSidebarOpen
          ? '256px'
          : '80px'
      : '256px';

  return (
    <div
      className="flex h-screen overflow-hidden"
      style={
        {
          '--sidebar-width': sidebarWidth,
        } as React.CSSProperties
      }
    >
      <Sidebar isOpen={isSidebarOpen} onToggle={toggleSidebar} />

      <main
        className={`
                    flex-1 overflow-auto scrollbar-thin
                    transition-all duration-300 ease-in-out
                    ${isSidebarOpen ? 'lg:ml-64' : 'lg:ml-[80px]'}
                    relative z-0
                `}
      >
        {/* Theme Decorations */}
        <div className="fixed top-0 right-0 w-[500px] h-[500px] bg-blob-orange/30 rounded-full blur-[100px] pointer-events-none -z-10"></div>
        <div className="fixed bottom-0 left-0 w-[500px] h-[500px] bg-blob-green/30 rounded-full blur-[100px] pointer-events-none -z-10"></div>
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

        <div className="pt-4 lg:pt-0 min-h-full">{children}</div>
        <Footer />
      </main>
    </div>
  );
}
