'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Check, Loader2, LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';
import { ButtonProps, Button } from './button';

interface MorphingButtonProps extends ButtonProps {
    status: 'idle' | 'loading' | 'success';
    idleText: string;
    successText?: string;
    icon?: LucideIcon;
}

export function MorphingButton({
    status,
    idleText,
    successText = 'Done',
    icon: Icon,
    className,
    disabled,
    ...props
}: MorphingButtonProps) {
    return (
        <Button
            {...props}
            disabled={disabled || status === 'loading' || status === 'success'}
            className={cn(
                'relative overflow-hidden transition-all duration-300',
                status === 'success' && 'bg-emerald-600 hover:bg-emerald-700 text-white',
                className
            )}
            asChild={false} // Force button for animation logic
        >
            <motion.div
                initial={false}
                animate={{
                    width: 'auto',
                }}
                className="flex items-center justify-center gap-2 min-w-[100px]"
            >
                <AnimatePresence mode="wait">
                    {status === 'idle' && (
                        <motion.div
                            key="idle"
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            className="flex items-center gap-2"
                        >
                            {Icon && <Icon className="w-4 h-4" />}
                            <span>{idleText}</span>
                        </motion.div>
                    )}
                    {status === 'loading' && (
                        <motion.div
                            key="loading"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="flex items-center gap-2"
                        >
                            <Loader2 className="w-4 h-4 animate-spin" />
                            <span>Processing...</span>
                        </motion.div>
                    )}
                    {status === 'success' && (
                        <motion.div
                            key="success"
                            initial={{ opacity: 0, scale: 0.5 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.5 }}
                            className="flex items-center gap-2"
                        >
                            <Check className="w-4 h-4" />
                            <span>{successText}</span>
                        </motion.div>
                    )}
                </AnimatePresence>
            </motion.div>
        </Button>
    );
}
