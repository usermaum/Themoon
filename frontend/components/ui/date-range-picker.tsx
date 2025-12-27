'use client';

import * as React from 'react';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';
import { Calendar as CalendarIcon } from 'lucide-react';
import { DateRange } from 'react-day-picker';

import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from '@/components/ui/popover';

interface DateRangePickerProps {
    className?: string;
    date: DateRange | undefined;
    onSelect: (date: DateRange | undefined) => void;
    placeholder?: string;
}

export function DateRangePicker({
    className,
    date,
    onSelect,
    placeholder = "기간 선택"
}: DateRangePickerProps) {
    return (
        <div className={cn("grid gap-2", className)}>
            <Popover>
                <PopoverTrigger asChild>
                    <Button
                        id="date"
                        variant={"outline"}
                        className={cn(
                            "w-full justify-start text-left font-normal border-latte-200 hover:bg-latte-50 hover:text-latte-900 transition-colors h-11 rounded-xl",
                            !date && "text-muted-foreground"
                        )}
                    >
                        <CalendarIcon className="mr-2 h-4 w-4 text-latte-400" />
                        {date?.from ? (
                            date.to ? (
                                <>
                                    {format(date.from, "yyyy-MM-dd", { locale: ko })} ~{" "}
                                    {format(date.to, "yyyy-MM-dd", { locale: ko })}
                                </>
                            ) : (
                                format(date.from, "yyyy-MM-dd", { locale: ko })
                            )
                        ) : (
                            <span className="text-latte-400">{placeholder}</span>
                        )}
                    </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                    <Calendar
                        initialFocus
                        mode="range"
                        defaultMonth={date?.from}
                        selected={date}
                        onSelect={onSelect}
                        numberOfMonths={2}
                        locale={ko}
                        className="p-3 border-latte-100 bg-white shadow-xl rounded-xl"
                        classNames={{
                            day_selected: "bg-latte-600 text-white hover:bg-latte-700 hover:text-white focus:bg-latte-700 focus:text-white",
                            day_today: "bg-latte-50 text-latte-900",

                        }}
                    />
                </PopoverContent>
            </Popover>
        </div>
    );
}
