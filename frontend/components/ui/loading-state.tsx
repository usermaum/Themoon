'use client'

import { ComponentType } from 'react'
import { Loader2, Coffee } from "lucide-react"
import { motion } from "framer-motion"

interface LoadingStateProps {
    message?: string
}

export default function LoadingState({ message = "Loading..." }: LoadingStateProps) {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.4 }}
            className="fixed inset-0 z-[100] grid place-items-center bg-white/80 backdrop-blur-md"
        >
            <div className="flex flex-col items-center justify-center gap-8">
                <div className="relative">
                    {/* Outer Glow/Pulse */}
                    <div className="absolute inset-0 animate-ping rounded-full bg-latte-200 opacity-20 delay-1000 duration-[3s]"></div>

                    {/* Icon Container */}
                    <div className="relative flex h-32 w-32 items-center justify-center rounded-3xl bg-white shadow-2xl ring-1 ring-latte-100">
                        <Coffee className="h-16 w-16 text-latte-600 animate-pulse duration-[2s]" strokeWidth={1.5} />
                    </div>

                    {/* Spinner Badge */}
                    <div className="absolute -bottom-2 -right-2 flex h-10 w-10 items-center justify-center rounded-full bg-latte-600 shadow-lg ring-4 ring-white">
                        <Loader2 className="h-5 w-5 text-white animate-spin" />
                    </div>
                </div>

                <div className="flex flex-col items-center gap-2">
                    <p className="text-xl font-serif font-bold text-latte-900 animate-pulse">
                        {message}
                    </p>
                    <p className="text-sm font-medium tracking-[0.2em] text-latte-400 uppercase">
                        Please wait
                    </p>
                </div>
            </div>
        </motion.div>
    )
}
