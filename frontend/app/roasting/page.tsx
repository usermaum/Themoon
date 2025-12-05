"use client";

import React, { useState, useEffect } from 'react';
import {
    Container,
    Paper,
    Title,
    TextInput,
    NumberInput,
    Select,
    Button,
    Group,
    Stack,
    Text,
    LoadingOverlay,
    Divider,
    Alert,
    Radio
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { Flame, ArrowRight, AlertCircle, CheckCircle } from 'lucide-react';

import PageHero from '@/components/ui/PageHero';
import { Bean, BeanAPI, RoastingAPI, RoastingCreateData } from '@/lib/api';
import { useLanguage } from '@/lib/i18n/LanguageContext';

export default function RoastingPage() {
    const { t } = useLanguage();

    // Data States
    const [greenBeans, setGreenBeans] = useState<Bean[]>([]);
    const [roastedBeans, setRoastedBeans] = useState<Bean[]>([]);
    const [loading, setLoading] = useState(false);

    // Form States
    const [selectedGreenBeanId, setSelectedGreenBeanId] = useState<string | null>(null);
    const [inputAmount, setInputAmount] = useState<number | string>('');
    const [roastProfile, setRoastProfile] = useState<string>('MEDIUM');

    // Output Strategy
    const [outputStrategy, setOutputStrategy] = useState<string>('new'); // 'new' or 'existing'
    const [existingRoastedBeanId, setExistingRoastedBeanId] = useState<string | null>(null);
    const [newBeanName, setNewBeanName] = useState<string>('');

    const [outputAmount, setOutputAmount] = useState<number | string>('');
    const [note, setNote] = useState<string>('');

    // Derived States
    const [lossRate, setLossRate] = useState<number | null>(null);

    useEffect(() => {
        fetchBeans();
    }, []);

    useEffect(() => {
        // Auto-calculate loss rate
        const inp = typeof inputAmount === 'number' ? inputAmount : parseFloat(inputAmount);
        const out = typeof outputAmount === 'number' ? outputAmount : parseFloat(outputAmount);

        if (inp > 0 && out > 0 && inp >= out) {
            const rate = ((inp - out) / inp) * 100;
            setLossRate(rate);
        } else {
            setLossRate(null);
        }
    }, [inputAmount, outputAmount]);

    const fetchBeans = async () => {
        setLoading(true);
        try {
            const [greens, roasteds] = await Promise.all([
                BeanAPI.getAll({ type: 'GREEN_BEAN', size: 100 }),
                BeanAPI.getAll({ type: 'ROASTED_BEAN', size: 100 })
            ]);
            setGreenBeans(greens.items);
            setRoastedBeans(roasteds.items);
        } catch (error) {
            console.error(error);
            notifications.show({
                title: 'Error',
                message: 'Failed to load bean lists',
                color: 'red'
            });
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async () => {
        if (!selectedGreenBeanId) {
            notifications.show({ title: 'Error', message: 'Please select a green bean', color: 'red' });
            return;
        }

        const inp = typeof inputAmount === 'number' ? inputAmount : parseFloat(inputAmount);
        const out = typeof outputAmount === 'number' ? outputAmount : parseFloat(outputAmount);

        if (!inp || inp <= 0) {
            notifications.show({ title: 'Error', message: 'Invalid input amount', color: 'red' });
            return;
        }
        if (!out || out <= 0) {
            notifications.show({ title: 'Error', message: 'Invalid output amount', color: 'red' });
            return;
        }
        if (out > inp) {
            notifications.show({ title: 'Warning', message: 'Output amount cannot be greater than input amount (typically)', color: 'orange' });
            // Proceeding is allowed but usually indicates error
        }

        if (outputStrategy === 'new' && !newBeanName) {
            notifications.show({ title: 'Error', message: 'Please enter a name for the new roasted bean', color: 'red' });
            return;
        }
        if (outputStrategy === 'existing' && !existingRoastedBeanId) {
            notifications.show({ title: 'Error', message: 'Please select an existing roasted bean', color: 'red' });
            return;
        }

        setLoading(true);
        try {
            const data: RoastingCreateData = {
                green_bean_id: parseInt(selectedGreenBeanId),
                input_amount: inp,
                output_amount: out,
                roast_profile: roastProfile as any,
                note: note,
                ...(outputStrategy === 'new'
                    ? { new_bean_name: newBeanName }
                    : { roasted_bean_id: parseInt(existingRoastedBeanId!) }
                )
            };

            await RoastingAPI.create(data);

            notifications.show({
                title: 'Success',
                message: 'Roasting completed successfully! Inventory updated.',
                color: 'green',
                icon: <CheckCircle />
            });

            // Reset Form (Partial)
            fetchBeans(); // Refresh stocks
            setInputAmount('');
            setOutputAmount('');
            setNewBeanName('');
            setNote('');

        } catch (error: any) {
            console.error(error);
            notifications.show({
                title: 'Error',
                message: error.response?.data?.detail || 'Roasting failed',
                color: 'red'
            });
        } finally {
            setLoading(false);
        }
    };

    // Helper to find Bean
    const selectedGreenBean = greenBeans.find(b => b.id.toString() === selectedGreenBeanId);

    return (
        <div>
            <PageHero
                title="Roasting Management"
                description="Process Green Beans into Roasted Beans"
                icon={<Flame className="w-10 h-10" />}
                backgroundImage="/images/hero/roasting-hero.png" // Ensure this image exists or is handled
            />

            <Container size="md" py="xl">
                <Paper shadow="sm" radius="md" p="xl" withBorder pos="relative">
                    <LoadingOverlay visible={loading} />

                    <Stack gap="lg">
                        <Title order={3}>New Roasting Session</Title>

                        {/* 1. Input Section */}
                        <Paper withBorder p="md" bg="gray.0">
                            <Stack>
                                <Group>
                                    <Text fw={700} c="green">Step 1: Input (Green Bean)</Text>
                                </Group>
                                <Select
                                    label="Select Green Bean"
                                    placeholder="Choose a green bean"
                                    data={greenBeans.map(b => ({ value: b.id.toString(), label: `${b.name} (Qty: ${b.quantity_kg}kg)` }))}
                                    value={selectedGreenBeanId}
                                    onChange={setSelectedGreenBeanId}
                                    searchable
                                    required
                                />

                                {selectedGreenBean && (
                                    <Text size="xs" c="dimmed">
                                        Origin: {selectedGreenBean.origin} | Variety: {selectedGreenBean.variety}
                                    </Text>
                                )}

                                <NumberInput
                                    label="Input Amount (kg)"
                                    placeholder="0.0"
                                    min={0}
                                    max={selectedGreenBean?.quantity_kg}
                                    value={inputAmount}
                                    onChange={setInputAmount}
                                    required
                                />
                            </Stack>
                        </Paper>

                        <CenterIcon />

                        {/* 2. Process Section */}
                        <Paper withBorder p="md" bg="gray.0">
                            <Stack>
                                <Text fw={700} c="orange">Step 2: Roasting Profile</Text>
                                <Select
                                    label="Roast Profile"
                                    data={['LIGHT', 'MEDIUM', 'DARK']}
                                    value={roastProfile}
                                    onChange={(v) => setRoastProfile(v || 'MEDIUM')}
                                    required
                                />
                            </Stack>
                        </Paper>

                        <CenterIcon />

                        {/* 3. Output Section */}
                        <Paper withBorder p="md" bg="gray.0">
                            <Stack>
                                <Text fw={700} c="brown">Step 3: Output (Roasted Bean)</Text>

                                <Radio.Group value={outputStrategy} onChange={setOutputStrategy} label="Target Bean">
                                    <Group mt="xs">
                                        <Radio value="new" label="Create New Bean" />
                                        <Radio value="existing" label="Add to Existing Bean" />
                                    </Group>
                                </Radio.Group>

                                {outputStrategy === 'new' ? (
                                    <TextInput
                                        label="New Bean Name"
                                        placeholder="e.g. Ethiopia Yirgacheffe G2 Medium"
                                        value={newBeanName}
                                        onChange={(e) => setNewBeanName(e.currentTarget.value)}
                                        required
                                    />
                                ) : (
                                    <Select
                                        label="Select Existing Roasted Bean"
                                        placeholder="Choose a roasted bean"
                                        data={roastedBeans.map(b => ({ value: b.id.toString(), label: b.name }))}
                                        value={existingRoastedBeanId}
                                        onChange={setExistingRoastedBeanId}
                                        searchable
                                        required
                                    />
                                )}

                                <NumberInput
                                    label="Output Amount (kg)"
                                    placeholder="0.0"
                                    min={0}
                                    value={outputAmount}
                                    onChange={setOutputAmount}
                                    required
                                />
                            </Stack>
                        </Paper>

                        {/* 4. Review & Support */}
                        {lossRate !== null && (
                            <Alert icon={<AlertCircle size={16} />} title="Performance" color={lossRate > 20 ? 'red' : 'blue'}>
                                Calculated Loss Rate: <strong>{lossRate.toFixed(1)}%</strong>
                                {lossRate > 20 && " (High loss rate, please check)"}
                            </Alert>
                        )}

                        <TextInput
                            label="Notes"
                            placeholder="Optional notes (e.g. batch number, weather)"
                            value={note}
                            onChange={(e) => setNote(e.currentTarget.value)}
                        />

                        <Button size="lg" color="orange" onClick={handleSubmit} fullWidth mt="xl">
                            Confirm Roasting
                        </Button>
                    </Stack>
                </Paper>

                {/* Roasting History Section */}
                <Stack mt={50} gap="md">
                    <Title order={3}>Recent Roasting Logs</Title>
                    <RoastingHistory />
                </Stack>
            </Container>
        </div>
    );
}

function CenterIcon() {
    return (
        <Group justify="center">
            <ArrowRight size={24} color="gray" style={{ transform: 'rotate(90deg)' }} />
        </Group>
    )
}

import { Table, Badge } from '@mantine/core';
import { RoastingLog } from '@/lib/api';

function RoastingHistory() {
    const [logs, setLogs] = useState<RoastingLog[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const data = await RoastingAPI.getHistory(10);
            setLogs(data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <Text size="sm">Loading logs...</Text>;
    if (logs.length === 0) return <Text size="sm" c="dimmed">No roasting history found.</Text>;

    return (
        <Paper withBorder radius="md" style={{ overflow: 'hidden' }}>
            <Table striped highlightOnHover>
                <Table.Thead>
                    <Table.Tr>
                        <Table.Th>Date</Table.Th>
                        <Table.Th>Input (Green)</Table.Th>
                        <Table.Th>Output (Roasted)</Table.Th>
                        <Table.Th>Loss Rate</Table.Th>
                        <Table.Th>Note</Table.Th>
                    </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                    {logs.map((log) => (
                        <Table.Tr key={log.id}>
                            <Table.Td>{new Date(log.roast_date).toLocaleDateString()}</Table.Td>
                            <Table.Td>
                                <Text size="sm" fw={500}>{log.green_bean_name}</Text>
                                <Text size="xs" c="dimmed">In: {log.input_quantity.toFixed(1)}kg</Text>
                            </Table.Td>
                            <Table.Td>
                                <Text size="sm" fw={500}>{log.roasted_bean_name}</Text>
                                <Text size="xs" c="dimmed">Out: {log.output_quantity.toFixed(1)}kg</Text>
                            </Table.Td>
                            <Table.Td>
                                <Badge
                                    color={log.loss_rate > 20 ? 'red' : log.loss_rate > 15 ? 'orange' : 'green'}
                                    variant="light"
                                >
                                    {log.loss_rate.toFixed(1)}%
                                </Badge>
                            </Table.Td>
                            <Table.Td>
                                <Text size="sm" span>{log.note || '-'}</Text>
                            </Table.Td>
                        </Table.Tr>
                    ))}
                </Table.Tbody>
            </Table>
        </Paper>
    );
}
