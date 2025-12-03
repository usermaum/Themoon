"use client";

import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Upload, FileText, Check, AlertCircle, Loader2, Plus, Trash2, ChevronsUpDown, FileInput } from 'lucide-react';
import { cn } from "@/lib/utils"
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

// API Base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface InboundItem {
    name: string;
    quantity: number;
    unit_price: number;
    total_price: number;
    matched_bean_id?: number;
    matched_bean_name?: string;
    match_score?: number;
}

interface OCRResult {
    supplier_name: string;
    invoice_number: string;
    date: string;
    total_amount: number;
    items: InboundItem[];
    temp_file_path: string;
}

interface Bean {
    id: number;
    name: string;
    origin: string;
    type: string;
}

export default function InboundPage() {
    const { t } = useLanguage();
    const [file, setFile] = useState<File | null>(null);
    const [previewUrl, setPreviewUrl] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [ocrResult, setOcrResult] = useState<OCRResult | null>(null);
    const [error, setError] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Bean Matching State
    const [beans, setBeans] = useState<Bean[]>([]);
    const [openComboboxes, setOpenComboboxes] = useState<{ [key: number]: boolean }>({});

    useEffect(() => {
        // Fetch beans for matching
        const fetchBeans = async () => {
            try {
                const response = await axios.get(`${API_BASE_URL}/beans?size=100`);
                setBeans(response.data.items);
            } catch (err) {
                console.error("Failed to fetch beans", err);
            }
        };
        fetchBeans();
    }, []);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const selectedFile = e.target.files[0];
            setFile(selectedFile);
            setPreviewUrl(URL.createObjectURL(selectedFile));
            setOcrResult(null);
            setError(null);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setIsLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(`${API_BASE_URL}/inbound/upload`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setOcrResult(response.data);
        } catch (err: any) {
            console.error("Upload failed", err);
            setError(err.response?.data?.detail || "Failed to upload and process image.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleItemChange = (index: number, field: keyof InboundItem, value: any) => {
        if (!ocrResult) return;

        const newItems = [...ocrResult.items];
        newItems[index] = { ...newItems[index], [field]: value };
        setOcrResult({ ...ocrResult, items: newItems });
    };

    const handleAddItem = () => {
        if (!ocrResult) return;
        const newItem: InboundItem = { name: "", quantity: 0, unit_price: 0, total_price: 0 };
        setOcrResult({ ...ocrResult, items: [...ocrResult.items, newItem] });
    };

    const handleRemoveItem = (index: number) => {
        if (!ocrResult) return;
        const newItems = ocrResult.items.filter((_, i) => i !== index);
        setOcrResult({ ...ocrResult, items: newItems });
    };

    const toggleCombobox = (index: number, isOpen: boolean) => {
        setOpenComboboxes(prev => ({ ...prev, [index]: isOpen }));
    };

    const handleConfirm = async () => {
        if (!ocrResult) return;

        setIsLoading(true);
        try {
            await axios.post(`${API_BASE_URL}/inbound/confirm`, ocrResult);
            alert("Inbound transaction confirmed successfully!");
            // Reset state
            setFile(null);
            setPreviewUrl(null);
            setOcrResult(null);
        } catch (err: any) {
            console.error("Confirmation failed", err);
            setError(err.response?.data?.detail || "Failed to confirm transaction.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div>
            <PageHero
                title={t('inbound.title')}
                description={t('inbound.description')}
                icon={<FileInput className="w-10 h-10" />}
                backgroundImage="/images/inbound-hero-placeholder.jpg"
            />
            <div className="p-8 max-w-7xl mx-auto">

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Left Column: Upload & Preview */}
                    <div className="space-y-6">
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-stone-200">
                            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                                <Upload className="w-5 h-5" /> {t('inbound.uploadReceipt')}
                            </h2>

                            <div
                                className="border-2 border-dashed border-stone-300 rounded-lg p-8 text-center hover:bg-stone-50 transition-colors cursor-pointer"
                                onClick={() => fileInputRef.current?.click()}
                            >
                                <input
                                    type="file"
                                    ref={fileInputRef}
                                    onChange={handleFileChange}
                                    className="hidden"
                                    accept="image/*"
                                />
                                {previewUrl ? (
                                    <img src={previewUrl} alt="Preview" className="max-h-96 mx-auto rounded shadow-sm" />
                                ) : (
                                    <div className="text-stone-500">
                                        <FileText className="w-12 h-12 mx-auto mb-2 opacity-50" />
                                        <p>{t('inbound.clickToUpload')}</p>
                                        <p className="text-sm opacity-70">{t('inbound.fileType')}</p>
                                    </div>
                                )}
                            </div>

                            {file && !ocrResult && (
                                <button
                                    onClick={handleUpload}
                                    disabled={isLoading}
                                    className="w-full mt-4 bg-amber-600 hover:bg-amber-700 text-white py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
                                >
                                    {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Upload className="w-5 h-5" />}
                                    {isLoading ? t('inbound.processing') : t('inbound.analyzeReceipt')}
                                </button>
                            )}
                        </div>
                    </div>

                    {/* Right Column: OCR Results */}
                    <div className="space-y-6">
                        {error && (
                            <div className="bg-red-50 text-red-600 p-4 rounded-lg flex items-center gap-2 border border-red-200">
                                <AlertCircle className="w-5 h-5" />
                                {error}
                            </div>
                        )}

                        {ocrResult && (
                            <div className="bg-white p-6 rounded-xl shadow-sm border border-stone-200">
                                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                                    <Check className="w-5 h-5 text-green-600" /> {t('inbound.verifiedData')}
                                </h2>

                                <div className="grid grid-cols-2 gap-4 mb-6">
                                    <div>
                                        <label className="block text-sm font-medium text-stone-600 mb-1">{t('inbound.supplier')}</label>
                                        <input
                                            type="text"
                                            value={ocrResult.supplier_name || ''}
                                            onChange={(e) => setOcrResult({ ...ocrResult, supplier_name: e.target.value })}
                                            className="w-full p-2 border rounded focus:ring-2 focus:ring-amber-500 outline-none"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-stone-600 mb-1">{t('inbound.invoiceNo')}</label>
                                        <input
                                            type="text"
                                            value={ocrResult.invoice_number || ''}
                                            onChange={(e) => setOcrResult({ ...ocrResult, invoice_number: e.target.value })}
                                            className="w-full p-2 border rounded focus:ring-2 focus:ring-amber-500 outline-none"
                                            placeholder="Optional"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-stone-600 mb-1">{t('inbound.date')}</label>
                                        <input
                                            type="date"
                                            value={ocrResult.date || ''}
                                            onChange={(e) => setOcrResult({ ...ocrResult, date: e.target.value })}
                                            className="w-full p-2 border rounded focus:ring-2 focus:ring-amber-500 outline-none"
                                        />
                                    </div>
                                </div>

                                <div className="mb-4">
                                    <div className="flex justify-between items-center mb-2">
                                        <h3 className="font-medium text-stone-700">{t('inbound.items')}</h3>
                                        <button onClick={handleAddItem} className="text-sm text-amber-600 hover:text-amber-700 flex items-center gap-1">
                                            <Plus className="w-4 h-4" /> {t('inbound.addItem')}
                                        </button>
                                    </div>

                                    <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2">
                                        {ocrResult.items.map((item, idx) => (
                                            <div key={idx} className="p-3 bg-stone-50 rounded-lg border border-stone-200 relative group">
                                                <button
                                                    onClick={() => handleRemoveItem(idx)}
                                                    className="absolute top-2 right-2 text-stone-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
                                                >
                                                    <Trash2 className="w-4 h-4" />
                                                </button>
                                                <div className="grid grid-cols-12 gap-2">
                                                    <div className="col-span-12 sm:col-span-6">
                                                        <label className="text-xs text-stone-500">{t('inbound.itemName')}</label>
                                                        <input
                                                            type="text"
                                                            value={item.name}
                                                            onChange={(e) => handleItemChange(idx, 'name', e.target.value)}
                                                            className="w-full p-1 border rounded text-sm"
                                                        />
                                                    </div>
                                                    <div className="col-span-4 sm:col-span-2">
                                                        <label className="text-xs text-stone-500">{t('inbound.qty')}</label>
                                                        <input
                                                            type="number"
                                                            value={item.quantity}
                                                            onChange={(e) => handleItemChange(idx, 'quantity', parseFloat(e.target.value))}
                                                            className="w-full p-1 border rounded text-sm"
                                                        />
                                                    </div>
                                                    <div className="col-span-4 sm:col-span-2">
                                                        <label className="text-xs text-stone-500">{t('inbound.unitPrice')}</label>
                                                        <input
                                                            type="number"
                                                            value={item.unit_price}
                                                            onChange={(e) => handleItemChange(idx, 'unit_price', parseFloat(e.target.value))}
                                                            className="w-full p-1 border rounded text-sm"
                                                        />
                                                    </div>
                                                    <div className="col-span-4 sm:col-span-2">
                                                        <label className="text-xs text-stone-500">{t('inbound.total')}</label>
                                                        <input
                                                            type="number"
                                                            value={item.total_price}
                                                            readOnly
                                                            className="w-full p-1 border rounded text-sm bg-stone-100 text-stone-500"
                                                        />
                                                    </div>
                                                </div>
                                                {/* Bean Matching with Combobox */}
                                                <div className="mt-2">
                                                    <div className="flex justify-between items-center mb-1">
                                                        <label className="text-xs text-stone-500 block">{t('inbound.matchedBean')}</label>
                                                        {item.match_score && item.match_score > 0 && (
                                                            <span className={cn(
                                                                "text-[10px] px-1.5 py-0.5 rounded-full",
                                                                item.match_score >= 80 ? "bg-green-100 text-green-700" :
                                                                    item.match_score >= 60 ? "bg-yellow-100 text-yellow-700" :
                                                                        "bg-red-100 text-red-700"
                                                            )}>
                                                                {t('inbound.matchScore').replace('{score}', item.match_score.toString())}
                                                            </span>
                                                        )}
                                                    </div>
                                                    <Popover open={openComboboxes[idx]} onOpenChange={(isOpen) => toggleCombobox(idx, isOpen)}>
                                                        <PopoverTrigger asChild>
                                                            <Button
                                                                variant="outline"
                                                                role="combobox"
                                                                aria-expanded={openComboboxes[idx]}
                                                                className="w-full justify-between h-8 text-sm font-normal"
                                                            >
                                                                {item.matched_bean_id
                                                                    ? beans.find((bean) => bean.id === item.matched_bean_id)?.name
                                                                    : t('inbound.selectBean')}
                                                                <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                                                            </Button>
                                                        </PopoverTrigger>
                                                        <PopoverContent className="w-[300px] p-0">
                                                            <Command>
                                                                <CommandInput placeholder="Search bean..." />
                                                                <CommandList>
                                                                    <CommandEmpty>No bean found.</CommandEmpty>
                                                                    <CommandGroup>
                                                                        {beans.map((bean) => (
                                                                            <CommandItem
                                                                                key={bean.id}
                                                                                value={bean.name}
                                                                                onSelect={() => {
                                                                                    handleItemChange(idx, 'matched_bean_id', bean.id);
                                                                                    toggleCombobox(idx, false);
                                                                                }}
                                                                            >
                                                                                <Check
                                                                                    className={cn(
                                                                                        "mr-2 h-4 w-4",
                                                                                        item.matched_bean_id === bean.id ? "opacity-100" : "opacity-0"
                                                                                    )}
                                                                                />
                                                                                {bean.name} <span className="text-xs text-stone-400 ml-2">({bean.origin})</span>
                                                                            </CommandItem>
                                                                        ))}
                                                                    </CommandGroup>
                                                                </CommandList>
                                                            </Command>
                                                        </PopoverContent>
                                                    </Popover>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                <div className="flex justify-between items-center pt-4 border-t border-stone-200">
                                    <div className="text-lg font-bold text-stone-800">
                                        {t('inbound.total')}: {ocrResult.items.reduce((sum, item) => sum + (item.quantity * item.unit_price), 0).toLocaleString()}
                                    </div>
                                    <button
                                        onClick={handleConfirm}
                                        disabled={isLoading}
                                        className="bg-green-600 hover:bg-green-700 text-white py-2 px-6 rounded-lg font-medium transition-colors flex items-center gap-2"
                                    >
                                        {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Check className="w-5 h-5" />}
                                        {t('inbound.confirmInbound')}
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
