import { useState, useEffect } from 'react'
import { useRouter, usePathname, useSearchParams } from 'next/navigation'
import { motion } from 'framer-motion'
import { Bean, BeanAPI, InventoryLog, InventoryLogAPI, InventoryLogCreateData } from '@/lib/api'
import PageHero from '@/components/ui/page-hero'
import InventoryStats from '@/components/inventory/InventoryStats' // Import Stats
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Package, Plus, Minus, Edit2, Trash2, X, AlertTriangle, Search, FileText } from 'lucide-react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Separator } from "@/components/ui/separator"
import MascotStatus from '@/components/ui/mascot-status'

const InventoryTable = ({ beans, onOpenModal }: { beans: Bean[], onOpenModal: (bean: Bean, type: 'IN' | 'OUT') => void }) => (
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

export default function InventoryPage() {
    const router = useRouter()
    const pathname = usePathname()
    const searchParams = useSearchParams()

    const [beans, setBeans] = useState<Bean[]>([])
    const [logs, setLogs] = useState<InventoryLog[]>([])
    const [beanSearch, setBeanSearch] = useState('')
    const [logSearch, setLogSearch] = useState('')
    const [debouncedBeanSearch, setDebouncedBeanSearch] = useState('')
    const [debouncedLogSearch, setDebouncedLogSearch] = useState('')
    const [loadingBeans, setLoadingBeans] = useState(true)
    const [loadingLogs, setLoadingLogs] = useState(true)
    const [error, setError] = useState<string | null>(null)

    // Stats State
    const [stats, setStats] = useState({
        totalWeight: 0,
        lowStockCount: 0,
        activeVarieties: 0
    })

    // Pagination State derived from URL
    const beanPage = Number(searchParams.get('beanPage')) || 1
    const logPage = Number(searchParams.get('logPage')) || 1

    // Total counts state
    const [beanTotal, setBeanTotal] = useState(0)
    const [logTotal, setLogTotal] = useState(0)

    // Tab State
    // Tab State derived from URL
    const activeTab = searchParams.get('tab') || 'all'
    const logTab = searchParams.get('logTab') || 'all'  // 입출고 기록 탭

    const beanLimit = 10
    const logLimit = 10

    // Modal state
    const [showModal, setShowModal] = useState(false)
    const [selectedBean, setSelectedBean] = useState<Bean | null>(null)
    const [transactionType, setTransactionType] = useState<'IN' | 'OUT'>('IN')
    const [quantity, setQuantity] = useState('')
    const [reason, setReason] = useState('')
    const [submitting, setSubmitting] = useState(false)

    // Edit modal state
    const [showEditModal, setShowEditModal] = useState(false)
    const [selectedLog, setSelectedLog] = useState<InventoryLog | null>(null)
    const [editQuantity, setEditQuantity] = useState('')
    const [editReason, setEditReason] = useState('')

    // Helper to update URL params
    const updatePage = (param: 'beanPage' | 'logPage', newPage: number) => {
        const params = new URLSearchParams(searchParams.toString())
        params.set(param, newPage.toString())
        router.push(`${pathname}?${params.toString()}`, { scroll: false })
    }

    // Debounce search
    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedBeanSearch(beanSearch)
            updatePage('beanPage', 1)
        }, 500)
        return () => clearTimeout(timer)
    }, [beanSearch])

    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedLogSearch(logSearch)
            updatePage('logPage', 1)
        }, 500)
        return () => clearTimeout(timer)
    }, [logSearch])

    // Calculate Stats on Mount (fetch all beans roughly)
    useEffect(() => {
        const fetchStats = async () => {
            try {
                // Fetch up to 1000 items to calculate global stats
                const data = await BeanAPI.getAll({ limit: 1000 })
                const allBeans = data.items

                const totalWeight = allBeans.reduce((sum, bean) => sum + bean.quantity_kg, 0)
                const lowStockCount = allBeans.filter(bean => bean.quantity_kg < 5).length
                const activeVarieties = allBeans.length

                setStats({
                    totalWeight,
                    lowStockCount,
                    activeVarieties
                })
            } catch (e) {
                console.error("Failed to fetch stats", e)
            }
        }
        fetchStats()
    }, []) // Run once on mount

    const fetchBeans = async (page: number, tab: string, search: string) => {
        try {
            const skip = (page - 1) * beanLimit

            let typeFilter: string[] | undefined = undefined
            let originFilter: string | undefined = undefined
            let excludeBlend: boolean | undefined = undefined

            if (tab === 'green') {
                typeFilter = ['GREEN_BEAN']
            } else if (tab === 'roasted') {
                typeFilter = ['ROASTED_BEAN']
                excludeBlend = true  // 원두 탭에서는 블렌드 제외
            } else if (tab === 'blend') {
                // 블렌드: type=BLEND_BEAN
                typeFilter = ['BLEND_BEAN']
            }

            const data = await BeanAPI.getAll({
                skip,
                limit: beanLimit,
                type: typeFilter,
                origin: originFilter,
                exclude_blend: excludeBlend,
                search: search || undefined
            })
            setBeans(data.items)
            setBeanTotal(data.total)
            setLoadingBeans(false)
        } catch (err) {
            console.error('Failed to fetch beans:', err)
            setError('원두 목록을 불러오는데 실패했습니다.')
            setLoadingBeans(false)
        }
    }

    const fetchLogs = async (page: number, tab: string, search: string) => {
        try {
            const skip = (page - 1) * logLimit

            // 탭에 따라 change_type 필터링
            let changeTypeFilter: string[] | undefined = undefined

            if (tab === 'in') {
                // 입고: PURCHASE, ROASTING_OUTPUT
                changeTypeFilter = ['PURCHASE', 'ROASTING_OUTPUT']
            } else if (tab === 'out') {
                // 출고: ROASTING_INPUT, SALES, LOSS, BLENDING_INPUT
                changeTypeFilter = ['ROASTING_INPUT', 'SALES', 'LOSS', 'BLENDING_INPUT']
            }
            // tab === 'all'이면 changeTypeFilter는 undefined로 모든 기록 조회

            const data = await InventoryLogAPI.getAll({
                skip,
                limit: logLimit,
                change_type: changeTypeFilter,
                search: search || undefined
            })
            setLogs(data.items)
            setLogTotal(data.total)
            setLoadingLogs(false)
        } catch (err) {
            console.error('Failed to fetch logs:', err)
            setError('입출고 기록을 불러오는데 실패했습니다.')
            setLoadingLogs(false)
        }
    }

    useEffect(() => {
        fetchBeans(beanPage, activeTab, debouncedBeanSearch)
    }, [beanPage, activeTab, debouncedBeanSearch])

    const handleTabChange = (value: string) => {
        const params = new URLSearchParams(searchParams.toString())
        params.set('tab', value)
        params.set('beanPage', '1') // Reset to page 1 on tab change
        router.push(`${pathname}?${params.toString()}`, { scroll: false })
    }

    useEffect(() => {
        fetchLogs(logPage, logTab, debouncedLogSearch)
    }, [logPage, logTab, debouncedLogSearch])

    const handleLogTabChange = (value: string) => {
        const params = new URLSearchParams(searchParams.toString())
        params.set('logTab', value)
        params.set('logPage', '1') // Reset to page 1 on tab change
        router.push(`${pathname}?${params.toString()}`, { scroll: false })
    }

    // Actions
    const openModal = (bean: Bean, type: 'IN' | 'OUT') => {
        setSelectedBean(bean)
        setTransactionType(type)
        setQuantity('')
        setReason('')
        setShowModal(true)
    }

    const closeModal = () => {
        setShowModal(false)
        setSelectedBean(null)
    }

    const openEditModal = (log: InventoryLog) => {
        setSelectedLog(log)
        setEditQuantity(Math.abs(log.change_amount).toString())
        setEditReason(log.notes || '')
        setShowEditModal(true)
    }

    const closeEditModal = () => {
        setShowEditModal(false)
        setSelectedLog(null)
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!selectedBean) return

        const quantityNum = parseFloat(quantity)
        if (isNaN(quantityNum) || quantityNum <= 0) {
            alert('올바른 수량을 입력해주세요.')
            return
        }

        const logData: InventoryLogCreateData = {
            bean_id: selectedBean.id,
            change_type: transactionType === 'IN' ? 'PURCHASE' : 'SALES',
            change_amount: transactionType === 'IN' ? quantityNum : -quantityNum,
            notes: reason || undefined,
        }

        try {
            setSubmitting(true)
            await InventoryLogAPI.create(logData)
            // Refresh both tables
            await fetchBeans(beanPage, activeTab, debouncedBeanSearch)
            updatePage('logPage', 1) // Reset log page to 1 to see new entry
            await fetchLogs(1, logTab, debouncedLogSearch)
            closeModal()
        } catch (err: any) {
            console.error('Failed to create inventory log:', err)
            alert(err.response?.data?.detail || '재고 처리에 실패했습니다.')
        } finally {
            setSubmitting(false)
        }
    }

    const handleEdit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!selectedLog) return

        const quantityNum = parseFloat(editQuantity)
        if (isNaN(quantityNum) || quantityNum <= 0) {
            alert('올바른 수량을 입력해주세요.')
            return
        }

        const finalQuantity = selectedLog.change_amount >= 0 ? quantityNum : -quantityNum

        try {
            setSubmitting(true)
            await InventoryLogAPI.update(selectedLog.id, finalQuantity, editReason || undefined)
            await fetchBeans(beanPage, activeTab, debouncedBeanSearch)
            await fetchLogs(logPage, logTab, debouncedLogSearch)
            closeEditModal()
        } catch (err: any) {
            console.error('Failed to update inventory log:', err)
            alert(err.response?.data?.detail || '수정에 실패했습니다.')
        } finally {
            setSubmitting(false)
        }
    }

    const handleDelete = async (id: number) => {
        if (!confirm('정말로 이 입출고 기록을 삭제하시겠습니까?')) return

        try {
            await InventoryLogAPI.delete(id)
            await fetchBeans(beanPage, activeTab, debouncedBeanSearch)
            await fetchLogs(logPage, logTab, debouncedLogSearch)
        } catch (err: any) {
            console.error('Failed to delete inventory log:', err)
            alert(err.response?.data?.detail || '삭제에 실패했습니다.')
        }
    }

    const getBeanName = (beanId: number) => {
        // Look up in current beans list first, but might be missing if paginated invisible
        // For accurate name, fetch log usually includes basic info or we need a map.
        // Simplified: Just check current beans list. Ideally logs should join bean name.
        const bean = beans.find(b => b.id === beanId)
        return bean ? bean.name : `Bean #${beanId}`
    }

    // Pagination calculations
    const beanTotalPages = Math.ceil(beanTotal / beanLimit)
    const logTotalPages = Math.ceil(logTotal / logLimit)

    return (
        <div className="min-h-screen">
            <PageHero
                title="재고 관리"
                description="원두의 입출고를 관리하고 현재 재고 현황을 확인하세요"
                icon={<Package />}
                image="/images/hero/inventory-hero.png"
                className="mb-8"
            />

            <div className="container mx-auto px-4 py-8">
                {error && (
                    <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-200 mb-6 flex items-center gap-2">
                        <span>⚠️</span> {error}
                    </div>
                )}

                {/* Dashboard Stats */}
                <InventoryStats
                    totalWeight={stats.totalWeight}
                    lowStockCount={stats.lowStockCount}
                    activeVarieties={stats.activeVarieties}
                />

                {/* 재고 현황 테이블 (Tabs 적용) */}
                <section className="mb-16">
                    <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-6 gap-4">
                        <h2 className="text-2xl font-serif font-bold text-latte-900 flex items-center gap-2">
                            <Package className="w-6 h-6 text-latte-400" />
                            현재 재고 현황
                        </h2>
                        <Button
                            onClick={() => router.push('/inventory/inbound')}
                            className="bg-latte-900 text-white hover:bg-latte-800 shadow-sm"
                        >
                            <FileText className="w-4 h-4 mr-2" />
                            명세서 입고 (OCR)
                        </Button>
                    </div>

                    <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full">
                        <div className="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
                            <TabsList className="bg-white/60 backdrop-blur-md p-1 rounded-full border border-latte-200 shadow-sm h-auto inline-flex">
                                <TabsTrigger
                                    value="all"
                                    className="rounded-full px-4 py-2 text-sm data-[state=active]:bg-latte-900 data-[state=active]:text-white transition-all"
                                >
                                    전체 보기
                                </TabsTrigger>
                                <TabsTrigger
                                    value="green"
                                    className="rounded-full px-4 py-2 text-sm data-[state=active]:bg-green-600 data-[state=active]:text-white transition-all"
                                >
                                    생두 (Green)
                                </TabsTrigger>
                                <TabsTrigger
                                    value="roasted"
                                    className="rounded-full px-4 py-2 text-sm data-[state=active]:bg-latte-600 data-[state=active]:text-white transition-all"
                                >
                                    원두 (Roasted)
                                </TabsTrigger>
                                <TabsTrigger
                                    value="blend"
                                    className="rounded-full px-4 py-2 text-sm data-[state=active]:bg-amber-600 data-[state=active]:text-white transition-all"
                                >
                                    블렌드 (Blend)
                                </TabsTrigger>
                            </TabsList>

                            <motion.div
                                layout
                                className="relative w-full md:w-72 group"
                            >
                                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-latte-400 group-focus-within:text-latte-600 transition-colors" />
                                <Input
                                    placeholder="원두명, 품종, 국가 검색..."
                                    value={beanSearch}
                                    onChange={(e) => setBeanSearch(e.target.value)}
                                    className="pl-11 pr-10 h-11 bg-white/80 backdrop-blur-sm border-latte-200 focus:border-latte-400 rounded-full shadow-sm transition-all focus:ring-2 focus:ring-latte-100"
                                />
                                {beanSearch && (
                                    <button
                                        onClick={() => setBeanSearch('')}
                                        className="absolute right-4 top-1/2 -translate-y-1/2 text-latte-400 hover:text-latte-600 focus:outline-none p-1 bg-latte-50 rounded-full"
                                    >
                                        <X className="w-3 h-3" />
                                    </button>
                                )}
                            </motion.div>
                        </div>

                        {['all', 'green', 'roasted', 'blend'].map((tabValue) => (
                            <TabsContent
                                key={tabValue}
                                value={tabValue}
                                className="mt-0 animate-in fade-in slide-in-from-bottom-4 duration-500"
                            >
                                <div className="bg-white rounded-[1em] shadow-sm overflow-hidden border border-latte-200">
                                    <div className="overflow-x-auto">
                                        <table className="min-w-full divide-y divide-latte-100">
                                            <thead className="bg-latte-50/50">
                                                <tr>
                                                    <th className="px-4 md:px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">원두명</th>
                                                    <th className="hidden md:table-cell px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">유형</th>
                                                    <th className="hidden lg:table-cell px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">특징</th>
                                                    <th className="hidden md:table-cell px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">원산지</th>
                                                    <th className="px-4 md:px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">현재 재고</th>
                                                    <th className="px-4 md:px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">상태</th>
                                                    <th className="px-4 md:px-6 py-4 text-right text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">작업</th>
                                                </tr>
                                            </thead>
                                            <tbody className="bg-white divide-y divide-latte-100">
                                                {beans.length === 0 ? (
                                                    <tr>
                                                        <td colSpan={7} className="px-6 py-12">
                                                            {beanSearch ? (
                                                                <MascotStatus
                                                                    variant="search"
                                                                    title="검색 결과가 없습니다"
                                                                    description={`'${beanSearch}'에 일치하는 원두를 찾을 수 없습니다.`}
                                                                    className="border-none shadow-none bg-transparent py-8"
                                                                />
                                                            ) : (
                                                                <MascotStatus
                                                                    variant="empty"
                                                                    title="재고가 없습니다"
                                                                    description="현재 관리 중인 원두 재고가 없습니다. 새로운 원두를 등록하거나 입고 처리를 진행해보세요."
                                                                    className="border-none shadow-none bg-transparent py-8"
                                                                    action={
                                                                        <Button onClick={() => router.push('/beans')} className="mt-4">
                                                                            <Plus className="w-4 h-4 mr-2" /> 새 원두 등록하기
                                                                        </Button>
                                                                    }
                                                                />
                                                            )}
                                                        </td>
                                                    </tr>
                                                ) : beans.map((bean) => (
                                                    <tr key={bean.id} className="hover:bg-latte-50/30 transition-colors">
                                                        <td className="px-4 md:px-6 py-4 whitespace-nowrap text-sm font-bold text-latte-900">
                                                            <div>{bean.name_ko || bean.name}</div>
                                                            {bean.name_en && <div className="text-xs font-normal text-latte-500 font-sans">{bean.name_en}</div>}
                                                        </td>
                                                        <td className="hidden md:table-cell px-6 py-4 whitespace-nowrap text-sm text-latte-500">
                                                            {bean.type === 'GREEN_BEAN' ? <Badge variant="outline" className="border-green-200 text-green-700 bg-green-50">생두</Badge> :
                                                                bean.type === 'BLEND_BEAN' ? <Badge variant="outline" className="border-amber-200 text-amber-700 bg-amber-50">블렌드</Badge> :
                                                                    <Badge variant="outline" className="border-latte-200 text-latte-700 bg-latte-50">원두</Badge>}
                                                        </td>
                                                        <td className="hidden lg:table-cell px-6 py-4 whitespace-nowrap text-sm text-latte-600">
                                                            {bean.roast_profile === 'LIGHT' ? <Badge className="bg-lime-500 hover:bg-lime-600 border-none text-white">신콩(Light)</Badge> :
                                                                bean.roast_profile === 'DARK' ? <Badge className="bg-slate-800 hover:bg-slate-900 border-none text-white">탄콩(Dark)</Badge> :
                                                                    bean.roast_profile === 'MEDIUM' ? <Badge variant="secondary" className="bg-orange-100 text-orange-800 hover:bg-orange-200 border-none">미디엄</Badge> :
                                                                        '-'}
                                                        </td>
                                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-latte-600">{bean.origin_ko || bean.origin || '-'}</td>
                                                        <td className="px-4 md:px-6 py-4 whitespace-nowrap text-sm font-mono text-latte-900 font-bold">{bean.quantity_kg.toFixed(2)} kg</td>
                                                        <td className="px-4 md:px-6 py-4 whitespace-nowrap">
                                                            {bean.quantity_kg < 5 ? <Badge variant="destructive" className="whitespace-nowrap">부족</Badge> :
                                                                bean.quantity_kg < 10 ? <Badge variant="secondary" className="bg-amber-100 text-amber-800 whitespace-nowrap">주의</Badge> :
                                                                    <Badge variant="default" className="bg-green-600 whitespace-nowrap">충분</Badge>}
                                                        </td>
                                                        <td className="px-4 md:px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-1 md:space-x-2">
                                                            <Button size="sm" variant="ghost" onClick={() => openModal(bean, 'IN')} className="text-green-600 hover:bg-green-50 px-2 md:px-3">
                                                                <Plus className="w-4 h-4 md:mr-1" /><span className="hidden md:inline">입고</span>
                                                            </Button>
                                                            <Button size="sm" variant="ghost" onClick={() => openModal(bean, 'OUT')} className="text-red-500 hover:bg-red-50 px-2 md:px-3">
                                                                <Minus className="w-4 h-4 md:mr-1" /><span className="hidden md:inline">출고</span>
                                                            </Button>
                                                        </td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                    {/* Bean Pagination */}
                                    {beans.length > 0 && (
                                        <div className="flex justify-center items-center py-4 gap-2 bg-latte-50/30 border-t border-latte-100">
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={() => updatePage('beanPage', Math.max(1, beanPage - 1))}
                                                disabled={beanPage === 1}
                                            >
                                                이전
                                            </Button>
                                            <span className="text-sm font-medium text-latte-600">
                                                {beanPage} / {beanTotalPages || 1}
                                            </span>
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={() => updatePage('beanPage', Math.min(beanTotalPages || 1, beanPage + 1))}
                                                disabled={beanPage >= (beanTotalPages || 1)}
                                            >
                                                다음
                                            </Button>
                                        </div>
                                    )}
                                </div>
                            </TabsContent>
                        ))}
                    </Tabs>
                </section>

                <Separator className="mb-16 bg-latte-200" />

                {/* 입출고 기록 테이블 */}
                <motion.section
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.2 }}
                >
                    <h2 className="text-2xl font-serif font-bold text-latte-900 mb-2">입출고 기록</h2>

                    {/* 입출고 기록 탭 */}
                    <Tabs value={logTab} onValueChange={handleLogTabChange} className="mb-2">
                        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-[0.5em]">
                            <TabsList className="grid w-full max-w-md grid-cols-3 bg-latte-100">
                                <TabsTrigger value="all">전체</TabsTrigger>
                                <TabsTrigger value="in">입고</TabsTrigger>
                                <TabsTrigger value="out">출고</TabsTrigger>
                            </TabsList>
                            <div className="relative w-full md:w-64">
                                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-latte-400" />
                                <Input
                                    placeholder="기록 검색 (원두명)..."
                                    value={logSearch}
                                    onChange={(e) => setLogSearch(e.target.value)}
                                    className="pl-9 pr-8 h-10 bg-white border-latte-200 focus:border-latte-400"
                                />
                                {logSearch && (
                                    <button
                                        onClick={() => setLogSearch('')}
                                        className="absolute right-3 top-1/2 -translate-y-1/2 text-latte-400 hover:text-latte-600 focus:outline-none"
                                    >
                                        <X className="w-4 h-4" />
                                    </button>
                                )}
                            </div>
                        </div>

                        {['all', 'in', 'out'].map((tabValue) => (
                            <TabsContent
                                key={tabValue}
                                value={tabValue}
                                className="mt-0 animate-in fade-in slide-in-from-bottom-4 duration-500"
                            >
                                <div className="bg-white rounded-[1em] shadow-sm overflow-hidden border border-latte-200">
                                    <div className="overflow-x-auto">
                                        <table className="min-w-full divide-y divide-latte-100">
                                            <thead className="bg-latte-50/50">
                                                <tr>
                                                    <th className="px-4 md:px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">날짜</th>
                                                    <th className="px-4 md:px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">원두</th>
                                                    <th className="hidden md:table-cell px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">유형</th>
                                                    <th className="px-4 md:px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">수량</th>
                                                    <th className="hidden md:table-cell px-6 py-4 text-left text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">사유</th>
                                                    <th className="hidden md:table-cell px-6 py-4 text-right text-xs font-serif font-bold text-latte-600 uppercase tracking-wider">작업</th>
                                                </tr>
                                            </thead>
                                            <tbody className="bg-white divide-y divide-latte-100">
                                                {logs.length === 0 ? (
                                                    <tr>
                                                        <td colSpan={6} className="px-6 py-12">
                                                            {logSearch ? (
                                                                <MascotStatus
                                                                    variant="search"
                                                                    title="검색 결과가 없습니다"
                                                                    description={`'${logSearch}'에 일치하는 기록을 찾을 수 없습니다.`}
                                                                    className="border-none shadow-none bg-transparent py-8"
                                                                />
                                                            ) : (
                                                                <MascotStatus
                                                                    variant="sleep"
                                                                    title="입출고 기록이 없습니다"
                                                                    description="아직 이력이 없네요. 로스팅이나 판매 기록이 생기면 이곳에서 관리자 냥이가 보여드릴게요!"
                                                                    className="border-none shadow-none bg-transparent py-8"
                                                                />
                                                            )}
                                                        </td>
                                                    </tr>
                                                ) : (
                                                    logs.map((log) => (
                                                        <tr key={log.id} className="hover:bg-latte-50/30 transition-colors">
                                                            <td className="px-4 md:px-6 py-4 whitespace-nowrap text-sm text-latte-500">
                                                                {new Date(log.created_at).toLocaleDateString('ko-KR')}
                                                                <span className="hidden md:inline"> {new Date(log.created_at).toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })}</span>
                                                            </td>
                                                            <td className="px-4 md:px-6 py-4 whitespace-nowrap text-sm font-medium text-latte-900">
                                                                <div>{log.bean?.name_ko || beans.find(b => b.id === log.bean_id)?.name_ko || log.bean?.name || getBeanName(log.bean_id)}</div>
                                                                {(log.bean?.name_en || beans.find(b => b.id === log.bean_id)?.name_en) && (
                                                                    <div className="text-xs font-normal text-latte-500 font-sans mt-0.5">
                                                                        {log.bean?.name_en || beans.find(b => b.id === log.bean_id)?.name_en}
                                                                    </div>
                                                                )}
                                                            </td>
                                                            <td className="hidden md:table-cell px-6 py-4 whitespace-nowrap">
                                                                <Badge variant={log.change_amount >= 0 ? 'default' : 'destructive'}
                                                                    className={log.change_amount >= 0 ? 'bg-green-600' : ''}>
                                                                    {log.change_amount >= 0 ? '입고' : '출고'}
                                                                </Badge>
                                                            </td>
                                                            <td className="px-4 md:px-6 py-4 whitespace-nowrap text-sm font-mono font-bold text-latte-900">
                                                                {log.change_amount > 0 ? '+' : ''}{log.change_amount.toFixed(1)} kg
                                                            </td>
                                                            <td className="hidden md:table-cell px-6 py-4 whitespace-nowrap text-sm text-latte-500">
                                                                {log.notes || '-'}
                                                            </td>
                                                            <td className="hidden md:table-cell px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                                                                <Button size="icon" variant="ghost" onClick={() => openEditModal(log)} className="text-latte-400 hover:bg-latte-100">
                                                                    <Edit2 className="w-4 h-4" />
                                                                </Button>
                                                                <Button size="icon" variant="ghost" onClick={() => handleDelete(log.id)} className="text-latte-400 hover:text-red-600 hover:bg-red-50">
                                                                    <Trash2 className="w-4 h-4" />
                                                                </Button>
                                                            </td>
                                                        </tr>
                                                    ))
                                                )}
                                            </tbody>
                                        </table>
                                    </div>
                                    {/* Logs Pagination */}
                                    {logs.length > 0 && (
                                        <div className="flex justify-center items-center py-4 gap-2 bg-latte-50/30 border-t border-latte-100">
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={() => updatePage('logPage', Math.max(1, logPage - 1))}
                                                disabled={logPage === 1}
                                            >
                                                이전
                                            </Button>
                                            <span className="text-sm font-medium text-latte-600">
                                                {logPage} / {logTotalPages || 1}
                                            </span>
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={() => updatePage('logPage', Math.min(logTotalPages || 1, logPage + 1))}
                                                disabled={logPage >= (logTotalPages || 1)}
                                            >
                                                다음
                                            </Button>
                                        </div>
                                    )}
                                </div>
                            </TabsContent>
                        ))}
                    </Tabs>
                </motion.section>

                {/* 입출고 등록 Modal */}
                {showModal && selectedBean && (
                    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 animate-in fade-in duration-200 p-4">
                        <div className="bg-white rounded-[2rem] p-6 md:p-8 w-full max-w-md shadow-2xl scale-100 animate-in zoom-in-95 duration-200 border border-latte-200">
                            <div className="flex justify-between items-center mb-6">
                                <h2 className="text-xl md:text-2xl font-serif font-bold text-latte-900">
                                    {transactionType === 'IN' ? '입고' : '출고'} 처리
                                </h2>
                                <Button variant="ghost" size="icon" onClick={closeModal} className="rounded-full hover:bg-latte-100">
                                    <X className="w-5 h-5 text-latte-500" />
                                </Button>
                            </div>

                            <div className="bg-latte-50 p-4 rounded-xl mb-6">
                                <p className="text-latte-600 text-sm">
                                    원두: <span className="font-bold text-latte-900 block text-lg">{selectedBean.name}</span>
                                </p>
                                <div className="mt-2 text-latte-600 text-sm">
                                    현재 재고: <span className="font-mono font-bold text-latte-900">{selectedBean.quantity_kg.toFixed(1)} kg</span>
                                </div>
                            </div>

                            <form onSubmit={handleSubmit} className="space-y-6">
                                <div>
                                    <label className="block text-sm font-medium text-latte-700 mb-2">
                                        수량 (kg) *
                                    </label>
                                    <Input
                                        type="number"
                                        required
                                        min="0.1"
                                        step="0.1"
                                        value={quantity}
                                        onChange={(e) => setQuantity(e.target.value)}
                                        placeholder="예: 10.0"
                                        className="font-mono text-lg"
                                        autoFocus
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-latte-700 mb-2">
                                        사유
                                    </label>
                                    <Input
                                        type="text"
                                        value={reason}
                                        onChange={(e) => setReason(e.target.value)}
                                        placeholder="예: 신규 구매, 로스팅 사용"
                                    />
                                </div>

                                <div className="flex justify-end gap-3 mt-8">
                                    <Button
                                        type="button"
                                        variant="outline"
                                        onClick={closeModal}
                                    >
                                        취소
                                    </Button>
                                    <Button
                                        type="submit"
                                        disabled={submitting}
                                        className={`${transactionType === 'IN'
                                            ? 'bg-green-600 hover:bg-green-700'
                                            : 'bg-red-600 hover:bg-red-700'
                                            } text-white`}
                                    >
                                        {submitting ? '처리 중...' : '확인'}
                                    </Button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}

                {/* 입출고 수정 Modal */}
                {showEditModal && selectedLog && (
                    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 animate-in fade-in duration-200 p-4">
                        <div className="bg-white rounded-[2rem] p-6 md:p-8 w-full max-w-md shadow-2xl scale-100 animate-in zoom-in-95 duration-200 border border-latte-200">
                            <div className="flex justify-between items-center mb-6">
                                <h2 className="text-xl md:text-2xl font-serif font-bold text-latte-900">
                                    수량/사유 수정
                                </h2>
                                <Button variant="ghost" size="icon" onClick={closeEditModal} className="rounded-full hover:bg-latte-100">
                                    <X className="w-5 h-5 text-latte-500" />
                                </Button>
                            </div>

                            <form onSubmit={handleEdit} className="space-y-6">
                                <div>
                                    <label className="block text-sm font-medium text-latte-700 mb-2">
                                        수량 (kg) *
                                    </label>
                                    <Input
                                        type="number"
                                        required
                                        min="0.1"
                                        step="0.1"
                                        value={editQuantity}
                                        onChange={(e) => setEditQuantity(e.target.value)}
                                        placeholder="예: 10.0"
                                        className="font-mono text-lg"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-latte-700 mb-2">
                                        사유
                                    </label>
                                    <Input
                                        type="text"
                                        value={editReason}
                                        onChange={(e) => setEditReason(e.target.value)}
                                        placeholder="예: 사유 수정"
                                    />
                                </div>

                                <div className="flex justify-end gap-3 mt-8">
                                    <Button
                                        type="button"
                                        variant="outline"
                                        onClick={closeEditModal}
                                    >
                                        취소
                                    </Button>
                                    <Button
                                        type="submit"
                                        disabled={submitting}
                                    >
                                        {submitting ? '처리 중...' : '수정 완료'}
                                    </Button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
