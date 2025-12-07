'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

interface PageHeroProps {
    title: string
    description?: string
    image?: string
    icon?: React.ReactNode
    className?: string
}

export default function PageHero({
    title,
    description,
    image,
    icon,
    className
}: PageHeroProps) {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
            className={cn(
                "relative w-full min-h-[400px] flex items-center overflow-hidden bg-latte-900 text-white shadow-md transition-transform hover:shadow-lg",
                className
            )}
        >
            {image && (
                <motion.div
                    initial={{ scale: 1.1, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ duration: 0.7, ease: 'easeOut' }}
                    className="absolute inset-0"
                >
                    <img
                        src={image}
                        alt={title}
                        className="w-full h-full object-cover opacity-90 transition-transform duration-700 hover:scale-105"
                    />
                    <div className="absolute inset-0 bg-latte-900/50 backdrop-blur-[2px]"></div>
                </motion.div>
            )}

            {/* Background Blobs (Visible if no image, or as subtle overlay) */}
            {!image && (
                <>
                    <div className="absolute -top-24 -right-24 w-64 h-64 bg-blob-orange/30 rounded-full blur-3xl pointer-events-none"></div>
                    <div className="absolute -bottom-24 -left-24 w-64 h-64 bg-blob-green/30 rounded-full blur-3xl pointer-events-none"></div>
                </>
            )}

            <div className="relative z-10 container mx-auto px-6 py-20 flex flex-col md:flex-row items-center gap-10 justify-center h-full">
                {icon && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.4, delay: 0.2 }}
                        className="p-6 rounded-full bg-white/10 backdrop-blur-md shadow-2xl text-latte-50 border border-white/20"
                    >
                        {React.cloneElement(icon as React.ReactElement<any>, { size: 64 })}
                    </motion.div>
                )}

                <div className="flex-1 text-center md:text-left max-w-3xl">
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.3 }}
                        className="font-serif text-5xl md:text-6xl font-bold mb-6 tracking-tight text-white drop-shadow-lg"
                    >
                        {title}
                    </motion.h1>
                    {description && (
                        <motion.p
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0.45 }}
                            className="text-xl md:text-2xl text-latte-100 leading-relaxed drop-shadow-md font-light"
                        >
                            {description}
                        </motion.p>
                    )}
                </div>
            </div>
        </motion.div>
    )
}

