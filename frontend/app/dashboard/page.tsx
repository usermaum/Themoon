"use client";

import React, { useEffect, useState } from 'react';
import { DashboardAPI, DashboardStats, LowStockBean, RecentActivity } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { AlertTriangle, Package, DollarSign, Activity, ArrowUpRight, ArrowDownRight, LayoutDashboard } from 'lucide-react';
import { cn } from "@/lib/utils";
import PageHero from '@/components/ui/PageHero';
import { useLanguage } from '@/lib/i18n/LanguageContext';

export default function DashboardPage() {
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [lowStock, setLowStock] = useState<LowStockBean[]>([]);
    const [activity, setActivity] = useState<RecentActivity[]>([]);
    const [loading, setLoading] = useState(true);
    const { t } = useLanguage();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [statsData, lowStockData, activityData] = await Promise.all([
                    DashboardAPI.getStats(),
                    DashboardAPI.getLowStock(),
                    DashboardAPI.getRecentActivity()
                ]);
                setStats(statsData);
                setLowStock(lowStockData);
                setActivity(activityData);
            } catch (error) {
                console.error("Failed to fetch dashboard data", error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return <div className="p-8 flex justify-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-900"></div></div>;
    }

    return (
        <div>
            <PageHero
                title={t('dashboard.title')}
                description={t('dashboard.description')}
                icon={<LayoutDashboard className="w-10 h-10" />}
                backgroundImage="/images/dashboard-hero-placeholder.jpg"
            />
            <div className="p-8 max-w-7xl mx-auto space-y-8">

                {/* Stats Cards */}
                <div className="grid gap-4 md:grid-cols-3">
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">{t('dashboard.totalValue')}</CardTitle>
                            <DollarSign className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">₩{stats?.total_value.toLocaleString()}</div>
                            <p className="text-xs text-muted-foreground">{t('dashboard.estimatedCost')}</p>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">{t('dashboard.totalWeight')}</CardTitle>
                            <Package className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{stats?.total_weight.toLocaleString()} kg</div>
                            <p className="text-xs text-muted-foreground">{t('dashboard.acrossTypes').replace('{count}', stats?.total_beans.toString() || '0')}</p>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">{t('dashboard.lowStockItems')}</CardTitle>
                            <AlertTriangle className="h-4 w-4 text-red-500" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold text-red-600">{lowStock.length}</div>
                            <p className="text-xs text-muted-foreground">{t('dashboard.itemsBelowThreshold')}</p>
                        </CardContent>
                    </Card>
                </div>

                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                    {/* Recent Activity */}
                    <Card className="col-span-4">
                        <CardHeader>
                            <CardTitle>{t('dashboard.recentActivity')}</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-8">
                                {activity.map((item) => (
                                    <div key={item.id} className="flex items-center">
                                        <div className={cn("h-9 w-9 rounded-full flex items-center justify-center border",
                                            item.type.includes('IN') ? "bg-green-100 border-green-200" : "bg-blue-100 border-blue-200"
                                        )}>
                                            {item.type.includes('IN') ?
                                                <ArrowDownRight className="h-5 w-5 text-green-600" /> :
                                                <ArrowUpRight className="h-5 w-5 text-blue-600" />
                                            }
                                        </div>
                                        <div className="ml-4 space-y-1">
                                            <p className="text-sm font-medium leading-none">{item.bean_name}</p>
                                            <p className="text-xs text-muted-foreground">
                                                {item.type}
                                            </p>
                                        </div>
                                        <div className={cn("ml-auto font-medium", item.type.includes('IN') ? "text-green-600" : "text-blue-600")}>
                                            {item.type.includes('IN') ? "+" : "-"}{item.amount} kg
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>

                    {/* Low Stock List */}
                    <Card className="col-span-3">
                        <CardHeader>
                            <CardTitle>{t('dashboard.lowStockAlerts')}</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                {lowStock.map((bean) => (
                                    <div key={bean.id} className="flex items-center justify-between p-3 bg-red-50 rounded-lg border border-red-100">
                                        <div>
                                            <p className="font-medium text-red-900">{bean.name}</p>
                                            <p className="text-xs text-red-600">{t('dashboard.threshold')}: {bean.threshold}kg</p>
                                        </div>
                                        <div className="text-right">
                                            <span className="text-lg font-bold text-red-700">{bean.quantity_kg}</span>
                                            <span className="text-xs text-red-600 ml-1">kg</span>
                                        </div>
                                    </div>
                                ))}
                                {lowStock.length === 0 && (
                                    <div className="text-center text-muted-foreground py-8">
                                        {t('dashboard.allStockHealthy')}
                                    </div>
                                )}
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
