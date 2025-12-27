'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
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
  FileText,
  BarChart3,
} from 'lucide-react';

import { useLoading } from '@/components/providers/loading-provider';

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
}

export default function Sidebar({ isOpen, onToggle }: SidebarProps) {
  const pathname = usePathname();
  const { startLoading } = useLoading();

  const navItems = [
    { name: 'Home', href: '/', icon: Home },
    { name: 'Beans', href: '/beans', icon: Coffee },
    { name: 'Roasting', href: '/roasting', icon: Flame },
    { name: 'Blends', href: '/blends', icon: Layers },
    { name: 'Inventory', href: '/inventory', icon: Package },
    { name: 'Inbound', href: '/inventory/inbound', icon: FileText },
    { name: 'Analytics', href: '/analytics', icon: BarChart3 },

  ];

  const isActive = (href: string) => {
    if (href === '/') {
      return pathname === '/';
    }
    return pathname.startsWith(href);
  };

  // Handle Navigation Click
  const handleNavigation = (href: string) => {
    if (pathname !== href) {
      startLoading();
    }
  };

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
        <div
          className={`
                    h-24 flex items-center relative overflow-hidden
                    ${isOpen ? 'px-6' : 'justify-center'} 
                    border-b border-latte-200/50
                `}
        >
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
                <h1 className="font-serif text-3xl font-bold text-latte-900 tracking-tighter leading-none">
                  The Moon
                </h1>
                <p className="text-xs font-bold text-latte-600 tracking-[0.3em] uppercase ml-1">
                  Drip Bar
                </p>
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
            const Icon = item.icon;
            const active = isActive(item.href);

            return (
              <div key={item.name} className="relative group">
                <Link
                  href={item.href}
                  onClick={() => handleNavigation(item.href)}
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
            );
          })}
        </div>

        {/* Settings Area (Replaces User Profile) */}
        <div className="p-4 border-t border-latte-200/50">
          <Link
            href="/settings"
            onClick={() => handleNavigation('/settings')}
            className={`
                    flex items-center
                    ${isOpen ? 'gap-4 px-4' : 'justify-center'}
                    py-3 rounded-2xl
                    transition-all duration-300
                    ${isActive('/settings')
                ? 'bg-white shadow-md text-latte-800'
                : 'text-latte-600 hover:bg-latte-100 hover:text-latte-800'
              }
                `}
          >
            <Settings className={`flex-shrink-0 ${isActive('/settings') ? 'w-5 h-5' : 'w-5 h-5 opacity-80'}`} />
            {isOpen && (
              <span className={`font-medium ${isActive('/settings') ? 'font-serif' : 'font-sans'}`}>
                Settings
              </span>
            )}
          </Link>
        </div>
      </aside>
    </>
  );
}
