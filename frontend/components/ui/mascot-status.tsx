'use client';

import React, { useMemo } from 'react';
import { motion } from 'framer-motion';
import { Search, Info, AlertTriangle, Moon, Loader2, CheckCircle2 } from 'lucide-react';

type MascotVariant = 'empty' | 'error' | 'search' | 'sleep' | 'not-found' | 'loading' | 'success';

interface MascotStatusProps {
    variant?: MascotVariant;
    title: string;
    description?: string;
    action?: React.ReactNode;
    className?: string;
    videoClassName?: string;
    textColor?: string;
}


const VIDEOS: Record<MascotVariant, string> = {
    empty: '/videos/mascot_default.mp4',
    search: '/videos/mascot_empty.mp4', // Updated per user request
    sleep: '/videos/mascot_sleep.mp4',
    error: '/videos/mascot_error.mp4',
    'not-found': '/videos/mascot_not_found.mp4',
    loading: '/videos/mascot_default.mp4', // Back to default (Rainy window)
    success: '/videos/mascot_default.mp4', // Happy default
};

export default function MascotStatus({
    variant = 'empty',
    title,
    description,
    action,
    className = '',
    videoClassName = 'w-60 h-60', // Updated default size (1.5x larger)
    textColor = 'text-latte-900', // Default color
}: MascotStatusProps) {
    const Icon = useMemo(() => {
        switch (variant) {
            case 'search': return Search;
            case 'error': return AlertTriangle;
            case 'sleep': return Moon;
            case 'loading': return Loader2;
            case 'success': return CheckCircle2;
            default: return Info;
        }
    }, [variant]);

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`flex flex-col items-center justify-center p-8 text-center w-full max-w-[450px] mx-auto ${className}`}
        >
            {/* Video Container (Mascot) */}
            <div className={`relative mb-6 rounded-full overflow-hidden border-4 border-latte-100 shadow-xl shadow-latte-200/50 flex-shrink-0 ${videoClassName}`}>
                <video
                    autoPlay
                    loop
                    muted
                    playsInline
                    className="w-full h-full object-cover scale-110"
                >
                    <source src={VIDEOS[variant]} type="video/mp4" />
                </video>
                <div className="absolute inset-0 bg-gradient-to-t from-latte-900/10 to-transparent pointer-events-none" />
            </div>

            {/* Text Content */}
            <div className="max-w-md space-y-3">
                <div className="flex items-center justify-center gap-2 mb-1">
                    <div className="p-1.5 bg-latte-50 rounded-lg">
                        <Icon className="w-4 h-4 text-latte-400" />
                    </div>
                    <span className="text-[10px] font-black uppercase tracking-[0.2em] text-latte-300">
                        {variant.replace('-', ' ')}
                    </span>
                </div>

                <h3 className={`text-2xl font-serif font-bold leading-tight ${textColor}`}>
                    {title}
                </h3>

                {description && (
                    <p className={`font-medium text-sm leading-relaxed ${textColor === 'text-latte-900' ? 'text-latte-500' : 'text-white/80'}`}>
                        {description}
                    </p>
                )}
            </div>

            {/* Action Button */}
            {action && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.3 }}
                    className="mt-8"
                >
                    {action}
                </motion.div>
            )}
        </motion.div>
    );
}
