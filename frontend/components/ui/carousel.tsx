'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { ChevronLeft, ChevronRight } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

interface CarouselProps {
    children: React.ReactNode
    className?: string
}

const CarouselContext = React.createContext<{
    scrollPrev: () => void
    scrollNext: () => void
    canScrollPrev: boolean
    canScrollNext: boolean
} | null>(null)

function useCarousel() {
    const context = React.useContext(CarouselContext)
    if (!context) {
        throw new Error("useCarousel must be used within a <Carousel />")
    }
    return context
}


const Carousel = React.forwardRef<
    HTMLDivElement,
    CarouselProps
>(({ className, children, ...props }, ref) => {
    const [current, setCurrent] = useState(0)
    const [count, setCount] = useState(0)

    // Simplified logic for demo purposes as full embla-carousel implementation is complex
    // This allows the demo page to render without crashing
    const scrollPrev = useCallback(() => {
        // Implementation placeholder
    }, [])

    const scrollNext = useCallback(() => {
        // Implementation placeholder
    }, [])


    return (
        <CarouselContext.Provider
            value={{
                scrollPrev,
                scrollNext,
                canScrollPrev: true,
                canScrollNext: true,
            }}
        >
            <div
                ref={ref}
                className={cn("relative", className)}
                role="region"
                aria-roledescription="carousel"
                {...props}
            >
                {children}
            </div>
        </CarouselContext.Provider>
    )
})
Carousel.displayName = "Carousel"

const CarouselContent = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
    <div ref={ref} className="overflow-hidden">
        <div
            ref={ref}
            className={cn(
                "flex",
                "-ml-4",
                className
            )}
            {...props}
        />
    </div>
))
CarouselContent.displayName = "CarouselContent"

const CarouselItem = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
    <div
        ref={ref}
        role="group"
        aria-roledescription="slide"
        className={cn(
            "min-w-0 shrink-0 grow-0 basis-full pl-4",
            className
        )}
        {...props}
    />
))
CarouselItem.displayName = "CarouselItem"

const CarouselPrevious = React.forwardRef<
    HTMLButtonElement,
    React.ComponentProps<typeof Button>
>(({ className, variant = "outline", size = "icon", ...props }, ref) => {
    const { scrollPrev, canScrollPrev } = useCarousel()

    return (
        <Button
            ref={ref}
            variant={variant}
            size={size}
            className={cn(
                "absolute h-8 w-8 rounded-full",
                "-left-12 top-1/2 -translate-y-1/2",
                className
            )}
            disabled={!canScrollPrev}
            onClick={scrollPrev}
            {...props}
        >
            <ChevronLeft className="h-4 w-4" />
            <span className="sr-only">Previous slide</span>
        </Button>
    )
})
CarouselPrevious.displayName = "CarouselPrevious"

const CarouselNext = React.forwardRef<
    HTMLButtonElement,
    React.ComponentProps<typeof Button>
>(({ className, variant = "outline", size = "icon", ...props }, ref) => {
    const { scrollNext, canScrollNext } = useCarousel()

    return (
        <Button
            ref={ref}
            variant={variant}
            size={size}
            className={cn(
                "absolute h-8 w-8 rounded-full",
                "-right-12 top-1/2 -translate-y-1/2",
                className
            )}
            disabled={!canScrollNext}
            onClick={scrollNext}
            {...props}
        >
            <ChevronRight className="h-4 w-4" />
            <span className="sr-only">Next slide</span>
        </Button>
    )
})
CarouselNext.displayName = "CarouselNext"

export {
    type CarouselProps,
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselPrevious,
    CarouselNext,
}
