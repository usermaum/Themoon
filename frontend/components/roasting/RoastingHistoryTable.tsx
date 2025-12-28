
"use client"

import * as React from "react"
import { format } from "date-fns"
import { ko } from "date-fns/locale"
import { Calendar as CalendarIcon, Filter, RefreshCcw } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover"
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { cn } from "@/lib/utils"
import { Badge } from "@/components/ui/badge"
import { RoastingLog } from "@/lib/api"



interface RoastingHistoryTableProps {
    logs: RoastingLog[]
    loading: boolean
    onFilterChange: (filters: any) => void
    onRowClick?: (log: RoastingLog) => void
}

export function RoastingHistoryTable({ logs, loading, onFilterChange, onRowClick }: RoastingHistoryTableProps) {
    const [date, setDate] = React.useState<Date | undefined>(undefined)
    const [beanType, setBeanType] = React.useState<string>("ALL")

    const handleFilterApply = () => {
        onFilterChange({
            start_date: date ? format(date, "yyyy-MM-dd") : undefined,
            bean_type: beanType !== "ALL" ? beanType : undefined,
        })
    }

    const handleReset = () => {
        setDate(undefined)
        setBeanType("ALL")
        onFilterChange({})
    }

    return (
        <div className="space-y-4">
            <div className="flex items-center justify-between gap-4 p-4 bg-muted/20 rounded-lg border">
                <div className="flex items-center gap-2">
                    <Filter className="w-4 h-4 text-muted-foreground" />
                    <span className="text-sm font-medium">필터</span>

                    <Popover>
                        <PopoverTrigger asChild>
                            <Button
                                variant={"outline"}
                                className={cn(
                                    "w-[200px] justify-start text-left font-normal",
                                    !date && "text-muted-foreground"
                                )}
                            >
                                <CalendarIcon className="mr-2 h-4 w-4" />
                                {date ? format(date, "PPP", { locale: ko }) : <span>날짜 선택</span>}
                            </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0">
                            <Calendar
                                mode="single"
                                selected={date}
                                onSelect={setDate}
                                initialFocus
                            />
                        </PopoverContent>
                    </Popover>

                    <Select value={beanType} onValueChange={setBeanType}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="원두 유형" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="ALL">전체 유형</SelectItem>
                            <SelectItem value="GREEN_BEAN">싱글 오리진</SelectItem>
                            <SelectItem value="BLEND_BEAN">블렌드</SelectItem>
                        </SelectContent>
                    </Select>
                </div>

                <div className="flex items-center gap-2">
                    <Button variant="ghost" size="sm" onClick={handleReset}>
                        <RefreshCcw className="w-4 h-4 mr-2" />
                        초기화
                    </Button>
                    <Button size="sm" onClick={handleFilterApply}>
                        조회 적용
                    </Button>
                </div>
            </div>

            <div className="rounded-md border">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>날짜</TableHead>
                            <TableHead>배치 번호</TableHead>
                            <TableHead>품목명</TableHead>
                            <TableHead>유형</TableHead>
                            <TableHead className="text-right">투입량</TableHead>
                            <TableHead className="text-right">생산량</TableHead>
                            <TableHead className="text-right hidden md:table-cell">손실률</TableHead>
                            <TableHead className="hidden md:table-cell">프로필</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {loading ? (
                            <TableRow>
                                <TableCell colSpan={8} className="h-24 text-center">
                                    데이터를 불러오는 중...
                                </TableCell>
                            </TableRow>
                        ) : logs.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={8} className="h-24 text-center text-muted-foreground">
                                    로스팅 이력이 없습니다.
                                </TableCell>
                            </TableRow>
                        ) : (
                            logs.map((log) => (
                                <TableRow
                                    key={log.id}
                                    className={cn("hover:bg-muted/50 transition-colors", onRowClick && "cursor-pointer")}
                                    onClick={() => onRowClick && onRowClick(log)}
                                >
                                    <TableCell>
                                        {format(new Date(log.roast_date), "yyyy-MM-dd")}
                                    </TableCell>
                                    <TableCell className="font-mono text-xs">{log.batch_no}</TableCell>
                                    <TableCell className="font-medium">{log.target_bean?.name || "-"}</TableCell>
                                    <TableCell>
                                        {log.target_bean?.type === "BLEND_BEAN" ? (
                                            <Badge variant="secondary">블렌드</Badge>
                                        ) : (
                                            <Badge variant="outline">싱글 오리진</Badge>
                                        )}
                                        )}
                                    </TableCell>
                                    <TableCell className="text-right">{log.input_weight_total}kg</TableCell>
                                    <TableCell className="text-right font-bold">{log.output_weight_total}kg</TableCell>
                                    <TableCell className="text-right text-muted-foreground hidden md:table-cell">
                                        {log.loss_rate ? `${log.loss_rate.toFixed(1)}%` : "-"}
                                    </TableCell>
                                    <TableCell className="hidden md:table-cell">
                                        {log.roast_profile && (
                                            <Badge variant={log.roast_profile === "DARK" ? "destructive" : "default"} className="text-[10px]">
                                                {log.roast_profile}
                                            </Badge>
                                        )}
                                    </TableCell>
                                </TableRow>
                            ))
                        )}
                    </TableBody>
                </Table>
            </div>
        </div>
    )
}
