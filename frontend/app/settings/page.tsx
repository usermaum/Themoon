'use client';

import React, { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Switch } from '@/components/ui/switch';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input'; // Assuming Input component exists
import { Slider } from '@/components/ui/slider'; // Assuming Slider component exists
import { SettingsAPI, SystemConfig } from '@/lib/api/settings';
import {
    Loader2, Save, RotateCcw, Image as ImageIcon, Box, Database,
    ArrowUp, ArrowDown, Plus, FileText, Code as CodeIcon,
    Truck, User, DollarSign, List as ListIcon, Info, Settings, Trash2
} from 'lucide-react';
import { toast } from '@/hooks/use-toast';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { KeyValueList } from '@/components/settings/key-value-list';
import { Textarea } from '@/components/ui/textarea';

import { MorphingButton } from '@/components/ui/morphing-button';
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
} from "@/components/ui/alert-dialog";

export default function AdminSettingsPage() {
    const [initialConfig, setInitialConfig] = useState<SystemConfig | null>(null);
    const [config, setConfig] = useState<SystemConfig | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [saveStatus, setSaveStatus] = useState<Record<string, 'idle' | 'loading' | 'success'>>({
        imageProcessing: 'idle',
        ocrModel: 'idle',
        ocrPrompt: 'idle'
    });

    useEffect(() => {
        loadConfig();
    }, []);

    const loadConfig = async () => {
        setIsLoading(true);
        try {
            const data = await SettingsAPI.getSystemConfig();
            setInitialConfig(JSON.parse(JSON.stringify(data)));
            setConfig(data);
        } catch (error) {
            console.error("Failed to load config", error);
            toast({ title: "Error", description: "Failed to load system configuration.", variant: "destructive" });
        } finally {
            setIsLoading(false);
        }
    };

    const isSectionDirty = (section: 'imageProcessing' | 'ocrModel' | 'ocrPrompt') => {
        if (!config || !initialConfig) return false;

        switch (section) {
            case 'imageProcessing':
                return JSON.stringify(config.image_processing) !== JSON.stringify(initialConfig.image_processing);
            case 'ocrModel':
                // Compare model_priority
                return JSON.stringify(config.ocr.model_priority) !== JSON.stringify(initialConfig.ocr.model_priority);
            case 'ocrPrompt':
                return JSON.stringify(config.ocr.prompt_structure) !== JSON.stringify(initialConfig.ocr.prompt_structure);
            default:
                return false;
        }
    };

    const handleSectionSave = async (section: 'imageProcessing' | 'ocrModel' | 'ocrPrompt') => {
        if (!config) return;

        setSaveStatus(prev => ({ ...prev, [section]: 'loading' }));
        try {
            await SettingsAPI.updateSystemConfig(config);
            toast({ title: "Success", description: "Settings saved successfully." });

            // Update initial state for this section
            setInitialConfig(JSON.parse(JSON.stringify(config)));

            setSaveStatus(prev => ({ ...prev, [section]: 'success' }));
            setTimeout(() => {
                setSaveStatus(prev => ({ ...prev, [section]: 'idle' }));
            }, 2000);
        } catch (error) {
            console.error(`Failed to save ${section}`, error);
            toast({ title: "Error", description: "Failed to save configuration.", variant: "destructive" });
            setSaveStatus(prev => ({ ...prev, [section]: 'idle' }));
        }
    };

    // Helper to update Image Processing Config
    const updateImgProc = (key: keyof SystemConfig['image_processing']['preprocess_for_ocr'], value: any) => {
        if (!config) return;
        setConfig({
            ...config,
            image_processing: {
                ...config.image_processing,
                preprocess_for_ocr: {
                    ...config.image_processing.preprocess_for_ocr,
                    [key]: value
                }
            }
        });
    };

    // Helper to update OCR Prompt Structure
    // Since prompt_structure is loosely typed in frontend interface as just objects, 
    // we assume it matches the backend Pydantic model structure.
    const updatePromptStruct = (section: string, newItems: Record<string, string>) => {
        if (!config) return;

        // Deep clone to avoid mutation issues
        const newConfig = JSON.parse(JSON.stringify(config));

        if (section === 'items') {
            // For items, we update the first element of the array template
            if (newConfig.ocr.prompt_structure.items && newConfig.ocr.prompt_structure.items.length > 0) {
                newConfig.ocr.prompt_structure.items[0] = newItems;
            }
        } else {
            // For standard dict sections
            // @ts-ignore - dynamic access to prompt_structure fields
            newConfig.ocr.prompt_structure[section] = newItems;
        }

        setConfig(newConfig);
    };

    // Helper to update Model Priority
    const moveModel = (index: number, direction: 'up' | 'down') => {
        if (!config) return;
        const newPriority = [...config.ocr.model_priority];
        if (direction === 'up' && index > 0) {
            [newPriority[index], newPriority[index - 1]] = [newPriority[index - 1], newPriority[index]];
        } else if (direction === 'down' && index < newPriority.length - 1) {
            [newPriority[index], newPriority[index + 1]] = [newPriority[index + 1], newPriority[index]];
        }
        setConfig({
            ...config,
            ocr: {
                ...config.ocr,
                model_priority: newPriority
            }
        });
    };

    // Helper to add a new model
    const [newModelName, setNewModelName] = useState('');
    const addModel = () => {
        if (!config || !newModelName.trim()) return;
        setConfig({
            ...config,
            ocr: {
                ...config.ocr,
                model_priority: [...config.ocr.model_priority, newModelName.trim()]
            }
        });
        setNewModelName('');
    };

    // Helper to remove a model
    const removeModel = (index: number) => {
        if (!config) return;
        const newPriority = config.ocr.model_priority.filter((_, i) => i !== index);
        setConfig({
            ...config,
            ocr: {
                ...config.ocr,
                model_priority: newPriority
            }
        });
    };

    // RAW JSON Editor State
    const [isJsonMode, setIsJsonMode] = useState(false);
    const [jsonText, setJsonText] = useState('');

    const toggleJsonMode = () => {
        if (!config) return;

        if (!isJsonMode) {
            // Enter JSON mode: Load current config into text
            setJsonText(JSON.stringify(config.ocr.prompt_structure, null, 2));
        }
        setIsJsonMode(!isJsonMode);
    };

    const applyJsonChanges = () => {
        if (!config) return;
        try {
            const parsed = JSON.parse(jsonText);
            setConfig({
                ...config,
                ocr: {
                    ...config.ocr,
                    prompt_structure: parsed
                }
            });
            toast({ title: "Success", description: "JSON structure applied. Don't forget to Save Changes." });
            setIsJsonMode(false);
        } catch (e) {
            toast({ title: "Invalid JSON", description: "Please check your JSON syntax.", variant: "destructive" });
        }
    };


    if (isLoading) {
        return (
            <div className="flex h-screen items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-latte-600" />
            </div>
        );
    }

    if (!config) return <div className="p-8 text-center text-red-500">Failed to load configuration.</div>;

    const imgConfig = config.image_processing.preprocess_for_ocr;
    const promptConfig = config.ocr.prompt_structure as any; // Cast to any for easier UI mapping


    return (
        <div className="bg-transparent font-sans">
            <main className="space-y-8">

                <div className="flex justify-end items-center gap-2">
                    <Button
                        variant="outline"
                        onClick={loadConfig}
                        className="bg-white hover:bg-latte-100 rounded-xl px-6 border-latte-200 text-latte-600 h-10"
                    >
                        <RotateCcw className="w-4 h-4 mr-2" /> 모든 설정 초기화
                    </Button>
                </div>

                {/* Group 1: Image Processing */}
                <Card className="bg-white border-latte-100 shadow-sm overflow-hidden rounded-[1em]">
                    <CardHeader className="bg-latte-50/50 border-b border-latte-100 pb-4">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <ImageIcon className="text-latte-600" />
                                <CardTitle className="text-lg font-bold text-latte-800">이미지 보정 설정</CardTitle>
                            </div>
                            <MorphingButton
                                status={saveStatus.imageProcessing}
                                idleText="설정 저장"
                                icon={Save}
                                onClick={() => handleSectionSave('imageProcessing')}
                                disabled={!isSectionDirty('imageProcessing')}
                                className="h-9 rounded-xl"
                            />
                        </div>
                        <CardDescription>OCR 인식률을 높이기 위해 이미지의 노이즈를 제거하고 선명도를 조절합니다.</CardDescription>
                    </CardHeader>
                    <CardContent className="p-6 space-y-6">
                        <div className="flex items-center justify-between group">
                            <div className="space-y-0.5">
                                <Label className="text-base text-latte-800">기울기 보정 (Auto-Deskew)</Label>
                                <p className="text-sm text-latte-500">이미지의 수평을 자동으로 맞춥니다.</p>
                            </div>
                            <Switch
                                checked={imgConfig.auto_rotate}
                                onCheckedChange={(c) => updateImgProc('auto_rotate', c)}
                                className="data-[state=checked]:bg-emerald-500 data-[state=unchecked]:bg-latte-200"
                            />
                        </div>

                        <div className="flex items-center justify-between group">
                            <div className="space-y-0.5">
                                <Label className="text-base text-latte-800">흑백 변환 (Grayscale)</Label>
                                <p className="text-sm text-latte-500">배경색을 제거하여 텍스트 가독성을 높입니다.</p>
                            </div>
                            <Switch
                                checked={imgConfig.to_grayscale}
                                onCheckedChange={(c) => updateImgProc('to_grayscale', c)}
                                className="data-[state=checked]:bg-emerald-500 data-[state=unchecked]:bg-latte-200"
                            />
                        </div>

                        <div className="space-y-4">
                            <div className="flex items-center justify-between group">
                                <div className="space-y-0.5">
                                    <Label className="text-base text-latte-800">대조도 강화 (Enhance Contrast)</Label>
                                    <p className="text-sm text-latte-500">배경과 글자의 대비를 높여 흐린 글자를 선명하게 만듭니다.</p>
                                </div>
                                <Switch
                                    checked={imgConfig.enhance_contrast}
                                    onCheckedChange={(c) => updateImgProc('enhance_contrast', c)}
                                    className="data-[state=checked]:bg-emerald-500 data-[state=unchecked]:bg-latte-200"
                                />
                            </div>
                            {imgConfig.enhance_contrast && (
                                <div className="pl-4 border-l-2 border-latte-200 animate-in slide-in-from-left-2">
                                    <Label className="mb-2 block text-sm font-medium text-latte-600">Contrast Factor: {imgConfig.contrast_factor}</Label>
                                    <div className="flex items-center gap-4">
                                        <span className="text-xs text-latte-400 font-mono">1.0</span>
                                        <Slider
                                            defaultValue={[imgConfig.contrast_factor]}
                                            max={3.0}
                                            min={1.0}
                                            step={0.1}
                                            onValueChange={(v) => updateImgProc('contrast_factor', v[0])}
                                            className="grow"
                                        />
                                        <span className="text-xs text-latte-400 font-mono">3.0</span>
                                    </div>
                                </div>
                            )}
                        </div>

                        <div className="space-y-4">
                            <div className="flex items-center justify-between group">
                                <div className="space-y-0.5">
                                    <Label className="text-base text-latte-800">노이스 제거 (Remove Noise)</Label>
                                    <p className="text-sm text-latte-500">점박이 노이즈를 제거하여 깨끗한 상태로 만듭니다.</p>
                                </div>
                                <Switch
                                    checked={imgConfig.remove_noise}
                                    onCheckedChange={(c) => updateImgProc('remove_noise', c)}
                                    className="data-[state=checked]:bg-emerald-500 data-[state=unchecked]:bg-latte-200"
                                />
                            </div>
                            {imgConfig.remove_noise && (
                                <div className="pl-4 border-l-2 border-latte-200 animate-in slide-in-from-left-2">
                                    <Label className="mb-2 block text-sm font-medium text-latte-600">Filter Size: {imgConfig.median_filter_size}px (홀수만 가능)</Label>
                                    <div className="flex items-center gap-4">
                                        <span className="text-xs text-latte-400 font-mono">3</span>
                                        <Slider
                                            defaultValue={[imgConfig.median_filter_size]}
                                            max={9}
                                            min={3}
                                            step={2}
                                            onValueChange={(v) => updateImgProc('median_filter_size', v[0])}
                                            className="grow"
                                        />
                                        <span className="text-xs text-latte-400 font-mono">9</span>
                                    </div>
                                </div>
                            )}
                        </div>

                        <div className="space-y-4">
                            <div className="flex items-center justify-between group">
                                <div className="space-y-0.5">
                                    <Label className="text-base text-latte-800">샤프닝 (Sharpen Text)</Label>
                                    <p className="text-sm text-latte-500">글자의 테두리를 날카롭게 다듬습니다.</p>
                                </div>
                                <Switch
                                    checked={imgConfig.enhance_sharpness}
                                    onCheckedChange={(c) => updateImgProc('enhance_sharpness', c)}
                                    className="data-[state=checked]:bg-emerald-500 data-[state=unchecked]:bg-latte-200"
                                />
                            </div>
                            {imgConfig.enhance_sharpness && (
                                <div className="pl-4 border-l-2 border-latte-200 animate-in slide-in-from-left-2">
                                    <Label className="mb-2 block text-sm font-medium text-latte-600">Sharpness Factor: {imgConfig.sharpness_factor}</Label>
                                    <div className="flex items-center gap-4">
                                        <span className="text-xs text-latte-400 font-mono">1.0</span>
                                        <Slider
                                            defaultValue={[imgConfig.sharpness_factor]}
                                            max={4.0}
                                            min={1.0}
                                            step={0.1}
                                            onValueChange={(v) => updateImgProc('sharpness_factor', v[0])}
                                            className="grow"
                                        />
                                        <span className="text-xs text-latte-400 font-mono">4.0</span>
                                    </div>
                                </div>
                            )}
                        </div>

                        <div className="flex items-center justify-between group">
                            <div className="space-y-0.5">
                                <Label className="text-base text-latte-800">해상도 업스케일링 (Upscale)</Label>
                                <p className="text-sm text-latte-500">저해상도 이미지를 인공지능이 판단하여 2배로 확대합니다.</p>
                            </div>
                            <Switch
                                checked={imgConfig.upscale_image}
                                onCheckedChange={(c) => updateImgProc('upscale_image', c)}
                                className="data-[state=checked]:bg-emerald-500 data-[state=unchecked]:bg-latte-200"
                            />
                        </div>
                    </CardContent>
                </Card>

                {/* Group 2: OCR Settings */}
                <Card className="bg-white border-latte-100 shadow-sm overflow-hidden rounded-[1em]">
                    <CardHeader className="bg-latte-50/50 border-b border-latte-100 pb-4">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <Box className="text-latte-600" />
                                <CardTitle className="text-lg font-bold text-latte-800">OCR 엔진 우선순위</CardTitle>
                            </div>
                            <MorphingButton
                                status={saveStatus.ocrModel}
                                idleText="순차 실행 설정 저장"
                                icon={Save}
                                onClick={() => handleSectionSave('ocrModel')}
                                disabled={!isSectionDirty('ocrModel')}
                                className="h-9 rounded-xl"
                            />
                        </div>
                        <CardDescription>
                            텍스트 추출에 사용할 인공지능 모델의 우선순위를 정합니다.
                            상위 모델이 실패할 경우 다음 순서의 모델이 자동 실행됩니다.
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="p-6">
                        <div className="bg-latte-50 rounded-xl border border-latte-200 divide-y divide-latte-200 mb-4 overflow-hidden">
                            {config.ocr.model_priority.map((model, index) => (
                                <div key={model} className="flex items-center justify-between p-3 bg-white hover:bg-latte-50 transition-colors">
                                    <div className="flex items-center gap-3">
                                        <span className="flex items-center justify-center w-6 h-6 rounded-full bg-latte-100 text-xs font-bold text-latte-600">
                                            {index + 1}
                                        </span>
                                        <span className="font-mono text-sm font-medium text-latte-800">{model}</span>
                                    </div>
                                    <div className="flex gap-1 items-center">
                                        <Button
                                            size="sm"
                                            variant="ghost"
                                            disabled={index === 0}
                                            onClick={() => moveModel(index, 'up')}
                                            className="h-8 w-8 p-0"
                                        >
                                            <ArrowUp className="w-4 h-4" />
                                        </Button>
                                        <Button
                                            size="sm"
                                            variant="ghost"
                                            disabled={index === config.ocr.model_priority.length - 1}
                                            onClick={() => moveModel(index, 'down')}
                                            className="h-8 w-8 p-0"
                                        >
                                            <ArrowDown className="w-4 h-4" />
                                        </Button>
                                        <div className="w-px h-4 bg-latte-200 mx-1"></div>
                                        <Button
                                            size="sm"
                                            variant="ghost"
                                            onClick={() => removeModel(index)}
                                            className="h-8 w-8 p-0 text-red-400 hover:text-red-600 hover:bg-red-50"
                                        >
                                            <Trash2 className="w-4 h-4" />
                                        </Button>
                                    </div>
                                </div>
                            ))}
                        </div>

                        <div className="flex items-center gap-2">
                            <Input
                                placeholder="모델 이름 추가 (예: gpt-4o)"
                                value={newModelName}
                                onChange={(e) => setNewModelName(e.target.value)}
                                className="font-mono text-sm rounded-xl h-10"
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter') addModel();
                                }}
                            />
                            <Button
                                variant="outline"
                                onClick={addModel}
                                disabled={!newModelName.trim()}
                                className="rounded-xl border-latte-200 hover:bg-latte-50 h-10 px-6"
                            >
                                <Plus className="w-4 h-4 mr-2" /> 추가
                            </Button>
                        </div>

                        {config.ocr._model_priority_rule && (
                            <div className="mt-4 p-3 bg-amber-50 text-amber-800 text-xs rounded border border-amber-200">
                                <strong>System Note:</strong> {config.ocr._model_priority_rule}
                            </div>
                        )}
                    </CardContent>
                </Card>

                {/* Group 3: OCR Prompt Configuration */}
                <Card className="bg-white border-latte-100 shadow-sm overflow-hidden rounded-[1em]">
                    <CardHeader className="bg-latte-50/50 border-b border-latte-100 pb-4">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <FileText className="text-latte-600" />
                                <CardTitle className="text-lg font-bold text-latte-800">추출 프롬프트 설정</CardTitle>
                            </div>
                            <div className="flex items-center gap-2">
                                <Button
                                    variant={isJsonMode ? "secondary" : "ghost"}
                                    size="sm"
                                    onClick={toggleJsonMode}
                                    className={cn(
                                        "rounded-xl h-9",
                                        isJsonMode ? "bg-latte-200 text-latte-900" : "text-latte-500 hover:text-latte-900"
                                    )}
                                >
                                    <CodeIcon className="w-4 h-4 mr-2" />
                                    {isJsonMode ? "비주얼 에디터" : "JSON 편집"}
                                </Button>
                                <MorphingButton
                                    status={saveStatus.ocrPrompt}
                                    idleText="프롬프트 저장"
                                    icon={Save}
                                    onClick={() => handleSectionSave('ocrPrompt')}
                                    disabled={!isSectionDirty('ocrPrompt')}
                                    className="h-9 rounded-xl"
                                />
                            </div>
                        </div>
                        <CardDescription>
                            인공지능이 영수증에서 어떤 정보를 어떻게 추출할지 정의합니다.
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="p-6">
                        {isJsonMode ? (
                            <div className="space-y-4 animate-in fade-in zoom-in-95 duration-200">
                                <div className="p-4 bg-latte-50 rounded-xl border border-latte-200">
                                    <Label className="mb-2 block text-latte-700">JSON 데이터 가이드</Label>
                                    <Textarea
                                        value={jsonText}
                                        onChange={(e) => setJsonText(e.target.value)}
                                        className="font-mono text-sm h-[400px] bg-white rounded-xl border-latte-200"
                                        spellCheck={false}
                                    />
                                    <div className="flex justify-end gap-2 mt-4">
                                        <Button
                                            variant="outline"
                                            onClick={toggleJsonMode}
                                            className="h-10 px-6 rounded-xl border-latte-200 text-latte-600 hover:bg-latte-50"
                                        >
                                            취소
                                        </Button>
                                        <AlertDialog>
                                            <AlertDialogTrigger asChild>
                                                <MorphingButton
                                                    status={saveStatus.ocrPrompt}
                                                    idleText="적용"
                                                    icon={CodeIcon}
                                                    onClick={() => { }}
                                                    className="bg-latte-900 hover:bg-latte-800 text-white h-10 px-8 rounded-xl"
                                                />
                                            </AlertDialogTrigger>
                                            <AlertDialogContent>
                                                <AlertDialogHeader>
                                                    <AlertDialogTitle>변경된 내용을 저장합니까?</AlertDialogTitle>
                                                    <AlertDialogDescription>
                                                        현재 작성된 JSON 설정으로 프롬프트를 업데이트합니다.
                                                        <br /><br />
                                                        <span className="font-bold text-amber-600">
                                                            ⚠️ 주의: 잘못된 JSON 형식은 OCR 추출 오류를 발생시킬 수 있습니다.
                                                        </span>
                                                    </AlertDialogDescription>
                                                </AlertDialogHeader>
                                                <AlertDialogFooter>
                                                    <AlertDialogCancel>취소</AlertDialogCancel>
                                                    <AlertDialogAction onClick={applyJsonChanges} className="bg-latte-900 hover:bg-latte-800 text-white">
                                                        저장 실행
                                                    </AlertDialogAction>
                                                </AlertDialogFooter>
                                            </AlertDialogContent>
                                        </AlertDialog>
                                    </div>
                                </div>
                                <div className="text-xs text-amber-600 bg-amber-50 p-3 rounded-lg border border-amber-200 leading-relaxed">
                                    <strong>⚠️ 주의:</strong> 항목명을 직접 변경하면 화면의 탭 구성이 손상될 수 있습니다. 항목 설명(Value) 위주로 수정해 주세요.
                                </div>
                            </div>
                        ) : (
                            <Tabs defaultValue="document_info" className="w-full">
                                <TabsList className="grid w-full grid-cols-3 lg:grid-cols-6 mb-4 bg-latte-100 p-1 h-auto rounded-xl">
                                    <TabsTrigger value="document_info" title="기본 정보" className="data-[state=active]:bg-white data-[state=active]:text-latte-900 data-[state=active]:shadow-sm py-2 rounded-lg transition-all"><FileText className="w-4 h-4 lg:mr-2" /><span className="hidden lg:inline text-xs">문서정보</span></TabsTrigger>
                                    <TabsTrigger value="supplier" title="공급자" className="data-[state=active]:bg-white data-[state=active]:text-latte-900 data-[state=active]:shadow-sm py-2 rounded-lg transition-all"><Truck className="w-4 h-4 lg:mr-2" /><span className="hidden lg:inline text-xs">공급자</span></TabsTrigger>
                                    <TabsTrigger value="receiver" title="수령인" className="data-[state=active]:bg-white data-[state=active]:text-latte-900 data-[state=active]:shadow-sm py-2 rounded-lg transition-all"><User className="w-4 h-4 lg:mr-2" /><span className="hidden lg:inline text-xs">수령인</span></TabsTrigger>
                                    <TabsTrigger value="amounts" title="금액" className="data-[state=active]:bg-white data-[state=active]:text-latte-900 data-[state=active]:shadow-sm py-2 rounded-lg transition-all"><DollarSign className="w-4 h-4 lg:mr-2" /><span className="hidden lg:inline text-xs">금액</span></TabsTrigger>
                                    <TabsTrigger value="items" title="품목 리스트" className="data-[state=active]:bg-white data-[state=active]:text-latte-900 data-[state=active]:shadow-sm py-2 rounded-lg transition-all"><ListIcon className="w-4 h-4 lg:mr-2" /><span className="hidden lg:inline text-xs">품목</span></TabsTrigger>
                                    <TabsTrigger value="additional_info" title="기타 정보" className="data-[state=active]:bg-white data-[state=active]:text-latte-900 data-[state=active]:shadow-sm py-2 rounded-lg transition-all"><Info className="w-4 h-4 lg:mr-2" /><span className="hidden lg:inline text-xs">기타</span></TabsTrigger>
                                </TabsList>

                                <TabsContent value="document_info">
                                    <KeyValueList
                                        items={promptConfig.document_info}
                                        onChange={(newItems) => updatePromptStruct('document_info', newItems)}
                                        keyLabel="필드명"
                                        valueLabel="추출 가이드 (인공지능에게 전달할 설명)"
                                    />
                                </TabsContent>
                                <TabsContent value="supplier">
                                    <KeyValueList
                                        items={promptConfig.supplier}
                                        onChange={(newItems) => updatePromptStruct('supplier', newItems)}
                                        keyLabel="필드명"
                                        valueLabel="추출 가이드"
                                    />
                                </TabsContent>
                                <TabsContent value="receiver">
                                    <KeyValueList
                                        items={promptConfig.receiver}
                                        onChange={(newItems) => updatePromptStruct('receiver', newItems)}
                                        keyLabel="필드명"
                                        valueLabel="추출 가이드"
                                    />
                                </TabsContent>
                                <TabsContent value="amounts">
                                    <KeyValueList
                                        items={promptConfig.amounts}
                                        onChange={(newItems) => updatePromptStruct('amounts', newItems)}
                                        keyLabel="필드명"
                                        valueLabel="추출 가이드"
                                    />
                                </TabsContent>
                                <TabsContent value="items">
                                    <div className="mb-4 text-xs text-latte-600 bg-latte-50 p-3 rounded-lg border border-latte-100">
                                        <strong>품목 템플릿:</strong> 영수증의 품목 리스트를 추출할 때 사용할 개별 항목 구조를 관리합니다.
                                    </div>
                                    <KeyValueList
                                        items={promptConfig.items && promptConfig.items[0] ? promptConfig.items[0] : {}}
                                        onChange={(newItems) => updatePromptStruct('items', newItems)}
                                        keyLabel="필드명"
                                        valueLabel="추출 가이드"
                                    />
                                </TabsContent>
                                <TabsContent value="additional_info">
                                    <KeyValueList
                                        items={promptConfig.additional_info}
                                        onChange={(newItems) => updatePromptStruct('additional_info', newItems)}
                                        keyLabel="필드명"
                                        valueLabel="추출 가이드"
                                    />
                                </TabsContent>
                            </Tabs>
                        )}
                    </CardContent>
                </Card>
            </main>
        </div>
    );
}
