'use client';

import { useState, useEffect } from 'react';
import { Bean, BeanAPI, BlendCreateData, Blend } from '@/lib/api';
import Link from 'next/link';
import {
    TextInput,
    Textarea,
    Select,
    NumberInput,
    Button,
    Group,
    Stack,
    Paper,
    Title,
    Text,
    ActionIcon,
    Box,
    Divider,
    LoadingOverlay
} from '@mantine/core';
import { Trash2, Plus, ArrowLeft } from 'lucide-react';
import { notifications } from '@mantine/notifications';

interface BlendFormProps {
    initialData?: Blend;
    onSubmit: (data: BlendCreateData) => Promise<void>;
    onDelete?: () => Promise<void>;
    isSubmitting: boolean;
    title: string;
    submitLabel: string;
}

export default function BlendForm({
    initialData,
    onSubmit,
    onDelete,
    isSubmitting,
    title,
    submitLabel,
}: BlendFormProps) {
    const [beans, setBeans] = useState<Bean[]>([]);
    const [loadingBeans, setLoadingBeans] = useState(true);

    // Form State
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [targetRoastLevel, setTargetRoastLevel] = useState<string | null>('Medium');
    const [notes, setNotes] = useState('');

    // Recipe State: [{ beanId: string, ratio: number }]
    const [recipe, setRecipe] = useState<{ beanId: string; ratio: number }[]>([
        { beanId: '', ratio: 0 },
    ]);

    useEffect(() => {
        const fetchBeans = async () => {
            try {
                const data = await BeanAPI.getAll({ size: 100 });
                setBeans(data.items);
            } catch (err) {
                console.error('Failed to fetch beans:', err);
                notifications.show({
                    title: 'Error',
                    message: 'Failed to load beans list',
                    color: 'red',
                });
            } finally {
                setLoadingBeans(false);
            }
        };
        fetchBeans();
    }, []);

    useEffect(() => {
        if (initialData) {
            setName(initialData.name);
            setDescription(initialData.description || '');
            setTargetRoastLevel(initialData.target_roast_level || 'Medium');
            setNotes(initialData.notes || '');

            if (initialData.recipe && initialData.recipe.length > 0) {
                setRecipe(
                    initialData.recipe.map((item) => ({
                        beanId: item.bean_id.toString(),
                        ratio: item.ratio * 100, // 0.5 -> 50
                    }))
                );
            }
        }
    }, [initialData]);

    const handleRecipeChange = (index: number, field: 'beanId' | 'ratio', value: string | number) => {
        const newRecipe = [...recipe];
        if (field === 'ratio') {
            newRecipe[index] = { ...newRecipe[index], ratio: value as number };
        } else {
            newRecipe[index] = { ...newRecipe[index], beanId: value as string };
        }
        setRecipe(newRecipe);
    };

    const addBeanRow = () => {
        setRecipe([...recipe, { beanId: '', ratio: 0 }]);
    };

    const removeBeanRow = (index: number) => {
        if (recipe.length > 1) {
            setRecipe(recipe.filter((_, i) => i !== index));
        }
    };

    const calculateTotalRatio = () => {
        return recipe.reduce((sum, item) => sum + (Number(item.ratio) || 0), 0);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (Math.abs(calculateTotalRatio() - 100) > 0.1) {
            notifications.show({
                title: 'Invalid Ratio',
                message: 'Total blend ratio must be 100%',
                color: 'red',
            });
            return;
        }

        const validRecipe = recipe.map(item => ({
            bean_id: parseInt(item.beanId),
            ratio: Number(item.ratio) / 100
        }));

        await onSubmit({
            name,
            description,
            target_roast_level: targetRoastLevel || 'Medium',
            notes,
            recipe: validRecipe,
        });
    };

    if (loadingBeans) {
        return <LoadingOverlay visible={true} />;
    }

    const beanOptions = beans.map(b => ({ value: b.id.toString(), label: `${b.name} (${b.origin})` }));

    return (
        <Box maw={800} mx="auto" py="xl">
            <Group justify="space-between" mb="lg">
                <Group>
                    <Link href="/blends" style={{ textDecoration: 'none' }}>
                        <Button variant="subtle" color="gray" leftSection={<ArrowLeft size={16} />}>
                            Back
                        </Button>
                    </Link>
                    <Title order={2}>{title}</Title>
                </Group>
                {onDelete && (
                    <Button color="red" variant="light" leftSection={<Trash2 size={16} />} onClick={onDelete}>
                        Delete
                    </Button>
                )}
            </Group>

            <Paper withBorder p="xl" radius="md" shadow="sm">
                <form onSubmit={handleSubmit}>
                    <Stack gap="lg">
                        <Title order={4}>Basic Information</Title>

                        <TextInput
                            label="Blend Name"
                            required
                            placeholder="e.g., Summer Breeze Blend"
                            value={name}
                            onChange={(e) => setName(e.currentTarget.value)}
                        />

                        <TextInput
                            label="Description"
                            placeholder="Brief description of the blend"
                            value={description}
                            onChange={(e) => setDescription(e.currentTarget.value)}
                        />

                        <Select
                            label="Target Roast Level"
                            data={[
                                'Light',
                                'Medium-Light',
                                'Medium',
                                'Medium-Dark',
                                'Dark'
                            ]}
                            value={targetRoastLevel}
                            onChange={setTargetRoastLevel}
                        />

                        <Divider my="sm" />

                        <Group justify="space-between" align="center">
                            <Title order={4}>Recipe Composition</Title>
                            <Text
                                fw={700}
                                c={Math.abs(calculateTotalRatio() - 100) < 0.1 ? 'teal' : 'red'}
                            >
                                Total: {calculateTotalRatio()}%
                            </Text>
                        </Group>

                        <Stack gap="md">
                            {recipe.map((item, index) => (
                                <Group key={index} grow align="flex-start">
                                    <Select
                                        placeholder="Select Bean"
                                        data={beanOptions}
                                        value={item.beanId}
                                        onChange={(val) => handleRecipeChange(index, 'beanId', val || '')}
                                        searchable
                                        required
                                        w={'60%'}
                                    />
                                    <NumberInput
                                        placeholder="Ratio"
                                        value={item.ratio}
                                        onChange={(val) => handleRecipeChange(index, 'ratio', val as number)}
                                        min={0}
                                        max={100}
                                        suffix="%"
                                        required
                                        w={'25%'}
                                    />
                                    <ActionIcon
                                        color="red"
                                        variant="subtle"
                                        onClick={() => removeBeanRow(index)}
                                        disabled={recipe.length === 1}
                                        mt={4}
                                    >
                                        <Trash2 size={18} />
                                    </ActionIcon>
                                </Group>
                            ))}
                            <Button variant="outline" onClick={addBeanRow} fullWidth style={{ borderStyle: 'dashed' }}>
                                + Add Bean
                            </Button>
                        </Stack>

                        <Divider my="sm" />

                        <Title order={4}>Notes</Title>
                        <Textarea
                            placeholder="Any additional notes"
                            value={notes}
                            onChange={(e) => setNotes(e.currentTarget.value)}
                            minRows={3}
                        />

                        <Group justify="flex-end" mt="xl">
                            <Link href="/blends" style={{ textDecoration: 'none' }}>
                                <Button variant="default">Cancel</Button>
                            </Link>
                            <Button type="submit" color="orange" loading={isSubmitting}>
                                {submitLabel}
                            </Button>
                        </Group>
                    </Stack>
                </form>
            </Paper>
        </Box>
    );
}
