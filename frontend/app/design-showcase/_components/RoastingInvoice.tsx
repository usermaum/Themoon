'use client';

import React, { useState } from 'react';
import { Moon, Circle, Triangle, Plus, ChevronDown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
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
    type: 'W' | 'N' | 'Pb' | 'Rh' | 'SD' | 'SC'; // Washed, Natural, Peaberry, etc.
    greenAmount1: string; // Changed to string for input handling
    roastedAmount1: string;
    greenAmount2: string;
    roastedAmount2: string;
}

// --- Mock Data (Editable Initial State) ---
const INITIAL_BEAN_DATA: BeanRow[] = [
    {
        id: 1,
        code: 'Eth',
        name: '예가체프',
        type: 'W',
        greenAmount1: '1500',
        roastedAmount1: '1315',
        greenAmount2: '1500',
        roastedAmount2: '1284',
    },
    {
        id: 2,
        code: 'Eth',
        name: '모모라',
        type: 'N',
        greenAmount1: '1500',
        roastedAmount1: '1295',
        greenAmount2: '1000',
        roastedAmount2: '829',
    },
    {
        id: 3,
        code: '',
        name: '코케허니',
        type: 'N',
        greenAmount1: '',
        roastedAmount1: '',
        greenAmount2: '1000',
        roastedAmount2: '840',
    },
    {
        id: 4,
        code: 'K',
        name: '우리가',
        type: 'W',
        greenAmount1: '1000',
        roastedAmount1: '883',
        greenAmount2: '1000',
        roastedAmount2: '834',
    },
    {
        id: 5,
        code: 'K',
        name: 'AA FAQ',
        type: 'W',
        greenAmount1: '500',
        roastedAmount1: '435',
        greenAmount2: '1500',
        roastedAmount2: '1250',
    },
    {
        id: 6,
        code: '',
        name: '키린야가',
        type: 'Pb',
        greenAmount1: '',
        roastedAmount1: '',
        greenAmount2: '',
        roastedAmount2: '',
    },
    {
        id: 7,
        code: 'Co',
        name: '후일라',
        type: 'W',
        greenAmount1: '500',
        roastedAmount1: '433',
        greenAmount2: '1000',
        roastedAmount2: '837',
    },
    {
        id: 8,
        code: 'Gu',
        name: '안티구아',
        type: 'W',
        greenAmount1: '500',
        roastedAmount1: '437',
        greenAmount2: '',
        roastedAmount2: '',
    },
    {
        id: 9,
        code: 'Cos',
        name: '엘탄케',
        type: 'Rh',
        greenAmount1: '',
        roastedAmount1: '',
        greenAmount2: '',
        roastedAmount2: '',
    },
    {
        id: 10,
        code: 'Br',
        name: '파인디카트모',
        type: 'N',
        greenAmount1: '',
        roastedAmount1: '',
        greenAmount2: '',
        roastedAmount2: '',
    },
    {
        id: 11,
        code: 'Eth',
        name: '디카페 SDM',
        type: 'SD',
        greenAmount1: '',
        roastedAmount1: '',
        greenAmount2: '',
        roastedAmount2: '',
    },
    {
        id: 12,
        code: 'Co',
        name: '디카페 SM',
        type: 'SC',
        greenAmount1: '500',
        roastedAmount1: '435',
        greenAmount2: '500',
        roastedAmount2: '423',
    },
    {
        id: 13,
        code: 'Br',
        name: '스위스워터',
        type: 'SD',
        greenAmount1: '',
        roastedAmount1: '',
        greenAmount2: '',
        roastedAmount2: '',
    },
];

const ORDER_BLEND_DATA = [
    { code: 'K', name: 'AA FAQ', type: 'W' },
    { code: 'Gu', name: '안티구아', type: 'W' },
    { code: 'Eth', name: '모모라', type: 'N' },
    { code: 'Eth', name: '시디모G4', type: 'W' },
];

const STOCK_SINGLE_DATA = [
    '예가체프',
    '모모라',
    '코케허니',
    '우리가',
    'AA FAQ',
    '키린야가',
    '후일라',
    '안티구아',
    '엘탄케',
    '파인디카트모',
    '디카페 SDM',
    '디카페 SM',
    '스위스워터',
];

const RESERVATION_LIST = [
    { name: '신, 우리가', green: '1000', roasted: '859' },
    { name: '신, 코케허니', green: '1000', roasted: '873' },
];

export function RoastingInvoice() {
    const [year, setYear] = useState('2025');
    const [month, setMonth] = useState('11');
    const [day, setDay] = useState('21');

    // State for editable table
    const [beanData, setBeanData] = useState<BeanRow[]>(INITIAL_BEAN_DATA);
    const [americanoCount, setAmericanoCount] = useState<string>('10'); // Mock Value

    // Helper for Type Colors
    const getTypeColor = (type: string) => {
        switch (type) {
            case 'W':
                return 'text-blue-600 dark:text-blue-400';
            case 'N':
                return 'text-red-600 dark:text-red-400';
            case 'Rh':
                return 'text-pink-600 dark:text-pink-400';
            default:
                return 'text-gray-500';
        }
    };

    // Handler for input changes in main table
    const handleBeanChange = (id: number, field: keyof BeanRow, value: string) => {
        setBeanData((prev) => prev.map((row) => (row.id === id ? { ...row, [field]: value } : row)));
    };

    return (
        <div className="bg-background min-h-screen p-4 md:p-8 font-sans transition-colors duration-200">
            {/* Header */}
            <header className="mb-8 flex flex-col md:flex-row justify-between items-center max-w-7xl mx-auto gap-4">
                <div className="flex flex-col items-center md:items-start">
                    <h1 className="text-3xl md:text-4xl font-bold text-gray-800 dark:text-white mb-1 tracking-tight">
                        더문드립바
                    </h1>
                    <h2 className="text-xl text-muted-foreground font-medium">The Moon Drip BAR</h2>
                </div>

                <div className="flex items-center space-x-4 bg-card px-6 py-3 rounded-lg shadow-sm border">
                    <div className="flex items-center space-x-2 text-lg font-medium">
                        <span>{year}년</span>
                        <input
                            className="w-10 text-center bg-transparent border-b focus:outline-none focus:border-amber-500 text-amber-600 font-bold"
                            value={month}
                            onChange={(e) => setMonth(e.target.value)}
                        />
                        <span>월</span>
                        <input
                            className="w-10 text-center bg-transparent border-b focus:outline-none focus:border-amber-500 text-amber-600 font-bold"
                            value={day}
                            onChange={(e) => setDay(e.target.value)}
                        />
                        <span>일</span>
                    </div>
                </div>

                <div className="flex items-center space-x-2">
                    <div className="relative w-12 h-12 flex items-center justify-center">
                        <Circle className="absolute top-0 left-0 text-blue-400/80 w-8 h-8 fill-current" />
                        <Triangle className="absolute bottom-0 left-0 text-red-400/80 w-8 h-8 fill-current rotate-180" />
                    </div>
                    <div className="text-right">
                        <div className="text-2xl font-bold leading-none">The</div>
                        <div className="text-2xl font-bold leading-none flex items-center">
                            Moon <Moon className="w-5 h-5 text-yellow-500 ml-1 fill-current -rotate-12" />
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content Grid */}
            <main className="grid grid-cols-1 lg:grid-cols-12 gap-6 max-w-7xl mx-auto">
                {/* Left Column (Main Table + Order Blend) */}
                <section className="lg:col-span-6 flex flex-col gap-6">
                    <Card className="rounded-xl shadow-md overflow-hidden border-0 bg-white dark:bg-zinc-900 border-border">
                        <div className="overflow-x-auto">
                            <Table className="w-full text-sm">
                                <TableHeader className="bg-gray-100 dark:bg-gray-800">
                                    <TableRow className="border-b border-border hover:bg-transparent">
                                        <TableHead className="w-8 text-center border-r font-bold text-gray-700 dark:text-gray-300">
                                            #
                                        </TableHead>
                                        <TableHead className="w-12 text-center border-r font-bold text-gray-700 dark:text-gray-300">
                                            Code
                                        </TableHead>
                                        <TableHead className="text-left font-bold border-r text-gray-700 dark:text-gray-300">
                                            Name
                                        </TableHead>
                                        <TableHead className="w-14 text-center border-r font-bold text-gray-700 dark:text-gray-300">
                                            Type
                                        </TableHead>
                                        <TableHead className="text-right bg-red-50/50 text-red-600 dark:text-red-400 border-r font-bold min-w-[70px]">
                                            생두량
                                        </TableHead>
                                        <TableHead className="text-right border-r font-bold text-gray-700 dark:text-gray-300 min-w-[70px]">
                                            볶은량
                                        </TableHead>
                                        <TableHead className="text-right bg-red-50/50 text-red-600 dark:text-red-400 border-r font-bold min-w-[70px]">
                                            생두량
                                        </TableHead>
                                        <TableHead className="text-right font-bold text-gray-700 dark:text-gray-300 min-w-[70px]">
                                            볶은량
                                        </TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody className="divide-y">
                                    {beanData.map((bean) => (
                                        <TableRow key={bean.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50">
                                            <TableCell className="p-2 text-center font-bold">{bean.id}</TableCell>
                                            <TableCell className="p-2 text-center text-xs font-mono">
                                                {bean.code}
                                            </TableCell>
                                            <TableCell className="p-2 font-medium whitespace-nowrap">
                                                {bean.name}
                                            </TableCell>
                                            <TableCell
                                                className={cn('p-2 text-center font-bold', getTypeColor(bean.type))}
                                            >
                                                {bean.type}
                                            </TableCell>

                                            {/* Editable Inputs */}
                                            <TableCell className="p-1 text-right">
                                                <Input
                                                    className="h-7 text-right p-1 bg-transparent border-none text-red-500 dark:text-red-400 font-mono focus-visible:ring-1 focus-visible:ring-offset-0"
                                                    value={bean.greenAmount1}
                                                    onChange={(e) =>
                                                        handleBeanChange(bean.id, 'greenAmount1', e.target.value)
                                                    }
                                                />
                                            </TableCell>
                                            <TableCell className="p-1 text-right">
                                                <Input
                                                    className="h-7 text-right p-1 bg-transparent border-none font-mono focus-visible:ring-1 focus-visible:ring-offset-0"
                                                    value={bean.roastedAmount1}
                                                    onChange={(e) =>
                                                        handleBeanChange(bean.id, 'roastedAmount1', e.target.value)
                                                    }
                                                />
                                            </TableCell>
                                            <TableCell className="p-1 text-right">
                                                <Input
                                                    className="h-7 text-right p-1 bg-transparent border-none text-red-500 dark:text-red-400 font-mono focus-visible:ring-1 focus-visible:ring-offset-0"
                                                    value={bean.greenAmount2}
                                                    onChange={(e) =>
                                                        handleBeanChange(bean.id, 'greenAmount2', e.target.value)
                                                    }
                                                />
                                            </TableCell>
                                            <TableCell className="p-1 text-right">
                                                <Input
                                                    className={cn(
                                                        'h-7 text-right p-1 bg-transparent border-none font-mono focus-visible:ring-1 focus-visible:ring-offset-0',
                                                        bean.id === 7 ? 'text-blue-600 dark:text-blue-400' : ''
                                                    )}
                                                    value={bean.roastedAmount2}
                                                    onChange={(e) =>
                                                        handleBeanChange(bean.id, 'roastedAmount2', e.target.value)
                                                    }
                                                />
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </div>

                        {/* Order Blend Section (Attached at bottom) */}
                        <div className="border-t bg-gray-50 dark:bg-gray-800/30">
                            <div className="bg-gray-200 dark:bg-gray-700 py-2 px-4 flex justify-between items-center border-b text-sm">
                                <span className="font-bold">주문 블랜드</span>
                                <div className="flex items-center gap-2">
                                    <span className="text-gray-500 text-xs">Blend Type:</span>
                                    <Select defaultValue="default">
                                        <SelectTrigger className="w-[120px] h-7 text-xs bg-white dark:bg-gray-800">
                                            <SelectValue placeholder="Select" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="default">House Blend</SelectItem>
                                            <SelectItem value="mild">Mild Blend</SelectItem>
                                            <SelectItem value="dark">Dark Roast</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>
                            <Table className="w-full text-sm">
                                <TableHeader className="bg-gray-100 dark:bg-gray-800">
                                    <TableRow>
                                        <TableHead className="w-12 text-center p-1 h-8">Code</TableHead>
                                        <TableHead className="text-left p-1 h-8">Name</TableHead>
                                        <TableHead className="w-12 text-center p-1 h-8">Type</TableHead>
                                        <TableHead className="p-1 h-8 text-center text-xs text-muted-foreground w-1/4">
                                            Notes
                                        </TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody className="divide-y">
                                    {ORDER_BLEND_DATA.map((item, idx) => (
                                        <TableRow key={idx}>
                                            <TableCell className="w-12 p-1 text-center font-bold bg-gray-50 dark:bg-gray-800">
                                                {item.code}
                                            </TableCell>
                                            <TableCell className="p-1 text-left font-medium pl-2">{item.name}</TableCell>
                                            <TableCell
                                                className={cn(
                                                    'w-12 p-1 text-center font-bold bg-blue-50 dark:bg-blue-900/10',
                                                    item.type === 'N' && 'bg-red-50 dark:bg-red-900/10 text-red-600'
                                                )}
                                            >
                                                <span className={getTypeColor(item.type)}>{item.type}</span>
                                            </TableCell>
                                            <TableCell className="p-1">
                                                <Input
                                                    className="h-6 text-xs bg-transparent border-transparent focus:border-input"
                                                    placeholder="비고 입력"
                                                />
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </div>
                    </Card>
                </section>

                {/* Right Column (Stock & Other Lists) */}
                <section className="lg:col-span-6 flex flex-col space-y-6">
                    <div className="grid grid-cols-2 gap-4">
                        {/* Single Stock */}
                        <Card className="rounded-xl shadow-md overflow-hidden border-0 bg-white dark:bg-zinc-900 border-border">
                            <Table className="w-full text-sm h-full">
                                <TableHeader className="bg-gray-100 dark:bg-gray-700">
                                    <TableRow>
                                        <TableHead className="py-2 px-3 text-left border-b border-r font-bold text-gray-700 dark:text-gray-200 h-9">
                                            싱글
                                        </TableHead>
                                        <TableHead className="py-2 px-3 text-center border-b font-bold text-gray-700 dark:text-gray-200 h-9">
                                            재고
                                        </TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody className="divide-y">
                                    {STOCK_SINGLE_DATA.map((name, idx) => (
                                        <TableRow key={idx} className="hover:bg-transparent h-8">
                                            <TableCell className="px-3 py-1 font-medium border-r">{name}</TableCell>
                                            <TableCell className="px-1 py-0 bg-gray-50 dark:bg-gray-800 p-0">
                                                <Input className="h-full w-full border-none bg-transparent text-center focus-visible:ring-0" />
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </Card>

                        <div className="flex flex-col gap-4">
                            {/* Sin/Tan Stock */}
                            <Card className="rounded-xl shadow-md overflow-hidden border-0 bg-white dark:bg-zinc-900 border-border">
                                <Table className="w-full text-sm">
                                    <TableHeader className="bg-gray-100 dark:bg-gray-700">
                                        <TableRow>
                                            <TableHead className="py-2 px-2 text-left border-b border-r font-bold text-gray-700 dark:text-gray-200 text-xs h-9">
                                                신,탄
                                            </TableHead>
                                            <TableHead className="py-2 px-2 text-center border-b border-r font-bold text-gray-700 dark:text-gray-200 text-xs h-9">
                                                재고
                                            </TableHead>
                                            <TableHead className="py-2 px-2 text-center border-b border-r font-bold text-gray-700 dark:text-gray-200 text-xs h-9">
                                                기타
                                            </TableHead>
                                            <TableHead className="py-2 px-2 text-center border-b font-bold text-gray-700 dark:text-gray-200 text-xs h-9">
                                                재고
                                            </TableHead>
                                        </TableRow>
                                    </TableHeader>
                                    <TableBody className="divide-y">
                                        <TableRow className="h-9">
                                            <TableCell className="px-2 py-1 font-medium border-r text-xs">
                                                산토스
                                            </TableCell>
                                            <TableCell className="px-0 py-0 bg-gray-50 dark:bg-gray-800 border-r">
                                                <Input className="h-full w-full border-none bg-transparent text-center focus-visible:ring-0 text-xs" />
                                            </TableCell>
                                            <TableCell className="px-0 py-0 border-r">
                                                <Input className="h-full w-full border-none bg-transparent text-center focus-visible:ring-0 text-xs" />
                                            </TableCell>
                                            <TableCell className="px-0 py-0 bg-gray-50 dark:bg-gray-800">
                                                <Input className="h-full w-full border-none bg-transparent text-center focus-visible:ring-0 text-xs" />
                                            </TableCell>
                                        </TableRow>
                                        <TableRow className="h-9">
                                            <TableCell className="px-2 py-1 font-medium border-r text-xs">
                                                시다모G4
                                            </TableCell>
                                            <TableCell className="px-0 py-0 bg-gray-50 dark:bg-gray-800 border-r">
                                                <Input className="h-full w-full border-none bg-transparent text-center focus-visible:ring-0 text-xs" />
                                            </TableCell>
                                            <TableCell className="px-0 py-0 border-r">
                                                <Input className="h-full w-full border-none bg-transparent text-center focus-visible:ring-0 text-xs" />
                                            </TableCell>
                                            <TableCell className="px-0 py-0 bg-gray-50 dark:bg-gray-800">
                                                <Input className="h-full w-full border-none bg-transparent text-center focus-visible:ring-0 text-xs" />
                                            </TableCell>
                                        </TableRow>
                                    </TableBody>
                                </Table>
                            </Card>

                            {/* New Moon Blend */}
                            <Card className="rounded-xl shadow-md overflow-hidden border-0 bg-white dark:bg-zinc-900 border-border">
                                <div className="bg-gray-200 dark:bg-gray-700 py-1 px-3 text-sm font-bold border-b text-center text-gray-800 dark:text-gray-200 flex items-center justify-between">
                                    <span>뉴문 블랜드</span>
                                    <Input
                                        className="w-16 h-6 text-center text-xs bg-white dark:bg-gray-800"
                                        placeholder="(  )"
                                    />
                                </div>
                                <div className="grid grid-cols-2 border-b text-xs font-bold bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300">
                                    <div className="py-1 text-center border-r">성두량</div>
                                    <div className="py-1 text-center">볶은량</div>
                                </div>
                                <Table className="w-full text-sm">
                                    <TableBody className="divide-y">
                                        {['산토스', '후일라', '시디모G4'].map((item, idx) => (
                                            <TableRow key={idx} className="h-8">
                                                <TableCell className="px-2 py-1 border-r w-1/2 text-xs font-medium">
                                                    {item}
                                                </TableCell>
                                                <TableCell className="px-0 py-0 bg-gray-50 dark:bg-gray-800 w-1/2">
                                                    <Input className="h-full w-full border-none bg-transparent text-center focus-visible:ring-0 text-xs" />
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </Card>

                            {/* Eclipse Moon Blend */}
                            <Card className="rounded-xl shadow-md overflow-hidden border-0 bg-white dark:bg-zinc-900 border-border">
                                <div className="bg-gray-200 dark:bg-gray-700 py-1 px-3 text-sm font-bold border-b text-center text-gray-800 dark:text-gray-200">
                                    이클립스문 (디카페인)
                                </div>
                                <div className="grid grid-cols-3 border-b text-xs font-bold bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300">
                                    <div className="py-1 text-center border-r col-span-1"></div>
                                    <div className="py-1 text-center border-r col-span-1">성두량</div>
                                    <div className="py-1 text-center col-span-1">볶은량</div>
                                </div>
                                <Table className="w-full text-sm">
                                    <TableBody className="divide-y">
                                        {['co디카페인', 'Br디카페인'].map((item, idx) => (
                                            <TableRow key={idx} className="h-8">
                                                <TableCell className="px-2 py-1 border-r w-1/3 text-xs font-medium">
                                                    {item}
                                                </TableCell>
                                                <TableCell className="px-0 py-0 border-r bg-gray-50 dark:bg-gray-800 w-1/3">
                                                    <Input className="h-full w-full border-none bg-transparent text-center focus-visible:ring-0 text-xs" />
                                                </TableCell>
                                                <TableCell className="px-0 py-0 bg-gray-50 dark:bg-gray-800 w-1/3">
                                                    <Input className="h-full w-full border-none bg-transparent text-center focus-visible:ring-0 text-xs" />
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </Card>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* Americano Counter */}
                        <Card className="rounded-xl shadow-md overflow-hidden border-0 bg-white dark:bg-zinc-900 border-border flex flex-col">
                            <div className="bg-gray-200 dark:bg-gray-700 py-2 text-center font-bold border-b text-lg text-gray-800 dark:text-gray-200">
                                아메리카노
                            </div>
                            <div className="flex-grow flex items-center justify-center p-4 bg-white dark:bg-gray-800">
                                <div className="flex items-end border-b-2 border-gray-400 dark:border-gray-500 px-4 pb-1">
                                    <Input
                                        className="text-2xl font-bold border-none text-center w-20 p-0 h-auto focus-visible:ring-0 bg-transparent shadow-none"
                                        value={americanoCount}
                                        onChange={(e) => setAmericanoCount(e.target.value)}
                                    />
                                </div>
                                <span className="ml-2 text-lg font-medium self-end mb-2">회</span>
                            </div>
                            <div className="h-16 border-t bg-gray-50 dark:bg-gray-900/20"></div>
                        </Card>

                        {/* Reservation List */}
                        <Card className="rounded-xl shadow-md overflow-hidden border-0 bg-white dark:bg-zinc-900 border-border">
                            <div className="bg-gray-200 dark:bg-gray-700 py-2 text-center font-bold border-b text-lg text-gray-800 dark:text-gray-200">
                                예약 리스트
                            </div>
                            <Table className="w-full text-sm">
                                <TableBody className="divide-y">
                                    {RESERVATION_LIST.map((res, idx) => (
                                        <TableRow key={idx} className="h-10">
                                            <TableCell className="px-3 py-2 border-r text-red-600 dark:text-red-400 font-serif italic text-left">
                                                {res.name}
                                            </TableCell>
                                            <TableCell className="px-0 py-0 border-r w-20">
                                                <Input
                                                    className="h-full w-full border-none bg-transparent text-right text-red-600 dark:text-red-400 font-mono focus-visible:ring-0"
                                                    defaultValue={res.green}
                                                />
                                            </TableCell>
                                            <TableCell className="px-0 py-0 w-20">
                                                <Input
                                                    className="h-full w-full border-none bg-transparent text-right text-blue-600 dark:text-blue-400 font-bold font-mono focus-visible:ring-0"
                                                    defaultValue={res.roasted}
                                                />
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                    {/* Empty Rows used for spacing/layout balance */}
                                    <TableRow className="h-10">
                                        <TableCell className="px-3 py-4 border-r"></TableCell>
                                        <TableCell className="px-3 py-4 border-r"></TableCell>
                                        <TableCell className="px-3 py-4"></TableCell>
                                    </TableRow>
                                </TableBody>
                            </Table>
                        </Card>
                    </div>
                </section>
            </main>

            {/* Floating Action Button */}
            <div className="fixed bottom-8 right-8 print:hidden">
                <Button className="w-14 h-14 rounded-full bg-amber-600 hover:bg-amber-700 shadow-lg p-0 transition-transform hover:scale-105 active:scale-95">
                    <Plus className="w-8 h-8 text-white" />
                </Button>
            </div>
        </div>
    );
}
