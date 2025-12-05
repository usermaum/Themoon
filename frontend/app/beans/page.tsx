'use client';

import { useState, useEffect, useCallback } from 'react';
import { Bean, BeanAPI } from '@/lib/api';
import Link from 'next/link';
import {
    Container,
    Title,
    Group,
    Button,
    Paper,
    SegmentedControl,
    TextInput,
    Table,
    Badge,
    Pagination,
    ActionIcon,
    Text,
    Center,
    LoadingOverlay
} from '@mantine/core';
import { Search, Plus, Trash, MapPin, Package } from 'lucide-react';
import PageHero from '@/components/ui/PageHero';
import { useLanguage } from '@/lib/i18n/LanguageContext';
import { notifications } from '@mantine/notifications';

export default function BeanManagementPage() {
    const { t } = useLanguage();
    const [beans, setBeans] = useState<Bean[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [search, setSearch] = useState('');
    const [filterType, setFilterType] = useState<'all' | 'green' | 'roasted'>('all');

    // 데이터 로드 함수를 useCallback으로 감싸서 의존성 관리
    const fetchBeans = useCallback(async () => {
        try {
            setLoading(true);

            let roastLevelParam: string | undefined = undefined;
            if (filterType === 'green') roastLevelParam = 'Green';
            if (filterType === 'roasted') roastLevelParam = 'Roasted';

            const data = await BeanAPI.getAll({
                page,
                size: 10,
                search: search || undefined,
                roast_level: roastLevelParam
            });
            // 데이터 안전성 확보
            setBeans(data.items || []);
            setTotalPages(data.pages);
            setError(null);
        } catch (err) {
            console.error('Failed to fetch beans:', err);
            setError('원두 목록을 불러오는데 실패했습니다.');
            setBeans([]);
        } finally {
            setLoading(false);
        }
    }, [page, search, filterType]);

    // page, search, filterType이 변경될 때마다 데이터 로드
    useEffect(() => {
        fetchBeans();
    }, [fetchBeans]);

    // 검색어 변경 핸들러 (페이지 1로 초기화)
    const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearch(e.target.value);
        setPage(1);
    };

    // 필터 변경 핸들러 (페이지 1로 초기화)
    const handleFilterChange = (value: string) => {
        setFilterType(value as any);
        setPage(1);
    };

    const handleDelete = async (id: number) => {
        if (!confirm('정말로 이 원두를 삭제하시겠습니까?')) return;

        try {
            await BeanAPI.delete(id);
            fetchBeans();
        } catch (err) {
            notifications.show({
                title: 'Error',
                message: '삭제에 실패했습니다.',
                color: 'red',
            });
        }
    };

    // Table Rows
    const rows = (beans || []).map((bean) => (
        <Table.Tr key={bean.id}>
            <Table.Td>
                <Link href={`/beans/${bean.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                    <Text fw={500} c="indigo">{bean.name}</Text>
                    <Text size="xs" c="dimmed">{bean.created_at && new Date(bean.created_at).toLocaleDateString()}</Text>
                </Link>
            </Table.Td>
            <Table.Td>
                <Group gap="xs">
                    <Badge variant="light" color="gray" leftSection={<MapPin size={10} />}>{bean.origin}</Badge>
                    <Text size="sm">{bean.variety}</Text>
                </Group>
            </Table.Td>
            <Table.Td>
                <Badge
                    variant="dot"
                    color={bean.roast_level === 'Green' ? 'green' : 'orange'}
                >
                    {bean.roast_level}
                </Badge>
            </Table.Td>
            <Table.Td>
                <Text fw={500} c={bean.quantity_kg < 5 ? 'red' : undefined}>
                    {bean.quantity_kg.toFixed(2)} kg
                </Text>
            </Table.Td>
            <Table.Td>
                <Text size="sm">₩{bean.purchase_price_per_kg?.toLocaleString() || '0'}</Text>
            </Table.Td>
            <Table.Td style={{ textAlign: 'right' }}>
                <ActionIcon variant="subtle" color="red" onClick={() => handleDelete(bean.id)}>
                    <Trash size={16} />
                </ActionIcon>
            </Table.Td>
        </Table.Tr>
    ));

    return (
        <div>
            <PageHero
                title={t('beans.title') || 'Raw Beans'} // Fallback if t returns key
                description={t('beans.description') || 'Manage your coffee bean inventory'}
                icon={<Package className="w-10 h-10" />}
                backgroundImage="/images/hero/beans-hero.png"
            />
            <Container size="xl" py="xl">
                {/* Header */}
                <Group justify="flex-end" mb="lg">
                    <Button
                        component={Link}
                        href="/beans/new"
                        leftSection={<Plus size={18} />}
                        color="orange"
                    >
                        Add New Bean
                    </Button>
                </Group>

                {/* Filters */}
                <Paper p="md" mb="lg" radius="md">
                    <Group justify="space-between">
                        <SegmentedControl
                            value={filterType}
                            onChange={handleFilterChange}
                            data={[
                                { label: 'All Beans', value: 'all' },
                                { label: 'Green Beans', value: 'green' },
                                { label: 'Roasted Beans', value: 'roasted' },
                            ]}
                        />
                        <TextInput
                            placeholder="Search beans..."
                            leftSection={<Search size={16} />}
                            value={search}
                            onChange={handleSearchChange}
                            style={{ flex: 1, maxWidth: 400 }}
                        />
                    </Group>
                </Paper>

                {/* Error */}
                {error && (
                    <Paper p="md" mb="lg" bg="red.0" c="red">
                        {error}
                    </Paper>
                )}

                {/* Table */}
                <Paper shadow="sm" radius="md" p="md" pos="relative">
                    <LoadingOverlay visible={loading} zIndex={100} overlayProps={{ radius: "sm", blur: 2 }} />
                    <Table.ScrollContainer minWidth={800}>
                        <Table verticalSpacing="sm">
                            <Table.Thead>
                                <Table.Tr>
                                    <Table.Th>Name</Table.Th>
                                    <Table.Th>Origin / Variety</Table.Th>
                                    <Table.Th>Roast Level</Table.Th>
                                    <Table.Th>Stock (kg)</Table.Th>
                                    <Table.Th>Price / kg</Table.Th>
                                    <Table.Th style={{ textAlign: 'right' }}>Actions</Table.Th>
                                </Table.Tr>
                            </Table.Thead>
                            <Table.Tbody>
                                {rows.length > 0 ? rows : (
                                    <Table.Tr>
                                        <Table.Td colSpan={6}>
                                            <Text ta="center" py="xl" c="dimmed">
                                                No beans found.
                                            </Text>
                                        </Table.Td>
                                    </Table.Tr>
                                )}
                            </Table.Tbody>
                        </Table>
                    </Table.ScrollContainer>
                </Paper>

                {/* Pagination */}
                <Center mt="xl">
                    <Pagination
                        total={totalPages}
                        value={page}
                        onChange={setPage}
                        color="indigo"
                    />
                </Center>
            </Container>
        </div>
    );
}
