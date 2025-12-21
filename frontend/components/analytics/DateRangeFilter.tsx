"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Calendar } from "lucide-react"

interface DateRangeFilterProps {
    onDateChange: (startDate: string | null, endDate: string | null) => void
}

export function DateRangeFilter({ onDateChange }: DateRangeFilterProps) {
    const [startDate, setStartDate] = useState<string>("")
    const [endDate, setEndDate] = useState<string>("")
    const [activePreset, setActivePreset] = useState<string>("all")

    const handlePreset = (preset: string) => {
        console.log("handlePreset called:", preset)
        setActivePreset(preset)
        const today = new Date()
        let start: Date | null = null

        switch (preset) {
            case "30days":
                start = new Date(today)
                start.setDate(today.getDate() - 30)
                break
            case "3months":
                start = new Date(today)
                start.setMonth(today.getMonth() - 3)
                break
            case "6months":
                start = new Date(today)
                start.setMonth(today.getMonth() - 6)
                break
            case "1year":
                start = new Date(today)
                start.setFullYear(today.getFullYear() - 1)
                break
            case "all":
                setStartDate("")
                setEndDate("")
                onDateChange(null, null)
                return
        }

        if (start) {
            const startStr = start.toISOString().split("T")[0]
            const endStr = today.toISOString().split("T")[0]

            // UI Update
            setStartDate(startStr)
            setEndDate(endStr)

            // Parent Callback
            onDateChange(startStr, endStr)
        }
    }

    const handleCustomDate = () => {
        setActivePreset("custom")
        if (startDate && endDate) {
            onDateChange(startDate, endDate)
        } else if (!startDate && !endDate) {
            onDateChange(null, null)
        }
    }

    const handleReset = () => {
        setStartDate("")
        setEndDate("")
        setActivePreset("all")
        onDateChange(null, null)
    }

    return (
        <Card>
            <CardContent className="pt-6">
                <div className="space-y-4">
                    <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4 text-muted-foreground" />
                        <h3 className="text-sm font-medium">기간 선택</h3>
                    </div>

                    {/* Preset Buttons */}
                    <div className="flex flex-wrap gap-2">
                        <Button
                            size="sm"
                            variant={activePreset === "all" ? "default" : "outline"}
                            onClick={() => handlePreset("all")}
                        >
                            전체
                        </Button>
                        <Button
                            size="sm"
                            variant={activePreset === "30days" ? "default" : "outline"}
                            onClick={() => handlePreset("30days")}
                        >
                            최근 30일
                        </Button>
                        <Button
                            size="sm"
                            variant={activePreset === "3months" ? "default" : "outline"}
                            onClick={() => handlePreset("3months")}
                        >
                            최근 3개월
                        </Button>
                        <Button
                            size="sm"
                            variant={activePreset === "6months" ? "default" : "outline"}
                            onClick={() => handlePreset("6months")}
                        >
                            최근 6개월
                        </Button>
                        <Button
                            size="sm"
                            variant={activePreset === "1year" ? "default" : "outline"}
                            onClick={() => handlePreset("1year")}
                        >
                            최근 1년
                        </Button>
                    </div>

                    {/* Custom Date Range */}
                    <div className="grid grid-cols-2 gap-2">
                        <div className="space-y-2">
                            <label className="text-xs text-muted-foreground">시작일</label>
                            <input
                                type="date"
                                value={startDate}
                                onChange={(e) => {
                                    const newStart = e.target.value
                                    setStartDate(newStart)
                                    setActivePreset("custom")
                                    if (newStart && endDate) {
                                        onDateChange(newStart, endDate)
                                    }
                                }}
                                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-xs text-muted-foreground">종료일</label>
                            <input
                                type="date"
                                value={endDate}
                                onChange={(e) => {
                                    const newEnd = e.target.value
                                    setEndDate(newEnd)
                                    setActivePreset("custom")
                                    if (startDate && newEnd) {
                                        onDateChange(startDate, newEnd)
                                    }
                                }}
                                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                            />
                        </div>
                    </div>

                    {/* Reset Button Only */}
                    <div>
                        <Button
                            size="sm"
                            variant="outline"
                            onClick={handleReset}
                            className="w-full"
                        >
                            초기화
                        </Button>
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}
