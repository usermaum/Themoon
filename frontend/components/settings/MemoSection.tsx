'use client';

import { useState } from 'react';
import useSWR from 'swr';
import { SettingsAPI, Memo } from '@/lib/api/settings';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { MessageSquare, Send, Trash2, Clock, Loader2, ChevronDown, ChevronUp, Circle, CheckCircle2, MessageCircle, MoreHorizontal } from 'lucide-react';
import { format } from 'date-fns';
import { MorphingButton } from '@/components/ui/morphing-button';
import { toast } from '@/hooks/use-toast';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover";
import { Badge } from "@/components/ui/badge";

const StatusBadge = ({ status }: { status?: string }) => {
    switch (status) {
        case 'done':
            return <Badge className="bg-emerald-100 text-emerald-700 hover:bg-emerald-100 border-0 px-2 py-0.5">완료</Badge>;
        case 'in_progress':
            return <Badge className="bg-amber-100 text-amber-700 hover:bg-amber-100 border-0 px-2 py-0.5">진행중</Badge>;
        case 'read':
            return <Badge className="bg-blue-100 text-blue-700 hover:bg-blue-100 border-0 px-2 py-0.5">읽음</Badge>;
        default:
            return <Badge className="bg-slate-100 text-slate-500 hover:bg-slate-100 border-0 px-2 py-0.5">안읽음</Badge>;
    }
};

const MemoItem = ({ memo, onDelete, onUpdate }: { memo: Memo, onDelete: (id: number) => void, onUpdate: () => void }) => {
    const [isExpanded, setIsExpanded] = useState(false);
    const [isReplying, setIsReplying] = useState(false);
    const [replyContent, setReplyContent] = useState(memo.admin_reply || '');

    const handleStatusUpdate = async (newStatus: string) => {
        try {
            await SettingsAPI.updateMemo(memo.id, { status: newStatus });
            onUpdate();
            toast({ title: '상태가 업데이트되었습니다.' });
        } catch (e) {
            toast({ title: '상태 업데이트 실패', variant: 'destructive' });
        }
    };

    const handleSaveReply = async () => {
        try {
            // 답변 달면 자동으로 'done'으로 갈지 여부는 선택이지만, 일단 답변 등록만 함.
            await SettingsAPI.updateMemo(memo.id, { admin_reply: replyContent });
            setIsReplying(false);
            onUpdate();
            toast({ title: '답변이 등록되었습니다.' });
        } catch (e) {
            toast({ title: '답변 등록 실패', variant: 'destructive' });
        }
    };

    const isLongContent = memo.content.length > 50 || memo.content.includes('\n');

    return (
        <motion.div
            layout
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className={`group relative bg-white border border-latte-100 p-5 rounded-2xl shadow-sm transition-all hover:shadow-md ${memo.status === 'done' ? 'opacity-80 bg-gray-50' : ''}`}
        >
            <div className="flex justify-between items-start gap-4 mb-3">
                <div className="flex items-center gap-2">
                    <StatusBadge status={memo.status} />
                    <span className="text-[10px] text-latte-400 font-mono flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {format(new Date(memo.created_at), 'yyyy-MM-dd HH:mm')}
                    </span>
                </div>

                <div className="flex items-center gap-0">
                    <Popover>
                        <PopoverTrigger asChild>
                            <Button variant="ghost" size="icon" className="h-7 w-7 text-latte-300 hover:text-latte-600">
                                <MoreHorizontal className="w-4 h-4" />
                            </Button>
                        </PopoverTrigger>
                        <PopoverContent align="end" className="w-36 p-1 bg-white border-latte-200">
                            <div className="flex flex-col space-y-0.5">
                                <Button variant="ghost" size="sm" className="justify-start h-7 text-xs font-normal hover:bg-latte-50" onClick={() => handleStatusUpdate('pending')}>
                                    <Circle className="w-3 h-3 mr-2 text-slate-400" /> 안읽음
                                </Button>
                                <Button variant="ghost" size="sm" className="justify-start h-7 text-xs font-normal hover:bg-latte-50" onClick={() => handleStatusUpdate('read')}>
                                    <CheckCircle2 className="w-3 h-3 mr-2 text-blue-500" /> 읽음 표시
                                </Button>
                                <Button variant="ghost" size="sm" className="justify-start h-7 text-xs font-normal hover:bg-latte-50" onClick={() => handleStatusUpdate('in_progress')}>
                                    <Loader2 className="w-3 h-3 mr-2 text-amber-500" /> 진행중
                                </Button>
                                <Button variant="ghost" size="sm" className="justify-start h-7 text-xs font-normal hover:bg-latte-50" onClick={() => handleStatusUpdate('done')}>
                                    <CheckCircle2 className="w-3 h-3 mr-2 text-emerald-500" /> 완료 처리
                                </Button>
                            </div>
                        </PopoverContent>
                    </Popover>

                    <Button variant="ghost" size="icon" className="h-7 w-7 text-latte-300 hover:text-red-500" onClick={() => onDelete(memo.id)}>
                        <Trash2 className="w-4 h-4" />
                    </Button>
                </div>
            </div>

            <div className="relative mb-2">
                <p className={`text-sm text-latte-800 leading-relaxed whitespace-pre-wrap ${!isExpanded ? 'line-clamp-1' : ''}`}>
                    {memo.content}
                </p>
                {isLongContent && (
                    <button
                        onClick={() => setIsExpanded(!isExpanded)}
                        className="text-xs text-latte-500 hover:text-latte-700 font-medium mt-1 flex items-center gap-1"
                    >
                        {isExpanded ? <><ChevronUp className="w-3 h-3" />접기</> : <><ChevronDown className="w-3 h-3" />더보기</>}
                    </button>
                )}
            </div>

            {/* Admin Reply Section */}
            {(memo.admin_reply || isReplying) && (
                <div className="mt-4 bg-latte-50/80 rounded-xl p-3 text-sm border border-latte-100/50">
                    <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2 text-latte-600 font-semibold text-xs">
                            <MessageCircle className="w-3 h-3" /> 관리자 답변
                        </div>
                        {isReplying ? (
                            <Button size="sm" variant="ghost" className="h-5 text-[10px]" onClick={() => setIsReplying(false)}>취소</Button>
                        ) : (
                            <Button size="sm" variant="ghost" className="h-5 text-[10px] opacity-0 group-hover:opacity-100 transition-opacity" onClick={() => setIsReplying(true)}>수정</Button>
                        )}
                    </div>

                    {isReplying ? (
                        <div className="space-y-2 animate-in fade-in zoom-in-95 duration-200">
                            <Textarea
                                value={replyContent}
                                onChange={(e) => setReplyContent(e.target.value)}
                                className="text-xs bg-white min-h-[60px] border-latte-200 focus:border-latte-400"
                                placeholder="작업 완료 여부나 피드백을 입력하세요..."
                            />
                            <div className="flex justify-end gap-2">
                                <Button size="sm" className="h-7 text-xs bg-latte-900" onClick={handleSaveReply}>저장</Button>
                            </div>
                        </div>
                    ) : (
                        <p className="text-latte-700 whitespace-pre-wrap text-[13px]">{memo.admin_reply}</p>
                    )}
                </div>
            )}

            {!memo.admin_reply && !isReplying && (
                <div className="mt-1 opacity-0 group-hover:opacity-100 transition-opacity flex justify-end">
                    <Button variant="ghost" size="sm" className="text-xs text-latte-400 h-6 hover:text-latte-600 hover:bg-latte-50" onClick={() => setIsReplying(true)}>
                        <MessageSquare className="w-3 h-3 mr-1" /> 답변 달기
                    </Button>
                </div>
            )}
        </motion.div>
    );
};

export default function MemoSection() {
    const { data: memos, mutate, isLoading } = useSWR<Memo[]>('/settings/memos', SettingsAPI.getMemos);
    const [content, setContent] = useState('');
    const [status, setStatus] = useState<'idle' | 'loading' | 'success'>('idle');

    const handleSubmit = async () => {
        if (!content.trim()) return;

        try {
            setStatus('loading');
            await SettingsAPI.addMemo(content);
            setContent('');
            mutate(); // Refresh list
            toast({ title: '요청 사항 등록 완료', description: '목록에 추가되었습니다.' });
            setStatus('success');
            setTimeout(() => setStatus('idle'), 2000);
        } catch (error) {
            console.error('Failed to add memo:', error);
            toast({ title: '등록 실패', description: '잠시 후 다시 시도해주세요.', variant: 'destructive' });
            setStatus('idle');
        }
    };

    const handleDelete = async (id: number) => {
        try {
            await SettingsAPI.deleteMemo(id);
            mutate();
            toast({ title: '삭제 완료' });
        } catch (error) {
            console.error('Failed to delete memo:', error);
            toast({ title: '삭제 실패', variant: 'destructive' });
        }
    };

    return (
        <Card className="border-latte-200 shadow-sm overflow-hidden rounded-[1em] bg-gradient-to-br from-white to-latte-50/30">
            <CardHeader className="bg-white/50 border-b border-latte-100 pb-4">
                <div className="flex items-center gap-2">
                    <div className="p-2 bg-latte-100 rounded-lg text-latte-600">
                        <MessageSquare className="w-5 h-5" />
                    </div>
                    <div>
                        <CardTitle className="text-lg font-serif text-latte-900">요청 사항 및 피드백</CardTitle>
                        <CardDescription className="text-latte-500">
                            개발자에게 기능을 요청하거나 작업 진행 상황을 관리하세요.
                        </CardDescription>
                    </div>
                </div>
            </CardHeader>
            <CardContent className="p-6">
                <div className="space-y-8">
                    {/* Input Area */}
                    <div className="space-y-4 font-sans">
                        <Textarea
                            placeholder="새로운 요청 사항을 입력하세요..."
                            className="min-h-[120px] bg-white border-latte-200 focus:border-latte-400 rounded-xl resize-none p-5 text-latte-900 shadow-sm focus:shadow-md transition-all duration-300"
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                        />
                        <div className="flex justify-end">
                            <MorphingButton
                                status={status}
                                idleText="등록하기"
                                icon={Send}
                                onClick={handleSubmit}
                                disabled={!content.trim()}
                                className="bg-latte-900 hover:bg-black text-white px-8 rounded-xl h-11 shadow-lg shadow-latte-200/50 transition-all hover:scale-[1.02] active:scale-[0.98]"
                            />
                        </div>
                    </div>

                    <div className="border-t border-latte-100 pt-6">
                        <h3 className="text-sm font-bold text-latte-600 mb-4 flex items-center justify-between">
                            <span className="flex items-center gap-2">
                                최근 요청 목록
                                <span className="text-xs font-normal text-latte-400 bg-latte-100 px-2 py-0.5 rounded-full">
                                    {memos?.length || 0}
                                </span>
                            </span>
                            {isLoading && <Loader2 className="w-3 h-3 animate-spin text-latte-300" />}
                        </h3>

                        <div className="space-y-4 max-h-[600px] overflow-y-auto pr-2 pb-8 pt-1 scrollbar-thin">
                            {!memos || memos.length === 0 ? (
                                <div className="text-center py-12 text-latte-400 text-sm italic bg-latte-50/50 rounded-2xl border border-dashed border-latte-200">
                                    아직 등록된 요청사항이 없습니다.
                                </div>
                            ) : (
                                <AnimatePresence initial={false}>
                                    {memos.slice().reverse().map((memo) => (
                                        <MemoItem
                                            key={memo.id}
                                            memo={memo}
                                            onDelete={handleDelete}
                                            onUpdate={() => mutate()}
                                        />
                                    ))}
                                </AnimatePresence>
                            )}
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
