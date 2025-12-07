import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { FileQuestion } from 'lucide-react'

export default function NotFound() {
    return (
        <div className="flex h-screen flex-col items-center justify-center gap-4 text-center">
            <div className="rounded-full bg-latte-100 p-4 text-latte-600">
                <FileQuestion className="h-8 w-8" />
            </div>
            <h2 className="text-2xl font-bold text-latte-900">Page Not Found</h2>
            <p className="max-w-md text-latte-600">
                The page you are looking for does not exist or has been moved.
            </p>
            <Link href="/">
                <Button className="bg-latte-800 text-white hover:bg-latte-900">
                    Return Home
                </Button>
            </Link>
        </div>
    )
}
