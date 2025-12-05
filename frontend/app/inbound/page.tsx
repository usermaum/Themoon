"use client";

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
    Container,
    Grid,
    Paper,
    Title,
    Text,
    Button,
    Group,
    Stack,
    FileButton,
    Image,
    Center,
    TextInput,
    NumberInput,
    ActionIcon,
    Select,
    Badge,
    Divider,
    LoadingOverlay
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import {
    Upload,
    FileText,
    Check,
    AlertCircle,
    Plus,
    Trash2,
    ScanEye
} from 'lucide-react';
import { useLanguage } from '@/lib/i18n/LanguageContext';
import PageHero from '@/components/ui/PageHero';

// API Base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface InboundItem {
    name: string;
    quantity: number;
    unit_price: number;
    total_price: number;
    matched_bean_id?: string; // Changed to string for Mantine Select compatibility
    matched_bean_name?: string;
    match_score?: number;
}

interface OCRResult {
    supplier_name: string;
    invoice_number: string;
    date: string;
    total_amount: number;
    items: InboundItem[];
    temp_file_path: string;
}

interface Bean {
    id: number;
    name: string;
    origin: string;
    type: string;
}

export default function InboundPage() {
    const { t } = useLanguage();
    const [file, setFile] = useState<File | null>(null);
    const [previewUrl, setPreviewUrl] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [ocrResult, setOcrResult] = useState<OCRResult | null>(null);
    const [beans, setBeans] = useState<Bean[]>([]);

    // Fetch beans for matching
    useEffect(() => {
        const fetchBeans = async () => {
            try {
                const response = await axios.get(`${API_BASE_URL}/beans?size=100`);
                setBeans(response.data.items);
            } catch (err) {
                console.error("Failed to fetch beans", err);
                notifications.show({
                    title: 'Error',
                    message: 'Failed to fetch beans list.',
                    color: 'red',
                });
            }
        };
        fetchBeans();
    }, []);

    const handleFileChange = (payload: File | null) => {
        if (payload) {
            setFile(payload);
            setPreviewUrl(URL.createObjectURL(payload));
            setOcrResult(null);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setIsLoading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(`${API_BASE_URL}/inbound/upload`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });

            // Transform matched_bean_id to string for Select component
            const result = response.data;
            result.items = result.items.map((item: any) => ({
                ...item,
                matched_bean_id: item.matched_bean_id ? item.matched_bean_id.toString() : null
            }));

            setOcrResult(result);
            notifications.show({
                title: 'Analysis Complete',
                message: t('inbound.analyzeReceipt') + ' Success!',
                color: 'green',
            });
        } catch (err: any) {
            console.error("Upload failed", err);
            notifications.show({
                title: 'Error',
                message: err.response?.data?.detail || "Failed to analyze receipt.",
                color: 'red',
            });
        } finally {
            setIsLoading(false);
        }
    };

    const handleItemChange = (index: number, field: keyof InboundItem, value: any) => {
        if (!ocrResult) return;
        const newItems = [...ocrResult.items];
        newItems[index] = { ...newItems[index], [field]: value };

        // Auto-calc total if quantity or unit_price changes
        if (field === 'quantity' || field === 'unit_price') {
            newItems[index].total_price = newItems[index].quantity * newItems[index].unit_price;
        }

        setOcrResult({ ...ocrResult, items: newItems });
    };

    const handleAddItem = () => {
        if (!ocrResult) return;
        const newItem: InboundItem = { name: "", quantity: 0, unit_price: 0, total_price: 0 };
        setOcrResult({ ...ocrResult, items: [...ocrResult.items, newItem] });
    };

    const handleRemoveItem = (index: number) => {
        if (!ocrResult) return;
        const newItems = ocrResult.items.filter((_, i) => i !== index);
        setOcrResult({ ...ocrResult, items: newItems });
    };

    const handleConfirm = async () => {
        if (!ocrResult) return;

        setIsLoading(true);
        try {
            // Transform back for API if needed (though backend likely handles int/string conversion)
            const payload = {
                ...ocrResult,
                items: ocrResult.items.map(item => ({
                    ...item,
                    matched_bean_id: item.matched_bean_id ? parseInt(item.matched_bean_id) : null
                }))
            };

            await axios.post(`${API_BASE_URL}/inbound/confirm`, payload);

            notifications.show({
                title: 'Success',
                message: 'Inbound transaction confirmed!',
                color: 'green',
            });

            // Reset
            setFile(null);
            setPreviewUrl(null);
            setOcrResult(null);
        } catch (err: any) {
            notifications.show({
                title: 'Error',
                message: err.response?.data?.detail || "Failed to confirm transaction.",
                color: 'red',
            });
        } finally {
            setIsLoading(false);
        }
    };

    const beanOptions = beans.map(bean => ({
        value: bean.id.toString(),
        label: `${bean.name} (${bean.origin})`
    }));

    return (
        <div>
            <PageHero
                title={t('inbound.title')}
                description={t('inbound.description')}
                icon={<ScanEye className="w-10 h-10" />}
                backgroundImage="/images/hero/inbound-hero.png"
            />

            <Container size="xl" py="xl">
                <Grid gutter="xl">
                    {/* Left: Upload Section */}
                    <Grid.Col span={{ base: 12, md: 5 }}>
                        <Paper shadow="sm" radius="md" p="xl" withBorder h="100%">
                            <Title order={4} mb="md" c="dimmed" flex={1}>
                                <Group gap="xs">
                                    <Upload size={20} />
                                    {t('inbound.uploadReceipt')}
                                </Group>
                            </Title>

                            <Stack align="center" justify="center" gap="md" py={previewUrl ? 'xs' : 'xl'}>
                                {previewUrl ? (
                                    <Image
                                        src={previewUrl}
                                        radius="md"
                                        alt="Receipt Preview"
                                        mah={400}
                                        fit="contain"
                                        className="border border-stone-200"
                                    />
                                ) : (
                                    <Center py={60} w="100%" bg="gray.0" style={{ borderRadius: 8, border: '2px dashed #dee2e6' }}>
                                        <Stack align="center" gap="xs" c="dimmed">
                                            <FileText size={48} strokeWidth={1} />
                                            <Text size="sm">{t('inbound.clickToUpload')}</Text>
                                        </Stack>
                                    </Center>
                                )}

                                <FileButton onChange={handleFileChange} accept="image/png,image/jpeg">
                                    {(props) => (
                                        <Button {...props} variant="light" size="md" fullWidth>
                                            {file ? 'Change File' : t('inbound.uploadReceipt')}
                                        </Button>
                                    )}
                                </FileButton>

                                {file && !ocrResult && (
                                    <Button
                                        fullWidth
                                        size="lg"
                                        color="orange"
                                        onClick={handleUpload}
                                        loading={isLoading}
                                        leftSection={<ScanEye size={20} />}
                                    >
                                        {t('inbound.analyzeReceipt')}
                                    </Button>
                                )}

                                <Button
                                    variant="outline"
                                    color="gray"
                                    size="xs"
                                    onClick={() => {
                                        setOcrResult({
                                            supplier_name: "Test Supplier",
                                            invoice_number: `TEST-${Date.now()}`,
                                            date: new Date().toISOString().split('T')[0],
                                            total_amount: 150000,
                                            items: [
                                                { name: "Test Item 1", quantity: 10, unit_price: 10000, total_price: 100000 },
                                                { name: "Test Item 2", quantity: 5, unit_price: 10000, total_price: 50000 }
                                            ],
                                            temp_file_path: "mock_test_path"
                                        });
                                    }}
                                >
                                    Test (Mock Data)
                                </Button>
                            </Stack>
                        </Paper>
                    </Grid.Col>

                    {/* Right: OCR Result Section */}
                    <Grid.Col span={{ base: 12, md: 7 }}>
                        {ocrResult ? (
                            <Paper shadow="sm" radius="md" p="xl" withBorder className="relative">
                                <LoadingOverlay visible={isLoading} />
                                <Title order={4} mb="lg" c="teal">
                                    <Group gap="xs">
                                        <Check size={20} />
                                        {t('inbound.verifiedData')}
                                    </Group>
                                </Title>

                                <Grid mb="lg">
                                    <Grid.Col span={4}>
                                        <TextInput
                                            label={t('inbound.supplier')}
                                            value={ocrResult.supplier_name}
                                            onChange={(e) => setOcrResult({ ...ocrResult, supplier_name: e.currentTarget.value })}
                                        />
                                    </Grid.Col>
                                    <Grid.Col span={4}>
                                        <TextInput
                                            label={t('inbound.invoiceNo')}
                                            value={ocrResult.invoice_number}
                                            onChange={(e) => setOcrResult({ ...ocrResult, invoice_number: e.currentTarget.value })}
                                        />
                                    </Grid.Col>
                                    <Grid.Col span={4}>
                                        <TextInput
                                            type="date"
                                            label={t('inbound.date')}
                                            value={ocrResult.date}
                                            onChange={(e) => setOcrResult({ ...ocrResult, date: e.currentTarget.value })}
                                        />
                                    </Grid.Col>
                                </Grid>

                                <Divider my="lg" label={t('inbound.items')} labelPosition="left" />

                                <Stack gap="xs">
                                    {ocrResult.items.map((item, idx) => (
                                        <Paper key={idx} p="sm" bg="gray.0" withBorder radius="md">
                                            <Grid align="center" gutter="xs">
                                                <Grid.Col span={1} style={{ textAlign: 'center' }}>
                                                    <ActionIcon color="red" variant="subtle" onClick={() => handleRemoveItem(idx)}>
                                                        <Trash2 size={16} />
                                                    </ActionIcon>
                                                </Grid.Col>
                                                <Grid.Col span={11}>
                                                    <Grid>
                                                        <Grid.Col span={5}>
                                                            <TextInput
                                                                size="xs"
                                                                label={t('inbound.itemName')}
                                                                value={item.name}
                                                                onChange={(e) => handleItemChange(idx, 'name', e.currentTarget.value)}
                                                            />
                                                        </Grid.Col>
                                                        <Grid.Col span={2}>
                                                            <NumberInput
                                                                size="xs"
                                                                label={t('inbound.qty')}
                                                                value={item.quantity}
                                                                onChange={(val) => handleItemChange(idx, 'quantity', val)}
                                                                min={0}
                                                            />
                                                        </Grid.Col>
                                                        <Grid.Col span={2}>
                                                            <NumberInput
                                                                size="xs"
                                                                label={t('inbound.unitPrice')}
                                                                value={item.unit_price}
                                                                onChange={(val) => handleItemChange(idx, 'unit_price', val)}
                                                                min={0}
                                                            />
                                                        </Grid.Col>
                                                        <Grid.Col span={3}>
                                                            <NumberInput
                                                                size="xs"
                                                                label={t('inbound.total')}
                                                                value={item.total_price}
                                                                readOnly
                                                                prefix="₩"
                                                            />
                                                        </Grid.Col>
                                                    </Grid>

                                                    {/* Bean Matching */}
                                                    <Group mt="xs" align="center">
                                                        <Text size="xs" c="dimmed" style={{ minWidth: 80 }}>{t('inbound.matchedBean')}:</Text>
                                                        <Select
                                                            size="xs"
                                                            placeholder="Select Bean"
                                                            data={beanOptions}
                                                            value={item.matched_bean_id}
                                                            onChange={(val) => handleItemChange(idx, 'matched_bean_id', val)}
                                                            searchable
                                                            clearable
                                                            style={{ flex: 1 }}
                                                        />
                                                        {item.match_score && (
                                                            <Badge
                                                                size="sm"
                                                                color={item.match_score >= 80 ? 'green' : item.match_score >= 60 ? 'yellow' : 'red'}
                                                            >
                                                                {item.match_score}% Match
                                                            </Badge>
                                                        )}
                                                    </Group>
                                                </Grid.Col>
                                            </Grid>
                                        </Paper>
                                    ))}
                                </Stack>

                                <Button
                                    variant="subtle"
                                    size="sm"
                                    leftSection={<Plus size={16} />}
                                    mt="md"
                                    onClick={handleAddItem}
                                >
                                    {t('inbound.addItem')}
                                </Button>

                                <Divider my="lg" />

                                <Group justify="space-between" align="center">
                                    <Text size="lg" fw={700}>
                                        Total: ₩{ocrResult.items.reduce((sum, item) => sum + (item.quantity * item.unit_price), 0).toLocaleString()}
                                    </Text>
                                    <Button
                                        color="green"
                                        size="md"
                                        leftSection={<Check size={20} />}
                                        onClick={handleConfirm}
                                        loading={isLoading}
                                    >
                                        {t('inbound.confirmInbound')}
                                    </Button>
                                </Group>
                            </Paper>
                        ) : (
                            <Paper shadow="sm" radius="md" p="xl" withBorder h="100%" bg="gray.0">
                                <Center h="100%">
                                    <Stack align="center" c="dimmed" gap="lg">
                                        <AlertCircle size={48} strokeWidth={1} />
                                        <Text size="lg" ta="center">Upload a receipt to start analysis</Text>
                                        <Text size="sm" ta="center" maw={300}>
                                            Upload an invoice image on the left side to automatically extract data and register inbound inventory.
                                        </Text>
                                    </Stack>
                                </Center>
                            </Paper>
                        )}
                    </Grid.Col>
                </Grid>
            </Container>
        </div>
    );
}
