'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { BlendAPI, BlendCreateData, Blend } from '@/lib/api';
import BlendForm from '@/components/blends/BlendForm';
import { notifications } from '@mantine/notifications';
import { Center, SimpleGrid, Paper, Card, Stack, Text, Alert, Grid, ScrollArea, Container, Group } from '@mantine/core'; // Mantine imports
import { AlertCircle } from 'lucide-react';
import PageHero from '@/components/ui/PageHero';
import { useLanguage } from '@/lib/i18n/LanguageContext';

export default function EditBlendPage({ params }: { params: { id: string } }) {
    const router = useRouter();
    const { t } = useLanguage();
    const [blend, setBlend] = useState<Blend | undefined>(undefined);
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchBlend = async () => {
            try {
                const data = await BlendAPI.getOne(parseInt(params.id));
                setBlend(data);
            } catch (err) {
                console.error('Failed to fetch blend:', err);
                setError('Failed to load blend details.');
                notifications.show({
                    title: 'Error',
                    message: 'Failed to load blend details.',
                    color: 'red',
                });
            } finally {
                setLoading(false);
            }
        };
        fetchBlend();
    }, [params.id]);

    const handleSubmit = async (data: BlendCreateData) => {
        setSubmitting(true);
        setError(null);

        try {
            await BlendAPI.update(parseInt(params.id), data);
            notifications.show({
                title: 'Success',
                message: 'Blend recipe updated.',
                color: 'green',
            });
            router.push('/blends');
        } catch (err) {
            console.error('Failed to update blend:', err);
            setError('Failed to update blend.');
            notifications.show({
                title: 'Error',
                message: 'Failed to update blend.',
                color: 'red',
            });
            setSubmitting(false);
        }
    };

    const handleDelete = async () => {
        if (!confirm('Are you sure you want to delete this blend?')) return;

        try {
            await BlendAPI.delete(parseInt(params.id));
            notifications.show({
                title: 'Success',
                message: 'Blend deleted.',
                color: 'green',
            });
            router.push('/blends');
        } catch (err) {
            console.error('Failed to delete blend:', err);
            notifications.show({
                title: 'Error',
                message: 'Failed to delete blend.',
                color: 'red',
            });
        }
    };

    if (loading) {
        return (
            <Center py={100}>
                <Text>Loading blend details...</Text>
            </Center>
        );
    }

    if (!blend) {
        return (
            <Center py={100}>
                <Text c="red">Blend not found.</Text>
            </Center>
        );
    }

    return (
        <div>
            {/* Wrapping BlendForm in a nice container or keeping it simple as it is likely a form component */}
            {/* Consider refactoring BlendForm to Mantine later, but for now just wrapping the page structure style */}
            <div className="p-4 md:p-8 max-w-5xl mx-auto">
                {error && (
                    <Alert icon={<AlertCircle size={16} />} title="Error" color="red" mb="xl">
                        {error}
                    </Alert>
                )}

                {/* 
                  Note: BlendForm likely contains Tailwind classes. 
                  Since user asked for "Dashboard Style Migration", deeply refactoring a child component 
                  might be out of scope if it works, but let's ensure the container is nice.
                  Ideally BlendForm should be refactored too to remove shadcn/tailwind dependencies,
                  but for this turn we fix the alert and ensure standard layout.
                */}
                <Paper p="xl" radius="xl" bg="white" shadow="sm">
                    <BlendForm
                        initialData={blend}
                        onSubmit={handleSubmit}
                        onDelete={handleDelete}
                        isSubmitting={submitting}
                        title="Edit Blend Recipe"
                        submitLabel="Update Recipe"
                    />
                </Paper>
            </div>
        </div>
    );
}
