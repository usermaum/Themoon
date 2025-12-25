'use client';

import useSWR from 'swr';
import { SettingsAPI, SystemStatus } from '@/lib/api/settings'; // Assuming admin.ts is created in lib/api
import { Loader2, Cpu, HardDrive, Database, Server } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';

export default function AdminDashboardPage() {
    const { data, error, isLoading } = useSWR<SystemStatus>(
        '/admin/status',
        SettingsAPI.getSystemStatus,
        { refreshInterval: 5000 } // Poll every 5 seconds
    );

    if (isLoading) {
        return (
            <div className="flex justify-center items-center h-64">
                <Loader2 className="w-8 h-8 animate-spin text-latte-400" />
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-8 text-center text-red-500 bg-red-50 rounded-xl border border-red-200">
                시스템 상태를 불러오는데 실패했습니다.
            </div>
        );
    }

    if (!data) return null;

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {/* CPU */}
            <StatusCard
                title="CPU 사용량"
                icon={Cpu}
                value={`${data.cpu.usage_percent}%`}
                status={data.cpu.status === 'normal' ? 'success' : 'warning'}
                subtext={data.cpu.status === 'critical' ? '과부하 상태' : '안정적'}
            >
                <Progress value={data.cpu.usage_percent} className="h-2" />
            </StatusCard>

            {/* Memory */}
            <StatusCard
                title="메모리"
                icon={Server}
                value={`${data.memory.usage_percent}%`}
                status={data.memory.usage_percent > 80 ? 'warning' : 'success'}
                subtext={`${data.memory.used_gb}GB / ${data.memory.total_gb}GB`}
            >
                <Progress value={data.memory.usage_percent} className="h-2" />
            </StatusCard>

            {/* Disk (Root) */}
            <StatusCard
                title="디스크 (Root)"
                icon={HardDrive}
                value={`${data.disk.usage_percent}%`}
                status={data.disk.usage_percent > 90 ? 'critical' : 'success'}
                subtext={`여유 공간: ${data.disk.free_gb.toFixed(1)}GB`}
            >
                <Progress value={data.disk.usage_percent} className="h-2" />
            </StatusCard>

            {/* Storage (Images) */}
            <StatusCard
                title="이미지 저장소"
                icon={Database}
                value={`${data.storage.images_size_mb} MB`}
                status="neutral"
                subtext="Total Images Size"
            />
        </div>
    );
}

function StatusCard({
    title,
    icon: Icon,
    value,
    status = 'neutral',
    subtext,
    children,
}: {
    title: string;
    icon: any;
    value: string;
    status?: 'success' | 'warning' | 'critical' | 'neutral';
    subtext?: string;
    children?: React.ReactNode;
}) {
    const statusColors = {
        success: 'text-green-600',
        warning: 'text-amber-500',
        critical: 'text-red-500',
        neutral: 'text-latte-900',
    };

    return (
        <Card className="border-latte-200 shadow-sm">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-latte-600">{title}</CardTitle>
                <Icon className="h-4 w-4 text-latte-400" />
            </CardHeader>
            <CardContent>
                <div className={`text-2xl font-bold ${statusColors[status]}`}>{value}</div>
                <p className="text-xs text-latte-400 mt-1 mb-3">{subtext}</p>
                {children}
            </CardContent>
        </Card>
    );
}
