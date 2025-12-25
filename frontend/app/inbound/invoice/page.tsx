'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Printer, Download, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';

// OCR Response 타입 정의
interface OCRData {
  debug_raw_text?: string;
  document_info?: {
    document_number?: string;
    contract_number?: string;
    issue_date?: string;
    invoice_date?: string;
    delivery_date?: string;
    payment_due_date?: string;
    invoice_type?: string;
  };
  supplier?: {
    name?: string;
    business_number?: string;
    address?: string;
    phone?: string;
    fax?: string;
    email?: string;
    representative?: string;
    contact_person?: string;
    contact_phone?: string;
  };
  receiver?: {
    name?: string;
    business_number?: string;
    address?: string;
    phone?: string;
    contact_person?: string;
  };
  amounts?: {
    subtotal?: number;
    tax_amount?: number;
    total_amount?: number;
    grand_total?: number;
    currency?: string;
  };
  items?: Array<{
    item_number?: string;
    bean_name?: string;
    bean_name_kr?: string;
    specification?: string;
    origin?: string;
    quantity?: number;
    unit?: string;
    unit_price?: number;
    amount?: number;
    note?: string;
  }>;
  additional_info?: {
    payment_terms?: string;
    shipping_method?: string;
    notes?: string;
    remarks?: string;
  };
}

export default function InvoicePage() {
  const router = useRouter();
  const [ocrData, setOcrData] = useState<OCRData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // sessionStorage에서 OCR 데이터 가져오기
    const storedData = sessionStorage.getItem('ocrResult');
    if (storedData) {
      try {
        const parsed = JSON.parse(storedData);
        setOcrData(parsed);
      } catch (error) {
        console.error('Failed to parse OCR data:', error);
      }
    }
    setLoading(false);
  }, []);

  // 금액 포맷팅 함수
  const formatCurrency = (amount?: number) => {
    if (!amount && amount !== 0) return '0';
    return amount.toLocaleString('ko-KR');
  };

  // 날짜 포맷팅 함수
  const formatDate = (dateStr?: string) => {
    if (!dateStr) return '';
    // YYYY-MM-DD 형식을 YYYY 년 MM월 DD일로 변환
    const [year, month, day] = dateStr.split('-');
    return `${year} 년 ${month}월 ${day}일`;
  };

  // 인쇄 기능
  const handlePrint = () => {
    window.print();
  };

  // 다운로드 기능 (PDF로 변환)
  const handleDownload = () => {
    window.print(); // 브라우저의 인쇄 다이얼로그에서 PDF로 저장 가능
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-lg">로딩 중...</p>
      </div>
    );
  }

  if (!ocrData) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4">
        <p className="text-lg text-red-600">OCR 데이터를 불러올 수 없습니다.</p>
        <Button onClick={() => router.push('/inventory/inbound')}>
          <ArrowLeft className="w-4 h-4 mr-2" />
          인바운드 페이지로 돌아가기
        </Button>
      </div>
    );
  }

  const { document_info, supplier, receiver, amounts, items, additional_info } = ocrData;

  // 총 중량 계산
  const totalWeight = items?.reduce((sum, item) => sum + (item.quantity || 0), 0) || 0;

  return (
    <div className="bg-background-light dark:bg-background-dark font-sans text-gray-800 dark:text-gray-200 min-h-screen p-4 md:p-8 flex justify-center items-start">
      {/* 인쇄/다운로드 버튼 (인쇄 시 숨김) */}
      <div className="no-print fixed top-4 right-4 z-50 flex gap-2">
        <Button variant="outline" size="sm" onClick={handlePrint}>
          <Printer className="w-4 h-4 mr-2" />
          인쇄
        </Button>
        <Button variant="outline" size="sm" onClick={handleDownload}>
          <Download className="w-4 h-4 mr-2" />
          다운로드
        </Button>
        <Button variant="outline" size="sm" onClick={() => router.back()}>
          <ArrowLeft className="w-4 h-4 mr-2" />
          돌아가기
        </Button>
      </div>

      {/* 거래명세서 컨테이너 */}
      <div className="page-container bg-surface-light dark:bg-surface-dark w-full max-w-4xl shadow-xl dark:shadow-none border border-border-light dark:border-border-dark p-6 md:p-10 relative">
        {/* 헤더: GSC 로고 + 거래명세서 타이틀 */}
        <div className="flex justify-between items-center mb-8 border-b-2 border-primary pb-4">
          <div className="w-32 h-24 bg-primary flex flex-col justify-center items-center text-white p-2 rounded-sm">
            <div className="text-3xl font-bold tracking-widest leading-none">
              {supplier?.name?.includes('GSC') || supplier?.name?.includes('지에스씨')
                ? 'GSC'
                : supplier?.name?.substring(0, 3) || '???'}
            </div>
            <div className="text-[0.6rem] tracking-wider uppercase mt-1">
              {supplier?.name?.includes('GSC') || supplier?.name?.includes('지에스씨')
                ? 'Green Coffee'
                : 'Coffee'}
            </div>
          </div>
          <div className="text-center flex-1">
            <h1 className="text-4xl md:text-5xl font-bold tracking-[0.5em] text-gray-900 dark:text-white mb-2">
              거 래 명 세 서
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-400 font-medium">(공급받는자용)</p>
          </div>
        </div>

        {/* 공급받는자 / 공급자 정보 테이블 */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-0 border border-gray-400 dark:border-gray-600 mb-6 text-sm">
          {/* 공급받는자 (좌측) */}
          <div className="flex border-b md:border-b-0 md:border-r border-gray-400 dark:border-gray-600">
            <div
              className="w-8 flex items-center justify-center bg-gray-100 dark:bg-gray-800 border-r border-gray-300 dark:border-gray-600 text-center p-2 font-bold"
              style={{ writingMode: 'vertical-rl' }}
            >
              공급받는자
            </div>
            <div className="flex-1">
              {/* 등록번호 */}
              <div className="flex border-b border-gray-300 dark:border-gray-600">
                <div className="w-20 bg-gray-50 dark:bg-gray-700/50 p-2 text-center border-r border-gray-300 dark:border-gray-600 flex items-center justify-center font-medium">
                  등록번호
                </div>
                <div className="flex-1 p-2 flex items-center justify-center font-bold text-lg tracking-widest text-primary dark:text-red-400">
                  {receiver?.business_number || '197-04-00506'}
                </div>
              </div>
              {/* 상호(법인명) + 성명 */}
              <div className="flex border-b border-gray-300 dark:border-gray-600 h-16">
                <div className="w-20 bg-gray-50 dark:bg-gray-700/50 p-2 text-center border-r border-gray-300 dark:border-gray-600 flex items-center justify-center font-medium">
                  상호
                  <br />
                  (법인명)
                </div>
                <div className="flex-1 flex">
                  <div className="flex-1 p-2 flex items-center justify-center border-r border-gray-300 dark:border-gray-600">
                    {receiver?.name || '더문커피'}
                  </div>
                  <div className="w-12 bg-gray-50 dark:bg-gray-700/50 p-1 flex items-center justify-center border-r border-gray-300 dark:border-gray-600 font-medium text-xs">
                    성명
                  </div>
                  <div className="flex-1 p-2 flex items-center justify-center">
                    {receiver?.contact_person || '김기문'}
                  </div>
                </div>
              </div>
              {/* 사업장 주소 */}
              <div className="flex border-b border-gray-300 dark:border-gray-600 h-16">
                <div className="w-20 bg-gray-50 dark:bg-gray-700/50 p-2 text-center border-r border-gray-300 dark:border-gray-600 flex items-center justify-center font-medium">
                  사업장
                  <br />
                  주소
                </div>
                <div className="flex-1 p-2 flex items-center justify-center text-center text-xs break-words">
                  {receiver?.address || '경기 부천시 부흥로315번길 27 (중동) 땅차커피 드립바'}
                </div>
              </div>
              {/* 업태 + 종목 */}
              <div className="flex">
                <div className="w-20 bg-gray-50 dark:bg-gray-700/50 p-2 text-center border-r border-gray-300 dark:border-gray-600 flex items-center justify-center font-medium">
                  업태
                </div>
                <div className="flex-1 flex">
                  <div className="flex-1 p-2 flex items-center justify-center border-r border-gray-300 dark:border-gray-600">
                    음식점업
                  </div>
                  <div className="w-12 bg-gray-50 dark:bg-gray-700/50 p-1 flex items-center justify-center border-r border-gray-300 dark:border-gray-600 font-medium text-xs">
                    종목
                  </div>
                  <div className="flex-1 p-2 flex items-center justify-center">커피전문점</div>
                </div>
              </div>
            </div>
          </div>

          {/* 공급자 (우측) */}
          <div className="flex">
            <div
              className="w-8 flex items-center justify-center bg-gray-100 dark:bg-gray-800 border-r border-gray-300 dark:border-gray-600 text-center p-2 font-bold"
              style={{ writingMode: 'vertical-rl' }}
            >
              공급자
            </div>
            <div className="flex-1">
              {/* 등록번호 */}
              <div className="flex border-b border-gray-300 dark:border-gray-600">
                <div className="w-20 bg-gray-50 dark:bg-gray-700/50 p-2 text-center border-r border-gray-300 dark:border-gray-600 flex items-center justify-center font-medium">
                  등록번호
                </div>
                <div className="flex-1 p-2 flex items-center justify-center font-bold text-lg tracking-widest text-primary dark:text-red-400">
                  {supplier?.business_number || '106-86-70680'}
                </div>
              </div>
              {/* 상호(법인명) + 성명 */}
              <div className="flex border-b border-gray-300 dark:border-gray-600 h-16 relative">
                <div className="w-20 bg-gray-50 dark:bg-gray-700/50 p-2 text-center border-r border-gray-300 dark:border-gray-600 flex items-center justify-center font-medium">
                  상호
                  <br />
                  (법인명)
                </div>
                <div className="flex-1 flex relative">
                  <div className="flex-1 p-2 flex items-center justify-center border-r border-gray-300 dark:border-gray-600 text-xs">
                    {supplier?.name || '지에스씨인터내셔날(주)'}
                  </div>
                  <div className="w-12 bg-gray-50 dark:bg-gray-700/50 p-1 flex items-center justify-center border-r border-gray-300 dark:border-gray-600 font-medium text-xs">
                    성명
                  </div>
                  <div className="flex-1 p-2 flex items-center justify-center relative">
                    <span className="relative z-10">
                      {supplier?.representative || '황두용,'}
                      <br />
                      {supplier?.contact_person || '조진환'}
                    </span>
                    {/* 인(印) 도장 */}
                    <div className="absolute inset-0 flex items-center justify-center opacity-70 pointer-events-none z-0 ml-6">
                      <div className="w-12 h-12 rounded-full border-2 border-red-600 text-red-600 flex items-center justify-center text-[0.6rem] font-bold rotate-[-15deg]">
                        (인)
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              {/* 사업장 주소 */}
              <div className="flex border-b border-gray-300 dark:border-gray-600 h-16">
                <div className="w-20 bg-gray-50 dark:bg-gray-700/50 p-2 text-center border-r border-gray-300 dark:border-gray-600 flex items-center justify-center font-medium">
                  사업장
                  <br />
                  주소
                </div>
                <div className="flex-1 p-2 flex items-center justify-center text-center text-xs break-words">
                  {supplier?.address || '서울특별시 마포구 동교로 65'}
                  <br />
                  {supplier?.address?.includes('2층') ? '' : '(망원동, 2층)'}
                </div>
              </div>
              {/* 업태 + 종목 */}
              <div className="flex">
                <div className="w-20 bg-gray-50 dark:bg-gray-700/50 p-2 text-center border-r border-gray-300 dark:border-gray-600 flex items-center justify-center font-medium">
                  업태
                </div>
                <div className="flex-1 flex">
                  <div className="flex-1 p-2 flex items-center justify-center border-r border-gray-300 dark:border-gray-600 text-xs">
                    도소매, 제조
                  </div>
                  <div className="w-12 bg-gray-50 dark:bg-gray-700/50 p-1 flex items-center justify-center border-r border-gray-300 dark:border-gray-600 font-medium text-xs">
                    종목
                  </div>
                  <div className="flex-1 p-2 flex items-center justify-center text-xs">
                    무역, 커피
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 품목 테이블 */}
        <div className="overflow-x-auto mb-6">
          <table className="w-full border-collapse border border-gray-400 dark:border-gray-600 text-sm">
            <thead>
              <tr className="bg-gray-100 dark:bg-gray-800 text-center font-bold">
                <th className="border border-gray-300 dark:border-gray-600 p-2 w-10">NO.</th>
                <th className="border border-gray-300 dark:border-gray-600 p-2">품 목</th>
                <th className="border border-gray-300 dark:border-gray-600 p-2 w-16">규격</th>
                <th className="border border-gray-300 dark:border-gray-600 p-2 w-16">수량</th>
                <th className="border border-gray-300 dark:border-gray-600 p-2 w-16">중량</th>
                <th className="border border-gray-300 dark:border-gray-600 p-2 w-24">단가</th>
                <th className="border border-gray-300 dark:border-gray-600 p-2 w-32">공급가액</th>
              </tr>
            </thead>
            <tbody>
              {/* OCR 추출 품목 */}
              {items && items.length > 0
                ? items.map((item, index) => (
                    <tr
                      key={index}
                      className="bg-white dark:bg-surface-dark hover:bg-gray-50 dark:hover:bg-gray-700/30"
                    >
                      <td className="border border-gray-300 dark:border-gray-600 p-2 text-center">
                        {item.item_number || index + 1}
                      </td>
                      <td className="border border-gray-300 dark:border-gray-600 p-2">
                        {item.bean_name || item.bean_name_kr || '-'}
                      </td>
                      <td className="border border-gray-300 dark:border-gray-600 p-2 text-center">
                        {item.specification || item.unit || '1kg'}
                      </td>
                      <td className="border border-gray-300 dark:border-gray-600 p-2 text-center">
                        {item.quantity || 0}
                      </td>
                      <td className="border border-gray-300 dark:border-gray-600 p-2 text-center">
                        {item.quantity || 0}
                      </td>
                      <td className="border border-gray-300 dark:border-gray-600 p-2 text-right">
                        {formatCurrency(item.unit_price)}
                      </td>
                      <td className="border border-gray-300 dark:border-gray-600 p-2 text-right">
                        {formatCurrency(item.amount)}
                      </td>
                    </tr>
                  ))
                : // 빈 행 (최소 10개)
                  Array.from({ length: 10 }).map((_, i) => (
                    <tr key={`empty-${i}`} className="bg-white dark:bg-surface-dark h-8">
                      <td className="border border-gray-300 dark:border-gray-600"></td>
                      <td className="border border-gray-300 dark:border-gray-600"></td>
                      <td className="border border-gray-300 dark:border-gray-600"></td>
                      <td className="border border-gray-300 dark:border-gray-600"></td>
                      <td className="border border-gray-300 dark:border-gray-600"></td>
                      <td className="border border-gray-300 dark:border-gray-600"></td>
                      <td className="border border-gray-300 dark:border-gray-600"></td>
                    </tr>
                  ))}
              {/* 추가 빈 행 (품목이 10개 미만일 경우) */}
              {items &&
                items.length > 0 &&
                items.length < 10 &&
                Array.from({ length: 10 - items.length }).map((_, i) => (
                  <tr key={`padding-${i}`} className="bg-white dark:bg-surface-dark h-8">
                    <td className="border border-gray-300 dark:border-gray-600"></td>
                    <td className="border border-gray-300 dark:border-gray-600"></td>
                    <td className="border border-gray-300 dark:border-gray-600"></td>
                    <td className="border border-gray-300 dark:border-gray-600"></td>
                    <td className="border border-gray-300 dark:border-gray-600"></td>
                    <td className="border border-gray-300 dark:border-gray-600"></td>
                    <td className="border border-gray-300 dark:border-gray-600"></td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>

        {/* 배송비 및 합계 */}
        <div className="border border-gray-400 dark:border-gray-600 p-2 flex flex-col md:flex-row justify-between items-center text-sm font-medium mb-6 bg-gray-50 dark:bg-gray-800">
          <div className="flex gap-4 w-full md:w-auto justify-between md:justify-start px-2">
            <span>배송비 : 0 원</span>
            <span>총 중량 : {totalWeight} Kg</span>
          </div>
          <div className="flex gap-4 w-full md:w-auto justify-between md:justify-end px-2 mt-2 md:mt-0">
            <span>합계금액 :</span>
            <span className="font-bold text-lg text-black dark:text-white">
              {formatCurrency(amounts?.total_amount || amounts?.grand_total)} 원
            </span>
          </div>
        </div>

        {/* 계약 정보 및 담당자 정보 */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          {/* 계약 정보 */}
          <div className="border border-gray-400 dark:border-gray-600 p-4 rounded-sm">
            <div className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-2">
              <div className="flex items-center">
                <span className="w-2 h-2 bg-black dark:bg-white rounded-full mr-2"></span>계약번호
              </div>
              <div>: {document_info?.contract_number || 'N/A'}</div>
              <div className="flex items-center">
                <span className="w-2 h-2 bg-black dark:bg-white rounded-full mr-2"></span>계약일자
              </div>
              <div>: {formatDate(document_info?.invoice_date || document_info?.issue_date)}</div>
              <div className="flex items-center">
                <span className="w-2 h-2 bg-black dark:bg-white rounded-full mr-2"></span>합계금액
              </div>
              <div className="font-bold">
                : {formatCurrency(amounts?.total_amount || amounts?.grand_total)} 원
              </div>
            </div>
          </div>

          {/* 담당자 정보 */}
          <div className="border border-gray-400 dark:border-gray-600 p-4 rounded-sm">
            <div className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-2">
              <div className="flex items-center">
                <span className="w-2 h-2 bg-black dark:bg-white rounded-full mr-2"></span>영업
                담당자
              </div>
              <div>: {supplier?.contact_person || '-'}</div>
              <div className="flex items-center">
                <span className="w-2 h-2 bg-black dark:bg-white rounded-full mr-2"></span>공급처
                대표 전화
              </div>
              <div>: {supplier?.phone || '-'}</div>
              <div className="flex items-center">
                <span className="w-2 h-2 bg-black dark:bg-white rounded-full mr-2"></span>담당자
                전화
              </div>
              <div>: {supplier?.contact_phone || '-'}</div>
              <div className="flex items-center">
                <span className="w-2 h-2 bg-black dark:bg-white rounded-full mr-2"></span>담당자
                이메일
              </div>
              <div>: {supplier?.email || '-'}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Print Styles */}
      <style jsx global>{`
        @media print {
          body {
            background-color: white !important;
            color: black !important;
          }
          .no-print {
            display: none !important;
          }
          .page-container {
            box-shadow: none !important;
            border: none !important;
            width: 100% !important;
            max-width: none !important;
            margin: 0 !important;
            padding: 0 !important;
          }
        }

        /* Tailwind 색상 변수 */
        :root {
          --primary: #630e15;
          --background-light: #f8f9fa;
          --background-dark: #1a1a1a;
          --surface-light: #ffffff;
          --surface-dark: #2d2d2d;
          --border-light: #e5e7eb;
          --border-dark: #404040;
        }

        .bg-primary {
          background-color: var(--primary);
        }

        .text-primary {
          color: var(--primary);
        }

        .border-primary {
          border-color: var(--primary);
        }

        .bg-background-light {
          background-color: var(--background-light);
        }

        .dark .bg-background-dark {
          background-color: var(--background-dark);
        }

        .bg-surface-light {
          background-color: var(--surface-light);
        }

        .dark .bg-surface-dark {
          background-color: var(--surface-dark);
        }

        .border-border-light {
          border-color: var(--border-light);
        }

        .dark .border-border-dark {
          border-color: var(--border-dark);
        }
      `}</style>
    </div>
  );
}
