'use client';

import React, { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Trash2, Plus, Lock, Unlock } from 'lucide-react';
import { Label } from '@/components/ui/label';

interface KeyValueListProps {
    items: Record<string, string>;
    onChange: (items: Record<string, string>) => void;
    keyLabel?: string;
    valueLabel?: string;
    keyPlaceholder?: string;
    valuePlaceholder?: string;
    disabled?: boolean;
}

interface Entry {
    key: string;
    value: string;
    isLocked: boolean;
}

export function KeyValueList({
    items,
    onChange,
    keyLabel = "Field Key",
    valueLabel = "Description / Instruction",
    keyPlaceholder = "e.g., invoice_date",
    valuePlaceholder = "e.g., 거래일 (YYYY-MM-DD)",
    disabled = false
}: KeyValueListProps) {
    // Internal state to track entries and their lock status
    const [entries, setEntries] = useState<Entry[]>([]);

    useEffect(() => {
        // Compare current state with props to avoid infinite loops
        // tailored to the Entry structure
        const currentParams = entries.reduce((acc, entry) => {
            if (entry.key) acc[entry.key] = entry.value;
            return acc;
        }, {} as Record<string, string>);

        const isSame = JSON.stringify(currentParams) === JSON.stringify(items);

        if (!isSame) {
            // When props change externally (or first load), we reset.
            // But we must preserve the 'isLocked' status of currently editable items 
            // to allow users to continue typing new keys without getting locked out.

            const newEntries = Object.entries(items).map(([k, v]) => {
                // Check if this key exists in our current local state
                const existingEntry = entries.find(e => e.key === k);

                // Logic:
                // 1. If key exists locally and was unlocked (user created it), keep it unlocked.
                // 2. If key exists and was locked, keep it locked.
                // 3. If key is new (external update or initial load), lock it by default (Safety).
                const shouldBeLocked = existingEntry ? existingEntry.isLocked : true;

                return {
                    key: k,
                    value: v,
                    isLocked: shouldBeLocked
                };
            });
            setEntries(newEntries);
        }
    }, [items]); // Implicit dependency on 'entries' for the merge logic is safe here as 'items' triggers the update

    const updateEntry = (index: number, field: 'key' | 'value', text: string) => {
        const newEntries = [...entries];
        if (field === 'key') newEntries[index].key = text;
        else newEntries[index].value = text;

        setEntries(newEntries);
        propagateChange(newEntries);
    };

    const removeEntry = (index: number) => {
        const newEntries = entries.filter((_, i) => i !== index);
        setEntries(newEntries);
        propagateChange(newEntries);
    };

    const addEntry = () => {
        // New items are UNLOCKED by default so user can type the key
        const newEntries = [...entries, { key: '', value: '', isLocked: false }];
        setEntries(newEntries);
        // We don't propagate immediately on add since empty key is invalid/weird in object
    };

    const propagateChange = (currentEntries: Entry[]) => {
        const newObj = currentEntries.reduce((acc, entry) => {
            // Only add if key is not empty
            if (entry.key) acc[entry.key] = entry.value;
            return acc;
        }, {} as Record<string, string>);
        onChange(newObj);
    };

    return (
        <div className="space-y-3">
            <div className="flex gap-4 px-1">
                <Label className="w-1/3 text-xs text-muted-foreground uppercase flex items-center gap-1">
                    {keyLabel}
                    <span className="text-[10px] font-normal text-amber-600 bg-amber-50 px-1 rounded border border-amber-200">
                        Locked
                    </span>
                </Label>
                <Label className="flex-1 text-xs text-muted-foreground uppercase">{valueLabel}</Label>
                <div className="w-8"></div>
            </div>

            <div className="space-y-2">
                {entries.map((entry, index) => (
                    <div key={index} className="flex gap-4 items-start group">
                        <div className="relative w-1/3">
                            <Input
                                value={entry.key}
                                onChange={(e) => updateEntry(index, 'key', e.target.value)}
                                placeholder={keyPlaceholder}
                                className={`font-mono text-sm pr-8 h-10 rounded-xl ${entry.isLocked ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : 'bg-white'}`}
                                readOnly={entry.isLocked}
                                disabled={disabled}
                            />
                            {entry.isLocked && (
                                <Lock className="w-3 h-3 absolute right-3 top-3 text-gray-400" />
                            )}
                        </div>

                        <Input
                            value={entry.value}
                            onChange={(e) => updateEntry(index, 'value', e.target.value)}
                            placeholder={valuePlaceholder}
                            className="flex-1 h-10 rounded-xl"
                            disabled={disabled}
                        />

                        <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => removeEntry(index)}
                            disabled={disabled}
                            className="h-10 w-10 text-muted-foreground hover:text-red-500 opacity-50 group-hover:opacity-100 transition-opacity"
                        >
                            <Trash2 className="w-4 h-4" />
                        </Button>
                    </div>
                ))}
            </div>

            {!disabled && (
                <Button
                    variant="outline"
                    size="sm"
                    onClick={addEntry}
                    className="w-full mt-2 border-dashed text-muted-foreground hover:text-foreground"
                >
                    <Plus className="w-4 h-4 mr-2" /> Add Item
                </Button>
            )}

            <p className="text-[10px] text-muted-foreground mt-2">
                * Field Names are locked for existing items to prevent system errors. Remove and re-add if renaming is absolutely necessary.
            </p>
        </div>
    );
}
