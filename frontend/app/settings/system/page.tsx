'use client';

import React, { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { RefreshCw, Server, Activity, CheckCircle2, Loader2, Cpu, HardDrive, Database, Send } from 'lucide-react';
import { toast } from '@/hooks/use-toast';
import { Button } from '@/components/ui/button';
import { SettingsAPI, SystemStatus } from '@/lib/api/settings';
import { MorphingButton } from '@/components/ui/morphing-button';
import MascotStatus from '@/components/ui/mascot-status';
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
import MemoSection from '@/components/settings/MemoSection';

const WaterDropEffect = () => {
    const [mounted, setMounted] = useState(false);
    useEffect(() => setMounted(true), []);

    if (!mounted) return null;

    // 물방울 데이터 생성 (밀도 대폭 증가 및 크기 다양화)
    const drops = Array.from({ length: 180 }).map((_, i) => {
        const size = Math.random() < 0.7 ? Math.random() * 3 + 2 : Math.random() * 8 + 4; // 작은 물방울(mist)과 큰 물방울 혼합
        return {
            id: i,
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            opacity: Math.random() * 0.5 + 0.2,
            duration: Math.random() * 20 + 15,
            delay: Math.random() * -20, // 시작 시점 랜덤화하여 이미 깔려있는 느낌
            size: size,
            jitter: Math.random() * 6 - 3,
            isMoving: Math.random() < 0.3, // 일부만 움직이게 하여 리얼함 유도
        };
    });

    return (
        <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
            {drops.map((drop) => (
                <motion.div
                    key={drop.id}
                    initial={{
                        y: drop.isMoving ? -100 : 0,
                        opacity: 0,
                    }}
                    animate={drop.isMoving ? {
                        y: ['0vh', '110vh'],
                        opacity: [0, drop.opacity, drop.opacity, 0],
                        x: [0, drop.jitter, 0, -drop.jitter, 0],
                    } : {
                        opacity: [0, drop.opacity, drop.opacity],
                    }}
                    transition={{
                        duration: drop.isMoving ? drop.duration : 2,
                        repeat: drop.isMoving ? Infinity : 0,
                        ease: "linear",
                        delay: drop.delay,
                    }}
                    className="absolute rounded-full"
                    style={{
                        left: drop.left,
                        top: drop.isMoving ? undefined : drop.top,
                        width: `${drop.size}px`,
                        height: `${drop.size * (drop.isMoving ? 1.4 : 1.1)}px`,
                        background: 'radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.4) 0%, rgba(255, 255, 255, 0.1) 60%, rgba(0, 0, 0, 0.05) 100%)',
                        boxShadow: `
                            inset -1px -1px 2px rgba(255, 255, 255, 0.3),
                            inset 1px 1px 2px rgba(0, 0, 0, 0.1),
                            0 1px 2px rgba(0, 0, 0, 0.1)
                        `,
                        backdropFilter: 'blur(0.5px)',
                    }}
                />
            ))}
        </div>
    );
};

export default function SystemSettingsPage() {
    const [isRestarting, setIsRestarting] = useState(false);
    const [isBackendRestarting, setIsBackendRestarting] = useState(false);
    const [status, setStatus] = useState<SystemStatus | null>(null);
    const [isMounted, setIsMounted] = useState(false);
    const [saveStatus, setSaveStatus] = useState<Record<string, 'idle' | 'loading' | 'success'>>({
        restart: 'idle',
        backendRestart: 'idle'
    });

    useEffect(() => {
        setIsMounted(true);
        const fetchStatus = async () => {
            try {
                const data = await SettingsAPI.getSystemStatus();
                setStatus(data);
            } catch (error) {
                console.error('Failed to fetch status:', error);
            }
        };

        fetchStatus();
        const interval = setInterval(fetchStatus, 5000);
        return () => clearInterval(interval);
    }, []);

    const handleRestart = async () => {
        try {
            setIsRestarting(true);
            await SettingsAPI.restartFrontend();
        } catch (error: any) {
            console.error('Failed to restart:', error);
            setIsRestarting(false);
            toast({
                title: '재시작 요청 실패',
                description: error.response?.data?.detail || '잠시 후 다시 시도해 주세요.',
                variant: 'destructive'
            });
        }
    };

    const handleRestartBackend = async () => {
        try {
            setIsBackendRestarting(true);
            await SettingsAPI.restartBackend();
        } catch (error: any) {
            console.error('Failed to restart backend:', error);
            setIsBackendRestarting(false);
            toast({
                title: '백엔드 재시작 요청 실패',
                description: error.response?.data?.detail || '잠시 후 다시 시도해 주세요.',
                variant: 'destructive'
            });
        }
    };

    // Polling logic when restarting
    useEffect(() => {
        if (!isRestarting) return;

        const checkServer = async () => {
            try {
                const res = await fetch(window.location.href, { method: 'GET', cache: 'no-store' });
                if (res.ok) {
                    window.location.reload();
                }
            } catch (e) {
                // Still down, keep waiting
            }
        };

        const interval = setInterval(checkServer, 2000);
        return () => clearInterval(interval);
    }, [isRestarting]);

    // Polling logic for backend restart
    useEffect(() => {
        if (!isBackendRestarting) return;

        const checkBackend = async () => {
            try {
                await SettingsAPI.getSystemStatus();
                window.location.reload();
            } catch (e) {
                // Still down
            }
        };

        const interval = setInterval(checkBackend, 3000);
        return () => clearInterval(interval);
    }, [isBackendRestarting]);

    return (
        <div className="bg-transparent font-sans">
            <main className="space-y-8">

                {/* Status Dashboard */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                    <Card className="bg-white border-latte-100 shadow-sm rounded-[1em] p-4 flex flex-col items-center text-center">
                        <div className="w-10 h-10 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center mb-3">
                            <Activity className="w-5 h-5" />
                        </div>
                        <h3 className="text-latte-900 font-bold text-sm mb-0.5">System</h3>
                        <p className="text-emerald-600 text-[13px] font-medium flex items-center gap-1">
                            <CheckCircle2 className="w-3 h-3" /> Operational
                        </p>
                    </Card>

                    <Card className="bg-white border-latte-100 shadow-sm rounded-[1em] p-4 flex flex-col items-center text-center">
                        <div className="w-10 h-10 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center mb-3">
                            <Cpu className="w-5 h-5" />
                        </div>
                        <h3 className="text-latte-900 font-bold text-sm mb-0.5">CPU Usage</h3>
                        <p className="text-latte-500 text-[13px]">{status?.cpu.usage_percent ?? '0'}%</p>
                    </Card>

                    <Card className="bg-white border-latte-100 shadow-sm rounded-[1em] p-4 flex flex-col items-center text-center">
                        <div className="w-10 h-10 rounded-full bg-violet-50 text-violet-600 flex items-center justify-center mb-3">
                            <HardDrive className="w-5 h-5" />
                        </div>
                        <h3 className="text-latte-900 font-bold text-sm mb-0.5">Memory</h3>
                        <p className="text-latte-500 text-[13px]">{status?.memory.usage_percent ?? '0'}%</p>
                    </Card>

                    <Card className="bg-white border-latte-100 shadow-sm rounded-[1em] p-4 flex flex-col items-center text-center">
                        <div className="w-10 h-10 rounded-full bg-amber-50 text-amber-600 flex items-center justify-center mb-3">
                            <Database className="w-5 h-5" />
                        </div>
                        <h3 className="text-latte-900 font-bold text-sm mb-0.5">Disk Free</h3>
                        <p className="text-latte-500 text-[13px]">{status?.disk.free_gb.toFixed(1) ?? '0'} GB</p>
                    </Card>

                    <Card className="bg-white border-latte-100 shadow-sm rounded-[1em] p-4 flex flex-col items-center text-center">
                        <div className="w-10 h-10 rounded-full bg-slate-50 text-slate-600 flex items-center justify-center mb-3">
                            <Server className="w-5 h-5" />
                        </div>
                        <h3 className="text-latte-900 font-bold text-sm mb-0.5">Platform</h3>
                        <p className="text-latte-500 text-[13px]">Next.js / FastAPI</p>
                    </Card>
                </div>

                {/* Memo/Request Section */}
                <div className="animate-in fade-in slide-in-from-bottom-4 duration-700 delay-200">
                    <MemoSection />
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Frontend Server Restart Card */}
                    <Card className="bg-white border-latte-100 shadow-sm overflow-hidden rounded-[1.5em] hover:shadow-md transition-shadow duration-300">
                        <CardHeader className="bg-rose-50/50 border-b border-rose-100/50 pb-6 pt-6">
                            <div className="flex items-center gap-3">
                                <div className="p-2 bg-rose-100 rounded-lg text-rose-600">
                                    <RefreshCw className="w-6 h-6" />
                                </div>
                                <div>
                                    <CardTitle className="text-xl font-bold text-rose-900">프론트엔드 재시작</CardTitle>
                                    <CardDescription className="text-rose-700/80 mt-1">
                                        Frontend Server Restart
                                    </CardDescription>
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent className="p-8 space-y-6">
                            <p className="text-sm text-latte-600 leading-relaxed bg-latte-50 p-4 rounded-xl border border-latte-100">
                                프론트엔드 서버를 완전히 종료하고 재시작합니다.
                                코드 변경사항 반영이나 심각한 오류 발생 시 사용하세요.
                            </p>

                            <div className="flex justify-end">
                                <AlertDialog>
                                    <AlertDialogTrigger asChild>
                                        <MorphingButton
                                            status={saveStatus.restart}
                                            idleText="프론트엔드 재시작"
                                            icon={RefreshCw}
                                            className="bg-white hover:bg-rose-50 text-rose-600 border-rose-200 h-12 w-full text-base font-semibold rounded-xl shadow-sm hover:shadow"
                                        />
                                    </AlertDialogTrigger>
                                    <AlertDialogContent>
                                        <AlertDialogHeader>
                                            <AlertDialogTitle>프론트엔드를 재시작하시겠습니까?</AlertDialogTitle>
                                            <AlertDialogDescription>
                                                프론트엔드 서버가 완전히 종료된 후 다시 시작됩니다.
                                                <br /><br />
                                                <span className="font-bold text-rose-600">
                                                    ⚠️ 주의: 시스템이 잠시 중단되며, 모든 사용자의 접속이 잠시 끊길 수 있습니다.
                                                </span>
                                            </AlertDialogDescription>
                                        </AlertDialogHeader>
                                        <AlertDialogFooter>
                                            <AlertDialogCancel>취소</AlertDialogCancel>
                                            <AlertDialogAction onClick={handleRestart} className="bg-rose-600 hover:bg-rose-700 text-white">
                                                재시작 실행
                                            </AlertDialogAction>
                                        </AlertDialogFooter>
                                    </AlertDialogContent>
                                </AlertDialog>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Backend Server Restart Card */}
                    <Card className="bg-white border-latte-100 shadow-sm overflow-hidden rounded-[1.5em] hover:shadow-md transition-shadow duration-300">
                        <CardHeader className="bg-violet-50/50 border-b border-violet-100/50 pb-6 pt-6">
                            <div className="flex items-center gap-3">
                                <div className="p-2 bg-violet-100 rounded-lg text-violet-600">
                                    <Server className="w-6 h-6" />
                                </div>
                                <div>
                                    <CardTitle className="text-xl font-bold text-violet-900">백엔드 재시작</CardTitle>
                                    <CardDescription className="text-violet-700/80 mt-1">
                                        Restart API Server
                                    </CardDescription>
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent className="p-8 space-y-6">
                            <p className="text-sm text-latte-600 leading-relaxed bg-latte-50 p-4 rounded-xl border border-latte-100">
                                백엔드(API) 서버를 종료하고 재시작합니다.
                                Python 코드 변경사항 반영이나 API 오류 발생 시 사용하세요.
                            </p>

                            <div className="flex justify-end">
                                <AlertDialog>
                                    <AlertDialogTrigger asChild>
                                        <MorphingButton
                                            status={saveStatus.backendRestart}
                                            idleText="API 서버 재시작"
                                            icon={RefreshCw}
                                            className="bg-white hover:bg-violet-50 text-violet-600 border-violet-200 h-12 w-full text-base font-semibold rounded-xl shadow-sm hover:shadow"
                                        />
                                    </AlertDialogTrigger>
                                    <AlertDialogContent>
                                        <AlertDialogHeader>
                                            <AlertDialogTitle>API 서버를 재시작하시겠습니까?</AlertDialogTitle>
                                            <AlertDialogDescription>
                                                백엔드 서버가 종료된 후 다시 시작됩니다.
                                                <br /><br />
                                                <span className="font-bold text-violet-600">
                                                    ⚠️ 주의: 잠시 동안 데이터 저장이 불가능할 수 있으며, 재시작 완료 시 페이지가 새로고침됩니다.
                                                </span>
                                            </AlertDialogDescription>
                                        </AlertDialogHeader>
                                        <AlertDialogFooter>
                                            <AlertDialogCancel>취소</AlertDialogCancel>
                                            <AlertDialogAction onClick={handleRestartBackend} className="bg-violet-600 hover:bg-violet-700 text-white">
                                                재시작 실행
                                            </AlertDialogAction>
                                        </AlertDialogFooter>
                                    </AlertDialogContent>
                                </AlertDialog>
                            </div>
                        </CardContent>
                    </Card>
                </div>

            </main >

            {/* Restart Overlays - Robust Portal Structure */}
            {isMounted && createPortal(
                <AnimatePresence>
                    {isRestarting && (
                        <motion.div
                            key="frontend-restart"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="fixed inset-0 bg-slate-950/90 backdrop-blur-2xl z-[9999] flex flex-col items-center justify-center text-white"
                        >
                            <WaterDropEffect />

                            <motion.div
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.9 }}
                                className="relative z-10 flex flex-col items-center"
                            >
                                <div className="max-w-md w-full">
                                    <MascotStatus
                                        variant="loading"
                                        title="문열어라 냥. 냥 냥."
                                        description="서버가 귀엽게 단장하는 중입니다..."
                                        className="bg-transparent shadow-none"
                                        videoClassName="w-80 h-80 border-white/20 shadow-amber-500/30"
                                        textColor="text-amber-100"
                                    />
                                </div>

                                <div className="mt-12 flex flex-col items-center gap-4">
                                    <div className="flex gap-2">
                                        <div className="w-2 h-2 bg-amber-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
                                        <div className="w-2 h-2 bg-amber-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
                                        <div className="w-2 h-2 bg-amber-400 rounded-full animate-bounce" />
                                    </div>
                                    <Button
                                        variant="outline"
                                        className="bg-white/5 text-white/60 border-white/10 hover:bg-white/10 hover:text-white rounded-full transition-all text-xs"
                                        onClick={() => window.location.reload()}
                                    >
                                        혹시 냥이가 졸고 있나요? 수동 새로고침
                                    </Button>
                                </div>
                            </motion.div>
                        </motion.div>
                    )}

                    {isBackendRestarting && (
                        <motion.div
                            key="backend-restart"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="fixed inset-0 bg-slate-950/90 backdrop-blur-2xl z-[9999] flex flex-col items-center justify-center text-white"
                        >
                            <WaterDropEffect />

                            <motion.div
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.9 }}
                                className="relative z-10 flex flex-col items-center"
                            >
                                <div className="max-w-md w-full">
                                    <MascotStatus
                                        variant="search"
                                        title="관리자 냥이가 일하는 중..."
                                        description="잠시만 기다려주세요 냥!"
                                        className="bg-white/10 border-white/10 backdrop-blur-3xl shadow-violet-500/10"
                                    />
                                </div>

                                <div className="mt-12 flex gap-2">
                                    <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
                                    <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
                                    <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce" />
                                </div>
                            </motion.div>
                        </motion.div>
                    )}
                </AnimatePresence>,
                document.body
            )}
        </div>
    );
}
