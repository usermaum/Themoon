
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const badgeVariants = cva(
    "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-latte-900 focus:ring-offset-2",
    {
        variants: {
            variant: {
                default:
                    "border-transparent bg-latte-800 text-latte-50 hover:bg-latte-800/80 shadow-[0_2px_10px_rgba(74,64,58,0.2)]",
                secondary:
                    "border-transparent bg-latte-200 text-latte-900 hover:bg-latte-200/80",
                destructive:
                    "border-transparent bg-red-500 text-slate-50 hover:bg-red-500/80",
                outline: "text-latte-800 border-latte-600",
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
