'use client';

import React, { useState } from 'react';
import { Moon, Circle, Triangle } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select';
import { cn } from '@/lib/utils';

// --- Types ---
interface BeanRow {
    id: number;
    code: string;
    name: string;
    type: 'W' | 'N' | 'Pb' | 'Rh' | 'SD' | 'SC';
    greenAmount1: string;
    roastedAmount1: string;
    greenAmount2: string;
    roastedAmount2: string;
}

const INITIAL_BEAN_DATA: BeanRow[] = [
    { id: 1, code: 'Eth', name: '예가체프', type: 'W', greenAmount1: '1500', roastedAmount1: '1315', greenAmount2: '1500', roastedAmount2: '1284' },
    { id: 2, code: 'Eth', name: '모모라', type: 'N', greenAmount1: '1500', roastedAmount1: '1295', greenAmount2: '1000', roastedAmount2: '829' },
    { id: 3, code: '', name: '코케허니', type: 'N', greenAmount1: '', roastedAmount1: '', greenAmount2: '1000', roastedAmount2: '840' },
    { id: 4, code: 'K', name: '우리가', type: 'W', greenAmount1: '1000', roastedAmount1: '883', greenAmount2: '1000', roastedAmount2: '834' },
    { id: 5, code: 'K', name: 'AA FAQ', type: 'W', greenAmount1: '500', roastedAmount1: '435', greenAmount2: '1500', roastedAmount2: '1250' },
];

const ORDER_BLEND_DATA = [
    { code: 'K', name: 'AA FAQ', type: 'W' },
    { code: 'Eth', name: '모모라', type: 'N' },
];

export function InvoiceTable() {
    const [beanData, setBeanData] = useState<BeanRow[]>(INITIAL_BEAN_DATA);

    const getTypeColor = (type: string) => {
        switch (type) {
            case 'W': return 'text-blue-600';
            case 'N': return 'text-red-600';
            case 'Rh': return 'text-pink-600';
            default: return 'text-gray-500';
        }
    };

    const handleBeanChange = (id: number, field: keyof BeanRow, value: string) => {
        setBeanData((prev) => prev.map((row) => (row.id === id ? { ...row, [field]: value } : row)));
    };

    return (
        <Card className="rounded-xl shadow-md overflow-hidden border border-latte-200 bg-white dark:bg-zinc-900">
            <div className="overflow-x-auto">
                <Table className="w-full text-sm">
                    <TableHeader className="bg-gray-50 dark:bg-gray-800">
                        <TableRow className="border-b border-latte-100">
                            <TableHead className="w-8 text-center border-r font-bold">#</TableHead>
                            <TableHead className="w-12 text-center border-r font-bold">Code</TableHead>
                            <TableHead className="text-left font-bold border-r">Name</TableHead>
                            <TableHead className="w-14 text-center border-r font-bold">Type</TableHead>
                            <TableHead className="text-right text-red-600 border-r font-bold">생두량 (1)</TableHead>
                            <TableHead className="text-right border-r font-bold">볶은량 (1)</TableHead>
                            <TableHead className="text-right text-red-600 border-r font-bold">생두량 (2)</TableHead>
                            <TableHead className="text-right font-bold">볶은량 (2)</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody className="divide-y divide-latte-50">
                        {beanData.map((bean) => (
                            <TableRow key={bean.id} className="hover:bg-gray-50/50">
                                <TableCell className="p-2 text-center font-bold text-latte-400">{bean.id}</TableCell>
                                <TableCell className="p-2 text-center text-xs font-mono text-latte-600">{bean.code}</TableCell>
                                <TableCell className="p-2 font-medium whitespace-nowrap text-latte-900">{bean.name}</TableCell>
                                <TableCell className={cn('p-2 text-center font-bold', getTypeColor(bean.type))}>{bean.type}</TableCell>
                                <TableCell className="p-1">
                                    <Input
                                        className="h-7 text-right bg-transparent border-none text-red-500 font-mono focus-visible:ring-1"
                                        value={bean.greenAmount1}
                                        onChange={(e) => handleBeanChange(bean.id, 'greenAmount1', e.target.value)}
                                    />
                                </TableCell>
                                <TableCell className="p-1">
                                    <Input
                                        className="h-7 text-right bg-transparent border-none font-mono focus-visible:ring-1"
                                        value={bean.roastedAmount1}
                                        onChange={(e) => handleBeanChange(bean.id, 'roastedAmount1', e.target.value)}
                                    />
                                </TableCell>
                                <TableCell className="p-1">
                                    <Input
                                        className="h-7 text-right bg-transparent border-none text-red-500 font-mono focus-visible:ring-1"
                                        value={bean.greenAmount2}
                                        onChange={(e) => handleBeanChange(bean.id, 'greenAmount2', e.target.value)}
                                    />
                                </TableCell>
                                <TableCell className="p-1">
                                    <Input
                                        className="h-7 text-right bg-transparent border-none font-mono focus-visible:ring-1"
                                        value={bean.roastedAmount2}
                                        onChange={(e) => handleBeanChange(bean.id, 'roastedAmount2', e.target.value)}
                                    />
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>

            <div className="border-t bg-latte-50/30">
                <div className="bg-latte-100/50 py-2 px-4 flex justify-between items-center border-b border-latte-200 text-sm">
                    <span className="font-bold text-latte-800">주문 블랜드 예약</span>
                    <Select defaultValue="house">
                        <SelectTrigger className="w-[140px] h-7 text-xs bg-white">
                            <SelectValue placeholder="블랜드 선택" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="house">House Blend</SelectItem>
                            <SelectItem value="mild">Mild Blend</SelectItem>
                        </SelectContent>
                    </Select>
                </div>
                <Table className="w-full text-sm">
                    <TableBody className="divide-y divide-latte-50">
                        {ORDER_BLEND_DATA.map((item, idx) => (
                            <TableRow key={idx}>
                                <TableCell className="w-12 p-2 text-center font-bold bg-latte-50/50">{item.code}</TableCell>
                                <TableCell className="p-2 text-left font-medium">{item.name}</TableCell>
                                <TableCell className={cn('w-12 p-2 text-center font-bold', getTypeColor(item.type))}>{item.type}</TableCell>
                                <TableCell className="p-1">
                                    <Input className="h-6 text-xs bg-transparent border-transparent hover:border-latte-300" placeholder="비고..." />
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        </Card>
    );
}
