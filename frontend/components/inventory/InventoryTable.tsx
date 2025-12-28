import { Bean } from '@/lib/api'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Plus, Minus, AlertTriangle } from 'lucide-react'

interface InventoryTableProps {
    beans: Bean[]
    onOpenModal: (bean: Bean, type: 'IN' | 'OUT') => void
}

export default function InventoryTable({ beans, onOpenModal }: InventoryTableProps) {
    return (
        <div className="bg-white/60 backdrop-blur-md rounded-[1.5rem] shadow-sm overflow-hidden border border-latte-200">
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-latte-100">
                    <thead className="bg-latte-50/50">
                        <tr>
                            <th className="px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">원두명</th>
                            <th className="px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">유형</th>
                            <th className="px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">특징</th>
                            <th className="px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">원산지</th>
                            <th className="px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">현재 재고</th>
                            <th className="px-6 py-4 text-center text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">상태</th>
                            <th className="px-6 py-4 text-right text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">작업</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white/40 divide-y divide-latte-100">
                        {beans.length === 0 ? (
                            <tr><td colSpan={7} className="px-6 py-12 text-center text-latte-400">데이터가 없습니다.</td></tr>
                        ) : beans.map((bean) => (
                            <tr key={bean.id} className="group hover:bg-latte-50/80 transition-all duration-200">
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="text-sm font-bold text-latte-900 group-hover:text-latte-700 transition-colors">{bean.name_ko || bean.name}</div>
                                    {bean.name_en && <div className="text-xs font-normal text-latte-400 font-sans">{bean.name_en}</div>}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    {bean.type === 'GREEN_BEAN' ? <Badge variant="secondary" className="bg-green-100 text-green-700 hover:bg-green-200 border-none">생두</Badge> :
                                        bean.type === 'BLEND_BEAN' ? <Badge variant="secondary" className="bg-amber-100 text-amber-700 hover:bg-amber-200 border-none">블렌드</Badge> :
                                            <Badge variant="secondary" className="bg-latte-100 text-latte-700 hover:bg-latte-200 border-none">원두</Badge>}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-latte-600">
                                    {bean.roast_profile === 'LIGHT' ? <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-lime-100 text-lime-800">신콩 (Light)</span> :
                                        bean.roast_profile === 'DARK' ? <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-800">탄콩 (Dark)</span> :
                                            bean.roast_profile === 'MEDIUM' ? <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-orange-100 text-orange-800">미디엄</span> :
                                                <span className="text-latte-300">-</span>}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-latte-600">{bean.origin_ko || bean.origin || '-'}</td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="text-sm font-mono text-latte-900 font-bold bg-latte-50 inline-block px-3 py-1 rounded-md border border-latte-100">
                                        {bean.quantity_kg.toFixed(2)} <span className="text-latte-400 font-normal">kg</span>
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-center">
                                    {bean.quantity_kg < 5 ?
                                        <div className="flex items-center justify-center gap-1.5 text-red-600 text-xs font-bold animate-pulse">
                                            <AlertTriangle className="w-4 h-4" /> 부족
                                        </div>
                                        :
                                        bean.quantity_kg < 10 ?
                                            <div className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-amber-50 text-amber-700 border border-amber-200">
                                                주의
                                            </div>
                                            :
                                            <div className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-50 text-green-700 border border-green-200">
                                                충분
                                            </div>
                                    }
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                                    <Button size="sm" variant="ghost" onClick={() => onOpenModal(bean, 'IN')} className="text-green-600 hover:text-green-700 hover:bg-green-50 rounded-full px-4 border border-transparent hover:border-green-200 transition-all font-bold">
                                        <Plus className="w-3.5 h-3.5 mr-1.5" /> 입고
                                    </Button>
                                    <Button size="sm" variant="ghost" onClick={() => onOpenModal(bean, 'OUT')} className="text-latte-400 hover:text-red-600 hover:bg-red-50 rounded-full px-4 border border-transparent hover:border-red-200 transition-all">
                                        <Minus className="w-3.5 h-3.5 mr-1.5" /> 출고
                                    </Button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}
