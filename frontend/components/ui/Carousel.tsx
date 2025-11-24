'use client'

import { useState, useEffect, useCallback } from 'react'

interface CarouselProps {
    children: React.ReactNode[]
    autoPlay?: boolean
    interval?: number
}

export default function Carousel({
    children,
    autoPlay = false,
    interval = 5000,
}: CarouselProps) {
    const [currentIndex, setCurrentIndex] = useState(0)
    const [isPaused, setIsPaused] = useState(false)

    const nextSlide = useCallback(() => {
        setCurrentIndex((prev) => (prev + 1) % children.length)
    }, [children.length])

    const prevSlide = () => {
        setCurrentIndex((prev) => (prev - 1 + children.length) % children.length)
    }

    useEffect(() => {
        if (!autoPlay || isPaused) return

        const timer = setInterval(nextSlide, interval)
        return () => clearInterval(timer)
    }, [autoPlay, interval, isPaused, nextSlide])

    if (!children || children.length === 0) return null

    return (
        <div
            className="relative w-full overflow-hidden group"
            onMouseEnter={() => setIsPaused(true)}
            onMouseLeave={() => setIsPaused(false)}
        >
            <div
                className="flex transition-transform duration-500 ease-out"
                style={{ transform: `translateX(-${currentIndex * 100}%)` }}
            >
                {children.map((child, index) => (
                    <div key={index} className="w-full flex-shrink-0 px-2">
                        {child}
                    </div>
                ))}
            </div>

            {/* Navigation Buttons */}
            <button
                onClick={prevSlide}
                className="absolute left-2 top-1/2 -translate-y-1/2 bg-white/80 dark:bg-gray-800/80 p-2 rounded-full shadow-md text-gray-800 dark:text-white opacity-0 group-hover:opacity-100 transition-opacity disabled:opacity-0"
                disabled={currentIndex === 0}
            >
                ←
            </button>
            <button
                onClick={nextSlide}
                className="absolute right-2 top-1/2 -translate-y-1/2 bg-white/80 dark:bg-gray-800/80 p-2 rounded-full shadow-md text-gray-800 dark:text-white opacity-0 group-hover:opacity-100 transition-opacity disabled:opacity-0"
                disabled={currentIndex === children.length - 1}
            >
                →
            </button>

            {/* Indicators */}
            <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex space-x-2">
                {children.map((_, index) => (
                    <button
                        key={index}
                        onClick={() => setCurrentIndex(index)}
                        className={`w-2 h-2 rounded-full transition-colors ${index === currentIndex
                                ? 'bg-indigo-600 dark:bg-indigo-400'
                                : 'bg-gray-300 dark:bg-gray-600'
                            }`}
                    />
                ))}
            </div>
        </div>
    )
}
