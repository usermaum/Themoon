
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
            "relative w-full rounded-[2rem] overflow-hidden bg-latte-900 text-white shadow-md mb-8 transition-transform hover:shadow-lg",
            className
        )}>
            {image && (
                <div className="absolute inset-0">
                    <img
                        src={image}
                        alt={title}
                        className="w-full h-full object-cover opacity-90 transition-transform duration-700 hover:scale-105"
                    />
                    <div className="absolute inset-0 bg-latte-900/50 backdrop-blur-[2px]"></div>
                </div>
            )}

            {/* Background Blobs (Visible if no image, or as subtle overlay) */}
            {!image && (
                <>
                    <div className="absolute -top-24 -right-24 w-64 h-64 bg-blob-orange/30 rounded-full blur-3xl pointer-events-none"></div>
                    <div className="absolute -bottom-24 -left-24 w-64 h-64 bg-blob-green/30 rounded-full blur-3xl pointer-events-none"></div>
                </>
            )}

            <div className="relative z-10 p-10 flex flex-col md:flex-row items-center gap-8">
                {icon && (
                    <div className="p-4 rounded-full bg-white/20 backdrop-blur-md shadow-sm text-latte-50 border border-white/30">
                        {React.cloneElement(icon as React.ReactElement, { size: 48 })}
                    </div>
                )}

                <div className="flex-1 text-center md:text-left">
                    <h1 className="font-serif text-4xl md:text-5xl font-bold mb-4 tracking-tight text-white drop-shadow-sm">
                        {title}
                    </h1>
                    {description && (
                        <p className="text-lg text-latte-100 max-w-2xl leading-relaxed drop-shadow-sm">
                            {description}
                        </p>
                    )}
                </div>
            </div>
        </div>
    )
}
