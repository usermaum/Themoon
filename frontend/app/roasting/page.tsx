"use client";

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
    Grid,
    Paper,
    Text,
    Title,
    Group,
    Button,
    Select,
    NumberInput,
    TextInput,
    Stack,
    Progress,
    Alert,
    LoadingOverlay,
    SegmentedControl
} from '@mantine/core';

import { Flame, Calculator, Info } from 'lucide-react';
import PageHero from '@/components/ui/PageHero';
import { useLanguage } from '@/lib/i18n/LanguageContext';
import { notifications } from '@mantine/notifications';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface Bean {
    id: number;
    name: string;
    english_name?: string;
    origin: string;
    grade?: string;
    type: string;
    quantity_kg: number;
    avg_cost_price: number;
}

export default function RoastingPage() {
    const { t } = useLanguage();
    const [greenBeans, setGreenBeans] = useState<Bean[]>([]);
    const [roastedBeans, setRoastedBeans] = useState<Bean[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isFetching, setIsFetching] = useState(true);

    // Form State
    const [selectedGreenBeanId, setSelectedGreenBeanId] = useState<string | null>(null);
    const [inputAmount, setInputAmount] = useState<number | string>('');
    const [outputAmount, setOutputAmount] = useState<number | string>('');
    const [roastLevel, setRoastLevel] = useState<string | null>("Medium");
    const [targetMode, setTargetMode] = useState<string>("new");
    const [newBeanName, setNewBeanName] = useState<string>("");
    const [selectedRoastedBeanId, setSelectedRoastedBeanId] = useState<string | null>(null);

    useEffect(() => {
        fetchBeans();
    }, []);

    const fetchBeans = async () => {
        setIsFetching(true);
        try {
            const response = await axios.get(`${API_BASE_URL}/beans?size=100`);
            const allBeans = response.data.items;
            setGreenBeans(allBeans.filter((b: Bean) => b.type === 'GREEN_BEAN'));
            setRoastedBeans(allBeans.filter((b: Bean) => b.type === 'ROASTED_SINGLE'));
        } catch (err) {
            console.error("Failed to fetch beans", err);
            notifications.show({
                title: 'Error',
                message: 'Failed to fetch beans data.',
                color: 'red',
            });
        } finally {
            setIsFetching(false);
        }
    };

    const selectedGreenBean = greenBeans.find(b => b.id.toString() === selectedGreenBeanId);

    // Calculations
    const inputVal = typeof inputAmount === 'number' ? inputAmount : parseFloat(inputAmount as string) || 0;
    const outputVal = typeof outputAmount === 'number' ? outputAmount : parseFloat(outputAmount as string) || 0;
    const lossRate = inputVal > 0 ? ((inputVal - outputVal) / inputVal * 100) : 0;
    const estimatedCost = (selectedGreenBean && outputVal > 0)
        ? (selectedGreenBean.avg_cost_price * inputVal) / outputVal
        : 0;

    // Auto-fill new name suggestion
    useEffect(() => {
        if (selectedGreenBean && targetMode === 'new' && !newBeanName) {
            const suggestedName = selectedGreenBean.name
                .replace("G1", "")
                .replace("G2", "")
                .replace("G4", "")
                .trim() + " Roasted";
            setNewBeanName(suggestedName);
        }
    }, [selectedGreenBeanId, targetMode]);

    const handleSubmit = async () => {
        if (!selectedGreenBeanId || inputVal <= 0 || outputVal <= 0) return;
        if (targetMode === 'new' && !newBeanName) return;
        if (targetMode === 'existing' && !selectedRoastedBeanId) return;

        setIsLoading(true);
        try {
            const payload = {
                green_bean_id: parseInt(selectedGreenBeanId),
                input_amount: inputVal,
                output_amount: outputVal,
                roast_level: roastLevel,
                ...(targetMode === 'new' ? { new_bean_name: newBeanName } : { roasted_bean_id: parseInt(selectedRoastedBeanId!) })
            };

            await axios.post(`${API_BASE_URL}/roasting/`, payload);

            notifications.show({
                title: 'Success',
                message: 'Roasting batch recorded successfully!',
                color: 'green',
                icon: <Flame size={16} />,
            });

            // Reset form
            setInputAmount('');
            setOutputAmount('');
            setNewBeanName("");
            setSelectedRoastedBeanId(null);

            // 재검색
            fetchBeans();
        } catch (err: any) {
            console.error("Roasting failed", err);
            notifications.show({
                title: 'Roasting Failed',
                message: err.response?.data?.detail || "Failed to record roasting.",
                color: 'red',
            });
        } finally {
            setIsLoading(false);
        }
    };

    const greenBeanOptions = greenBeans.map(bean => ({
        value: bean.id.toString(),
        label: `${bean.name} (${bean.quantity_kg}kg)`
    }));

    const roastedBeanOptions = roastedBeans.map(bean => ({
        value: bean.id.toString(),
        label: bean.name
    }));

    return (
        <div>
            <PageHero
                title={t('roasting.title')}
                description={t('roasting.description')}
                icon={<Flame className="w-10 h-10" />}
                backgroundImage="/images/hero/roasting-hero.png"
            />

            <div className="p-4 md:p-8 max-w-7xl mx-auto">
                <Grid gutter="xl">
                    {/* Left: Input Form */}
                    <Grid.Col span={{ base: 12, md: 8 }}>
                        <Paper shadow="sm" radius="md" p="xl" withBorder className="relative">
                            <LoadingOverlay visible={isFetching || isLoading} zIndex={1000} overlayProps={{ radius: "sm", blur: 2 }} />

                            <Title order={3} mb="lg" c="dimmed">{t('roasting.newBatch')}</Title>

                            <Stack gap="lg">
                                {/* 1. Select Green Bean */}
                                <Select
                                    label={t('roasting.sourceGreenBean')}
                                    placeholder={t('roasting.selectGreenBean')}
                                    data={greenBeanOptions}
                                    value={selectedGreenBeanId}
                                    onChange={setSelectedGreenBeanId}
                                    searchable
                                    nothingFoundMessage="No green beans found"
                                    maxDropdownHeight={280}
                                    size="md"
                                    required
                                />

                                <Group grow align="flex-start">
                                    {/* 2. Input Amount */}
                                    <NumberInput
                                        label={t('roasting.inputAmount')}
                                        placeholder="0.0"
                                        suffix=" kg"
                                        value={inputAmount}
                                        onChange={setInputAmount}
                                        min={0}
                                        max={selectedGreenBean?.quantity_kg}
                                        error={selectedGreenBean && inputVal > selectedGreenBean.quantity_kg ? t('roasting.exceedsStock').replace('{stock}', selectedGreenBean.quantity_kg.toString()) : null}
                                        required
                                        size="md"
                                    />

                                    {/* 3. Output Amount */}
                                    <NumberInput
                                        label={t('roasting.outputAmount')}
                                        placeholder="0.0"
                                        suffix=" kg"
                                        value={outputAmount}
                                        onChange={setOutputAmount}
                                        min={0}
                                        required
                                        size="md"
                                    />
                                </Group>

                                {/* 4. Target Mode Selection */}
                                <SegmentedControl
                                    value={targetMode}
                                    onChange={setTargetMode}
                                    data={[
                                        { label: t('roasting.newRoastedBean'), value: 'new' },
                                        { label: t('roasting.existingRoastedBean'), value: 'existing' },
                                    ]}
                                    fullWidth
                                    size="md"
                                />

                                {targetMode === 'new' ? (
                                    <TextInput
                                        label={t('roasting.newBeanName')}
                                        placeholder={t('roasting.enterNewBeanName')}
                                        value={newBeanName}
                                        onChange={(event) => setNewBeanName(event.currentTarget.value)}
                                        required
                                        size="md"
                                    />
                                ) : (
                                    <Select
                                        label={t('roasting.selectRoastedBean')}
                                        placeholder={t('roasting.selectExistingRoastedBean')}
                                        data={roastedBeanOptions}
                                        value={selectedRoastedBeanId}
                                        onChange={setSelectedRoastedBeanId}
                                        searchable
                                        nothingFoundMessage="No roasted beans found"
                                        size="md"
                                    />
                                )}

                                <Select
                                    label={t('roasting.roastLevel')}
                                    data={[
                                        { value: 'Light', label: 'Light (Cinnamon/New England)' },
                                        { value: 'Medium', label: 'Medium (American/City)' },
                                        { value: 'Medium-Dark', label: 'Medium-Dark (Full City)' },
                                        { value: 'Dark', label: 'Dark (Vienna/French)' },
                                    ]}
                                    value={roastLevel}
                                    onChange={setRoastLevel}
                                    size="md"
                                />

                                <Button
                                    size="xl"
                                    color="orange"
                                    fullWidth
                                    mt="md"
                                    onClick={handleSubmit}
                                    loading={isLoading}
                                    leftSection={<Flame size={20} />}
                                >
                                    {t('roasting.startRoasting')}
                                </Button>
                            </Stack>
                        </Paper>
                    </Grid.Col>

                    {/* Right: Real-time Stats */}
                    <Grid.Col span={{ base: 12, md: 4 }}>
                        <Stack gap="md">
                            <Paper shadow="md" p="xl" radius="md" bg="dark.7" c="white">
                                <Group mb="xl">
                                    <Calculator size={24} className="text-amber-400" />
                                    <Text fw={700} size="lg">{t('roasting.batchAnalysis')}</Text>
                                </Group>

                                <Stack gap="xs" mb="xl">
                                    <Text size="sm" c="dimmed">{t('roasting.lossRate')}</Text>
                                    <Group align="flex-end" gap={4}>
                                        <Text size="xl" fw={700} c={lossRate > 20 ? 'red.4' : 'teal.4'}>
                                            {lossRate.toFixed(1)}%
                                        </Text>
                                        <Text size="sm" c="dimmed" mb={4}>{t('roasting.weightLoss')}</Text>
                                    </Group>
                                    <Progress
                                        value={lossRate}
                                        color={lossRate > 20 ? 'red' : 'teal'}
                                        size="sm"
                                        radius="sm"
                                    />
                                </Stack>

                                <Stack gap="xs" pt="lg" style={{ borderTop: '1px solid #444' }}>
                                    <Text size="sm" c="dimmed">{t('roasting.estCostPrice')}</Text>
                                    <Group align="flex-end" gap={4}>
                                        <Text size="xl" fw={700} c="amber.4">
                                            ₩{Math.round(estimatedCost).toLocaleString()}
                                        </Text>
                                        <Text size="sm" c="dimmed" mb={4}>/ kg</Text>
                                    </Group>
                                    <Text size="xs" c="dimmed">
                                        {t('roasting.basedOnGreenBean').replace('{cost}', selectedGreenBean ? Math.round(selectedGreenBean.avg_cost_price).toLocaleString() : '0')}
                                    </Text>
                                </Stack>
                            </Paper>

                            <Alert variant="light" color="orange" title={t('roasting.roastingTip')} icon={<Info size={16} />}>
                                {t('roasting.roastingTipContent')}
                            </Alert>
                        </Stack>
                    </Grid.Col>
                </Grid>
            </div>
        </div>
    );
}
