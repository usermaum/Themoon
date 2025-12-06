
import * as React from "react"
import { cn } from "@/lib/utils"
import Link from 'next/link'

// --- Compound Components (shadcn style) ---
// Note: CardRoot is exported as Card to maintain compatibility with Shadcn imports
const CardRoot = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
    <div
        ref={ref}
        className={cn(
            "rounded-[2rem] border border-latte-200 bg-white text-latte-800 shadow-sm transition-all duration-300 hover:shadow-lg hover:border-latte-300",
            className
        )}
        {...props}
    />
))
CardRoot.displayName = "Card"

const CardHeader = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
    <div
        ref={ref}
        className={cn("flex flex-col space-y-1.5 p-6", className)}
        {...props}
    />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<
    HTMLParagraphElement,
    React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
    <h3
        ref={ref}
        className={cn(
            "font-serif text-2xl font-semibold leading-none tracking-tight text-latte-900",
            className
        )}
        {...props}
    />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<
    HTMLParagraphElement,
    React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
    <p
        ref={ref}
        className={cn("text-sm text-latte-600", className)}
        {...props}
    />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
    <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
    <div
        ref={ref}
        className={cn("flex items-center p-6 pt-0", className)}
        {...props}
    />
))
CardFooter.displayName = "CardFooter"

// --- Legacy Functional Component (Adapter) ---
// This allows using the Card component as a single prop-based component if needed
// while favoring the Composition pattern for new code.
interface LegacyCardProps {
    title: string
    description: string
    imageUrl?: string
    tags?: string[]
    href?: string
    actionText?: string
    className?: string
}

function LegacyCard({
    title,
    description,
    imageUrl,
    tags = [],
    href,
    actionText = '자세히 보기',
    className,
}: LegacyCardProps) {
    return (
        <CardRoot className={cn("overflow-hidden flex flex-col h-full", className)}>
            {imageUrl && (
                <div className="relative h-48 w-full">
                    <img
                        src={imageUrl}
                        alt={title}
                        className="w-full h-full object-cover"
                    />
                </div>
            )}
            <CardContent className="p-6 flex-1 flex flex-col">
                <div className="flex-1">
                    {tags.length > 0 && (
                        <div className="flex flex-wrap gap-2 mb-3">
                            {tags.map((tag) => (
                                <span
                                    key={tag}
                                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-latte-100 text-latte-800"
                                >
                                    {tag}
                                </span>
                            ))}
                        </div>
                    )}
                    <CardTitle className="mb-2">{title}</CardTitle>
                    <CardDescription className="line-clamp-3">
                        {description}
                    </CardDescription>
                </div>
                {href && (
                    <div className="mt-6">
                        <Link
                            href={href}
                            className="text-latte-600 hover:text-latte-900 font-medium text-sm inline-flex items-center gap-1 group"
                        >
                            {actionText}
                            <span className="group-hover:translate-x-1 transition-transform">→</span>
                        </Link>
                    </div>
                )}
            </CardContent>
        </CardRoot>
    )
}

export { CardRoot as Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }
export default LegacyCard
