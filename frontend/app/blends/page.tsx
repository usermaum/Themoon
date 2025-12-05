"use client";

import React, { useState, useEffect } from 'react';
import {
    Container,
    Grid,
    Card,
    Image,
    Text,
    Badge,
    Button,
    Group,
    Stack,
    Skeleton,
    Alert,
    Center,
    ActionIcon,
    Menu,
    rem
} from '@mantine/core';
import {
    Plus,
    MoreVertical,
    Edit,
    Trash2,
    Layers,
    AlertCircle
} from 'lucide-react';
import { useRouter } from 'next/navigation';
import { useLanguage } from '@/lib/i18n/LanguageContext';
import PageHero from '@/components/ui/PageHero';
import { Blend, BlendAPI } from '@/lib/api';
import { notifications } from '@mantine/notifications';

export default function BlendsPage() {
    const { t } = useLanguage();
    const router = useRouter();
    const [blends, setBlends] = useState<Blend[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetchBlends();
    }, []);

    const fetchBlends = async () => {
        try {
            setLoading(true);
            const data = await BlendAPI.getAll({});
            setBlends(data);
        } catch (err) {
            console.error('Failed to fetch blends:', err);
            setError('Failed to load blend recipes.');
            notifications.show({
                title: 'Error',
                message: 'Failed to load blend recipes.',
                color: 'red',
            });
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id: number) => {
        if (!confirm(t('common.confirmDelete') || 'Are you sure you want to delete this blend?')) return;

        try {
            await BlendAPI.delete(id);

            setBlends(blends.filter(b => b.id !== id));
            notifications.show({
                title: 'Success',
                message: 'Blend recipe deleted.',
                color: 'green',
            });
        } catch (err) {
            console.error(err);
            notifications.show({
                title: 'Error',
                message: 'Failed to delete blend.',
                color: 'red',
            });
        }
    };

    return (
        <div>
            <PageHero
                title={t('blends.title') || "Blends"}
                description={t('blends.description') || "Create and manage coffee blends"}
                icon={<Layers className="w-10 h-10" />}
                backgroundImage="/images/hero/blends-hero.png"
            />

            <Container size="xl" py="xl">
                <Group justify="flex-end" mb="xl">
                    <Button
                        leftSection={<Plus size={20} />}
                        onClick={() => router.push('/blends/new')}
                        size="md"
                        color="orange"
                    >
                        Create New Blend
                    </Button>
                </Group>

                {error && (
                    <Alert icon={<AlertCircle size={16} />} title="Error" color="red" mb="xl">
                        {error}
                    </Alert>
                )}

                {loading ? (
                    <Grid>
                        {[1, 2, 3].map(i => (
                            <Grid.Col key={i} span={{ base: 12, sm: 6, lg: 4 }}>
                                <Skeleton height={300} radius="xl" />
                            </Grid.Col>
                        ))}
                    </Grid>
                ) : blends.length === 0 ? (
                    <Center py={60}>
                        <Stack align="center" gap="md" c="dimmed">
                            <Layers size={48} strokeWidth={1} />
                            <Text size="lg">No blend recipes found</Text>
                            <Button variant="light" onClick={() => router.push('/blends/new')}>
                                Create your first blend
                            </Button>
                        </Stack>
                    </Center>
                ) : (
                    <Grid>
                        {blends.map((blend) => (
                            <Grid.Col key={blend.id} span={{ base: 12, sm: 6, lg: 4 }}>
                                <Card padding="lg" radius="xl" withBorder className="h-full hover:shadow-md transition-shadow">
                                    <Card.Section>
                                        <Image
                                            src="/images/blend-placeholder.jpg"
                                            height={200}
                                            alt={blend.name}
                                            fallbackSrc="https://placehold.co/600x400?text=Blend"
                                        />
                                    </Card.Section>

                                    <Group justify="space-between" mt="md" mb="xs">
                                        <Text fw={700} size="xl" style={{ fontFamily: 'var(--font-playfair)' }}>
                                            {blend.name}
                                        </Text>
                                        <Menu withinPortal position="bottom-end" shadow="sm">
                                            <Menu.Target>
                                                <ActionIcon variant="subtle" color="gray">
                                                    <MoreVertical size={16} />
                                                </ActionIcon>
                                            </Menu.Target>
                                            <Menu.Dropdown>
                                                <Menu.Item leftSection={<Edit size={14} />} onClick={() => router.push(`/blends/${blend.id}`)}>
                                                    View Details
                                                </Menu.Item>
                                                <Menu.Item
                                                    leftSection={<Trash2 size={14} />}
                                                    color="red"
                                                    onClick={() => handleDelete(blend.id)}
                                                >
                                                    Delete
                                                </Menu.Item>
                                            </Menu.Dropdown>
                                        </Menu>
                                    </Group>

                                    <Text size="sm" c="dimmed" lineClamp={2} mb="md" h={40}>
                                        {blend.description || "No description provided."}
                                    </Text>

                                    <Group gap="xs" mb="md">
                                        {blend.target_roast_level && (
                                            <Badge variant="light" color="brown">
                                                {blend.target_roast_level}
                                            </Badge>
                                        )}
                                        {/* Add more badges if data available, e.g. ratio count */}
                                    </Group>

                                    <Button
                                        variant="light"
                                        color="orange"
                                        fullWidth
                                        mt="auto"
                                        radius="xl"
                                        onClick={() => router.push(`/blends/${blend.id}`)}
                                    >
                                        View Recipe
                                    </Button>
                                </Card>
                            </Grid.Col>
                        ))}
                    </Grid>
                )}
            </Container>
        </div>
    );
}
