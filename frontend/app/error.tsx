'use client' // Error components must be Client Components

import { useEffect } from 'react'
import { Button } from '@/components/ui/Button'
import { AlertCircle } from 'lucide-react'

export default function Error({
    error,
    reset,
}: {
    error: Error & { digest?: string }
    reset: () => void
}) {
    useEffect(() => {
        // Log the error to an error reporting service
        console.error(error)
    }, [error])

    return (
        <div className="flex h-screen flex-col items-center justify-center gap-4 text-center">
            <div className="rounded-full bg-red-100 p-4 text-red-600">
                <AlertCircle className="h-8 w-8" />
            </div>
            <h2 className="text-2xl font-bold text-latte-900">Something went wrong!</h2>
            <p className="max-w-md text-latte-600">
                {error.message || "An unexpected error occurred."}
            </p>
            <div className="flex gap-2">
                <Button
                    onClick={() => window.location.href = '/'}
                    variant="outline"
                >
                    Go Home
                </Button>
                <Button
                    onClick={() => reset()}
                    className="bg-latte-800 text-white hover:bg-latte-900"
                >
                    Try again
                </Button>
            </div>
        </div>
    )
}
