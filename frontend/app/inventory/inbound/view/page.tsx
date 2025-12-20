'use client'

import React, { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Button } from '@/components/ui/button'

interface OCRData {
  debug_raw_text?: string
  document_info?: {
    contract_number?: string
    invoice_date?: string
    invoice_type?: string
  }
  supplier?: {
    name?: string
    business_number?: string
    address?: string
    phone?: string
    email?: string
    representative?: string
    contact_person?: string
  }
  receiver?: {
    name?: string
    business_number?: string
    address?: string
    phone?: string
  }
  amounts?: {
    subtotal?: number
    tax_amount?: number
    total_amount?: number
    grand_total?: number
  }
  items?: Array<{
    item_number?: string
    bean_name?: string
    bean_name_kr?: string
    specification?: string
    origin?: string
    quantity?: number
    unit?: string
    unit_price?: number
    amount?: number
    note?: string
  }>
  additional_info?: {
    payment_terms?: string
    shipping_method?: string
    notes?: string
  }
}

export default function InvoiceViewPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [ocrData, setOcrData] = useState<OCRData | null>(null)
  const [activeTab, setActiveTab] = useState<'invoice' | 'debug'>('invoice')

  useEffect(() => {
    // URL 파라미터 또는 sessionStorage에서 데이터 로드
    const dataParam = searchParams.get('data')
    if (dataParam) {
      try {
        setOcrData(JSON.parse(decodeURIComponent(dataParam)))
      } catch (e) {
        console.error('Failed to parse data:', e)
      }
    } else {
      const storedData = sessionStorage.getItem('invoiceData')
      if (storedData) {
        setOcrData(JSON.parse(storedData))
      }
    }
  }, [searchParams])

  const formatNumber = (num: number | undefined) => {
    if (!num || num === 0) return ''
    return num.toLocaleString('ko-KR')
  }

  const totalWeight = ocrData?.items?.reduce((sum, item) => sum + (item.quantity || 0), 0) || 0
  const grandTotal = ocrData?.amounts?.grand_total || ocrData?.amounts?.total_amount || 0

  // 빈 행 추가 (최소 15행)
  const allItems = [
    ...(ocrData?.items || []),
    ...Array.from({ length: Math.max(0, 15 - (ocrData?.items?.length || 0)) }, () => ({}))
  ]

  if (!ocrData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">데이터 로딩 중...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* 탭 메뉴 */}
        <div className="mb-6 flex gap-4 justify-center print:hidden">
          <Button
            onClick={() => setActiveTab('invoice')}
            variant={activeTab === 'invoice' ? 'default' : 'outline'}
            className="px-6 py-3"
          >
            📄 거래명세서
          </Button>
          <Button
            onClick={() => setActiveTab('debug')}
            variant={activeTab === 'debug' ? 'default' : 'outline'}
            className="px-6 py-3"
          >
            🔍 OCR 원본 데이터
          </Button>
        </div>

        {/* 거래명세서 탭 */}
        {activeTab === 'invoice' && (
          <div className="bg-white border-4 border-black p-8 print:border-2">
            {/* 헤더 섹션 */}
            <div className="flex items-start justify-between mb-8">
              {/* GSC 로고 */}
              <div className="w-32 h-24 bg-[#8B0000] flex items-center justify-center">
                <div className="text-white text-center">
                  <div className="text-2xl font-bold">GSC</div>
                  <div className="text-xs">GREEN COFFEE</div>
                </div>
              </div>

              {/* 제목 */}
              <div className="flex-1 text-center">
                <h1 className="text-4xl font-bold mb-2">거래명세서</h1>
                <p className="text-sm text-gray-600">(공급받는자용)</p>
              </div>

              <div className="w-32"></div>
            </div>

            {/* 정보 섹션 (2단 레이아웃) */}
            <div className="grid grid-cols-2 gap-4 mb-6">
              {/* 왼쪽: 수신자 정보 */}
              <div className="border-2 border-black p-3 space-y-1">
                <InfoRow label="등록번호" value={ocrData.receiver?.business_number} />
                <InfoRow label="상호\n(법인명)" value={ocrData.receiver?.name || 'The Moon Coffee'} />
                <InfoRow label="사업장" value={ocrData.receiver?.address} small />
                <InfoRow label="성명" value="" />
                <InfoRow label="담당자" value={ocrData.receiver?.phone} />
              </div>

              {/* 오른쪽: 공급자 정보 (도장 포함) */}
              <div className="border-2 border-black p-3 space-y-1 relative">
                {/* 도장 이미지 */}
                <div className="absolute top-2 right-2 w-20 h-20 bg-red-100 rounded-full border-2 border-red-600 flex items-center justify-center">
                  <div className="text-red-600 text-xs font-bold text-center leading-tight">
                    <div>{ocrData.supplier?.name?.split(' ')[0] || 'GSC'}</div>
                    <div className="text-[10px]">(주)</div>
                  </div>
                </div>

                <InfoRow label="등록번호" value={ocrData.supplier?.business_number} />
                <InfoRow label="상호\n(법인명)" value={ocrData.supplier?.name} />
                <InfoRow label="사업장" value={ocrData.supplier?.address} small />
                <InfoRow label="성명" value={ocrData.supplier?.representative} />
                <InfoRow label="담당자" value={ocrData.supplier?.contact_person} />
              </div>
            </div>

            {/* 품목 테이블 */}
            <div className="border-2 border-black mb-6">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-100 border-b-2 border-black">
                    <th className="border-r border-black px-2 py-2 w-12">NO.</th>
                    <th className="border-r border-black px-2 py-2">품 목</th>
                    <th className="border-r border-black px-2 py-2 w-16">규격</th>
                    <th className="border-r border-black px-2 py-2 w-16">수량</th>
                    <th className="border-r border-black px-2 py-2 w-16">중량</th>
                    <th className="border-r border-black px-2 py-2 w-24">단가</th>
                    <th className="px-2 py-2 w-28">공급가액</th>
                  </tr>
                </thead>
                <tbody>
                  {allItems.map((item: any, index) => (
                    <tr key={index} className="border-b border-gray-300">
                      <td className="border-r border-gray-300 px-2 py-1.5 text-center">{index + 1}</td>
                      <td className="border-r border-gray-300 px-2 py-1.5 text-xs">
                        {item.bean_name || item.bean_name_kr || ''}
                      </td>
                      <td className="border-r border-gray-300 px-2 py-1.5 text-center text-xs">
                        {item.specification || ''}
                      </td>
                      <td className="border-r border-gray-300 px-2 py-1.5 text-right">
                        {formatNumber(item.quantity)}
                      </td>
                      <td className="border-r border-gray-300 px-2 py-1.5 text-right">
                        {formatNumber(item.quantity)}
                      </td>
                      <td className="border-r border-gray-300 px-2 py-1.5 text-right">
                        {formatNumber(item.unit_price)}
                      </td>
                      <td className="px-2 py-1.5 text-right">{formatNumber(item.amount)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* 하단 요약 섹션 */}
            <div className="grid grid-cols-2 gap-4">
              {/* 왼쪽: 합계 정보 */}
              <div className="space-y-2">
                <SummaryItem label="박스합" value="0 원" />
                <SummaryItem label="총 중량" value={`${totalWeight} Kg`} />
                <SummaryItem label="합계금액" value={`${formatNumber(grandTotal)} 원`} bold />
              </div>

              {/* 오른쪽: 계약 정보 */}
              <div className="space-y-1 text-sm">
                <ContactItem label="계약번호" value={ocrData.document_info?.contract_number} />
                <ContactItem label="계약일자" value={ocrData.document_info?.invoice_date} />
                <ContactItem label="본계금액" value={`${formatNumber(grandTotal)} 원`} />
                <ContactItem label="공급 담당자" value={ocrData.supplier?.contact_person} />
                <ContactItem label="공급자전화번호" value={ocrData.supplier?.phone} />
                <ContactItem label="공급자이메일" value={ocrData.supplier?.email} />
              </div>
            </div>

            {/* 액션 버튼 */}
            <div className="mt-8 flex justify-center gap-4 print:hidden">
              <Button onClick={() => window.print()} size="lg">
                🖨️ 인쇄하기
              </Button>
              <Button onClick={() => router.back()} variant="outline" size="lg">
                ← 돌아가기
              </Button>
            </div>
          </div>
        )}

        {/* OCR 원본 데이터 탭 */}
        {activeTab === 'debug' && (
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6">🔍 OCR 원본 데이터</h2>

            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold mb-3">📋 구조화된 JSON 데이터</h3>
                <pre className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-auto max-h-96 text-sm">
                  {JSON.stringify(ocrData, null, 2)}
                </pre>
              </div>

              {ocrData.debug_raw_text && (
                <div>
                  <h3 className="text-lg font-semibold mb-3">📄 원본 텍스트</h3>
                  <div className="bg-gray-50 p-4 rounded-lg border-2 border-gray-200 max-h-96 overflow-auto">
                    <pre className="whitespace-pre-wrap text-sm">{ocrData.debug_raw_text}</pre>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* 프린트 스타일 */}
      <style jsx global>{`
        @media print {
          body {
            background: white;
          }
          .print\\:hidden {
            display: none !important;
          }
          .print\\:border-2 {
            border-width: 2px !important;
          }
        }
      `}</style>
    </div>
  )
}

// 헬퍼 컴포넌트
function InfoRow({ label, value, small = false }: { label: string; value?: string; small?: boolean }) {
  return (
    <div className="flex text-sm">
      <span className="w-24 font-semibold bg-gray-100 px-2 py-1 border border-gray-300 whitespace-pre-line">
        {label}
      </span>
      <span className={`flex-1 px-2 py-1 border border-gray-300 ${small ? 'text-xs leading-relaxed' : ''}`}>
        {value || ''}
      </span>
    </div>
  )
}

function SummaryItem({ label, value, bold = false }: { label: string; value: string; bold?: boolean }) {
  return (
    <div className="flex items-center text-sm">
      <span className="font-semibold">● {label} :</span>
      <span className={`ml-2 ${bold ? 'text-lg font-bold' : ''}`}>{value}</span>
    </div>
  )
}

function ContactItem({ label, value }: { label: string; value?: string }) {
  return (
    <div className="flex items-center">
      <span className="font-semibold">● {label} :</span>
      <span className="ml-2 text-sm">{value || ''}</span>
    </div>
  )
}
