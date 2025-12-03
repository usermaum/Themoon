"use client";

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Flame, ArrowRight, Scale, Calculator, Loader2, Check } from 'lucide-react';
import { Button } from "@/components/ui/Button"
import PageHero from '@/components/ui/PageHero'
import { useLanguage } from '@/lib/i18n/LanguageContext';
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from "@/components/ui/command"
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover"
import { cn } from "@/lib/utils"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface Bean {
    id: number;
    name: string;
    english_name?: string;
    origin: string;
    grade?: string;
    type: string;
    quantity_kg: number;
    avg_cost_price: number;
}

export default function RoastingPage() {
    const { t } = useLanguage();
    const [greenBeans, setGreenBeans] = useState<Bean[]>([]);
    const [roastedBeans, setRoastedBeans] = useState<Bean[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    // Form State
    const [selectedGreenBeanId, setSelectedGreenBeanId] = useState<number | null>(null);
    const [inputAmount, setInputAmount] = useState<string>("");
    const [outputAmount, setOutputAmount] = useState<string>("");
    const [roastLevel, setRoastLevel] = useState<string>("Medium");
    const [targetMode, setTargetMode] = useState<"new" | "existing">("new");
    const [newBeanName, setNewBeanName] = useState<string>("");
    const [selectedRoastedBeanId, setSelectedRoastedBeanId] = useState<number | null>(null);

    // UI State
    const [openGreenCombobox, setOpenGreenCombobox] = useState(false);
    const [openRoastedCombobox, setOpenRoastedCombobox] = useState(false);

    useEffect(() => {
        fetchBeans();
    }, []);

    const fetchBeans = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/beans?size=100`);
            const allBeans = response.data.items;
            setGreenBeans(allBeans.filter((b: Bean) => b.type === 'GREEN_BEAN'));
            setRoastedBeans(allBeans.filter((b: Bean) => b.type === 'ROASTED_SINGLE'));
        } catch (err) {
            console.error("Failed to fetch beans", err);
        }
    };

    const selectedGreenBean = greenBeans.find(b => b.id === selectedGreenBeanId);

    // Calculations
    const inputVal = parseFloat(inputAmount) || 0;
    const outputVal = parseFloat(outputAmount) || 0;
    const lossRate = inputVal > 0 ? ((inputVal - outputVal) / inputVal * 100) : 0;
    const estimatedCost = (selectedGreenBean && outputVal > 0)
        ? (selectedGreenBean.avg_cost_price * inputVal) / outputVal
        : 0;

    const handleSubmit = async () => {
        if (!selectedGreenBeanId || inputVal <= 0 || outputVal <= 0) return;
        if (targetMode === 'new' && !newBeanName) return;
        if (targetMode === 'existing' && !selectedRoastedBeanId) return;

        setIsLoading(true);
        try {
            const payload = {
                green_bean_id: selectedGreenBeanId,
                input_amount: inputVal,
                output_amount: outputVal,
                roast_level: roastLevel,
                ...(targetMode === 'new' ? { new_bean_name: newBeanName } : { roasted_bean_id: selectedRoastedBeanId })
            };

            await axios.post(`${API_BASE_URL}/roasting/`, payload);
            alert("Roasting recorded successfully!");

            // Reset form
            setInputAmount("");
            setOutputAmount("");
            setNewBeanName("");
            setSelectedRoastedBeanId(null);
            fetchBeans(); // Refresh stock
        } catch (err: any) {
            console.error("Roasting failed", err);
            alert(err.response?.data?.detail || "Failed to record roasting.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div>
            <PageHero
                title={t('roasting.title')}
                description={t('roasting.description')}
                icon={<Flame className="w-10 h-10" />}
                backgroundImage="/images/roasting-hero-placeholder.jpg"
            />
            <div className="p-8 max-w-7xl mx-auto">

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Left: Input Form */}
                    <div className="lg:col-span-2 space-y-6">
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-stone-200">
                            <h2 className="text-xl font-semibold mb-6 text-stone-800">{t('roasting.newBatch')}</h2>

                            {/* 1. Select Green Bean */}
                            <div className="mb-6">
                                <label className="block text-sm font-medium text-stone-600 mb-2">{t('roasting.sourceGreenBean')}</label>
                                <Popover open={openGreenCombobox} onOpenChange={setOpenGreenCombobox}>
                                    <PopoverTrigger asChild>
                                        <Button
                                            variant="outline"
                                            role="combobox"
                                            aria-expanded={openGreenCombobox}
                                            className="w-full justify-between"
                                        >
                                            {selectedGreenBeanId
                                                ? greenBeans.find((bean) => bean.id === selectedGreenBeanId)?.name
                                                : t('roasting.selectGreenBean')}
                                            <ArrowRight className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                                        </Button>
                                    </PopoverTrigger>
                                    <PopoverContent className="w-[400px] p-0">
                                        <Command>
                                            <CommandInput placeholder="Search green bean..." />
                                            <CommandList>
                                                <CommandEmpty>No green bean found.</CommandEmpty>
                                                <CommandGroup>
                                                    {greenBeans.map((bean) => (
                                                        <CommandItem
                                                            key={bean.id}
                                                            value={bean.name}
                                                            onSelect={() => {
                                                                setSelectedGreenBeanId(bean.id);
                                                                setOpenGreenCombobox(false);
                                                                // Auto-fill new name suggestion
                                                                if (!newBeanName) {
                                                                    setNewBeanName(bean.name.replace("G1", "").replace("G2", "").replace("G4", "").trim() + " Roasted");
                                                                }
                                                            }}
                                                        >
                                                            <Check
                                                                className={cn(
                                                                    "mr-2 h-4 w-4",
                                                                    selectedGreenBeanId === bean.id ? "opacity-100" : "opacity-0"
                                                                )}
                                                            />
                                                            <div className="flex flex-col">
                                                                <span className="font-medium">{bean.name}</span>
                                                                <span className="text-xs text-stone-500">{bean.english_name}</span>
                                                                <span className="text-xs text-stone-400">
                                                                    {bean.grade} | Stock: {bean.quantity_kg}kg | Cost: ₩{Math.round(bean.avg_cost_price).toLocaleString()}
                                                                </span>
                                                            </div>
                                                        </CommandItem>
                                                    ))}
                                                </CommandGroup>
                                            </CommandList>
                                        </Command>
                                    </PopoverContent>
                                </Popover>
                            </div>

                            <div className="grid grid-cols-2 gap-6 mb-6">
                                {/* 2. Input Amount */}
                                <div>
                                    <label className="block text-sm font-medium text-stone-600 mb-2">{t('roasting.inputAmount')}</label>
                                    <div className="relative">
                                        <input
                                            type="number"
                                            value={inputAmount}
                                            onChange={(e) => setInputAmount(e.target.value)}
                                            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-amber-500 outline-none pl-10"
                                            placeholder="0.0"
                                        />
                                        <Scale className="absolute left-3 top-3.5 w-5 h-5 text-stone-400" />
                                    </div>
                                    {selectedGreenBean && inputVal > selectedGreenBean.quantity_kg && (
                                        <p className="text-xs text-red-500 mt-1">{t('roasting.exceedsStock').replace('{stock}', selectedGreenBean.quantity_kg.toString())}</p>
                                    )}
                                </div>

                                {/* 3. Output Amount */}
                                <div>
                                    <label className="block text-sm font-medium text-stone-600 mb-2">{t('roasting.outputAmount')}</label>
                                    <div className="relative">
                                        <input
                                            type="number"
                                            value={outputAmount}
                                            onChange={(e) => setOutputAmount(e.target.value)}
                                            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-amber-500 outline-none pl-10"
                                            placeholder="0.0"
                                        />
                                        <Scale className="absolute left-3 top-3.5 w-5 h-5 text-stone-400" />
                                    </div>
                                </div>
                            </div>

                            {/* 4. Target Bean */}
                            <div className="mb-6">
                                <label className="block text-sm font-medium text-stone-600 mb-2">{t('roasting.targetRoastedBean')}</label>
                                <div className="flex gap-4 mb-3">
                                    <label className="flex items-center gap-2 cursor-pointer">
                                        <input type="radio" checked={targetMode === 'new'} onChange={() => setTargetMode('new')} className="text-amber-600" />
                                        <span className="text-sm">{t('roasting.createNewProduct')}</span>
                                    </label>
                                    <label className="flex items-center gap-2 cursor-pointer">
                                        <input type="radio" checked={targetMode === 'existing'} onChange={() => setTargetMode('existing')} className="text-amber-600" />
                                        <span className="text-sm">{t('roasting.addToExisting')}</span>
                                    </label>
                                </div>

                                {targetMode === 'new' ? (
                                    <input
                                        type="text"
                                        value={newBeanName}
                                        onChange={(e) => setNewBeanName(e.target.value)}
                                        className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-amber-500 outline-none"
                                        placeholder={t('roasting.newBeanNamePlaceholder')}
                                    />
                                ) : (
                                    <Popover open={openRoastedCombobox} onOpenChange={setOpenRoastedCombobox}>
                                        <PopoverTrigger asChild>
                                            <Button
                                                variant="outline"
                                                role="combobox"
                                                aria-expanded={openRoastedCombobox}
                                                className="w-full justify-between"
                                            >
                                                {selectedRoastedBeanId
                                                    ? roastedBeans.find((bean) => bean.id === selectedRoastedBeanId)?.name
                                                    : t('roasting.selectRoastedBean')}
                                                <ArrowRight className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                                            </Button>
                                        </PopoverTrigger>
                                        <PopoverContent className="w-[400px] p-0">
                                            <Command>
                                                <CommandInput placeholder="Search roasted bean..." />
                                                <CommandList>
                                                    <CommandEmpty>No roasted bean found.</CommandEmpty>
                                                    <CommandGroup>
                                                        {roastedBeans.map((bean) => (
                                                            <CommandItem
                                                                key={bean.id}
                                                                value={bean.name}
                                                                onSelect={() => {
                                                                    setSelectedRoastedBeanId(bean.id);
                                                                    setOpenRoastedCombobox(false);
                                                                }}
                                                            >
                                                                <Check
                                                                    className={cn(
                                                                        "mr-2 h-4 w-4",
                                                                        selectedRoastedBeanId === bean.id ? "opacity-100" : "opacity-0"
                                                                    )}
                                                                />
                                                                {bean.name}
                                                            </CommandItem>
                                                        ))}
                                                    </CommandGroup>
                                                </CommandList>
                                            </Command>
                                        </PopoverContent>
                                    </Popover>
                                )}
                            </div>

                            <div className="mb-6">
                                <label className="block text-sm font-medium text-stone-600 mb-2">{t('roasting.roastLevel')}</label>
                                <select
                                    value={roastLevel}
                                    onChange={(e) => setRoastLevel(e.target.value)}
                                    className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-amber-500 outline-none bg-white"
                                >
                                    <option value="Light">Light (Cinnamon/New England)</option>
                                    <option value="Medium">Medium (American/City)</option>
                                    <option value="Medium-Dark">Medium-Dark (Full City)</option>
                                    <option value="Dark">Dark (Vienna/French)</option>
                                </select>
                            </div>

                            <button
                                onClick={handleSubmit}
                                disabled={isLoading || !selectedGreenBeanId || inputVal <= 0}
                                className="w-full bg-orange-600 hover:bg-orange-700 text-white py-4 rounded-xl font-bold text-lg transition-colors flex items-center justify-center gap-2 shadow-lg shadow-orange-200"
                            >
                                {isLoading ? <Loader2 className="w-6 h-6 animate-spin" /> : <Flame className="w-6 h-6" />}
                                {t('roasting.startRoasting')}
                            </button>
                        </div>
                    </div>

                    {/* Right: Real-time Stats */}
                    <div className="space-y-6">
                        <div className="bg-stone-900 text-white p-6 rounded-xl shadow-lg">
                            <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                                <Calculator className="w-5 h-5 text-amber-400" /> {t('roasting.batchAnalysis')}
                            </h3>

                            <div className="space-y-6">
                                <div>
                                    <p className="text-stone-400 text-sm mb-1">{t('roasting.lossRate')}</p>
                                    <div className="flex items-end gap-2">
                                        <span className={`text-4xl font-bold ${lossRate > 20 ? 'text-red-400' : 'text-green-400'}`}>
                                            {lossRate.toFixed(1)}%
                                        </span>
                                        <span className="text-stone-500 mb-1">{t('roasting.weightLoss')}</span>
                                    </div>
                                    <div className="w-full bg-stone-800 h-2 rounded-full mt-2 overflow-hidden">
                                        <div
                                            className={`h-full ${lossRate > 20 ? 'bg-red-500' : 'bg-green-500'}`}
                                            style={{ width: `${Math.min(lossRate, 100)}%` }}
                                        />
                                    </div>
                                </div>

                                <div className="pt-6 border-t border-stone-800">
                                    <p className="text-stone-400 text-sm mb-1">{t('roasting.estCostPrice')}</p>
                                    <div className="flex items-end gap-2">
                                        <span className="text-3xl font-bold text-amber-400">
                                            ₩{Math.round(estimatedCost).toLocaleString()}
                                        </span>
                                        <span className="text-stone-500 mb-1">/ kg</span>
                                    </div>
                                    <p className="text-xs text-stone-500 mt-2">
                                        {t('roasting.basedOnGreenBean').replace('{cost}', selectedGreenBean ? Math.round(selectedGreenBean.avg_cost_price).toLocaleString() : '0')}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <div className="bg-amber-50 p-6 rounded-xl border border-amber-100">
                            <h4 className="font-semibold text-amber-900 mb-2">{t('roasting.roastingTip')}</h4>
                            <p className="text-sm text-amber-800 leading-relaxed">
                                {t('roasting.roastingTipContent')}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
