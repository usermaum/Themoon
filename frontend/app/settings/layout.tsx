'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, ScrollText, Settings, Wrench } from 'lucide-react';
import { cn } from '@/lib/utils';
import PageHero from '@/components/ui/page-hero';

export default function SettingsLayout({ children }: { children: React.ReactNode }) {
    const pathname = usePathname();

    const tabs = [
        { name: '설정', href: '/settings', icon: Settings },
        { name: '대시보드', href: '/settings/dashboard', icon: LayoutDashboard },
        { name: '로그 뷰어', href: '/settings/logs', icon: ScrollText },
        { name: '관리자 도구', href: '/settings/system', icon: Wrench },
    ];

    return (
        <div className="min-h-screen bg-latte-50/50 pb-20">
            <PageHero
                title="System Settings"
                description="시스템 설정 및 상태 모니터링"
                icon={<Settings className="w-10 h-10" />}
                image="/images/hero/settings-hero.png"
            />

            <div className="container mx-auto px-4 max-w-7xl relative z-10 mt-8">
                <div className="max-w-5xl mx-auto space-y-8">
                    <div className="bg-latte-100 rounded-xl p-1 flex items-center gap-1 shadow-sm border border-latte-200/50 overflow-x-auto">
                        {tabs.map((tab) => {
                            const isActive = pathname === tab.href;
                            const Icon = tab.icon;
                            return (
                                <Link
                                    key={tab.href}
                                    href={tab.href}
                                    className={cn(
                                        'flex-1 flex items-center justify-center gap-2 px-6 py-2.5 rounded-lg text-sm font-bold transition-all whitespace-nowrap',
                                        isActive
                                            ? 'bg-white text-latte-900 shadow-sm'
                                            : 'text-latte-500 hover:text-latte-700 hover:bg-white/50'
                                    )}
                                >
                                    <Icon className="w-4 h-4" />
                                    {tab.name}
                                </Link>
                            );
                        })}
                    </div>

                    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                        {children}
                    </div>
                </div>
            </div>
        </div>
    );
}
