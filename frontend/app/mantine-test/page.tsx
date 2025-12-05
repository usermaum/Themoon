'use client';

import { Button, Container, Title, Text, Group, Paper } from '@mantine/core';

export default function MantineTestPage() {
    return (
        <Container size="sm" py="xl">
            <Paper shadow="md" p="xl" radius="md" withBorder>
                <Title order={2} mb="md">Mantine UI Integration Test</Title>
                <Text c="dimmed" mb="lg">
                    Mantine UI v7이 성공적으로 설정되었습니다. 이 페이지는 Tailwind CSS와 Mantine UI가 공존하는지 확인합니다.
                </Text>

                <Group>
                    <Button variant="filled" color="blue">Primary Button</Button>
                    <Button variant="light" color="cyan">Light Button</Button>
                    <Button variant="outline" color="grape">Outline Button</Button>
                </Group>

                <div className="mt-8 p-4 bg-gray-100 rounded-lg">
                    <Text size="sm" fw={500}>Tailwind CSS Utility Test:</Text>
                    <div className="text-blue-500 font-bold">
                        이 텍스트는 Tailwind CSS 'text-blue-500 font-bold' 클래스를 사용합니다.
                    </div>
                </div>
            </Paper>
        </Container>
    );
}
