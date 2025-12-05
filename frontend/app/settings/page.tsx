"use client";

import React from 'react';
import { Container, Paper, Title, Text, Stack, Group, Switch, Divider, Badge, Button } from '@mantine/core';
import { Settings as SettingsIcon, Globe, Database, Info } from 'lucide-react';
import PageHero from '@/components/ui/PageHero';
import { useLanguage } from '@/lib/i18n/LanguageContext';

export default function SettingsPage() {
    const { language, setLanguage, t } = useLanguage();

    return (
        <div>
            <PageHero
                title="Settings"
                description="Application Configuration & Information"
                icon={<SettingsIcon className="w-10 h-10" />}
                backgroundImage="/images/hero/inventory-hero.png" // Re-use inventory hero or placeholder
            />

            <Container size="md" py="xl">
                <Stack gap="xl">

                    {/* General Settings */}
                    <Paper withBorder p="xl" radius="md">
                        <Group justify="space-between" mb="md">
                            <Group>
                                <Globe size={20} />
                                <Title order={4}>General Settings</Title>
                            </Group>
                        </Group>
                        <Divider mb="md" />

                        <Group justify="space-between">
                            <Stack gap={0}>
                                <Text fw={500}>Application Language</Text>
                                <Text size="sm" c="dimmed">Select your preferred interface language</Text>
                            </Stack>
                            <Group>
                                <Button
                                    variant={language === 'ko' ? 'filled' : 'light'}
                                    color="indigo"
                                    onClick={() => setLanguage('ko')}
                                >
                                    한국어
                                </Button>
                                <Button
                                    variant={language === 'en' ? 'filled' : 'light'}
                                    color="indigo"
                                    onClick={() => setLanguage('en')}
                                >
                                    English
                                </Button>
                            </Group>
                        </Group>
                    </Paper>

                    {/* System Info */}
                    <Paper withBorder p="xl" radius="md">
                        <Group justify="space-between" mb="md">
                            <Group>
                                <Info size={20} />
                                <Title order={4}>System Information</Title>
                            </Group>
                        </Group>
                        <Divider mb="md" />

                        <Stack gap="xs">
                            <Group justify="space-between">
                                <Text>App Version</Text>
                                <Badge color="blue">v0.1.0</Badge>
                            </Group>
                            <Group justify="space-between">
                                <Text>Environment</Text>
                                <Badge color="green">Production</Badge>
                            </Group>
                            <Group justify="space-between">
                                <Text>Latest Update</Text>
                                <Text size="sm" c="dimmed">2025-12-06</Text>
                            </Group>
                        </Stack>
                    </Paper>

                    {/* Database Status (Mock for now) */}
                    <Paper withBorder p="xl" radius="md">
                        <Group justify="space-between" mb="md">
                            <Group>
                                <Database size={20} />
                                <Title order={4}>Database Status</Title>
                            </Group>
                            <Badge color="green" variant="dot">Connected</Badge>
                        </Group>
                        <Divider mb="md" />
                        <Text size="sm" c="dimmed">
                            PostgreSQL database is active and responding.
                        </Text>
                    </Paper>

                </Stack>
            </Container>
        </div>
    );
}
