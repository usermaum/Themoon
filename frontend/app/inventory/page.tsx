"use client";

import React, { useState, useEffect } from 'react';
import {
    Container,
    Paper,
    Title,
    Table,
    Badge,
    Button,
    Group,
    Text,
    Modal,
    NumberInput,
    TextInput,
    Stack,
    LoadingOverlay,
    ActionIcon,
    ScrollArea,
    Center,
    Tabs,
    rem
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { notifications } from '@mantine/notifications';

import { Package, Edit, Trash2, Plus, Minus, Sprout, Coffee } from 'lucide-react';

import PageHero from '@/components/ui/PageHero';
import { Bean, BeanAPI, InventoryLog, InventoryLogAPI, InventoryLogCreateData } from '@/lib/api';
import { useLanguage } from '@/lib/i18n/LanguageContext';

export default function InventoryPage() {
    const { t } = useLanguage();
    const [greenBeans, setGreenBeans] = useState<Bean[]>([]);
    const [roastedBeans, setRoastedBeans] = useState<Bean[]>([]);

    // Combined beans for helper function lookups
    const allBeans = [...greenBeans, ...roastedBeans];

    const [logs, setLogs] = useState<InventoryLog[]>([]);
    const [loading, setLoading] = useState(true);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [activeTab, setActiveTab] = useState<string | null>('green');

    // Modal States
    const [opened, { open, close }] = useDisclosure(false);
    const [editOpened, { open: openEdit, close: closeEdit }] = useDisclosure(false);

    // Form States
    const [selectedBean, setSelectedBean] = useState<Bean | null>(null);
    const [transactionType, setTransactionType] = useState<'IN' | 'OUT'>('IN');
    const [quantity, setQuantity] = useState<number | string>('');
    const [reason, setReason] = useState('');

    // Edit Form States
    const [selectedLog, setSelectedLog] = useState<InventoryLog | null>(null);
    const [editQuantity, setEditQuantity] = useState<number | string>('');
    const [editReason, setEditReason] = useState('');

    const fetchData = async () => {
        try {
            setLoading(true);
            const [greenData, roastedData, logsData] = await Promise.all([
                BeanAPI.getAll({ size: 100, type: 'GREEN_BEAN' }),
                BeanAPI.getAll({ size: 100, type: 'ROASTED_BEAN' }),
                InventoryLogAPI.getAll({ limit: 50 })
            ]);

            // If backend hasn't been migrated or old data exists, greenData might be empty if everything is untyped.
            // But we assume the update_schema script didn't delete data, just added columns. 
            // Existing data has type=GREEN_BEAN by default in model, but actual DB values might be NULL if not migrated properly for existing rows.
            // For now, let's trust the API returns what matches.

            setGreenBeans(greenData.items);
            setRoastedBeans(roastedData.items);
            setLogs(logsData);
        } catch (err) {
            console.error('Failed to fetch data:', err);
            notifications.show({
                title: 'Error',
                message: 'Failed to fetch inventory data.',
                color: 'red',
            });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    // Handlers
    const handleOpenModal = (bean: Bean, type: 'IN' | 'OUT') => {
        setSelectedBean(bean);
        setTransactionType(type);
        setQuantity('');
        setReason('');
        open();
    };

    const handleOpenEditModal = (log: InventoryLog) => {
        setSelectedLog(log);
        setEditQuantity(Math.abs(log.quantity_change));
        setEditReason(log.reason || '');
        openEdit();
    };

    const handleSubmit = async () => {
        if (!selectedBean) return;
        const qty = typeof quantity === 'number' ? quantity : parseFloat(quantity);

        if (!qty || qty <= 0) {
            notifications.show({
                title: 'Invalid Input',
                message: 'Please enter a valid quantity.',
                color: 'red',
            });
            return;
        }

        setIsSubmitting(true);
        try {
            const logData: InventoryLogCreateData = {
                bean_id: selectedBean.id,
                transaction_type: transactionType,
                quantity_change: transactionType === 'IN' ? qty : -qty,
                reason: reason || undefined,
            };

            await InventoryLogAPI.create(logData);
            await fetchData();
            close();
            notifications.show({
                title: 'Success',
                message: t('inventory.success'),
                color: 'green',
            });
        } catch (err: any) {
            notifications.show({
                title: 'Error',
                message: err.response?.data?.detail || 'Failed to update inventory.',
                color: 'red',
            });
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleEditSubmit = async () => {
        if (!selectedLog) return;
        const qty = typeof editQuantity === 'number' ? editQuantity : parseFloat(editQuantity);

        if (!qty || qty <= 0) {
            notifications.show({
                title: 'Invalid Input',
                message: 'Please enter a valid quantity.',
                color: 'red',
            });
            return;
        }

        const finalQuantity = selectedLog.transaction_type === 'IN' ? qty : -qty;

        setIsSubmitting(true);
        try {
            await InventoryLogAPI.update(selectedLog.id, finalQuantity, editReason || undefined);
            await fetchData();
            closeEdit();
            notifications.show({
                title: 'Success',
                message: t('inventory.success'),
                color: 'green',
            });
        } catch (err: any) {
            notifications.show({
                title: 'Error',
                message: err.response?.data?.detail || 'Failed to update log.',
                color: 'red',
            });
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleDelete = async (id: number) => {
        if (!confirm(t('inventory.deleteConfirm'))) return;

        try {
            await InventoryLogAPI.delete(id);
            await fetchData();
            notifications.show({
                title: 'Deleted',
                message: 'Record deleted successfully',
                color: 'blue',
            });
        } catch (err: any) {
            notifications.show({
                title: 'Error',
                message: err.response?.data?.detail || 'Failed to delete record.',
                color: 'red',
            });
        }
    };

    const getBeanName = (beanId: number) => {
        const bean = allBeans.find(b => b.id === beanId);
        return bean ? bean.name : `Bean #${beanId}`;
    };

    // Render Rows Helper
    const renderBeanRows = (beanList: Bean[]) => (
        beanList.length === 0 ? (
            <Table.Tr>
                <Table.Td colSpan={5}>
                    <Center p="xl" c="dimmed">{t('inventory.noStock') || "No stock items found."}</Center>
                </Table.Td>
            </Table.Tr>
        ) : (
            beanList.map((bean) => (
                <Table.Tr key={bean.id}>
                    <Table.Td fw={500}>
                        <Group gap="xs">
                            <Text size="sm" fw={500}>{bean.name}</Text>
                            {bean.roast_profile && (
                                <Badge size="xs" variant="outline" color="gray">{bean.roast_profile}</Badge>
                            )}
                        </Group>
                    </Table.Td>
                    <Table.Td>{bean.origin}</Table.Td>
                    <Table.Td fw={700}>{bean.quantity_kg.toFixed(1)} kg</Table.Td>
                    <Table.Td>
                        {bean.quantity_kg < 5 ? (
                            <Badge color="red" variant="light">Shortage</Badge>
                        ) : bean.quantity_kg < 10 ? (
                            <Badge color="yellow" variant="light">Warning</Badge>
                        ) : (
                            <Badge color="green" variant="light">Good</Badge>
                        )}
                    </Table.Td>
                    <Table.Td style={{ textAlign: 'right' }}>
                        <Group gap="xs" justify="flex-end">
                            <Button
                                size="xs"
                                variant="light"
                                color="indigo"
                                leftSection={<Plus size={14} />}
                                onClick={() => handleOpenModal(bean, 'IN')}
                            >
                                {t('inventory.inbound')}
                            </Button>
                            <Button
                                size="xs"
                                variant="light"
                                color="red"
                                leftSection={<Minus size={14} />}
                                onClick={() => handleOpenModal(bean, 'OUT')}
                            >
                                {t('inventory.outbound')}
                            </Button>
                        </Group>
                    </Table.Td>
                </Table.Tr>
            ))
        )
    );

    const logRows = logs.length === 0 ? (
        <Table.Tr>
            <Table.Td colSpan={6}>
                <Center p="xl" c="dimmed">{t('inventory.noHistory')}</Center>
            </Table.Td>
        </Table.Tr>
    ) : (
        logs.map((log) => (
            <Table.Tr key={log.id}>
                <Table.Td c="dimmed" fz="sm">{new Date(log.created_at).toLocaleString()}</Table.Td>
                <Table.Td fw={500}>{getBeanName(log.bean_id)}</Table.Td>
                <Table.Td>
                    <Badge
                        color={log.transaction_type === 'IN' ? 'teal' : 'orange'}
                        variant="dot"
                    >
                        {log.transaction_type === 'IN' ? t('inventory.inbound') : t('inventory.outbound')}
                    </Badge>
                </Table.Td>
                <Table.Td fw={600} c={log.transaction_type === 'IN' ? 'teal' : 'orange'}>
                    {log.quantity_change > 0 ? '+' : ''}{log.quantity_change.toFixed(1)} kg
                </Table.Td>
                <Table.Td>{log.reason || '-'}</Table.Td>
                <Table.Td style={{ textAlign: 'right' }}>
                    <Group gap={4} justify="flex-end">
                        <ActionIcon variant="subtle" color="gray" onClick={() => handleOpenEditModal(log)}>
                            <Edit size={16} />
                        </ActionIcon>
                        <ActionIcon variant="subtle" color="red" onClick={() => handleDelete(log.id)}>
                            <Trash2 size={16} />
                        </ActionIcon>
                    </Group>
                </Table.Td>
            </Table.Tr>
        ))
    );

    return (
        <div>
            <PageHero
                title={t('inventory.title')}
                description={t('inventory.description')}
                icon={<Package className="w-10 h-10" />}
                backgroundImage="/images/hero/inventory-hero.png"
            />

            <Container size="xl" py="xl">
                <Stack gap="xl">
                    {/* Stock Status Section */}
                    <Paper shadow="sm" radius="md" p="md" withBorder>
                        <Group justify="space-between" mb="md">
                            <Title order={3}>{t('inventory.currentStock')}</Title>
                        </Group>

                        <Tabs value={activeTab} onChange={setActiveTab} color="orange" variant="pills" radius="md">
                            <Tabs.List mb="md">
                                <Tabs.Tab value="green" leftSection={<Sprout size={16} />}>
                                    Green Beans (생두)
                                </Tabs.Tab>
                                <Tabs.Tab value="roasted" leftSection={<Coffee size={16} />}>
                                    Roasted Beans (원두)
                                </Tabs.Tab>
                            </Tabs.List>

                            <Tabs.Panel value="green">
                                <ScrollArea>
                                    <Table verticalSpacing="sm" highlightOnHover>
                                        <Table.Thead bg="gray.0">
                                            <Table.Tr>
                                                <Table.Th>{t('inventory.beanName')}</Table.Th>
                                                <Table.Th>{t('inventory.origin')}</Table.Th>
                                                <Table.Th>{t('inventory.current')}</Table.Th>
                                                <Table.Th>{t('inventory.status')}</Table.Th>
                                                <Table.Th style={{ textAlign: 'right' }}>{t('inventory.actions')}</Table.Th>
                                            </Table.Tr>
                                        </Table.Thead>
                                        <Table.Tbody>
                                            {loading ? (
                                                <Table.Tr>
                                                    <Table.Td colSpan={5}>
                                                        <Center p="xl"><LoadingOverlay visible={true} /></Center>
                                                    </Table.Td>
                                                </Table.Tr>
                                            ) : renderBeanRows(greenBeans)}
                                        </Table.Tbody>
                                    </Table>
                                </ScrollArea>
                            </Tabs.Panel>

                            <Tabs.Panel value="roasted">
                                <ScrollArea>
                                    <Table verticalSpacing="sm" highlightOnHover>
                                        <Table.Thead bg="gray.0">
                                            <Table.Tr>
                                                <Table.Th>{t('inventory.beanName')}</Table.Th>
                                                <Table.Th>{t('inventory.origin')}</Table.Th>
                                                <Table.Th>{t('inventory.current')}</Table.Th>
                                                <Table.Th>{t('inventory.status')}</Table.Th>
                                                <Table.Th style={{ textAlign: 'right' }}>{t('inventory.actions')}</Table.Th>
                                            </Table.Tr>
                                        </Table.Thead>
                                        <Table.Tbody>
                                            {loading ? (
                                                <Table.Tr>
                                                    <Table.Td colSpan={5}>
                                                        <Center p="xl"><LoadingOverlay visible={true} /></Center>
                                                    </Table.Td>
                                                </Table.Tr>
                                            ) : renderBeanRows(roastedBeans)}
                                        </Table.Tbody>
                                    </Table>
                                </ScrollArea>
                            </Tabs.Panel>
                        </Tabs>
                    </Paper>

                    {/* History Section */}
                    <Paper shadow="sm" radius="md" p="md" withBorder>
                        <Title order={3} mb="md">{t('inventory.history')}</Title>
                        <ScrollArea>
                            <Table verticalSpacing="sm">
                                <Table.Thead bg="gray.0">
                                    <Table.Tr>
                                        <Table.Th>{t('inventory.date')}</Table.Th>
                                        <Table.Th>{t('inventory.beanName')}</Table.Th>
                                        <Table.Th>{t('inventory.type')}</Table.Th>
                                        <Table.Th>{t('inventory.amount')}</Table.Th>
                                        <Table.Th>{t('inventory.reason')}</Table.Th>
                                        <Table.Th style={{ textAlign: 'right' }}>{t('inventory.actions')}</Table.Th>
                                    </Table.Tr>
                                </Table.Thead>
                                <Table.Tbody>
                                    {loading ? (
                                        <Table.Tr>
                                            <Table.Td colSpan={6}>
                                                <Center p="xl"><LoadingOverlay visible={true} /></Center>
                                            </Table.Td>
                                        </Table.Tr>
                                    ) : logRows}
                                </Table.Tbody>
                            </Table>
                        </ScrollArea>
                    </Paper>
                </Stack>
            </Container>

            {/* Create Modal */}
            <Modal
                opened={opened}
                onClose={close}
                title={transactionType === 'IN' ? t('inventory.inboundAction') : t('inventory.outboundAction')}
                centered
            >
                <Stack>
                    <Text size="sm" c="dimmed">
                        {t('inventory.beanName')}: <Text span fw={700} c="bright">{selectedBean?.name}</Text>
                    </Text>
                    <Text size="sm" c="dimmed">
                        {t('inventory.current')}: <Text span fw={700} c="bright">{selectedBean?.quantity_kg.toFixed(1)} kg</Text>
                    </Text>

                    <NumberInput
                        label={t('inventory.amount') + " (kg)"}
                        placeholder="0.0"
                        value={quantity}
                        onChange={setQuantity}
                        min={0.1}
                        step={0.1}
                        required
                        data-autofocus
                    />

                    <TextInput
                        label={t('inventory.reason')}
                        placeholder="e.g. New Purchase"
                        value={reason}
                        onChange={(e) => setReason(e.currentTarget.value)}
                    />

                    <Group justify="flex-end" mt="md">
                        <Button variant="default" onClick={close}>{t('inventory.cancel')}</Button>
                        <Button
                            color={transactionType === 'IN' ? 'indigo' : 'red'}
                            onClick={handleSubmit}
                            loading={isSubmitting}
                        >
                            {t('inventory.confirm')}
                        </Button>
                    </Group>
                </Stack>
            </Modal>

            {/* Edit Modal */}
            <Modal
                opened={editOpened}
                onClose={closeEdit}
                title={t('inventory.editAction')}
                centered
            >
                <Stack>
                    <Text size="sm" c="dimmed">
                        {t('inventory.beanName')}: <Text span fw={700} c="bright">{selectedLog && getBeanName(selectedLog.bean_id)}</Text>
                    </Text>

                    <NumberInput
                        label={t('inventory.amount') + " (kg)"}
                        value={editQuantity}
                        onChange={setEditQuantity}
                        min={0.1}
                        step={0.1}
                        required
                    />

                    <TextInput
                        label={t('inventory.reason')}
                        value={editReason}
                        onChange={(e) => setEditReason(e.currentTarget.value)}
                    />

                    <Group justify="flex-end" mt="md">
                        <Button variant="default" onClick={closeEdit}>{t('inventory.cancel')}</Button>
                        <Button onClick={handleEditSubmit} loading={isSubmitting}>
                            {t('inventory.confirm')}
                        </Button>
                    </Group>
                </Stack>
            </Modal>
        </div>
    );
}
