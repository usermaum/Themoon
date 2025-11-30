interface PageHeroProps {
    title: string
    description: string
    backgroundImage?: string
    icon?: string
    showBackground?: boolean
}

export default function PageHero({
    title,
    description,
    backgroundImage,
    icon,
    showBackground = true
}: PageHeroProps) {
    return (
        <div className="relative overflow-hidden z-0">
            {/* 배경 이미지 또는 그라데이션 */}
            {backgroundImage ? (
                <div className="absolute inset-0 -z-10 bg-gray-900">
                    <img
                        src={backgroundImage}
                        alt="Background"
                        className="absolute inset-0 w-full h-full object-cover opacity-60"
                    />
                </div>
            ) : (
                showBackground && (
                    <div className="absolute inset-0 bg-gradient-to-r from-indigo-600 to-purple-600" />
                )
            )}

            {/* 장식적인 패턴 */}
            <div className="absolute inset-0 opacity-10 -z-10">
                <div className="absolute top-0 left-0 w-64 h-64 bg-white rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2" />
                <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full blur-3xl translate-x-1/2 translate-y-1/2" />
            </div>

            {/* 콘텐츠 */}
            <div className="relative z-0 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
                <div className="flex items-center gap-6">
                    {/* 아이콘 */}
                    {icon && (
                        <div className="hidden md:block">
                            <div className="w-20 h-20 bg-white/10 backdrop-blur-md rounded-2xl flex items-center justify-center shadow-2xl border border-white/20">
                                <span className="text-5xl">{icon}</span>
                            </div>
                        </div>
                    )}

                    {/* 텍스트 */}
                    <div className="flex-1">
                        <h1 className="text-4xl md:text-5xl font-bold text-white mb-3 tracking-tight">
                            {title}
                        </h1>
                        <p className="text-lg md:text-xl text-white/90 max-w-3xl leading-relaxed">
                            {description}
                        </p>
                    </div>
                </div>

                {/* 하단 장식선 */}
                <div className="mt-8 h-1 w-24 bg-white/30 rounded-full" />
            </div>
        </div>
    )
}
