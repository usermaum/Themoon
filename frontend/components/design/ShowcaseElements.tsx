'use client';

import { motion } from 'framer-motion';
import { LucideIcon, TrendingUp, Coffee, AlertTriangle, BarChart3, Sparkles } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';

export function StatCard({
    title,
    value,
    unit,
    icon: Icon,
    color,
    progress
}: {
    title: string;
    value: string;
    unit: string;
    icon: LucideIcon;
    color: string;
    progress?: number;
}) {
    return (
        <Card className="bg-white border-latte-100 shadow-sm hover:shadow-md transition-shadow rounded-[1.5rem]">
            <CardContent className="p-6">
                <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-latte-500 uppercase tracking-wider">
                        {title}
                    </span>
                    <Icon className={`w-4 h-4 ${color}`} />
                </div>
                <div className="flex items-baseline gap-2">
                    <span className="text-4xl font-serif font-bold text-latte-900">{value}</span>
                    <span className="text-latte-400">{unit}</span>
                </div>
                {progress !== undefined && (
                    <div className="mt-4 h-1 bg-latte-100 rounded-full overflow-hidden">
                        <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${progress}%` }}
                            className="h-full bg-latte-800"
                        />
                    </div>
                )}
            </CardContent>
        </Card>
    );
}

export function WarningCard({
    title,
    message,
    buttonText
}: {
    title: string;
    message: string;
    buttonText: string;
}) {
    return (
        <Card className="bg-amber-50 border-amber-200 border-2 border-dashed relative overflow-hidden rounded-[1.5rem]">
            <div className="absolute -top-4 -right-4 w-24 h-24 bg-amber-200/20 rounded-full" />
            <CardHeader className="pb-2">
                <CardTitle className="text-amber-900 flex items-center gap-2">
                    <AlertTriangle className="w-5 h-5" /> {title}
                </CardTitle>
            </CardHeader>
            <CardContent>
                <div className="text-sm text-amber-700 leading-relaxed" dangerouslySetInnerHTML={{ __html: message }} />
                <Button
                    size="sm"
                    className="mt-4 bg-amber-600 hover:bg-amber-700 text-white w-full h-10 rounded-xl"
                >
                    {buttonText}
                </Button>
            </CardContent>
        </Card>
    );
}

export function PaperMenuCard() {
    return (
        <Card className="bg-[#FCFAF8] border-none shadow-xl relative transform -rotate-1 rounded-[1.5rem] h-full">
            <div className="absolute inset-0 border-2 border-dashed border-latte-200 m-2 rounded-xl pointer-events-none" />
            <CardHeader className="text-center pt-8 pb-2">
                <div className="w-12 h-1 bg-latte-300 mx-auto mb-4" />
                <CardTitle className="font-serif italic text-3xl text-latte-900">
                    Today's Pick
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 px-8 pb-8">
                <div className="flex justify-between border-b border-latte-100 pb-2">
                    <span className="font-bold text-latte-800">Hand Drip</span>
                    <span className="font-mono text-latte-500">₩ 6,500</span>
                </div>
                <div className="flex justify-between border-b border-latte-100 pb-2">
                    <span className="font-bold text-latte-800">Flat White</span>
                    <span className="font-mono text-latte-500">₩ 5,500</span>
                </div>
                <p className="text-center text-xs text-latte-400 mt-4 italic font-serif">
                    Roasted daily at TheMoon
                </p>
            </CardContent>
        </Card>
    );
}

export function GlassCard({
    title,
    description,
    badge
}: {
    title: string;
    description: string;
    badge: string;
}) {
    return (
        <div className="relative group perspective-1000 h-full">
            <motion.div
                whileHover={{ rotateY: 10, rotateX: -5 }}
                className="h-full bg-white/40 backdrop-blur-xl rounded-[2rem] border border-white/60 p-8 shadow-2xl relative z-10 overflow-hidden"
            >
                <div className="absolute -bottom-10 -right-10 w-40 h-40 bg-latte-400/20 rounded-full blur-3xl group-hover:bg-latte-500/30 transition-colors" />
                <div className="w-14 h-14 bg-latte-900 rounded-2xl flex items-center justify-center text-white mb-6">
                    <Sparkles className="w-7 h-7" />
                </div>
                <h3 className="text-2xl font-serif font-bold text-latte-900 mb-4">
                    {title}
                </h3>
                <p className="text-latte-700 leading-relaxed mb-6">
                    {description}
                </p>
                <Badge className="bg-white/50 text-latte-900 border-white/20 px-3 py-1">{badge}</Badge>
            </motion.div>
            <div className="absolute inset-0 bg-latte-200/20 rounded-[2rem] transform translate-x-4 translate-y-4 -z-10" />
        </div>
    );
}

export function MinimalistStatCard({
    value,
    title,
    target,
    trend
}: {
    value: string;
    title: string;
    target: string;
    trend: string;
}) {
    return (
        <Card className="bg-white border-latte-200 rounded-[2.5rem] p-8 shadow-sm flex flex-col justify-between overflow-hidden h-full">
            <div>
                <div className="flex justify-between items-start mb-10">
                    <div className="bg-latte-50 p-4 rounded-2xl">
                        <BarChart3 className="w-8 h-8 text-latte-600" />
                    </div>
                    <Badge variant="outline" className="text-latte-400 border-latte-200 px-3 py-1">
                        Live
                    </Badge>
                </div>
                <h2 className="text-5xl font-bold text-latte-900 tracking-tighter mb-2">
                    {value}
                </h2>
                <p className="text-latte-500 font-medium">{title}</p>
            </div>
            <div className="pt-8 border-t border-latte-50">
                <div className="flex justify-between text-sm">
                    <span className="text-latte-400">Target: {target}</span>
                    <span className="text-green-600 font-bold">{trend}</span>
                </div>
            </div>
        </Card>
    );
}
