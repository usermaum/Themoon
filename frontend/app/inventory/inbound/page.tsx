"use client"

import { useState, useCallback, useEffect } from "react"
import { useForm, useFieldArray } from "react-hook-form"
import { useRouter } from "next/navigation"
import { Upload, Link as LinkIcon, Clipboard, Image as ImageIcon, Loader2, Save, AlertCircle, CheckCircle2, FileText, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { BeanAPI } from "@/lib/api"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Separator } from "@/components/ui/separator"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { useToast } from "@/hooks/use-toast"
import Image from "next/image"

// Types
interface InboundItem {
    bean_name: string
    quantity: number
    unit_price: number
    amount: number
}

interface InboundForm {
    supplier_name: string
    supplier_phone?: string
    contact_phone?: string
    supplier_email?: string
    contract_number?: string
    receiver_name?: string
    invoice_date: string
    total_amount: number
    items: InboundItem[]
    drive_link?: string
    notes?: string
}

export default function InboundPage() {
    const router = useRouter()
    const [activeTab, setActiveTab] = useState("file")
    const [selectedFile, setSelectedFile] = useState<File | null>(null)
    const [pastedImage, setPastedImage] = useState<File | null>(null)
    const [urlInput, setUrlInput] = useState("")
    const [previewUrl, setPreviewUrl] = useState<string | null>(null)
    const [isAnalyzing, setIsAnalyzing] = useState(false)
    const [driveLink, setDriveLink] = useState<string | null>(null)

    const [ocrResult, setOcrResult] = useState<any>(null) // Temporary for debugging
    const [duplicateStatus, setDuplicateStatus] = useState<{ status: 'idle' | 'checking' | 'duplicate' | 'available', message: string }>({ status: 'idle', message: '' })
    const [itemStatus, setItemStatus] = useState<Record<string, { status: string, bean_id: number | null }>>({})

    const { toast } = useToast()

    const { register, control, handleSubmit, setValue, reset, watch } = useForm<InboundForm>({
        defaultValues: {
            items: [{ bean_name: "", quantity: 0, unit_price: 0, amount: 0 }]
        }
    })

    const { fields, append, remove } = useFieldArray({
        control,
        name: "items"
    })

    // Handle File Selection
    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0]
            setSelectedFile(file)
            setPastedImage(null)
            setPreviewUrl(URL.createObjectURL(file))
        }
    }

    // Handle Paste
    const handlePaste = useCallback((e: ClipboardEvent) => {
        const items = e.clipboardData?.items
        if (!items) return

        for (let i = 0; i < items.length; i++) {
            const item = items[i]
            if (item.type.indexOf("image") !== -1) {
                const file = item.getAsFile()
                if (file) {
                    setPastedImage(file)
                    setSelectedFile(null)
                    setPreviewUrl(URL.createObjectURL(file))
                    setActiveTab("clipboard")
                    toast({ title: "이미지 붙여넣기 완료", description: "클립보드 이미지를 가져왔습니다." })
                }
            }
        }
    }, [toast])

    useEffect(() => {
        document.addEventListener("paste", handlePaste as any)
        return () => document.removeEventListener("paste", handlePaste as any)
    }, [handlePaste])

    // Analyze Logic
    const handleAnalyze = async () => {
        setIsAnalyzing(true)
        setOcrResult(null)
        const formData = new FormData()

        if (activeTab === "file" && selectedFile) {
            formData.append("file", selectedFile)
        } else if (activeTab === "clipboard" && pastedImage) {
            formData.append("file", pastedImage)
        } else if (activeTab === "url" && urlInput) {
            formData.append("url", urlInput)
        } else {
            toast({ title: "입력값 없음", description: "이미지나 URL을 입력해주세요.", variant: "destructive" })
            setIsAnalyzing(false)
            return
        }

        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/inbound/analyze`, {
                method: "POST",
                body: formData, // Auto sets Content-Type for multipart if file present
            })

            if (!response.ok) {
                const err = await response.json()
                throw new Error(err.detail || "분석 실패")
            }

            const data = await response.json()
            setOcrResult(data) // Save raw data for debug view

            // Auto-fill form using structured data
            // 계약번호 (우선순위: 구조화된 데이터 > 하위 호환성 필드)
            const contractNum = data.document_info?.contract_number || data.contract_number || ""
            setValue("contract_number", contractNum)

            // Auto-trigger duplicate check
            if (contractNum) {
                checkDuplicate(contractNum)
            }

            // 공급처 정보 (Supplier Information)
            setValue("supplier_name", data.supplier?.name || data.supplier_name || "")
            setValue("supplier_phone", data.supplier?.phone || data.supplier_phone || "")
            setValue("contact_phone", data.supplier?.contact_phone || "")
            setValue("supplier_email", data.supplier?.email || data.supplier_email || "")

            // 공급처 담당자 (공급자의 contact_person 또는 representative)
            // receiver_name 필드를 공급처 담당자로 사용 (폼 구조 유지)
            setValue("receiver_name", data.supplier?.contact_person || data.supplier?.representative || "")

            // 날짜 및 금액
            setValue("invoice_date", data.document_info?.invoice_date || data.invoice_date || "")
            setValue("total_amount", data.amounts?.total_amount || data.total_amount || 0)

            // 품목 정보
            setValue("items", data.items || [])
            setDriveLink(data.drive_link)

            toast({ title: "분석 완료", description: "명세서 내용을 자동으로 입력했습니다." })

            // Check items existence
            if (data.items && data.items.length > 0) {
                const names = data.items.map((i: any) => i.bean_name || "").filter((n: string) => n !== "")
                checkItemsBatch(names)
            }

        } catch (error: any) {
            toast({ title: "오류 발생", description: error.message, variant: "destructive" })
        } finally {
            setIsAnalyzing(false)
        }
    }

    // Check Status Logic
    const checkItemsBatch = async (names: string[]) => {
        console.log("Checking items:", names)
        if (names.length === 0) return
        try {
            const results = await BeanAPI.checkBatch(names)
            console.log("Check results:", results)

            // Functional update to avoid stale state
            setItemStatus(prev => {
                const newStatus: any = { ...prev }
                results.forEach((r: any) => {
                    newStatus[r.input_name] = { status: r.status, bean_id: r.bean_id }
                })
                return newStatus
            })
        } catch (e) {
            console.error("Failed to check items", e)
        }
    }

    // Duplicate Check Logic
    const checkDuplicate = async (contractNumber: string) => {
        if (!contractNumber || contractNumber.trim() === "") {
            setDuplicateStatus({ status: 'idle', message: '' })
            return
        }

        setDuplicateStatus({ status: 'checking', message: '확인 중...' })
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/inbound/check-duplicate/${contractNumber}`)
            if (response.ok) {
                const data = await response.json()
                if (data.exists) {
                    setDuplicateStatus({ status: 'duplicate', message: data.detail })
                } else {
                    setDuplicateStatus({ status: 'available', message: data.detail })
                }
            } else {
                setDuplicateStatus({ status: 'idle', message: '확인 불가' })
            }
        } catch (error) {
            console.error("Duplicate check error:", error)
            setDuplicateStatus({ status: 'idle', message: '확인 불가' })
        }
    }

    // Watch contract number changes for debounce or blur handling
    // Simple approach: Use onBlur on the input


    const onSubmit = async (data: InboundForm) => {
        // Validation
        if (!data.contract_number || data.contract_number.trim() === "") {
            toast({ title: "필수 입력값 누락", description: "계약/주문 번호(Contract No.)는 필수입니다.", variant: "destructive" })
            return
        }
        if (!data.supplier_name || data.supplier_name.trim() === "") {
            toast({ title: "필수 입력값 누락", description: "공급처 정보(상호명)는 필수입니다.", variant: "destructive" })
            return
        }
        if (data.items.length === 0) {
            toast({ title: "필수 입력값 누락", description: "최소 1개 이상의 품목이 필요합니다.", variant: "destructive" })
            return
        }

        try {
            const payload = {
                items: data.items,
                document: {
                    supplier_name: data.supplier_name,
                    contract_number: data.contract_number,
                    supplier_phone: data.supplier_phone,
                    supplier_email: data.supplier_email,
                    receiver_name: data.receiver_name,

                    invoice_date: data.invoice_date,
                    total_amount: data.total_amount,
                    image_url: driveLink, // Using the local link
                    notes: data.notes
                },
                // NEW: Include full OCR data for detailed storage (Option B)
                document_info: ocrResult?.document_info,
                supplier: ocrResult?.supplier,
                receiver: ocrResult?.receiver,
                amounts: ocrResult?.amounts,
                additional_info: ocrResult?.additional_info,
            }

            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/inbound/confirm`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            })

            if (!response.ok) {
                const err = await response.json()
                throw new Error(err.detail || "저장 실패")
            }

            toast({ title: "저장 완료", description: "입고 데이터가 성공적으로 저장되었습니다." })
            // Optional: Reset form or redirect
            // reset()
        } catch (error: any) {
            // Check if it's a duplicate error and show a friendly message
            if (error.message.includes("Duplicate Contract Number") || error.message.includes("이미 등록된")) {
                toast({ title: "저장 실패", description: "이미 등록된 명세서(계약번호)입니다. 중복을 확인해주세요.", variant: "destructive" })
            } else {
                toast({ title: "저장 실패", description: error.message, variant: "destructive" })
            }
        }
    }

    return (
        <div className="container mx-auto p-6 space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">명세서 입고 (Inbound)</h1>
                    <p className="text-muted-foreground">명세서 사진을 업로드하면 자동으로 재고를 등록합니다.</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Left: Input & Preview */}
                <div className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>입력 소스</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                                <TabsList className="grid w-full grid-cols-3">
                                    <TabsTrigger value="file"><Upload className="w-4 h-4 mr-2" /> 파일 업로드</TabsTrigger>
                                    <TabsTrigger value="clipboard"><Clipboard className="w-4 h-4 mr-2" /> 붙여넣기</TabsTrigger>
                                    <TabsTrigger value="url"><LinkIcon className="w-4 h-4 mr-2" /> URL 입력</TabsTrigger>
                                </TabsList>

                                <div className="mt-4 space-y-4">
                                    <TabsContent value="file">
                                        <div className="grid w-full max-w-sm items-center gap-1.5">
                                            <Label htmlFor="picture">명세서 이미지</Label>
                                            <Input id="picture" type="file" accept="image/*" onChange={handleFileChange} />
                                        </div>
                                    </TabsContent>

                                    <TabsContent value="clipboard">
                                        <div className="h-32 border-2 border-dashed rounded-lg flex flex-col items-center justify-center text-muted-foreground bg-muted/50">
                                            <Clipboard className="h-8 w-8 mb-2" />
                                            <p>Ctrl+V를 눌러 이미지를 붙여넣으세요</p>
                                        </div>
                                    </TabsContent>

                                    <TabsContent value="url">
                                        <div className="grid w-full items-center gap-1.5">
                                            <Label htmlFor="url">이미지 URL</Label>
                                            <Input id="url" placeholder="https://..." value={urlInput} onChange={(e) => setUrlInput(e.target.value)} />
                                        </div>
                                    </TabsContent>
                                </div>
                            </Tabs>

                            {previewUrl && (
                                <div className="mt-6 border rounded-lg overflow-hidden relative aspect-video bg-black/5">
                                    <Image src={previewUrl} alt="Preview" fill className="object-contain" />
                                </div>
                            )}

                            <Button
                                className="w-full mt-6"
                                onClick={handleAnalyze}
                                disabled={isAnalyzing || (!selectedFile && !pastedImage && !urlInput)}
                            >
                                {isAnalyzing ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Gemini가 분석 중입니다...
                                    </>
                                ) : (
                                    <>
                                        <ImageIcon className="mr-2 h-4 w-4" /> 명세서 분석 시작 (OCR)
                                    </>
                                )}
                            </Button>
                        </CardContent>
                    </Card>

                    {driveLink && (
                        <Alert>
                            <AlertTitle>이미지 저장됨</AlertTitle>
                            <AlertDescription>
                                이미지가 서버에 저장되었습니다. <a href={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}${driveLink}`} target="_blank" className="underline font-bold">이미지 보기</a>
                            </AlertDescription>
                        </Alert>
                    )}

                    {/* Temporary Debug View with Invoice Button */}
                    {ocrResult && (
                        <Card className="border-blue-400 bg-blue-50/50">
                            <CardHeader className="py-3">
                                <CardTitle className="text-sm font-mono text-blue-800 flex items-center justify-between">
                                    <span className="flex items-center gap-2">
                                        ✅ OCR 분석 완료
                                    </span>
                                    <Button
                                        size="sm"
                                        onClick={() => {
                                            sessionStorage.setItem('ocrResult', JSON.stringify(ocrResult))
                                            router.push('/inbound/invoice')
                                        }}
                                        className="bg-blue-600 hover:bg-blue-700"
                                    >
                                        <FileText className="w-4 h-4 mr-2" />
                                        📄 거래명세서 보기
                                    </Button>
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="py-2 pb-4 space-y-3">
                                <div className="grid grid-cols-2 gap-2 text-sm">
                                    <div className="bg-white p-2 rounded border">
                                        <span className="text-gray-600 text-xs">공급자:</span>
                                        <div className="font-semibold">{ocrResult.supplier?.name || ocrResult.supplier_name || '-'}</div>
                                    </div>
                                    <div className="bg-white p-2 rounded border">
                                        <span className="text-gray-600 text-xs">계약번호:</span>
                                        <div className="font-semibold">{ocrResult.document_info?.contract_number || ocrResult.contract_number || '-'}</div>
                                    </div>
                                    <div className="bg-white p-2 rounded border">
                                        <span className="text-gray-600 text-xs">품목 수:</span>
                                        <div className="font-semibold">{ocrResult.items?.length || 0}개</div>
                                    </div>
                                    <div className="bg-white p-2 rounded border">
                                        <span className="text-gray-600 text-xs">합계:</span>
                                        <div className="font-semibold">{(ocrResult.amounts?.total_amount || ocrResult.total_amount || 0).toLocaleString()}원</div>
                                    </div>
                                </div>
                                <details className="text-xs bg-white p-2 rounded border">
                                    <summary className="cursor-pointer font-semibold text-gray-700">🔍 원본 데이터 보기 (개발자용)</summary>
                                    <pre className="mt-2 p-2 bg-gray-50 rounded overflow-auto max-h-40 font-mono text-xs">
                                        {JSON.stringify(ocrResult, null, 2)}
                                    </pre>
                                </details>
                            </CardContent>
                        </Card>
                    )}
                </div>

                {/* Right: Form */}
                <div className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>입고 상세 정보</CardTitle>
                            <CardDescription>추출된 정보를 확인하고 수정하세요.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <Label className="text-destructive font-bold">계약/주문 번호 (필수)*</Label>
                                        <div className="relative">
                                            <Input
                                                {...register("contract_number")}
                                                placeholder="발주번호 or 문서번호"
                                                className={`bg-muted/10 border-destructive/20 ${duplicateStatus.status === 'duplicate' ? 'border-red-500 focus-visible:ring-red-500' : duplicateStatus.status === 'available' ? 'border-green-500 focus-visible:ring-green-500' : ''}`}
                                                onBlur={(e) => checkDuplicate(e.target.value)}
                                            />
                                            <div className="absolute right-3 top-2.5">
                                                {duplicateStatus.status === 'checking' && <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />}
                                                {duplicateStatus.status === 'duplicate' && <AlertCircle className="h-4 w-4 text-red-500" />}
                                                {duplicateStatus.status === 'available' && <CheckCircle2 className="h-4 w-4 text-green-500" />}
                                            </div>
                                        </div>
                                        {duplicateStatus.status !== 'idle' && (
                                            <p className={`text-xs ${duplicateStatus.status === 'duplicate' ? 'text-red-500' : duplicateStatus.status === 'available' ? 'text-green-500' : 'text-muted-foreground'}`}>
                                                {duplicateStatus.message}
                                            </p>
                                        )}
                                    </div>
                                    <div className="space-y-2">
                                        <Label>날짜 (Date)</Label>
                                        <Input {...register("invoice_date")} type="date" />
                                    </div>
                                </div>

                                <Separator className="my-2" />

                                <div className="space-y-4">
                                    <Label className="text-base font-semibold">공급처 정보 (Supplier)</Label>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="space-y-2">
                                            <Label>상호명 (Company Name) *</Label>
                                            <Input {...register("supplier_name")} placeholder="지에스씨인터내셔날(주)" />
                                        </div>
                                        <div className="space-y-2">
                                            <Label>담당자 (Contact Person)</Label>
                                            <Input {...register("receiver_name")} placeholder="이혜인" />
                                        </div>
                                        <div className="space-y-2">
                                            <Label>공급처 대표 전화 (Main Phone)</Label>
                                            <Input {...register("supplier_phone")} placeholder="070-4366-6276" />
                                        </div>
                                        <div className="space-y-2">
                                            <Label>담당자 전화 (Contact Phone)</Label>
                                            <Input {...register("contact_phone")} placeholder="010-9269-3047" />
                                        </div>
                                        <div className="space-y-2">
                                            <Label>이메일 (Email)</Label>
                                            <Input {...register("supplier_email")} placeholder="h.y.lee@coffeegsc.co.kr" />
                                        </div>
                                    </div>
                                </div>
                                <Separator className="my-2" />

                                <div className="space-y-2">
                                    <Label>품목 (Items)</Label>
                                    <div className="border rounded-md divide-y">

                                        {fields.map((field: any, index: number) => {
                                            // Watch current item name to show status
                                            const currentName = watch(`items.${index}.bean_name`)
                                            const status = itemStatus[currentName]

                                            return (
                                                <div key={field.id} className="p-3 grid grid-cols-12 gap-2 item-center text-sm relative">
                                                    <div className="col-span-12 mb-1 flex gap-2 h-5">
                                                        {status?.status === 'MATCH' && <Badge variant="default" className="bg-green-600 hover:bg-green-700 text-[10px] py-0 px-2">기존 상품 (Matched)</Badge>}
                                                        {status?.status === 'NEW' && <Badge variant="secondary" className="text-[10px] py-0 px-2 bg-blue-100 text-blue-800 hover:bg-blue-200">신규 상품 (New)</Badge>}
                                                    </div>
                                                    <div className="col-span-5">
                                                        <Input
                                                            {...register(`items.${index}.bean_name`)}
                                                            placeholder="원두명"
                                                            className="h-8"
                                                            onBlur={(e) => checkItemsBatch([e.target.value])}
                                                        />
                                                    </div>
                                                    <div className="col-span-2">
                                                        <Input {...register(`items.${index}.quantity`)} type="number" step="0.1" placeholder="수량" className="h-8" />
                                                    </div>
                                                    <div className="col-span-3">
                                                        <Input {...register(`items.${index}.amount`)} type="number" placeholder="금액" className="h-8" />
                                                    </div>
                                                    <div className="col-span-2 flex justify-end">
                                                        <Button type="button" variant="ghost" size="sm" onClick={() => remove(index)}>삭제</Button>
                                                    </div>
                                                </div>
                                            )
                                        })}
                                    </div>
                                    <Button type="button" variant="outline" size="sm" className="w-full" onClick={() => append({ bean_name: "", quantity: 0, unit_price: 0, amount: 0 })}>
                                        + 항목 추가
                                    </Button>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <Label>총 금액 (Total)</Label>
                                        <Input {...register("total_amount")} type="number" />
                                    </div>
                                </div>

                                <Separator />

                                <Button type="submit" className="w-full" size="lg">
                                    <Save className="mr-2 h-4 w-4" /> 입고 확정 및 저장
                                </Button>
                            </form>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    )
}
