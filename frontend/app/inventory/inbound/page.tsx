'use client';

import { useState, useCallback, useEffect } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { useRouter } from 'next/navigation';
import {
  Upload,
  Link as LinkIcon,
  Clipboard,
  Image as ImageIcon,
  Loader2,
  Save,
  AlertCircle,
  CheckCircle2,
  FileText,
  RefreshCw,
  Trash2,
  X,
  Info,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { formatCurrency } from '@/lib/utils';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { BeanAPI } from '@/lib/api';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Separator } from '@/components/ui/separator';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { useToast } from '@/hooks/use-toast';
import PageHero from '@/components/ui/page-hero';
import Image from 'next/image';
import DigitalReceipt from '@/components/inbound/DigitalReceipt'; // Import DigitalReceipt

// Types
interface InboundItem {
  bean_name: string;
  quantity: number;
  unit_price: number;
  amount: number;
  order_number?: string;
}

interface OrderGroup {
  order_number: string;
  order_date: string;
  items: InboundItem[];
  subtotal: number;
}

interface InboundForm {
  supplier_name: string;
  supplier_phone?: string;
  contact_phone?: string;
  supplier_email?: string;
  contract_number?: string;
  receiver_name?: string;
  invoice_date: string;
  total_amount: number;
  items: InboundItem[];
  drive_link?: string;
  original_image_path?: string;
  webview_image_path?: string;
  thumbnail_image_path?: string;
  image_width?: number;
  image_height?: number;
  file_size_bytes?: number;
  notes?: string;
}

export default function InboundPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState('file');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [pastedImage, setPastedImage] = useState<File | null>(null);
  const [urlInput, setUrlInput] = useState('');
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [driveLink, setDriveLink] = useState<string | null>(null);

  const [ocrResult, setOcrResult] = useState<any>(null); // Temporary for debugging
  const [duplicateStatus, setDuplicateStatus] = useState<{
    status: 'idle' | 'checking' | 'duplicate' | 'available';
    message: string;
  }>({ status: 'idle', message: '' });
  const [itemStatus, setItemStatus] = useState<
    Record<string, { status: string; bean_id: number | null }>
  >({});

  // Multi-order states
  const [hasMultipleOrders, setHasMultipleOrders] = useState(false);
  const [totalOrderCount, setTotalOrderCount] = useState(0);
  const [orderGroups, setOrderGroups] = useState<OrderGroup[]>([]);

  // Modal states
  const [showMultiOrderModal, setShowMultiOrderModal] = useState(false);
  const [showConfirmDialog, setShowConfirmDialog] = useState(false);
  const [showCancelConfirmDialog, setShowCancelConfirmDialog] = useState(false);

  // Pending orders
  const [pendingOrders, setPendingOrders] = useState<OrderGroup[]>([]);
  const [selectedOrderIndex, setSelectedOrderIndex] = useState<number | null>(null);

  // Dialog States
  const [showSaveConfirm, setShowSaveConfirm] = useState(false);
  const [itemToDelete, setItemToDelete] = useState<number | null>(null);

  const { toast } = useToast();

  const { register, control, handleSubmit, setValue, reset, watch } = useForm<InboundForm>({
    defaultValues: {
      supplier_name: '',
      supplier_phone: '',
      contact_phone: '',
      supplier_email: '',
      contract_number: '',
      receiver_name: '',
      invoice_date: '',
      total_amount: 0,
      items: [{ bean_name: '', quantity: 0, unit_price: 0, amount: 0 }],
      notes: '',
    },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'items',
  });

  // Handle File Selection
  // Handle File Selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      // Reset form and states when new file is selected
      reset();
      setDuplicateStatus({ status: 'idle', message: '' });
      setItemStatus({});
      setOcrResult(null);
      setDriveLink(null);
      setUrlInput('');
      setPreviewUrl(null);

      const file = e.target.files[0];
      setSelectedFile(file);
      setPastedImage(null);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  // Handle Paste
  const handlePaste = useCallback(
    (e: ClipboardEvent) => {
      const items = e.clipboardData?.items;
      if (!items) return;

      for (let i = 0; i < items.length; i++) {
        const item = items[i];
        if (item.type.indexOf('image') !== -1) {
          const file = item.getAsFile();
          if (file) {
            setPastedImage(file);
            setSelectedFile(null);
            setPreviewUrl(URL.createObjectURL(file));
            setActiveTab('clipboard');
            toast({
              title: '이미지 붙여넣기 완료',
              description: '클립보드 이미지를 가져왔습니다.',
            });
          }
        }
      }
    },
    [toast]
  );

  useEffect(() => {
    document.addEventListener('paste', handlePaste as any);
    return () => document.removeEventListener('paste', handlePaste as any);
  }, [handlePaste]);

  // Analyze Logic
  const [statusMessage, setStatusMessage] = useState('');

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    setOcrResult(null);
    setStatusMessage('분석 준비 중...');
    const formData = new FormData();

    if (activeTab === 'file' && selectedFile) {
      formData.append('file', selectedFile);
    } else if (activeTab === 'clipboard' && pastedImage) {
      formData.append('file', pastedImage);
    } else if (activeTab === 'url' && urlInput) {
      formData.append('url', urlInput);
    } else {
      toast({
        title: '입력값 없음',
        description: '이미지나 URL을 입력해주세요.',
        variant: 'destructive',
      });
      setIsAnalyzing(false);
      return;
    }

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/inbound/analyze`,
        {
          method: 'POST',
          body: formData,
        }
      );

      if (!response.ok) {
        if (response.status === 429) {
          throw new Error('일일 사용량이 초과되었습니다. 잠시 후(약 1분) 다시 시도해주세요.');
        }
        const err = await response.json();
        if (err.detail === 'INVALID_DOCUMENT') {
          throw new Error(
            '명세서 형식이 아닙니다. 올바른 문서 이미지를 업로드하거나 다시 확인해주세요.'
          );
        }
        throw new Error(err.detail || '분석 요청 실패');
      }

      // Stream Reader setup
      const reader = response.body?.getReader();
      if (!reader) throw new Error('분석 스트림을 읽을 수 없습니다.');

      const decoder = new TextDecoder();
      let finalData = null;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const update = JSON.parse(line);

            if (update.status === 'progress') {
              setStatusMessage(update.message);
            } else if (update.status === 'complete') {
              finalData = update.data;
            } else if (update.status === 'error') {
              throw new Error(update.message);
            }
          } catch (e) {
            // Ignore incomplete JSON chunks or parse errors
            // In production, might want to buffer incomplete lines.
            // But NDJSON is usually line-buffered.
            if ((e as Error).message !== 'Unexpected end of JSON input') {
              console.warn('Stream parse error:', e);
            }
          }
        }
      }

      if (!finalData) {
        throw new Error('분석 결과가 없습니다.');
      }

      const data = finalData;
      setStatusMessage('분석 완료!');
      setOcrResult(data);

      // Check for multiple orders
      if (data.has_multiple_orders) {
        setHasMultipleOrders(true);
        setTotalOrderCount(data.total_order_count);
        setOrderGroups(data.order_groups);
        setShowMultiOrderModal(true);
        toast({
          title: '다중 주문 감지',
          description: `${data.total_order_count}개의 주문번호가 발견되었습니다.`
        });
        return;
      }

      // Auto-fill form using structured data (single order flow)
      const contractNum = data.document_info?.contract_number || data.contract_number || '';
      setValue('contract_number', contractNum);

      if (contractNum) {
        checkDuplicate(contractNum);
      }

      // 공급처 정보
      setValue('supplier_name', data.supplier?.name || data.supplier_name || '');
      setValue('supplier_phone', data.supplier?.phone || data.supplier_phone || '');
      setValue('contact_phone', data.supplier?.contact_phone || '');
      setValue('supplier_email', data.supplier?.email || data.supplier_email || '');

      // 공급처 담당자
      setValue(
        'receiver_name',
        data.supplier?.contact_person || data.supplier?.representative || ''
      );

      // 날짜 및 금액
      setValue('invoice_date', data.document_info?.invoice_date || data.invoice_date || '');
      setValue('total_amount', data.amounts?.total_amount || data.total_amount || 0);

      // 품목 정보
      setValue('items', data.items || []);
      setDriveLink(data.drive_link);

      toast({ title: '분석 완료', description: '명세서 내용을 자동으로 입력했습니다.' });

      if (data.items && data.items.length > 0) {
        const names = data.items.map((i: any) => i.bean_name || '').filter((n: string) => n !== '');
        checkItemsBatch(names);
      }
    } catch (error: any) {
      reset();
      setOcrResult(null);
      setDriveLink(null);
      setDuplicateStatus({ status: 'idle', message: '' });
      setSelectedFile(null);
      setPastedImage(null);
      setUrlInput('');
      setPreviewUrl(null);

      toast({ title: '오류 발생', description: error.message, variant: 'destructive' });
    } finally {
      setIsAnalyzing(false);
      setStatusMessage('');
    }
  };

  // Check Status Logic
  const checkItemsBatch = async (names: string[]) => {
    console.log('Checking items:', names);
    if (names.length === 0) return;
    try {
      const results = await BeanAPI.checkBatch(names);
      console.log('Check results:', results);

      // Functional update to avoid stale state
      setItemStatus((prev) => {
        const newStatus: any = { ...prev };
        results.forEach((r: any) => {
          newStatus[r.input_name] = { status: r.status, bean_id: r.bean_id };
        });
        return newStatus;
      });
    } catch (e) {
      console.error('Failed to check items', e);
    }
  };

  // Duplicate Check Logic
  const checkDuplicate = async (contractNumber: string) => {
    if (!contractNumber || contractNumber.trim() === '') {
      setDuplicateStatus({ status: 'idle', message: '' });
      return;
    }

    setDuplicateStatus({ status: 'checking', message: '확인 중...' });
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/inbound/check-duplicate/${contractNumber}`
      );
      if (response.ok) {
        const data = await response.json();
        if (data.exists) {
          setDuplicateStatus({ status: 'duplicate', message: data.detail });
        } else {
          setDuplicateStatus({ status: 'available', message: data.detail });
        }
      } else {
        setDuplicateStatus({ status: 'idle', message: '확인 불가' });
      }
    } catch (error) {
      console.error('Duplicate check error:', error);
      setDuplicateStatus({ status: 'idle', message: '확인 불가' });
    }
  };

  // Watch contract number changes for debounce or blur handling
  // Simple approach: Use onBlur on the input

  const onSubmit = async (data: InboundForm) => {
    // Validation
    if (duplicateStatus.status !== 'available') {
      toast({
        title: '계약번호 확인 필요',
        description: '계약/주문 번호 중복 확인이 완료되지 않았습니다.',
        variant: 'destructive',
      });
      return;
    }

    if (!data.contract_number || data.contract_number.trim() === '') {
      toast({
        title: '필수 입력값 누락',
        description: '계약/주문 번호(Contract No.)는 필수입니다.',
        variant: 'destructive',
      });
      return;
    }
    if (!data.supplier_name || data.supplier_name.trim() === '') {
      toast({
        title: '필수 입력값 누락',
        description: '공급처 정보(상호명)는 필수입니다.',
        variant: 'destructive',
      });
      return;
    }
    if (data.items.length === 0) {
      toast({
        title: '필수 입력값 누락',
        description: '최소 1개 이상의 품목이 필요합니다.',
        variant: 'destructive',
      });
      return;
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
          notes: data.notes,
          // Tiered Storage
          original_image_path: ocrResult?.original_image_path,
          webview_image_path: ocrResult?.webview_image_path,
          thumbnail_image_path: ocrResult?.thumbnail_image_path,
          image_width: ocrResult?.image_width,
          image_height: ocrResult?.image_height,
          file_size_bytes: ocrResult?.file_size_bytes,
        },
        // NEW: Include full OCR data for detailed storage (Option B)
        document_info: ocrResult?.document_info,
        supplier: ocrResult?.supplier,
        receiver: ocrResult?.receiver,
        amounts: ocrResult?.amounts,
        additional_info: ocrResult?.additional_info,
      };

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/inbound/confirm`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        }
      );

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || '저장 실패');
      }

      toast({ title: '저장 완료', description: '입고 데이터가 성공적으로 저장되었습니다.' });

      // 입력 폼 전체 초기화 (Full Reset)
      reset();
      setOcrResult(null);
      setDriveLink(null);
      setDuplicateStatus({ status: 'idle', message: '' });
      setSelectedFile(null);
      setPastedImage(null);
      setUrlInput('');
      setPreviewUrl(null);
      setItemStatus({});
    } catch (error: any) {
      // Check if it's a duplicate error and show a friendly message
      if (
        error.message.includes('Duplicate Contract Number') ||
        error.message.includes('이미 등록된')
      ) {
        toast({
          title: '저장 실패',
          description: '이미 등록된 명세서(계약번호)입니다. 중복을 확인해주세요.',
          variant: 'destructive',
        });
      } else {
        toast({ title: '저장 실패', description: error.message, variant: 'destructive' });
      }
    }
  };

  const handleSaveConfirm = () => {
    // Trigger validation and submit
    handleSubmit(onSubmit, (errors) => {
      console.error("Form Validation Errors:", errors);
      toast({
        title: "입력값 확인 필요",
        description: "필수 입력 항목을 확인해주세요.",
        variant: "destructive"
      });
    })();
    setShowSaveConfirm(false);
  };

  const handleDeleteConfirm = () => {
    if (itemToDelete !== null) {
      remove(itemToDelete);
      setItemToDelete(null);
    }
  };

  // Multi-order handlers
  const handleAcceptMultiOrders = () => {
    setShowMultiOrderModal(false);
    setPendingOrders([...orderGroups]);
    toast({
      title: '개별 처리 모드',
      description: '각 주문을 개별적으로 처리할 수 있습니다.',
    });
  };

  const handleCancelMultiOrders = () => {
    setShowMultiOrderModal(false);
    setShowCancelConfirmDialog(true);
  };

  const confirmCancelWork = () => {
    // Reset all states
    setOcrResult(null);
    setHasMultipleOrders(false);
    setOrderGroups([]);
    setPendingOrders([]);
    setShowCancelConfirmDialog(false);
    setDriveLink(null);
    setSelectedFile(null);
    setPastedImage(null);
    setUrlInput('');
    setPreviewUrl(null);
    setDuplicateStatus({ status: 'idle', message: '' });
    setItemStatus({});
    reset();

    toast({
      title: '작업 취소',
      description: '모든 데이터가 초기화되었습니다.',
    });
  };

  const handleAddOrder = (orderGroup: OrderGroup, index: number) => {
    setSelectedOrderIndex(index);
    setShowConfirmDialog(true);
  };

  const confirmAddOrder = async () => {
    if (selectedOrderIndex === null) return;

    const orderGroup = pendingOrders[selectedOrderIndex];

    try {
      const payload = {
        items: orderGroup.items,
        document: {
          supplier_name: ocrResult?.supplier?.name || ocrResult?.supplier_name || '',
          contract_number: orderGroup.order_number,
          supplier_phone: ocrResult?.supplier?.phone || ocrResult?.supplier_phone || '',
          supplier_email: ocrResult?.supplier?.email || ocrResult?.supplier_email || '',
          receiver_name: ocrResult?.supplier?.contact_person || ocrResult?.supplier?.representative || '',
          invoice_date: orderGroup.order_date,
          total_amount: orderGroup.subtotal,
          image_url: driveLink,
          notes: '',
          // Tiered Storage
          original_image_path: ocrResult?.original_image_path,
          webview_image_path: ocrResult?.webview_image_path,
          thumbnail_image_path: ocrResult?.thumbnail_image_path,
          image_width: ocrResult?.image_width,
          image_height: ocrResult?.image_height,
          file_size_bytes: ocrResult?.file_size_bytes,
        },
        // Include full OCR data
        document_info: ocrResult?.document_info,
        supplier: ocrResult?.supplier,
        receiver: ocrResult?.receiver,
        amounts: {
          ...ocrResult?.amounts,
          total_amount: orderGroup.subtotal,
        },
        additional_info: ocrResult?.additional_info,
      };

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/inbound/confirm`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        }
      );

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || '입고 처리 실패');
      }

      toast({
        title: '입고 처리 완료',
        description: `${orderGroup.order_number} 주문이 성공적으로 처리되었습니다.`,
      });

      // Remove from pending orders
      const newPendingOrders = pendingOrders.filter((_, i) => i !== selectedOrderIndex);
      setPendingOrders(newPendingOrders);
      setShowConfirmDialog(false);
      setSelectedOrderIndex(null);

      // Check if all orders are processed
      if (newPendingOrders.length === 0) {
        toast({
          title: '모든 주문 처리 완료',
          description: '모든 주문이 성공적으로 입고 처리되었습니다.',
        });

        // Reset to allow new document upload
        setOcrResult(null);
        setHasMultipleOrders(false);
        setOrderGroups([]);
        setPendingOrders([]);
        setDriveLink(null);
        setDuplicateStatus({ status: 'idle', message: '' });
        setItemStatus({});
        reset();
      }
    } catch (error: any) {
      toast({
        title: '입고 처리 실패',
        description: error.message,
        variant: 'destructive',
      });
    }
  };

  return (
    <div className="space-y-8 pb-20">
      <PageHero
        title="명세서 입고 (Inbound)"
        description="명세서 사진을 업로드하면 자동으로 재고를 등록합니다."
        icon={<FileText />}
        image="/images/hero/inbound_hero.png"
        className="mb-8"
        compact={true}
      />

      <div className="container mx-auto px-4 max-w-7xl">

        {/* Step Indicator */}
        <div className="flex justify-center mb-10">
          <div className="flex items-center gap-4 text-sm font-medium">
            <div className="flex items-center gap-2 text-latte-900">
              <div className="w-8 h-8 rounded-full bg-latte-900 text-white flex items-center justify-center font-bold">1</div>
              <span>업로드</span>
            </div>
            <div className="w-12 h-px bg-latte-200"></div>
            <div className={`flex items-center gap-2 ${ocrResult ? 'text-latte-900' : 'text-latte-400'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${ocrResult ? 'bg-latte-900 text-white' : 'bg-latte-100'}`}>2</div>
              <span>분석 & 확인</span>
            </div>
            <div className="w-12 h-px bg-latte-200"></div>
            <div className="flex items-center gap-2 text-latte-400">
              <div className="w-8 h-8 rounded-full bg-latte-100 flex items-center justify-center font-bold">3</div>
              <span>저장</span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left: Input & Preview */}
          <div className="space-y-6">
            <Card className="overflow-hidden border-latte-200 shadow-md">
              <CardHeader className="bg-latte-50/50 border-b border-latte-100">
                <CardTitle className="flex items-center gap-2">
                  <Upload className="w-5 h-5" /> 입력 소스
                </CardTitle>
              </CardHeader>
              <CardContent className="p-6">
                <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                  <TabsList className="grid w-full grid-cols-3 mb-6 bg-latte-100/50 p-1 rounded-lg">
                    <TabsTrigger value="file" className="rounded-md data-[state=active]:bg-white data-[state=active]:shadow-sm">
                      <Upload className="w-4 h-4 mr-2" /> 파일
                    </TabsTrigger>
                    <TabsTrigger value="clipboard" className="rounded-md data-[state=active]:bg-white data-[state=active]:shadow-sm">
                      <Clipboard className="w-4 h-4 mr-2" /> 붙여넣기
                    </TabsTrigger>
                    <TabsTrigger value="url" className="rounded-md data-[state=active]:bg-white data-[state=active]:shadow-sm">
                      <LinkIcon className="w-4 h-4 mr-2" /> URL
                    </TabsTrigger>
                  </TabsList>

                  <div className="space-y-4">
                    <TabsContent value="file" className="mt-0">
                      <div className="space-y-3">
                        <Label htmlFor="picture" className="text-sm font-bold text-latte-900 hidden">
                          명세서 이미지
                        </Label>
                        <div className="relative group perspective-1000">
                          <label
                            htmlFor="picture"
                            className={`flex flex-col items-center justify-center w-full h-64 px-4 transition-all duration-300 bg-white border-2 border-dashed rounded-[1.5em] appearance-none cursor-pointer hover:border-latte-600 hover:shadow-lg focus:outline-none overflow-hidden relative ${selectedFile ? 'border-green-500 bg-green-50/10' : 'border-latte-300'}`}
                          >
                            {/* Animated background shape */}
                            <div className="absolute inset-0 bg-gradient-to-br from-latte-50/0 to-latte-100/50 opacity-0 group-hover:opacity-100 transition-opacity" />

                            <div className="flex flex-col items-center justify-center pt-5 pb-6 relative z-10">
                              {selectedFile ? (
                                <>
                                  <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4 animate-in zoom-in spin-in-12 duration-500">
                                    <CheckCircle2 className="w-8 h-8 text-green-600" />
                                  </div>
                                  <p className="text-lg font-bold text-latte-900">
                                    {selectedFile.name}
                                  </p>
                                  <p className="text-sm text-latte-500 mt-2 bg-white/80 px-3 py-1 rounded-full border border-latte-100">
                                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB • 변경하려면 클릭
                                  </p>
                                </>
                              ) : (
                                <>
                                  <div className="w-20 h-20 bg-latte-50 rounded-full flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 group-hover:bg-latte-100">
                                    <Upload className="w-10 h-10 text-latte-400 group-hover:text-latte-600 transition-colors" />
                                  </div>
                                  <p className="text-lg font-bold text-latte-700">
                                    명세서 이미지를 드래그하세요
                                  </p>
                                  <p className="text-sm text-latte-400 mt-2">
                                    또는 클릭하여 파일 선택 (JPG, PNG)
                                  </p>
                                </>
                              )}
                            </div>
                            <input
                              id="picture"
                              type="file"
                              accept="image/*"
                              className="hidden"
                              onChange={handleFileChange}
                            />
                          </label>
                        </div>
                      </div>
                    </TabsContent>

                    <TabsContent value="clipboard">
                      <div className="space-y-2">
                        <Label className="text-sm font-medium text-latte-700">명세서 이미지</Label>
                        <div className="h-32 border-2 border-dashed rounded-[1em] flex flex-col items-center justify-center text-latte-500 bg-latte-50/30 border-latte-200">
                          <Clipboard className="h-8 w-8 mb-2 text-latte-400" />
                          <p className="text-sm font-medium">Ctrl+V를 눌러 이미지를 붙여넣으세요</p>
                        </div>
                      </div>
                    </TabsContent>

                    <TabsContent value="url">
                      <div className="grid w-full items-center gap-1.5">
                        <Label htmlFor="url" className="text-sm font-medium text-latte-700">
                          이미지 URL
                        </Label>
                        <Input
                          id="url"
                          placeholder="https://..."
                          value={urlInput}
                          onChange={(e) => setUrlInput(e.target.value)}
                          className="rounded-xl border-latte-200"
                        />
                      </div>
                    </TabsContent>
                  </div>
                </Tabs>

                {previewUrl && (
                  <div className="mt-6 border-2 border-latte-200 rounded-[1em] overflow-hidden relative aspect-video bg-latte-50/50">
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
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      {statusMessage || '분석 중...'}
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
                  이미지가 서버에 저장되었습니다.{' '}
                  <a
                    href={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}${driveLink}`}
                    target="_blank"
                    className="underline font-bold"
                  >
                    이미지 보기
                  </a>
                </AlertDescription>
              </Alert>
            )}

            {/* Receipt Preview */}
            {ocrResult && (
              <div className="mt-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
                <DigitalReceipt
                  data={ocrResult}
                  onConfirm={() => {
                    const formElement = document.getElementById('inbound-form');
                    if (formElement) {
                      formElement.scrollIntoView({ behavior: 'smooth' });
                      toast({
                        title: "상세 정보 확인",
                        description: "우측(모바일: 하단) 입력 폼에서 내용을 수정할 수 있습니다."
                      });
                    }
                  }}
                />
              </div>
            )}
          </div>

          {/* Right: Form */}
          <div className="space-y-6" id="inbound-form">
            <Card>
              <CardHeader>
                <CardTitle>입고 상세 정보</CardTitle>
                <CardDescription>추출된 정보를 확인하고 수정하세요.</CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={(e) => { e.preventDefault(); setShowSaveConfirm(true); }} className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label className="text-destructive font-bold">계약/주문 번호 (필수)*</Label>
                      <div className="relative">
                        <Input
                          {...register('contract_number')}
                          placeholder="발주번호 or 문서번호"
                          className={`bg-muted/10 border-destructive/20 ${duplicateStatus.status === 'duplicate' ? 'border-red-500 focus-visible:ring-red-500' : duplicateStatus.status === 'available' ? 'border-green-500 focus-visible:ring-green-500' : ''}`}
                          onBlur={(e) => checkDuplicate(e.target.value)}
                        />
                        {watch('contract_number') && (
                          <button
                            type="button"
                            onClick={() => {
                              setValue('contract_number', '');
                              setDuplicateStatus({ status: 'idle', message: '' });
                            }}
                            className="absolute right-10 top-1/2 -translate-y-1/2 text-latte-400 hover:text-latte-600 p-1"
                          >
                            <X className="w-4 h-4" />
                          </button>
                        )}
                        <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
                          {duplicateStatus.status === 'checking' && (
                            <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
                          )}
                          {duplicateStatus.status === 'duplicate' && (
                            <AlertCircle className="h-4 w-4 text-red-500" />
                          )}
                          {duplicateStatus.status === 'available' && (
                            <CheckCircle2 className="h-4 w-4 text-green-500" />
                          )}
                        </div>
                      </div>
                      {duplicateStatus.status !== 'idle' && (
                        <p
                          className={`text-xs ${duplicateStatus.status === 'duplicate' ? 'text-red-500' : duplicateStatus.status === 'available' ? 'text-green-500' : 'text-muted-foreground'}`}
                        >
                          {duplicateStatus.message}
                        </p>
                      )}
                    </div>
                    <div className="space-y-2">
                      <Label>날짜 (Date)</Label>
                      <Input {...register('invoice_date')} type="date" />
                    </div>
                  </div>

                  <Separator className="my-2" />

                  <div className="space-y-4">
                    <Label className="text-base font-semibold">공급처 정보 (Supplier)</Label>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label>상호명 (Company Name) *</Label>
                        <div className="relative">
                          <Input
                            {...register('supplier_name')}
                            placeholder="공급처 명을 입력하세요"
                            className="pr-10"
                          />
                          {watch('supplier_name') && (
                            <button
                              type="button"
                              onClick={() => setValue('supplier_name', '')}
                              className="absolute right-3 top-1/2 -translate-y-1/2 text-latte-400 hover:text-latte-600 p-1"
                            >
                              <X className="w-4 h-4" />
                            </button>
                          )}
                        </div>
                      </div>
                      <div className="space-y-2">
                        <Label>담당자 (Contact Person)</Label>
                        <div className="relative">
                          <Input {...register('receiver_name')} placeholder="홍길동" className="pr-10" />
                          {watch('receiver_name') && (
                            <button
                              type="button"
                              onClick={() => setValue('receiver_name', '')}
                              className="absolute right-3 top-1/2 -translate-y-1/2 text-latte-400 hover:text-latte-600 p-1"
                            >
                              <X className="w-4 h-4" />
                            </button>
                          )}
                        </div>
                      </div>
                      <div className="space-y-2">
                        <Label>공급처 대표 전화 (Main Phone)</Label>
                        <div className="relative">
                          <Input {...register('supplier_phone')} placeholder="000-0000-0000" className="pr-10" />
                          {watch('supplier_phone') && (
                            <button
                              type="button"
                              onClick={() => setValue('supplier_phone', '')}
                              className="absolute right-3 top-1/2 -translate-y-1/2 text-latte-400 hover:text-latte-600 p-1"
                            >
                              <X className="w-4 h-4" />
                            </button>
                          )}
                        </div>
                      </div>
                      <div className="space-y-2">
                        <Label>담당자 전화 (Contact Phone)</Label>
                        <div className="relative">
                          <Input {...register('contact_phone')} placeholder="010-0000-0000" className="pr-10" />
                          {watch('contact_phone') && (
                            <button
                              type="button"
                              onClick={() => setValue('contact_phone', '')}
                              className="absolute right-3 top-1/2 -translate-y-1/2 text-latte-400 hover:text-latte-600 p-1"
                            >
                              <X className="w-4 h-4" />
                            </button>
                          )}
                        </div>
                      </div>
                      <div className="space-y-2">
                        <Label>이메일 (Email)</Label>
                        <div className="relative">
                          <Input
                            {...register('supplier_email')}
                            placeholder="example@email.com"
                            className="pr-10"
                          />
                          {watch('supplier_email') && (
                            <button
                              type="button"
                              onClick={() => setValue('supplier_email', '')}
                              className="absolute right-3 top-1/2 -translate-y-1/2 text-latte-400 hover:text-latte-600 p-1"
                            >
                              <X className="w-4 h-4" />
                            </button>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                  <Separator className="my-2" />

                  <div className="space-y-2">
                    <Label>품목 (Items)</Label>
                    <div className="border rounded-md divide-y">
                      {fields.map((field: any, index: number) => {
                        // Watch current item name to show status
                        const currentName = watch(`items.${index}.bean_name`);
                        const status = itemStatus[currentName];

                        return (
                          <div
                            key={field.id}
                            className="p-3 grid grid-cols-12 gap-2 item-center text-sm relative"
                          >
                            <div className="col-span-12 mb-1 flex gap-2 h-5">
                              {status?.status === 'MATCH' && (
                                <Badge
                                  variant="default"
                                  className="bg-green-600 hover:bg-green-700 text-[10px] py-0 px-2"
                                >
                                  기존 상품 (Matched)
                                </Badge>
                              )}
                              {status?.status === 'NEW' && (
                                <Badge
                                  variant="secondary"
                                  className="text-[10px] py-0 px-2 bg-blue-100 text-blue-800 hover:bg-blue-200"
                                >
                                  신규 상품 (New)
                                </Badge>
                              )}
                            </div>
                            <div className="col-span-5 relative">
                              <Input
                                {...register(`items.${index}.bean_name`)}
                                placeholder="원두명"
                                className="h-8 pr-10"
                                onBlur={(e) => checkItemsBatch([e.target.value])}
                              />
                              {watch(`items.${index}.bean_name`) && (
                                <button
                                  type="button"
                                  onClick={() => setValue(`items.${index}.bean_name`, '')}
                                  className="absolute right-3 top-1/2 -translate-y-1/2 text-latte-400 hover:text-latte-600 p-0.5"
                                >
                                  <X className="w-3 h-3" />
                                </button>
                              )}
                            </div>
                            <div className="col-span-2">
                              <Input
                                {...register(`items.${index}.quantity`)}
                                type="number"
                                step="0.1"
                                placeholder="수량"
                                className="h-8"
                              />
                            </div>
                            <div className="col-span-3">
                              <Input
                                {...register(`items.${index}.amount`)}
                                type="number"
                                placeholder="금액"
                                className="h-8"
                              />
                            </div>
                            <div className="col-span-2 flex justify-end">
                              <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                onClick={() => setItemToDelete(index)}
                                className="text-red-400 hover:text-red-600 hover:bg-red-50"
                              >
                                <Trash2 className="w-4 h-4 mr-1" />
                                삭제
                              </Button>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      className="w-full"
                      onClick={() =>
                        append({ bean_name: '', quantity: 0, unit_price: 0, amount: 0 })
                      }
                    >
                      + 항목 추가
                    </Button>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>총 금액 (Total)</Label>
                      <Input {...register('total_amount')} type="number" />
                    </div>
                  </div>

                  <Separator />

                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <span className="w-full">
                          <Button
                            type="button"
                            className="w-full"
                            size="lg"
                            disabled={duplicateStatus.status !== 'available'}
                            onClick={() => setShowSaveConfirm(true)}
                          >
                            <Save className="mr-2 h-4 w-4" /> 저장
                          </Button>
                        </span>
                      </TooltipTrigger>
                      {duplicateStatus.status !== 'available' && (
                        <TooltipContent>
                          <p>계약번호 중복 확인 및 검증이 필요합니다</p>
                        </TooltipContent>
                      )}
                    </Tooltip>
                  </TooltipProvider>
                </form>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Save Confirmation Dialog */}
      <AlertDialog open={showSaveConfirm} onOpenChange={setShowSaveConfirm}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>입고 내역 저장</AlertDialogTitle>
            <AlertDialogDescription>
              작성하신 입고 내역을 저장하시겠습니까?
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>취소</AlertDialogCancel>
            <AlertDialogAction onClick={handleSaveConfirm} className="bg-primary text-primary-foreground hover:bg-primary/90">
              저장하기
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={itemToDelete !== null} onOpenChange={(open) => !open && setItemToDelete(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>항목 삭제</AlertDialogTitle>
            <AlertDialogDescription>
              정말로 이 항목을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>취소</AlertDialogCancel>
            <AlertDialogAction onClick={handleDeleteConfirm} className="bg-red-600 hover:bg-red-700 text-white">
              삭제하기
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Multi-Order Detection Modal */}
      <AlertDialog open={showMultiOrderModal} onOpenChange={setShowMultiOrderModal}>
        <AlertDialogContent className="max-w-2xl">
          <AlertDialogHeader>
            <AlertDialogTitle className="flex items-center gap-2 text-amber-600">
              <AlertCircle className="w-6 h-6" />
              다중 주문 감지
            </AlertDialogTitle>
            <AlertDialogDescription>
              이 명세서에는 <strong className="text-amber-900">{totalOrderCount}개의 주문 번호</strong>가 포함되어 있습니다.
              각 주문을 개별적으로 입고 처리할 수 있습니다.
            </AlertDialogDescription>
          </AlertDialogHeader>

          <div className="space-y-2 max-h-96 overflow-y-auto">
            {orderGroups.map((order, index) => (
              <div key={index} className="p-3 bg-latte-50 rounded-lg border border-latte-200">
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-2">
                    <Badge variant="outline" className="font-mono">
                      {order.order_number}
                    </Badge>
                    <span className="text-sm text-latte-600">{order.order_date}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-sm text-latte-600">
                      {order.items.length}개 품목
                    </span>
                    <span className="font-mono font-bold text-latte-900">
                      {formatCurrency(order.subtotal)}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <AlertDialogFooter>
            <AlertDialogCancel onClick={handleCancelMultiOrders}>취소</AlertDialogCancel>
            <AlertDialogAction onClick={handleAcceptMultiOrders} className="bg-latte-900 hover:bg-latte-800">
              확인 - 개별 처리 모드로 전환
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Cancel Confirmation Dialog */}
      <AlertDialog open={showCancelConfirmDialog} onOpenChange={setShowCancelConfirmDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle className="text-amber-600">
              작업 취소 확인
            </AlertDialogTitle>
            <AlertDialogDescription>
              <div className="bg-amber-50 border-2 border-amber-200 rounded-lg p-4 mt-2">
                <p className="text-amber-900 font-bold">
                  ⚠️ 모든 내용이 초기화됩니다
                </p>
                <p className="text-sm text-amber-800 mt-2">
                  진행 중인 OCR 분석 결과가 모두 삭제되며, 복구할 수 없습니다.
                </p>
              </div>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel onClick={() => setShowCancelConfirmDialog(false)}>
              돌아가기
            </AlertDialogCancel>
            <AlertDialogAction
              onClick={confirmCancelWork}
              className="bg-amber-600 hover:bg-amber-700"
            >
              확인 - 작업 취소
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Add Order Confirmation Dialog */}
      <AlertDialog open={showConfirmDialog} onOpenChange={setShowConfirmDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle className="text-red-600 flex items-center gap-2">
              <AlertCircle className="w-6 h-6" />
              입고 처리 확인
            </AlertDialogTitle>
            <AlertDialogDescription>
              <div className="space-y-3">
                {selectedOrderIndex !== null && pendingOrders[selectedOrderIndex] && (
                  <>
                    <p className="font-bold text-base text-gray-900">
                      주문번호: {pendingOrders[selectedOrderIndex].order_number}
                    </p>
                    <p className="text-sm text-gray-600">
                      총 {pendingOrders[selectedOrderIndex].items.length}개 품목 /
                      {' '}{formatCurrency(pendingOrders[selectedOrderIndex].subtotal)}
                    </p>
                  </>
                )}

                <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4">
                  <p className="text-red-900 font-bold mb-2">
                    ⚠️ 주의사항
                  </p>
                  <ul className="list-disc list-inside text-sm text-red-800 space-y-1">
                    <li><strong>입고 처리 후 리스트에서 삭제됩니다</strong></li>
                    <li><strong>취소 불가능합니다</strong></li>
                    <li>재고가 즉시 업데이트됩니다</li>
                    <li>입고 내역이 데이터베이스에 저장됩니다</li>
                  </ul>
                </div>
              </div>
            </AlertDialogDescription>
          </AlertDialogHeader>

          <AlertDialogFooter>
            <AlertDialogCancel>취소</AlertDialogCancel>
            <AlertDialogAction
              onClick={confirmAddOrder}
              className="bg-red-600 hover:bg-red-700"
            >
              확인 - 입고 처리
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Pending Orders List */}
      {pendingOrders.length > 0 && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-5xl max-h-[90vh] overflow-y-auto">
            <CardHeader className="border-b border-latte-200">
              <div className="flex justify-between items-center">
                <CardTitle className="text-2xl font-bold">입고 대기 주문 목록</CardTitle>
                <Badge variant="secondary" className="text-base">
                  {pendingOrders.length}개 주문 대기 중
                </Badge>
              </div>
              <CardDescription>
                각 주문을 개별적으로 처리하세요. 처리된 주문은 리스트에서 자동 삭제됩니다.
              </CardDescription>
            </CardHeader>

            <CardContent className="p-6">
              <div className="space-y-4">
                {pendingOrders.map((orderGroup, index) => (
                  <Card key={orderGroup.order_number} className="border-2 border-latte-200 hover:border-latte-400 transition-colors">
                    <CardHeader className="bg-latte-50/50">
                      <CardTitle className="flex justify-between items-center text-lg">
                        <div className="flex items-center gap-3">
                          <Badge variant="outline" className="text-base font-mono">
                            {orderGroup.order_number}
                          </Badge>
                          <span className="text-sm text-latte-600 font-normal">
                            {orderGroup.order_date}
                          </span>
                        </div>
                        <span className="font-mono font-bold text-xl text-latte-900">
                          {formatCurrency(orderGroup.subtotal)}
                        </span>
                      </CardTitle>
                    </CardHeader>

                    <CardContent className="p-4">
                      <div className="overflow-x-auto">
                        <table className="w-full">
                          <thead className="bg-latte-50 border-b border-latte-200">
                            <tr>
                              <th className="text-left p-2 font-semibold">품명</th>
                              <th className="text-right p-2 font-semibold">수량</th>
                              <th className="text-right p-2 font-semibold">단가</th>
                              <th className="text-right p-2 font-semibold">금액</th>
                            </tr>
                          </thead>
                          <tbody>
                            {orderGroup.items.map((item, idx) => (
                              <tr key={idx} className="border-b border-latte-100 last:border-0">
                                <td className="p-2">{item.bean_name}</td>
                                <td className="text-right p-2">
                                  {item.quantity} kg
                                </td>
                                <td className="text-right p-2">
                                  {formatCurrency(item.unit_price || 0)}
                                </td>
                                <td className="text-right p-2 font-bold">
                                  {formatCurrency(item.amount)}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>

                      <div className="mt-4">
                        <Button
                          onClick={() => handleAddOrder(orderGroup, index)}
                          className="w-full bg-green-600 hover:bg-green-700"
                          size="lg"
                        >
                          <CheckCircle2 className="w-5 h-5 mr-2" />
                          이 주문 입고 처리하기
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
