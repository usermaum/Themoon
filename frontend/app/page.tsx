/**
 * TheMoon 메인 페이지
 *
 * 원본 참조: /mnt/d/Ai/WslProject/TheMoon_Project/app/pages/Dashboard.py
 */

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-8 text-center">
          TheMoon 로스팅 원가 계산
        </h1>
        <p className="text-center text-gray-600 mb-8">
          커피 로스팅 원가 계산 및 재고 관리 시스템
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-12">
          <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold mb-2">원두 관리</h2>
            <p className="text-gray-600">원두 정보 및 가격 관리</p>
          </div>

          <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold mb-2">블렌드 관리</h2>
            <p className="text-gray-600">블렌드 레시피 및 원가 계산</p>
          </div>

          <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold mb-2">재고 관리</h2>
            <p className="text-gray-600">실시간 재고 추적</p>
          </div>
        </div>

        <div className="mt-12 text-center">
          <p className="text-sm text-gray-500">
            원본 프로젝트: <code className="bg-gray-100 px-2 py-1 rounded">/mnt/d/Ai/WslProject/TheMoon_Project</code>
          </p>
        </div>
      </div>
    </main>
  )
}
