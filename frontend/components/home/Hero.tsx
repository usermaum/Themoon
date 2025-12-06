
import Link from 'next/link'
import { Button } from '@/components/ui/Button'

export default function Hero() {
    return (
        <div className="relative rounded-[2rem] overflow-hidden my-6 mx-4 md:mx-0 shadow-xl">
            <div className="absolute inset-0">
                <img
                    className="w-full h-full object-cover"
                    src="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1920&q=80"
                    alt="Hand drip coffee brewing"
                />
                <div className="absolute inset-0 bg-latte-900/40 backdrop-blur-[2px]"></div>
            </div>

            {/* Blobs */}
            <div className="absolute top-0 right-0 w-96 h-96 bg-blob-orange/40 rounded-full blur-[80px] pointer-events-none mix-blend-soft-light"></div>
            <div className="absolute bottom-0 left-0 w-96 h-96 bg-blob-green/40 rounded-full blur-[80px] pointer-events-none mix-blend-soft-light"></div>

            <div className="relative max-w-7xl mx-auto py-24 px-4 sm:py-32 sm:px-6 lg:px-8 text-center md:text-left">
                <h1 className="font-serif text-4xl font-bold tracking-tight text-white sm:text-6xl drop-shadow-sm">
                    The Moon <span className="text-latte-200">Drip Bar</span>
                </h1>
                <p className="mt-6 text-xl text-latte-100 max-w-3xl leading-relaxed drop-shadow-sm">
                    프리미엄 로스팅 관리 시스템에 오신 것을 환영합니다.
                    <br />
                    원두 재고부터 블렌딩 레시피까지, 모든 과정을 체계적으로 관리하세요.
                </p>
                <div className="mt-10 flex gap-4 justify-center md:justify-start">
                    <Button asChild size="lg" className="text-lg">
                        <Link href="/beans">
                            원두 관리 시작하기
                        </Link>
                    </Button>
                    <Button asChild variant="outline" size="lg" className="text-lg bg-white/10 border-white/30 text-white hover:bg-white/20 hover:text-white backdrop-blur-md">
                        <Link href="/blends">
                            블렌드 레시피 보기
                        </Link>
                    </Button>
                </div>
            </div>
        </div>
    )
}
