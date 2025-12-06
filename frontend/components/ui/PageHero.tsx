
import React from 'react'
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
        <div className={cn(
            "relative w-full rounded-[2rem] overflow-hidden bg-latte-100 text-latte-800 shadow-sm border border-latte-200 mb-8 transition-transform hover:shadow-md",
            className
        )}>
            {/* Background Blobs for Hero */}
            <div className="absolute -top-24 -right-24 w-64 h-64 bg-blob-orange/30 rounded-full blur-3xl pointer-events-none"></div>
            <div className="absolute -bottom-24 -left-24 w-64 h-64 bg-blob-green/30 rounded-full blur-3xl pointer-events-none"></div>

            <div className="relative z-10 p-10 flex flex-col md:flex-row items-center gap-8">
                {icon && (
                    <div className="p-4 rounded-full bg-white/60 backdrop-blur-md shadow-sm text-latte-600">
                        {React.cloneElement(icon as React.ReactElement, { size: 48 })}
                    </div>
                )}

                <div className="flex-1 text-center md:text-left">
                    <h1 className="font-serif text-4xl md:text-5xl font-bold mb-4 tracking-tight text-latte-900">
                        {title}
                    </h1>
                    {description && (
                        <p className="text-lg text-latte-700 max-w-2xl leading-relaxed">
                            {description}
                        </p>
                    )}
                </div>
            </div>
        </div>
    )
}
