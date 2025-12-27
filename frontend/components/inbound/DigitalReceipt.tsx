import { motion, Variants } from 'framer-motion'
import { FileText, Calendar, Building, Package, CreditCard, ChevronRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { formatCurrency } from '@/lib/utils'
import { Badge } from '@/components/ui/badge'

interface DigitalReceiptProps {
    data: any
    onConfirm: () => void
}

export default function DigitalReceipt({ data, onConfirm }: DigitalReceiptProps) {
    if (!data) return null;

    // Animation for receipt printing effect
    const receiptVariants: Variants = {
        hidden: { scaleY: 0.1, opacity: 0, transformOrigin: "top" },
        visible: {
            scaleY: 1,
            opacity: 1,
            transition: { type: "spring", damping: 15, duration: 0.8 }
        }
    }

    return (
        <div className="relative perspective-1000">
            {/* Receipt Visual */}
            <motion.div
                variants={receiptVariants}
                initial="hidden"
                animate="visible"
                className="bg-white w-full max-w-sm mx-auto shadow-2xl overflow-hidden relative border-t-8 border-latte-900"
                style={{
                    filter: 'drop-shadow(0 20px 30px rgba(0,0,0,0.15))',
                    maskImage: 'radial-gradient(circle at bottom, transparent 6px, black 6.5px)',
                    maskSize: '20px 20px',
                    maskPosition: 'bottom',
                    maskRepeat: 'repeat-x',
                    paddingBottom: '20px'
                }}
            >
                {/* Paper Texture Overlay */}
                <div className="absolute inset-0 bg-[url('/images/texture/paper.png')] opacity-10 pointer-events-none mix-blend-multiply" />

                {/* Header */}
                <div className="p-6 text-center border-b-2 border-dashed border-latte-100">
                    <div className="w-12 h-12 bg-latte-900 rounded-full flex items-center justify-center mx-auto mb-3 text-white">
                        <FileText className="w-6 h-6" />
                    </div>
                    <h3 className="text-xl font-serif font-bold text-latte-900 tracking-wider">INBOUND RECEIPT</h3>
                    <p className="text-xs text-latte-400 uppercase tracking-widest mt-1">THE MOON COFFEE LAB</p>
                </div>

                {/* Meta Info */}
                <div className="p-6 space-y-4 text-sm">
                    <div className="flex justify-between items-center">
                        <div className="flex items-center text-latte-500 gap-2">
                            <Building className="w-4 h-4" />
                            <span>공급처</span>
                        </div>
                        <span className="font-bold text-latte-900">{data.supplier?.name || data.supplier_name || '미확인'}</span>
                    </div>
                    <div className="flex justify-between items-center">
                        <div className="flex items-center text-latte-500 gap-2">
                            <Calendar className="w-4 h-4" />
                            <span>일자</span>
                        </div>
                        <span className="font-mono">{data.document_info?.invoice_date || data.invoice_date || '-'}</span>
                    </div>
                    <div className="flex justify-between items-center">
                        <div className="flex items-center text-latte-500 gap-2">
                            <FileText className="w-4 h-4" />
                            <span>문서 번호</span>
                        </div>
                        <span className="font-mono text-xs">{data.document_info?.contract_number || data.contract_number || '-'}</span>
                    </div>
                </div>

                {/* Dashed Divider */}
                <div className="relative h-px bg-latte-200 my-2 mx-4" style={{ backgroundImage: 'linear-gradient(to right, #e5e5e5 50%, transparent 50%)', backgroundSize: '10px 1px', backgroundRepeat: 'repeat-x' }} />

                {/* Items List */}
                <div className="p-6">
                    <div className="flex justify-between items-center mb-3">
                        <span className="text-xs font-bold text-latte-400 uppercase">Items</span>
                        <Badge variant="secondary" className="bg-latte-100 text-latte-600 font-mono text-xs">
                            {data.items?.length || 0}
                        </Badge>
                    </div>

                    <ul className="space-y-3 mb-6">
                        {(data.items || []).slice(0, 5).map((item: any, idx: number) => (
                            <li key={idx} className="flex justify-between items-start text-sm">
                                <span className="text-latte-800 font-medium line-clamp-1 flex-1 pr-2">{item.bean_name}</span>
                                <div className="text-right whitespace-nowrap">
                                    <span className="block font-bold text-latte-900">{item.quantity} kg</span>
                                    {item.unit_price > 0 && <span className="block text-xs text-latte-400">@{formatCurrency(item.unit_price)}</span>}
                                </div>
                            </li>
                        ))}
                        {(data.items || []).length > 5 && (
                            <li className="text-center text-xs text-latte-400 italic pt-2">
                                ...외 {data.items.length - 5}건
                            </li>
                        )}
                    </ul>

                    {/* Total */}
                    <div className="bg-latte-900 text-latte-50 p-4 rounded-lg flex justify-between items-center shadow-inner">
                        <span className="text-sm font-medium opacity-80">Total Due</span>
                        <span className="text-xl font-mono font-bold tracking-tight">
                            {formatCurrency(data.amounts?.total_amount || data.total_amount || 0)}
                            <span className="text-sm ml-1 opacity-60">KRW</span>
                        </span>
                    </div>
                </div>

                {/* Action Button */}
                <div className="p-6 pt-0">
                    <Button
                        onClick={onConfirm}
                        className="w-full h-12 text-lg font-bold bg-green-600 hover:bg-green-700 text-white shadow-lg hover:shadow-xl transition-all group"
                    >
                        <span>상세 확인하기</span>
                        <ChevronRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                    </Button>
                </div>
            </motion.div>
        </div>
    )
}
