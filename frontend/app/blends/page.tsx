"use client";

import React, { useState, useEffect } from 'react';
import {
    Container,
    Paper,
    Title,
    Text,
    Button,
    Group,
    Stack,
    Grid,
    Card,
    Badge,
    ActionIcon,
    Modal,
    TextInput,
    NumberInput,
    Select,
    LoadingOverlay,
    Table,
    ScrollArea,
    Divider,
    Alert
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { notifications } from '@mantine/notifications';
import { Layers, Plus, Trash, Settings, Play, CheckCircle, AlertCircle } from 'lucide-react';

import PageHero from '@/components/ui/PageHero';
import { Blend, BlendAPI, Bean, BeanAPI, BlendCreateData, BlendRecipeItem } from '@/lib/api';

export default function BlendsPage() {
    const [blends, setBlends] = useState<Blend[]>([]);
    const [beans, setBeans] = useState<Bean[]>([]); // Roasted beans for ingredients
    const [loading, setLoading] = useState(false);

    // Modals
    const [createOpened, { open: openCreate, close: closeCreate }] = useDisclosure(false);
    const [produceOpened, { open: openProduce, close: closeProduce }] = useDisclosure(false);

    // Create Form State
    const [newBlendName, setNewBlendName] = useState('');
    const [newBlendNote, setNewBlendNote] = useState('');
    const [recipeItems, setRecipeItems] = useState<BlendRecipeItem[]>([]);

    // Produce State
    const [selectedBlend, setSelectedBlend] = useState<Blend | null>(null);
    const [productionAmount, setProductionAmount] = useState<number | string>('');

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        try {
            const [blendsData, beansData] = await Promise.all([
                BlendAPI.getAll(),
                BeanAPI.getAll({ type: 'ROASTED_BEAN', size: 100 })
            ]);
            setBlends(blendsData);
            setBeans(beansData.items);
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Failed to load data', color: 'red' });
        } finally {
            setLoading(false);
        }
    };

    // --- Create Handlers ---
    const handleAddIngredient = () => {
        setRecipeItems([...recipeItems, { bean_id: 0, ratio: 0 }]);
    };

    const handleIngredientChange = (index: number, field: keyof BlendRecipeItem, value: any) => {
        const newItems = [...recipeItems];
        if (field === 'bean_id') value = parseInt(value);
        if (field === 'ratio') value = parseFloat(value);

        newItems[index] = { ...newItems[index], [field]: value };
        setRecipeItems(newItems);
    };

    const handleRemoveIngredient = (index: number) => {
        setRecipeItems(recipeItems.filter((_, i) => i !== index));
    };

    const handleCreateBlend = async () => {
        // Validation
        if (!newBlendName) return notifications.show({ message: 'Name is required', color: 'red' });
        if (recipeItems.length === 0) return notifications.show({ message: 'Add at least one ingredient', color: 'red' });

        const totalRatio = recipeItems.reduce((sum, item) => sum + item.ratio, 0);
        if (Math.abs(totalRatio - 1.0) > 0.01) { // Allow small float error
            return notifications.show({ message: `Total ratio must be 1.0 (Current: ${totalRatio.toFixed(2)})`, color: 'red' });
        }

        setLoading(true);
        try {
            await BlendAPI.create({
                name: newBlendName,
                notes: newBlendNote,
                recipe: recipeItems
            });
            notifications.show({ message: 'Blend created successfully', color: 'green' });
            closeCreate();
            fetchData();
            // Reset
            setNewBlendName('');
            setNewBlendNote('');
            setRecipeItems([]);
        } catch (error: any) {
            notifications.show({ title: 'Error', message: error.message || 'Creation failed', color: 'red' });
        } finally {
            setLoading(false);
        }
    };

    // --- Produce Handlers ---
    const handleOpenProduce = (blend: Blend) => {
        setSelectedBlend(blend);
        setProductionAmount('');
        openProduce();
    };

    const handleProduceBlend = async () => {
        if (!selectedBlend || !productionAmount) return;

        const amount = typeof productionAmount === 'number' ? productionAmount : parseFloat(productionAmount);
        if (amount <= 0) return notifications.show({ message: 'Invalid amount', color: 'red' });

        setLoading(true);
        try {
            await BlendAPI.produce(selectedBlend.id, { amount });
            notifications.show({
                title: 'Success',
                message: `Produced ${amount}kg of ${selectedBlend.name}`,
                color: 'green',
                icon: <CheckCircle />
            });
            closeProduce();
            // Optional: refresh stocks if we were showing them
            fetchData(); // Just to be safe
        } catch (error: any) {
            notifications.show({
                title: 'Production Failed',
                message: error.response?.data?.detail || 'Unknown error',
                color: 'red'
            });
        } finally {
            setLoading(false);
        }
    };

    const getBeanName = (id: number) => beans.find(b => b.id === id)?.name || `Unknown Bean ${id}`;
    const getBeanStock = (id: number) => beans.find(b => b.id === id)?.quantity_kg || 0;

    return (
        <div>
            <PageHero
                title="Blending Management"
                description="Create Recipes and Produce Blends"
                icon={<Layers className="w-10 h-10" />}
                backgroundImage="/images/hero/blends-hero.png"
            />

            <Container size="xl" py="xl">
                <Paper shadow="sm" radius="md" p="md" withBorder>
                    <Group justify="space-between" mb="lg">
                        <Title order={3}>Blend Products</Title>
                        <Button leftSection={<Plus size={16} />} color="orange" onClick={openCreate}>
                            New Blend
                        </Button>
                    </Group>

                    <Grid>
                        {blends.map(blend => (
                            <Grid.Col key={blend.id} span={{ base: 12, md: 6, lg: 4 }}>
                                <Card padding="lg" radius="md" withBorder>
                                    <Group justify="space-between" mb="xs">
                                        <Text fw={500}>{blend.name}</Text>
                                        <Badge color="orange" variant="light">Blend</Badge>
                                    </Group>

                                    <Text size="sm" c="dimmed" mb="md">
                                        {blend.notes || 'No description'}
                                    </Text>

                                    <Divider my="sm" label="Recipe" labelPosition="center" />

                                    <Table mb="md">
                                        <Table.Tbody>
                                            {blend.recipe?.map((item, idx) => (
                                                <Table.Tr key={idx}>
                                                    <Table.Td>{getBeanName(item.bean_id)}</Table.Td>
                                                    <Table.Td align="right">{(item.ratio * 100).toFixed(0)}%</Table.Td>
                                                </Table.Tr>
                                            ))}
                                        </Table.Tbody>
                                    </Table>

                                    <Button
                                        fullWidth
                                        variant="light"
                                        color="blue"
                                        leftSection={<Play size={16} />}
                                        onClick={() => handleOpenProduce(blend)}
                                    >
                                        Produce
                                    </Button>
                                </Card>
                            </Grid.Col>
                        ))}
                    </Grid>
                </Paper>
            </Container>

            {/* Create Modal */}
            <Modal opened={createOpened} onClose={closeCreate} title="Create New Blend Recipe" size="lg">
                <Stack>
                    <TextInput
                        label="Blend Name"
                        placeholder="e.g. House Blend"
                        value={newBlendName}
                        onChange={(e) => setNewBlendName(e.currentTarget.value)}
                        required
                    />
                    <TextInput
                        label="Notes"
                        placeholder="Description"
                        value={newBlendNote}
                        onChange={(e) => setNewBlendNote(e.currentTarget.value)}
                    />

                    <Text fw={500} mt="md">Ingredients</Text>
                    {recipeItems.map((item, index) => (
                        <Group key={index} grow align="flex-end">
                            <Select
                                label={index === 0 ? "Bean" : ""}
                                placeholder="Select Bean"
                                data={beans.map(b => ({ value: b.id.toString(), label: `${b.name} (${b.quantity_kg}kg)` }))}
                                value={item.bean_id ? item.bean_id.toString() : null}
                                onChange={(val) => handleIngredientChange(index, 'bean_id', val)}
                                searchable
                            />
                            <NumberInput
                                label={index === 0 ? "Ratio (0.0 - 1.0)" : ""}
                                placeholder="0.5"
                                min={0} max={1} step={0.1} decimalScale={2}
                                value={item.ratio}
                                onChange={(val) => handleIngredientChange(index, 'ratio', val)}
                            />
                            <ActionIcon color="red" variant="subtle" onClick={() => handleRemoveIngredient(index)} mb={4}>
                                <Trash size={16} />
                            </ActionIcon>
                        </Group>
                    ))}

                    <Button variant="default" size="xs" leftSection={<Plus size={14} />} onClick={handleAddIngredient}>
                        Add Ingredient
                    </Button>

                    <Group justify="right" mt="xl">
                        <Button variant="subtle" onClick={closeCreate}>Cancel</Button>
                        <Button color="orange" onClick={handleCreateBlend}>Create Blend</Button>
                    </Group>
                </Stack>
            </Modal>

            {/* Produce Modal */}
            <Modal opened={produceOpened} onClose={closeProduce} title={`Produce: ${selectedBlend?.name}`} size="md">
                <Stack>
                    <Alert icon={<AlertCircle size={16} />} title="Stock Check" color="blue">
                        Enter the amount to produce. The system will automatically check if enough roasted beans are available.
                    </Alert>

                    <NumberInput
                        label="Production Amount (kg)"
                        placeholder="10.0"
                        min={0}
                        value={productionAmount}
                        onChange={setProductionAmount}
                        required
                    />

                    {selectedBlend && productionAmount && (
                        <Table striped highlightOnHover withTableBorder>
                            <Table.Thead>
                                <Table.Tr>
                                    <Table.Th>Ingredient</Table.Th>
                                    <Table.Th>Required</Table.Th>
                                    <Table.Th>Stock</Table.Th>
                                </Table.Tr>
                            </Table.Thead>
                            <Table.Tbody>
                                {selectedBlend.recipe?.map((item, idx) => {
                                    const required = (parseFloat(productionAmount as string) || 0) * item.ratio;
                                    const stock = getBeanStock(item.bean_id);
                                    const isEnough = stock >= required;
                                    return (
                                        <Table.Tr key={idx}>
                                            <Table.Td>{getBeanName(item.bean_id)}</Table.Td>
                                            <Table.Td>{required.toFixed(2)} kg</Table.Td>
                                            <Table.Td style={{ color: isEnough ? 'green' : 'red', fontWeight: isEnough ? 400 : 700 }}>
                                                {stock.toFixed(2)} kg
                                            </Table.Td>
                                        </Table.Tr>
                                    );
                                })}
                            </Table.Tbody>
                        </Table>
                    )}

                    <Group justify="right" mt="xl">
                        <Button variant="subtle" onClick={closeProduce}>Cancel</Button>
                        <Button color="blue" onClick={handleProduceBlend} loading={loading}>
                            Confirm Production
                        </Button>
                    </Group>
                </Stack>
            </Modal>
        </div>
    );
}
