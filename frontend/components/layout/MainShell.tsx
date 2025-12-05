'use client';

import { AppShell, Burger, Group, Title, NavLink, ScrollArea, useMantineColorScheme, ActionIcon, Flex, Tooltip, Avatar, Text, UnstyledButton } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { useState, useEffect } from 'react';
import {
    Home,
    LayoutDashboard,
    Flame,
    Coffee,
    Layers,
    Package,
    Truck,
    Sun,
    Moon,
    Globe,
    LogOut
} from 'lucide-react';
import { useLanguage } from '@/lib/i18n/LanguageContext';

interface MainShellProps {
    children: React.ReactNode;
}

export function MainShell({ children }: MainShellProps) {
    const [mounted, setMounted] = useState(false);
    const { t, language, setLanguage } = useLanguage();
    const { colorScheme, toggleColorScheme } = useMantineColorScheme();
    const [opened, { toggle }] = useDisclosure();
    const pathname = usePathname();

    useEffect(() => {
        setMounted(true);
    }, []);

    const navItems = [
        { name: t('nav.home'), href: '/', icon: LayoutDashboard }, // Home is now Dashboard
        { name: t('nav.roasting'), href: '/roasting', icon: Flame },
        { name: t('nav.beans'), href: '/beans', icon: Coffee },
        { name: t('nav.blends'), href: '/blends', icon: Layers },
        { name: t('nav.inventory'), href: '/inventory', icon: Package },
        { name: t('nav.inbound'), href: '/inbound', icon: Truck },
    ];

    const handleLanguageToggle = () => {
        setLanguage(language === 'ko' ? 'en' : 'ko');
    };

    return (
        <AppShell
            layout="alt"
            header={{ height: 80 }}
            navbar={{
                width: 300, // Slightly wider for artistic feel
                breakpoint: 'sm',
                collapsed: { mobile: !opened },
            }}
            padding="md"
            styles={{
                main: {
                    backgroundColor: 'transparent',
                },
                root: {
                }
            }}
        >
            <AppShell.Header style={{ backgroundColor: 'transparent', borderBottom: 'none' }}>
                <Group h="100%" px="xl" justify="flex-end" style={{ backdropFilter: 'blur(0px)' }}>
                    <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" mr="auto" />

                    <Group gap="lg">
                        {/* Search Bar Placeholder matching design lab */}
                        <div style={{ position: 'relative', display: 'none' }} className="hidden md:block">
                            {/* Add search later if functional */}
                        </div>

                        <Tooltip label={language === 'ko' ? 'Switch to English' : '한국어로 전환'}>
                            <ActionIcon
                                variant="subtle"
                                size="lg"
                                radius="xl"
                                color="gray"
                                onClick={handleLanguageToggle}
                                aria-label="Toggle language"
                            >
                                <Globe size={22} style={{ color: '#8D7B68' }} />
                                <span
                                    style={{ fontSize: '9px', position: 'absolute', bottom: 0, right: 0, fontWeight: 'bold', color: '#4A403A' }}
                                    suppressHydrationWarning
                                >
                                    {language.toUpperCase()}
                                </span>
                            </ActionIcon>
                        </Tooltip>

                        <ActionIcon
                            variant="subtle"
                            size="lg"
                            radius="xl"
                            color="gray"
                            onClick={() => toggleColorScheme()}
                            aria-label="Toggle color scheme"
                        >
                            {!mounted ? (
                                <div style={{ width: 22, height: 22 }} />
                            ) : (
                                colorScheme === 'dark' ? <Sun size={22} style={{ color: '#e6dbd3' }} /> : <Moon size={22} style={{ color: '#8D7B68' }} />
                            )}
                        </ActionIcon>

                        <UnstyledButton>
                            <Group gap="xs">
                                <Avatar
                                    src={null}
                                    alt="User"
                                    radius="xl"
                                    size="md"
                                    color="orange"
                                    style={{ border: '2px solid #E6D5C3' }}
                                >
                                    PM
                                </Avatar>
                                <div style={{ flex: 1 }}>
                                    <Text size="sm" fw={500} style={{ color: '#4A403A' }}>
                                        Pmaum
                                    </Text>
                                    <Text c="dimmed" size="xs">
                                        Head Roaster
                                    </Text>
                                </div>
                            </Group>
                        </UnstyledButton>
                    </Group>
                </Group>
            </AppShell.Header>

            <AppShell.Navbar p="0" style={{ backgroundColor: 'rgba(255, 255, 255, 0.5)', backdropFilter: 'blur(20px)', borderRight: '1px solid rgba(230, 213, 195, 0.5)' }}>
                {/* Logo Section with Orbs */}
                <div style={{ height: '160px', position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', borderBottom: '1px solid rgba(230,213,195,0.5)', overflow: 'hidden' }}>
                    <div style={{ position: 'absolute', top: '-40px', left: '-40px', width: '128px', height: '128px', backgroundColor: '#FFD6BA', borderRadius: '50%', filter: 'blur(32px)', opacity: 0.5 }}></div>
                    <div style={{ position: 'absolute', bottom: '-40px', right: '-40px', width: '128px', height: '128px', backgroundColor: '#C3E2DD', borderRadius: '50%', filter: 'blur(32px)', opacity: 0.5 }}></div>

                    <Link href="/" style={{ textDecoration: 'none', color: 'inherit', display: 'flex', flexDirection: 'column', alignItems: 'center', zIndex: 10 }}>
                        <Title order={2} style={{ fontFamily: 'var(--font-playfair)', fontWeight: 700, color: '#4A403A', fontSize: '2rem' }}>
                            The Moon
                        </Title>
                        <Text size="xs" span style={{ letterSpacing: '0.2em', color: '#8D7B68', marginTop: '4px', textTransform: 'uppercase' }}>
                            Artisan Coffee
                        </Text>
                    </Link>
                </div>

                <ScrollArea style={{ height: 'calc(100vh - 160px - 80px)' }} px="md">
                    <Flex direction="column" gap="sm" pt="xl">
                        {navItems.map((item) => {
                            const active = item.href === '/' ? pathname === '/' : pathname.startsWith(item.href);
                            return (
                                <NavLink
                                    key={item.name}
                                    component={Link}
                                    href={item.href}
                                    label={<Text fw={500} size="md" style={{ fontFamily: active ? 'var(--font-playfair)' : 'inherit' }}>{item.name}</Text>}
                                    leftSection={<item.icon size={22} strokeWidth={1.5} />}
                                    active={active}
                                    variant="subtle"
                                    color="orange"
                                    h={56}
                                    style={{
                                        borderRadius: '20px',
                                        color: active ? '#4A403A' : '#8D7B68',
                                        backgroundColor: active ? '#FFF' : 'transparent',
                                        boxShadow: active ? '0 4px 12px rgba(74, 64, 58, 0.05)' : 'none',
                                    }}
                                    className="hover:bg-white/50 transition-all duration-300"
                                />
                            );
                        })}
                    </Flex>
                </ScrollArea>

                <div style={{ padding: '16px' }} className="mt-auto">
                    <NavLink
                        label="Log out"
                        leftSection={<LogOut size={20} />}
                        variant="subtle"
                        color="gray"
                        style={{ borderRadius: '12px', color: '#8D7B68' }}
                    />
                </div>
            </AppShell.Navbar>

            <AppShell.Main>
                {/* Background Decor Elements from Design Lab */}
                <div style={{ position: 'fixed', top: 0, right: 0, width: '500px', height: '500px', backgroundColor: '#FFD6BA', borderRadius: '50%', filter: 'blur(100px)', opacity: 0.2, pointerEvents: 'none', zIndex: -1 }}></div>
                <div style={{ position: 'fixed', bottom: 0, left: 0, width: '500px', height: '500px', backgroundColor: '#C3E2DD', borderRadius: '50%', filter: 'blur(100px)', opacity: 0.2, pointerEvents: 'none', zIndex: -1 }}></div>

                {children}
            </AppShell.Main>
        </AppShell>
    );
}
