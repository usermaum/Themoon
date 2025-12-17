"use client"

import { useState, useCallback, useEffect } from "react"
import { useForm, useFieldArray } from "react-hook-form"
import { Upload, Link as LinkIcon, Clipboard, Image as ImageIcon, Loader2, Save } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
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
    invoice_date: string
    total_amount: number
    items: InboundItem[]
    drive_link?: string
    notes?: string
}

export default function InboundPage() {
    const [activeTab, setActiveTab] = useState("file")
    const [selectedFile, setSelectedFile] = useState<File | null>(null)
    const [pastedImage, setPastedImage] = useState<File | null>(null)
    const [urlInput, setUrlInput] = useState("")
    const [previewUrl, setPreviewUrl] = useState<string | null>(null)
    const [isAnalyzing, setIsAnalyzing] = useState(false)
    const [driveLink, setDriveLink] = useState<string | null>(null)

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

            // Auto-fill form
            setValue("supplier_name", data.supplier_name || "")
            setValue("invoice_date", data.invoice_date || "")
            setValue("total_amount", data.total_amount || 0)
            setValue("items", data.items || [])
            setDriveLink(data.drive_link)

            toast({ title: "분석 완료", description: "명세서 내용을 자동으로 입력했습니다." })
        } catch (error: any) {
            toast({ title: "오류 발생", description: error.message, variant: "destructive" })
        } finally {
            setIsAnalyzing(false)
        }
    }

    const onSubmit = async (data: InboundForm) => {
        try {
            const payload = {
                items: data.items,
                document: {
                    supplier_name: data.supplier_name,
                    invoice_date: data.invoice_date,
                    total_amount: data.total_amount,
                    image_url: driveLink, // Using the local link
                    notes: data.notes
                }
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
            toast({ title: "저장 실패", description: error.message, variant: "destructive" })
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
                                        <Label>공급처 (Supplier)</Label>
                                        <Input {...register("supplier_name")} placeholder="공급처명" />
                                    </div>
                                    <div className="space-y-2">
                                        <Label>날짜 (Date)</Label>
                                        <Input {...register("invoice_date")} type="date" />
                                    </div>
                                </div>

                                <div className="space-y-2">
                                    <Label>품목 (Items)</Label>
                                    <div className="border rounded-md divide-y">
                                        {fields.map((field: any, index: number) => (
                                            <div key={field.id} className="p-3 grid grid-cols-12 gap-2 item-center text-sm">
                                                <div className="col-span-5">
                                                    <Input {...register(`items.${index}.bean_name`)} placeholder="원두명" className="h-8" />
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
                                        ))}
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
