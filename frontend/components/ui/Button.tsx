import React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
    "inline-flex items-center justify-center whitespace-nowrap rounded-full text-sm font-medium ring-offset-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-artistic-peach focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
    {
        variants: {
            variant: {
                default: "bg-artistic-text text-white hover:bg-artistic-text/90 shadow-sm",
                destructive: "bg-red-500 text-white hover:bg-red-600 shadow-sm",
                outline: "border border-artistic-border bg-transparent hover:bg-artistic-base hover:text-artistic-text",
                secondary: "bg-artistic-peach text-artistic-text hover:bg-artistic-peach/80 shadow-sm",
                ghost: "hover:bg-artistic-base hover:text-artistic-text",
                link: "text-artistic-text underline-offset-4 hover:underline",
                mint: "bg-artistic-mint text-artistic-text hover:bg-artistic-mint/80 shadow-sm",
                cream: "bg-artistic-cream text-artistic-text hover:bg-artistic-border shadow-sm",
            },
            size: {
                default: "h-10 px-6 py-2",
                sm: "h-9 rounded-full px-4",
                lg: "h-12 rounded-full px-8 text-base",
                icon: "h-10 w-10",
            },
        },
        defaultVariants: {
            variant: "default",
            size: "default",
        },
    }
)

export interface ButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
    asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant, size, asChild = false, ...props }, ref) => {
        return (
            <button
                className={cn(buttonVariants({ variant, size, className }))}
                ref={ref}
                {...props}
            />
        )
    }
)
Button.displayName = "Button"

export { Button, buttonVariants }
