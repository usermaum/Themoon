'use client'

import { useState, useEffect } from 'react'
import { Bean, BeanAPI, InventoryLog, InventoryLogAPI, InventoryLogCreateData } from '@/lib/api'
import PageHero from '@/components/ui/PageHero'

export default function InventoryPage() {
    const [beans, setBeans] = useState<Bean[]>([])
    const [logs, setLogs] = useState<InventoryLog[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

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

    const fetchData = async () => {
        try {
            setLoading(true)
            const [beansData, logsData] = await Promise.all([
                BeanAPI.getAll({ size: 100 }),
                InventoryLogAPI.getAll({ limit: 50 })
            ])
            setBeans(beansData.items)
            setLogs(logsData)
            setError(null)
        } catch (err) {
            console.error('Failed to fetch data:', err)
            setError('데이터를 불러오는데 실패했습니다.')
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchData()
    }, [])

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
        setEditQuantity(Math.abs(log.quantity_change).toString())
        setEditReason(log.reason || '')
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
            transaction_type: transactionType,
            quantity_change: transactionType === 'IN' ? quantityNum : -quantityNum,
            reason: reason || undefined,
        }

        try {
            setSubmitting(true)
            await InventoryLogAPI.create(logData)
            await fetchData()
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

        const finalQuantity = selectedLog.transaction_type === 'IN' ? quantityNum : -quantityNum

        try {
            setSubmitting(true)
            await InventoryLogAPI.update(selectedLog.id, finalQuantity, editReason || undefined)
            await fetchData()
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
            await fetchData()
        } catch (err: any) {
            console.error('Failed to delete inventory log:', err)
            alert(err.response?.data?.detail || '삭제에 실패했습니다.')
        }
    }

    const getBeanName = (beanId: number) => {
        const bean = beans.find(b => b.id === beanId)
        return bean ? bean.name : `Bean #${beanId}`
    }

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <PageHero
                title="재고 관리"
                description="원두의 입출고를 관리하고 현재 재고 현황을 확인하세요"
                icon="📦"
                backgroundImage="/inventory_background.png"
            />

            <div className="container mx-auto px-4 py-8">
                {error && (
                    <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-6">
                        {error}
                    </div>
                )}

                {loading ? (
                    <div className="text-center py-12 text-gray-500">
                        데이터를 불러오는 중입니다...
                    </div>
                ) : (
                    <>
                        {/* 재고 현황 테이블 */}
                        <section className="mb-8">
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">현재 재고 현황</h2>
                            <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden border border-gray-200 dark:border-gray-700">
                                <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                                    <thead className="bg-gray-50 dark:bg-gray-900">
                                        <tr>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                원두명
                                            </th>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                원산지
                                            </th>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                현재 재고
                                            </th>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                상태
                                            </th>
                                            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                작업
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                                        {beans.map((bean) => (
                                            <tr key={bean.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                                                    {bean.name}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                                    {bean.origin}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                                    <span className="font-semibold">{bean.quantity_kg.toFixed(1)} kg</span>
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap">
                                                    {bean.quantity_kg < 5 ? (
                                                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                                                            재고 부족
                                                        </span>
                                                    ) : bean.quantity_kg < 10 ? (
                                                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                                                            주의
                                                        </span>
                                                    ) : (
                                                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                                            충분
                                                        </span>
                                                    )}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                                                    <button
                                                        onClick={() => openModal(bean, 'IN')}
                                                        className="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-300"
                                                    >
                                                        입고
                                                    </button>
                                                    <button
                                                        onClick={() => openModal(bean, 'OUT')}
                                                        className="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                                                    >
                                                        출고
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </section>

                        {/* 입출고 기록 테이블 */}
                        <section>
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">입출고 기록</h2>
                            <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden border border-gray-200 dark:border-gray-700">
                                <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                                    <thead className="bg-gray-50 dark:bg-gray-900">
                                        <tr>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                날짜
                                            </th>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                원두
                                            </th>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                유형
                                            </th>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                수량
                                            </th>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                사유
                                            </th>
                                            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                작업
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                                        {logs.length === 0 ? (
                                            <tr>
                                                <td colSpan={6} className="px-6 py-12 text-center text-gray-500">
                                                    입출고 기록이 없습니다.
                                                </td>
                                            </tr>
                                        ) : (
                                            logs.map((log) => (
                                                <tr key={log.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                        {new Date(log.created_at).toLocaleString('ko-KR')}
                                                    </td>
                                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                                        {getBeanName(log.bean_id)}
                                                    </td>
                                                    <td className="px-6 py-4 whitespace-nowrap">
                                                        <span className={`px-2 py-1 text-xs font-semibold rounded-full ${log.transaction_type === 'IN'
                                                                ? 'bg-green-100 text-green-800'
                                                                : 'bg-red-100 text-red-800'
                                                            }`}>
                                                            {log.transaction_type === 'IN' ? '입고' : '출고'}
                                                        </span>
                                                    </td>
                                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                                        {log.quantity_change > 0 ? '+' : ''}{log.quantity_change.toFixed(1)} kg
                                                    </td>
                                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                        {log.reason || '-'}
                                                    </td>
                                                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                                                        <button
                                                            onClick={() => openEditModal(log)}
                                                            className="text-indigo-600 hover:text-indigo-900"
                                                        >
                                                            수정
                                                        </button>
                                                        <button
                                                            onClick={() => handleDelete(log.id)}
                                                            className="text-red-600 hover:text-red-900"
                                                        >
                                                            삭제
                                                        </button>
                                                    </td>
                                                </tr>
                                            ))
                                        )}
                                    </tbody>
                                </table>
                            </div>
                        </section>
                    </>
                )}

                {/* 입출고 등록 Modal */}
                {showModal && selectedBean && (
                    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md">
                            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
                                {transactionType === 'IN' ? '입고' : '출고'} 처리
                            </h2>
                            <p className="text-gray-600 dark:text-gray-400 mb-4">
                                원두: <span className="font-semibold">{selectedBean.name}</span>
                                <br />
                                현재 재고: <span className="font-semibold">{selectedBean.quantity_kg.toFixed(1)} kg</span>
                            </p>

                            <form onSubmit={handleSubmit} className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                        수량 (kg) *
                                    </label>
                                    <input
                                        type="number"
                                        required
                                        min="0.1"
                                        step="0.1"
                                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                                        value={quantity}
                                        onChange={(e) => setQuantity(e.target.value)}
                                        placeholder="예: 10.0"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                        사유
                                    </label>
                                    <input
                                        type="text"
                                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                                        value={reason}
                                        onChange={(e) => setReason(e.target.value)}
                                        placeholder="예: 신규 구매, 로스팅 사용"
                                    />
                                </div>

                                <div className="flex justify-end gap-3 mt-6">
                                    <button
                                        type="button"
                                        onClick={closeModal}
                                        className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-700"
                                    >
                                        취소
                                    </button>
                                    <button
                                        type="submit"
                                        disabled={submitting}
                                        className={`px-4 py-2 rounded-lg text-white ${transactionType === 'IN'
                                                ? 'bg-indigo-600 hover:bg-indigo-700'
                                                : 'bg-red-600 hover:bg-red-700'
                                            } disabled:opacity-50 disabled:cursor-not-allowed`}
                                    >
                                        {submitting ? '처리 중...' : '확인'}
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}

                {/* 입출고 수정 Modal */}
                {showEditModal && selectedLog && (
                    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md">
                            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
                                입출고 기록 수정
                            </h2>
                            <p className="text-gray-600 dark:text-gray-400 mb-4">
                                원두: <span className="font-semibold">{getBeanName(selectedLog.bean_id)}</span>
                                <br />
                                유형: <span className="font-semibold">{selectedLog.transaction_type === 'IN' ? '입고' : '출고'}</span>
                            </p>

                            <form onSubmit={handleEdit} className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                        수량 (kg) *
                                    </label>
                                    <input
                                        type="number"
                                        required
                                        min="0.1"
                                        step="0.1"
                                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                                        value={editQuantity}
                                        onChange={(e) => setEditQuantity(e.target.value)}
                                        placeholder="예: 10.0"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                        사유
                                    </label>
                                    <input
                                        type="text"
                                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-transparent"
                                        value={editReason}
                                        onChange={(e) => setEditReason(e.target.value)}
                                        placeholder="예: 신규 구매, 로스팅 사용"
                                    />
                                </div>

                                <div className="flex justify-end gap-3 mt-6">
                                    <button
                                        type="button"
                                        onClick={closeEditModal}
                                        className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-700"
                                    >
                                        취소
                                    </button>
                                    <button
                                        type="submit"
                                        disabled={submitting}
                                        className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
                                    >
                                        {submitting ? '처리 중...' : '수정 완료'}
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
