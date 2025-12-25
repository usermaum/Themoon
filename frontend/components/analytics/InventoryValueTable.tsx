import { useState } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Search,
  ChevronLeft,
  ChevronRight,
  X,
  ChevronsUpDown,
  ChevronUp,
  ChevronDown,
} from 'lucide-react';

import MascotStatus from '@/components/ui/mascot-status';

import { formatCurrency } from '@/lib/utils';

interface InventoryValueTableProps {
  data: {
    bean_name: string;
    quantity_kg: number;
    avg_price: number;
    total_value: number;
  }[];
}

export function InventoryValueTable({ data }: InventoryValueTableProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'asc' | 'desc' } | null>(
    null
  );
  const itemsPerPage = 10;

  const totalValue = data.reduce((sum, item) => sum + item.total_value, 0);

  // Filter Logic
  const filteredData = data.filter((item) =>
    item.bean_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Sort Logic
  const sortedData = [...filteredData].sort((a, b) => {
    if (!sortConfig) return 0;

    const { key, direction } = sortConfig;
    const aValue = (a as any)[key];
    const bValue = (b as any)[key];

    if (aValue < bValue) return direction === 'asc' ? -1 : 1;
    if (aValue > bValue) return direction === 'asc' ? 1 : -1;
    return 0;
  });

  // Pagination Logic
  const totalPages = Math.ceil(sortedData.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const currentData = sortedData.slice(startIndex, startIndex + itemsPerPage);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1); // Reset to first page on search
  };

  const handleSort = (key: string) => {
    let direction: 'asc' | 'desc' = 'asc';
    if (sortConfig && sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const getSortIcon = (key: string) => {
    if (!sortConfig || sortConfig.key !== key) return <ChevronsUpDown className="ml-2 h-4 w-4" />;
    if (sortConfig.direction === 'asc') return <ChevronUp className="ml-2 h-4 w-4" />;
    return <ChevronDown className="ml-2 h-4 w-4" />;
  };

  return (
    <Card className="rounded-[1em]">
      <CardHeader>
        <CardTitle>재고 자산 가치</CardTitle>
        <CardDescription>현재 보유 재고의 평가액 (FIFO 기준)</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
          <div className="text-2xl font-bold">총 자산: ₩{formatCurrency(totalValue)}</div>
          <div className="relative w-full md:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="품목 검색..."
              value={searchTerm}
              onChange={handleSearch}
              className="pl-9 pr-8"
            />
            {searchTerm && (
              <button
                onClick={() => {
                  setSearchTerm('');
                  setCurrentPage(1);
                }}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground focus:outline-none"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>
        </div>

        <div className="bg-white rounded-[1em] shadow-sm overflow-hidden border border-latte-200">
          <Table>
            <TableHeader>
              <TableRow className="bg-latte-100/50 hover:bg-latte-100/60 border-latte-200">
                <TableHead
                  className="cursor-pointer hover:text-latte-900 text-latte-700 font-semibold transition-colors"
                  onClick={() => handleSort('bean_name')}
                >
                  <div className="flex items-center">
                    품목명
                    {getSortIcon('bean_name')}
                  </div>
                </TableHead>
                <TableHead
                  className="text-right cursor-pointer hover:text-latte-900 text-latte-700 font-semibold transition-colors"
                  onClick={() => handleSort('quantity_kg')}
                >
                  <div className="flex items-center justify-end">
                    보유량 (kg)
                    {getSortIcon('quantity_kg')}
                  </div>
                </TableHead>
                <TableHead
                  className="text-right cursor-pointer hover:text-latte-900 text-latte-700 font-semibold transition-colors"
                  onClick={() => handleSort('avg_price')}
                >
                  <div className="flex items-center justify-end">
                    평균단가
                    {getSortIcon('avg_price')}
                  </div>
                </TableHead>
                <TableHead
                  className="text-right cursor-pointer hover:text-latte-900 text-latte-700 font-semibold transition-colors"
                  onClick={() => handleSort('total_value')}
                >
                  <div className="flex items-center justify-end">
                    평가액
                    {getSortIcon('total_value')}
                  </div>
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {currentData.length > 0 ? (
                currentData.map((item) => (
                  <TableRow key={item.bean_name} className="hover:bg-latte-50/30 transition-colors border-latte-100">
                    <TableCell className="font-medium text-latte-900">{item.bean_name}</TableCell>
                    <TableCell className="text-right text-latte-700">
                      {item.quantity_kg.toLocaleString()} kg
                    </TableCell>
                    <TableCell className="text-right text-latte-700">₩{formatCurrency(item.avg_price)}</TableCell>
                    <TableCell className="text-right font-medium text-latte-900">
                      ₩{formatCurrency(item.total_value)}
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={4} className="h-64 text-center">
                    <div className="flex justify-center items-center h-full">
                      <MascotStatus
                        variant="search"
                        title="검색 결과가 없습니다"
                        description={`'${searchTerm}'에 대한 검색 결과가 없습니다.`}
                        action={
                          <Button
                            variant="outline"
                            onClick={() => {
                              setSearchTerm('');
                              setCurrentPage(1);
                            }}
                          >
                            검색 초기화
                          </Button>
                        }
                      />
                    </div>
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>

        {/* Pagination Controls */}
        {totalPages > 1 && (
          <div className="flex items-center justify-center space-x-2 py-4">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              disabled={currentPage === 1}
            >
              <ChevronLeft className="h-4 w-4" />
              이전
            </Button>
            <div className="text-sm font-medium">
              {currentPage} / {totalPages} 페이지
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
            >
              다음
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
