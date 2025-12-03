import React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const badgeVariants = cva(
    "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
    {
        variants: {
            variant: {
                default:
                    "border-transparent bg-artistic-text text-white hover:bg-artistic-text/80",
                secondary:
                    "border-transparent bg-artistic-peach text-artistic-text hover:bg-artistic-peach/80",
                destructive:
                    "border-transparent bg-red-500 text-white hover:bg-red-600",
                outline: "text-artistic-text border-artistic-border",
                mint: "border-transparent bg-artistic-mint text-artistic-text hover:bg-artistic-mint/80",
                cream: "border-transparent bg-artistic-cream text-artistic-muted hover:bg-artistic-border",
            },
        },
        defaultVariants: {
            variant: "default",
        },
    }
)

export interface BadgeProps
    extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> { }

function Badge({ className, variant, ...props }: BadgeProps) {
    return (
        <div className={cn(badgeVariants({ variant }), className)} {...props} />
    )
}

export { Badge, badgeVariants }
