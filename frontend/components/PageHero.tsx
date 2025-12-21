import { LucideIcon } from "lucide-react"

interface PageHeroProps {
    icon: LucideIcon
    title: string
    description: string
    variant?: "default" | "midnight" | "sunrise"
}

export function PageHero({
    icon: Icon,
    title,
    description,
    variant = "default",
}: PageHeroProps) {
    const variants = {
        default: "bg-gradient-to-br from-latte-50 to-latte-100/50",
        midnight: "bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white",
        sunrise: "bg-gradient-to-br from-orange-50 to-amber-50",
    }

    return (
        <div className={`
      relative overflow-hidden rounded-3xl p-8 md:p-10 mb-8 mt-2
      ${variants[variant]}
      shadow-sm border border-latte-200/50
    `}>
            <div className="relative z-10 flex flex-col md:flex-row gap-6 md:items-center">
                <div className={`
          p-3 rounded-2xl w-fit
          ${variant === 'midnight' ? 'bg-white/10 text-white' : 'bg-white shadow-sm text-latte-600'}
        `}>
                    <Icon className="w-8 h-8 md:w-10 md:h-10" />
                </div>
                <div className="space-y-2">
                    <h1 className="text-3xl md:text-4xl font-serif font-bold tracking-tight">
                        {title}
                    </h1>
                    <p className={`
            text-base md:text-lg max-w-2xl
            ${variant === 'midnight' ? 'text-slate-300' : 'text-latte-600'}
          `}>
                        {description}
                    </p>
                </div>
            </div>

            {/* Background Decor */}
            <div className="absolute top-0 right-0 -mt-10 -mr-10 w-64 h-64 bg-blob-orange/20 rounded-full blur-3xl pointer-events-none" />
            <div className="absolute bottom-0 left-0 -mb-10 -ml-10 w-48 h-48 bg-blob-green/20 rounded-full blur-3xl pointer-events-none" />
        </div>
    )
}
