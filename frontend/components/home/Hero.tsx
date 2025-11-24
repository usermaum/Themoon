import Link from 'next/link'

export default function Hero() {
    return (
        <div className="relative bg-gray-900 overflow-hidden">
            <div className="absolute inset-0">
                <img
                    className="w-full h-full object-cover opacity-30"
                    src="https://images.unsplash.com/photo-1497935586351-b67a49e012bf?ixlib=rb-1.2.1&auto=format&fit=crop&w=1951&q=80"
                    alt="Coffee beans background"
                />
                <div className="absolute inset-0 bg-gradient-to-r from-gray-900 via-gray-900/80 to-transparent" />
            </div>
            <div className="relative max-w-7xl mx-auto py-24 px-4 sm:py-32 sm:px-6 lg:px-8">
                <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-5xl lg:text-6xl">
                    The Moon Drip Bar
                </h1>
                <p className="mt-6 text-xl text-gray-300 max-w-3xl">
                    프리미엄 로스팅 관리 시스템에 오신 것을 환영합니다.
                    <br />
                    원두 재고부터 블렌딩 레시피까지, 모든 과정을 체계적으로 관리하세요.
                </p>
                <div className="mt-10 flex gap-4">
                    <Link
                        href="/beans"
                        className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
                    >
                        원두 관리 시작하기
                    </Link>
                    <Link
                        href="/blends"
                        className="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-200 bg-white/10 hover:bg-white/20 backdrop-blur-sm transition-colors"
                    >
                        블렌드 레시피 보기
                    </Link>
                </div>
            </div>
        </div>
    )
}
