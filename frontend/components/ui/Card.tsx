import Image from 'next/image'
import Link from 'next/link'

interface CardProps {
    title: string
    description: string
    imageUrl?: string
    tags?: string[]
    href?: string
    actionText?: string
}

export default function Card({
    title,
    description,
    imageUrl,
    tags = [],
    href,
    actionText = '자세히 보기',
}: CardProps) {
    return (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 border border-gray-100 dark:border-gray-700 flex flex-col h-full">
            {imageUrl && (
                <div className="relative h-48 w-full">
                    <img
                        src={imageUrl}
                        alt={title}
                        className="w-full h-full object-cover"
                    />
                </div>
            )}
            <div className="p-6 flex-1 flex flex-col">
                <div className="flex-1">
                    <div className="flex flex-wrap gap-2 mb-3">
                        {tags.map((tag) => (
                            <span
                                key={tag}
                                className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800 dark:bg-indigo-900/50 dark:text-indigo-200"
                            >
                                {tag}
                            </span>
                        ))}
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                        {title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-300 text-sm line-clamp-3">
                        {description}
                    </p>
                </div>
                {href && (
                    <div className="mt-6">
                        <Link
                            href={href}
                            className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 font-medium text-sm inline-flex items-center gap-1 group"
                        >
                            {actionText}
                            <span className="group-hover:translate-x-1 transition-transform">→</span>
                        </Link>
                    </div>
                )}
            </div>
        </div>
    )
}
