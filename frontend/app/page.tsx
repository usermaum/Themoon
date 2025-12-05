"use client";

import React, { useEffect, useState } from 'react';
import { DashboardAPI, DashboardStats, LowStockBean, RecentActivity, BlendAPI, Blend } from '@/lib/api';
import {
  Grid,
  Card,
  Text,
  Group,
  RingProgress,
  ThemeIcon,
  SimpleGrid,
  Badge,
  Paper,
  Stack,
  Center,
  Loader,
  Title
} from '@mantine/core';
import {
  Package,
  DollarSign,
  ArrowUpRight,
  ArrowDownRight,
  AlertTriangle,
  LayoutDashboard,
  Activity,
  CheckCircle,
  Layers
} from 'lucide-react';
import PageHero from '@/components/ui/PageHero';
import { useLanguage } from '@/lib/i18n/LanguageContext';
import { notifications } from '@mantine/notifications';

export default function HomePage() {
  const { t } = useLanguage();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [lowStock, setLowStock] = useState<LowStockBean[]>([]);
  const [activity, setActivity] = useState<RecentActivity[]>([]);
  const [blends, setBlends] = useState<Blend[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsData, lowStockData, activityData, blendsData] = await Promise.all([
          DashboardAPI.getStats(),
          DashboardAPI.getLowStock(),
          DashboardAPI.getRecentActivity(),
          BlendAPI.getAll({ limit: 100 })
        ]);
        setStats(statsData);
        setLowStock(lowStockData);
        setActivity(activityData);
        setBlends(blendsData || []);
      } catch (error) {
        console.error("Failed to fetch dashboard data", error);
        notifications.show({
          title: 'Error',
          message: 'Failed to fetch dashboard data',
          color: 'red',
        });
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <Center h="100vh">
        <Loader size="xl" color="orange" type="dots" />
      </Center>
    );
  }

  return (
    <div>
      <PageHero
        title={t('dashboard.title')}
        description={t('dashboard.description')}
        icon={<LayoutDashboard className="w-10 h-10" />}
        backgroundImage="/images/hero/home-hero.png"
      />

      <div className="p-4 md:p-8 max-w-[1600px] mx-auto space-y-8">
        {/* Stats Overview */}
        <SimpleGrid cols={{ base: 1, sm: 2, lg: 4 }} spacing="lg">
          {/* Total Value */}
          <Card radius="xl" padding="xl" shadow="sm" className="hover:shadow-md transition-all">
            <Group justify="space-between" align="flex-start">
              <Stack gap="xs">
                <Text size="sm" c="dimmed" fw={700} tt="uppercase">{t('dashboard.totalValue')}</Text>
                <Text size="xl" fw={700} style={{ fontFamily: 'var(--font-playfair)', fontSize: '2rem' }}>
                  ₩{stats?.total_value.toLocaleString()}
                </Text>
                <Text size="xs" c="green" fw={500} mt="sm">
                  {t('dashboard.estimatedCost')}
                </Text>
              </Stack>
              <ThemeIcon size={48} radius="xl" variant="light" color="indigo">
                <DollarSign size={24} />
              </ThemeIcon>
            </Group>
          </Card>

          {/* Total Weight */}
          <Card radius="xl" padding="xl" shadow="sm" className="hover:shadow-md transition-all">
            <Group justify="space-between" align="flex-start">
              <Stack gap="xs">
                <Text size="sm" c="dimmed" fw={700} tt="uppercase">{t('dashboard.totalWeight')}</Text>
                <Text size="xl" fw={700} style={{ fontFamily: 'var(--font-playfair)', fontSize: '2rem' }}>
                  {stats?.total_weight.toLocaleString()} kg
                </Text>
                <Text size="xs" c="dimmed" mt="sm">
                  {t('dashboard.acrossTypes').replace('{count}', stats?.total_beans.toString() || '0')}
                </Text>
              </Stack>
              <ThemeIcon size={48} radius="xl" variant="light" color="orange">
                <Package size={24} />
              </ThemeIcon>
            </Group>
          </Card>

          {/* Blends Count - Added to match old home page data */}
          <Card radius="xl" padding="xl" shadow="sm" className="hover:shadow-md transition-all">
            <Group justify="space-between" align="flex-start">
              <Stack gap="xs">
                <Text size="sm" c="dimmed" fw={700} tt="uppercase">{t('blends.title') || 'Blend Recipes'}</Text>
                <Text size="xl" fw={700} style={{ fontFamily: 'var(--font-playfair)', fontSize: '2rem' }}>
                  {blends.length}
                </Text>
                <Text size="xs" c="dimmed" mt="sm">
                  Active Recipes
                </Text>
              </Stack>
              <ThemeIcon size={48} radius="xl" variant="light" color="grape">
                <Layers size={24} />
              </ThemeIcon>
            </Group>
          </Card>

          {/* Low Stock */}
          <Card radius="xl" padding="xl" shadow="sm" className="hover:shadow-md transition-all">
            <Group justify="space-between" align="flex-start">
              <Stack gap="xs">
                <Text size="sm" c="dimmed" fw={700} tt="uppercase">{t('dashboard.lowStockItems')}</Text>
                <Text size="xl" fw={700} c={lowStock.length > 0 ? "red" : "green"} style={{ fontFamily: 'var(--font-playfair)', fontSize: '2rem' }}>
                  {lowStock.length}
                </Text>
                <Text size="xs" c={lowStock.length > 0 ? "red" : "green"} mt="sm" fw={500}>
                  {lowStock.length > 0 ? t('dashboard.itemsBelowThreshold') : t('dashboard.allStockHealthy')}
                </Text>
              </Stack>
              <RingProgress
                size={60}
                thickness={6}
                roundCaps
                sections={[
                  { value: lowStock.length * 10, color: lowStock.length > 0 ? 'red' : 'green' }
                ]}
                label={
                  <Center>
                    <AlertTriangle size={16} color={lowStock.length > 0 ? 'var(--mantine-color-red-6)' : 'var(--mantine-color-green-6)'} />
                  </Center>
                }
              />
            </Group>
          </Card>
        </SimpleGrid>

        <Grid gutter="lg">
          {/* Recent Activity */}
          <Grid.Col span={{ base: 12, md: 8 }}>
            <Card radius="xl" padding="lg" shadow="sm" h="100%">
              <Group justify="space-between" mb="lg">
                <Group gap="xs">
                  <Activity size={20} className="text-stone-500" />
                  <Title order={4} style={{ fontFamily: 'var(--font-playfair)' }}>{t('dashboard.recentActivity')}</Title>
                </Group>
              </Group>

              <Stack gap="md">
                {activity.map((item) => (
                  <Paper key={item.id} p="md" radius="lg" bg="gray.0" withBorder>
                    <Group justify="space-between">
                      <Group>
                        <ThemeIcon
                          radius="xl"
                          size="lg"
                          variant="light"
                          color={item.type.includes('IN') ? 'green' : 'blue'}
                        >
                          {item.type.includes('IN') ? <ArrowDownRight size={18} /> : <ArrowUpRight size={18} />}
                        </ThemeIcon>
                        <div>
                          <Text fw={600} size="sm">{item.bean_name}</Text>
                          <Text size="xs" c="dimmed" tt="uppercase">{item.type}</Text>
                        </div>
                      </Group>
                      <Group gap="xl">
                        <Text size="sm" c="dimmed" visibleFrom="xs">
                          {new Date(item.date).toLocaleDateString()}
                        </Text>
                        <Badge
                          size="lg"
                          variant="light"
                          color={item.type.includes('IN') ? 'green' : 'blue'}
                        >
                          {item.type.includes('IN') ? '+' : '-'}{item.amount} kg
                        </Badge>
                      </Group>
                    </Group>
                  </Paper>
                ))}
                {activity.length === 0 && (
                  <Center py="xl">
                    <Text c="dimmed">No recent activity.</Text>
                  </Center>
                )}
              </Stack>
            </Card>
          </Grid.Col>

          {/* Low Stock Alerts */}
          <Grid.Col span={{ base: 12, md: 4 }}>
            <Card radius="xl" padding="lg" shadow="sm" h="100%" bg="red.0" style={{ borderColor: 'var(--mantine-color-red-2)' }}>
              <Group justify="space-between" mb="lg">
                <Group gap="xs">
                  <AlertTriangle size={20} className="text-red-500" />
                  <Title order={4} c="red.9" style={{ fontFamily: 'var(--font-playfair)' }}>{t('dashboard.lowStockAlerts')}</Title>
                </Group>
              </Group>

              <Stack>
                {lowStock.length > 0 ? (
                  lowStock.map((bean) => (
                    <Paper key={bean.id} p="md" radius="lg" bg="white" shadow="xs">
                      <Group justify="space-between" align="center">
                        <div>
                          <Text fw={600} c="red.9">{bean.name}</Text>
                          <Text size="xs" c="red.5">{t('dashboard.threshold')}: {bean.threshold}kg</Text>
                        </div>
                        <Stack align="flex-end" gap={0}>
                          <Text fw={700} c="red.7" size="lg">{bean.quantity_kg}</Text>
                          <Text size="xs" c="red.5">kg remaining</Text>
                        </Stack>
                      </Group>
                    </Paper>
                  ))
                ) : (
                  <Center h="100%" py="xl" style={{ flexDirection: 'column', gap: 16 }}>
                    <ThemeIcon radius="50%" size={60} color="green" variant="light">
                      <CheckCircle size={30} />
                    </ThemeIcon>
                    <Text ta="center" c="green.8" fw={500}>
                      All stock levels are healthy!
                    </Text>
                  </Center>
                )}
              </Stack>
            </Card>
          </Grid.Col>
        </Grid>
      </div>
    </div>
  );
}
