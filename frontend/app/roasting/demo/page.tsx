'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, useAnimation } from 'framer-motion';
import PageHero from '@/components/ui/page-hero';
import { Flame, Gauge, Fan, Play, Pause, RotateCcw, Thermometer } from 'lucide-react';

export default function RoastingDemoPage() {
    return (
        <div className="min-h-screen bg-[#FDFBF7] flex flex-col">
            <PageHero
                title="Roasting Simulator"
                description="가상 로스팅 체험관에 오신 것을 환영합니다. 직접 로스터가 되어 원두를 볶아보세요!"
                icon={<Flame />}
                image="/images/hero/roasting-hero.png" // Fallback to existing hero
            />

            <div className="flex-1 container mx-auto px-6 py-12 max-w-6xl">
                <RoastingSimulatorInterface />
            </div>
        </div>
    );
}

function RoastingSimulatorInterface() {
    const [status, setStatus] = useState<'IDLE' | 'ROASTING' | 'COOLING' | 'FINISHED'>('IDLE');
    const [temperature, setTemperature] = useState(20); // Ambient temp
    const [time, setTime] = useState(0);
    const [beanColor, setBeanColor] = useState('#9CA3AF'); // Initial Green/Gray

    // Simulation Loop
    useEffect(() => {
        let interval: NodeJS.Timeout;
        if (status === 'ROASTING') {
            interval = setInterval(() => {
                setTime(t => t + 1);
                setTemperature(temp => {
                    // Simple logic: Temp rises, but slows down
                    const increment = Math.max(0.5, (220 - temp) * 0.05);
                    return Math.min(230, temp + increment);
                });
            }, 100);
        }
        return () => clearInterval(interval);
    }, [status]);

    // Color Change Logic based on Temp
    useEffect(() => {
        if (temperature < 150) setBeanColor('#869668'); // Green
        else if (temperature < 180) setBeanColor('#EAB308'); // Yellow
        else if (temperature < 205) setBeanColor('#A86F3E'); // Light Brown
        else if (temperature < 215) setBeanColor('#5D4037'); // Medium Brown
        else setBeanColor('#3E2723'); // Dark Brown
    }, [temperature]);

    const handleStart = () => {
        setStatus('ROASTING');
        setTemperature(100); // Pre-heat
        setTime(0);
    };

    const handleStop = () => {
        setStatus('FINISHED');
    };

    const handleReset = () => {
        setStatus('IDLE');
        setTemperature(20);
        setTime(0);
        setBeanColor('#869668');
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 h-[600px]">
            {/* Left: Visualizer (Drum) */}
            <div className="lg:col-span-2 bg-zinc-900 rounded-3xl p-8 relative overflow-hidden shadow-2xl flex items-center justify-center border-4 border-zinc-800">
                <div className="absolute top-6 left-6 text-zinc-500 font-mono text-xs flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${status === 'ROASTING' ? 'bg-red-500 animate-pulse' : 'bg-zinc-600'}`} />
                    STATUS: {status}
                </div>

                {/* Roasting Drum Animation */}
                <motion.div
                    className="w-96 h-96 relative"
                    animate={status === 'ROASTING' ? { rotate: 360 } : { rotate: 0 }}
                    transition={{ repeat: Infinity, duration: 4, ease: "linear" }}
                >
                    {/* Simplified Drum Graphic */}
                    <div className="absolute inset-0 border-[12px] border-zinc-700 rounded-full border-dashed opacity-50" />
                    <div className="absolute inset-4 border-[2px] border-zinc-700 rounded-full opacity-30" />

                    {/* Beans Particles (Simulated by simple circles for now) */}
                    <div className="absolute inset-0 flex items-center justify-center">
                        <motion.div
                            className="w-64 h-64 rounded-full blur-xl transition-colors duration-1000"
                            style={{ backgroundColor: beanColor }}
                            animate={{ scale: [0.95, 1.05, 0.95] }}
                            transition={{ repeat: Infinity, duration: 2 }}
                        />
                        <motion.div
                            className="w-48 h-48 rounded-full transition-colors duration-1000 mix-blend-overlay"
                            style={{ backgroundColor: beanColor }}
                        />
                    </div>
                </motion.div>

                {/* Flame Effect */}
                {status === 'ROASTING' && (
                    <motion.div
                        className="absolute bottom-10 left-1/2 -translate-x-1/2 w-full h-32 bg-orange-500/20 blur-3xl rounded-full"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: [0.3, 0.6, 0.3], scale: [0.9, 1.1, 0.9] }}
                        transition={{ repeat: Infinity, duration: 1 }}
                    />
                )}
            </div>

            {/* Right: Control Panel */}
            <div className="bg-zinc-100 rounded-3xl p-6 flex flex-col gap-6 border border-zinc-200">
                {/* Display */}
                <div className="bg-zinc-900 rounded-2xl p-6 text-green-400 font-mono shadow-inner border border-zinc-800">
                    <div className="flex justify-between items-end mb-4">
                        <span className="text-zinc-500 text-sm">BEAN TEMP</span>
                        <span className="text-4xl font-bold">{Math.round(temperature)}°C</span>
                    </div>
                    <div className="flex justify-between items-end">
                        <span className="text-zinc-500 text-sm">DURATION</span>
                        <span className="text-2xl">{Math.floor(time / 60)}:{(time % 60).toString().padStart(2, '0')}</span>
                    </div>
                </div>

                {/* Controls Simulation */}
                <div className="grid grid-cols-2 gap-4 flex-1">
                    <ControlKnob label="GAS POWER" icon={<Flame size={16} />} value={75} />
                    <ControlKnob label="AIR FLOW" icon={<Fan size={16} />} value={40} />
                    <ControlKnob label="DRUM SPEED" icon={<RotateCcw size={16} />} value={60} />
                </div>

                {/* Actions */}
                <div className="flex gap-3 mt-auto">
                    {status === 'IDLE' || status === 'FINISHED' ? (
                        <button
                            onClick={handleStart}
                            className="flex-1 bg-latte-900 text-white rounded-xl py-4 font-bold hover:bg-black transition-colors flex items-center justify-center gap-2"
                        >
                            <Play size={20} fill="currentColor" /> START
                        </button>
                    ) : (
                        <button
                            onClick={handleStop}
                            className="flex-1 bg-amber-600 text-white rounded-xl py-4 font-bold hover:bg-amber-700 transition-colors flex items-center justify-center gap-2"
                        >
                            <Pause size={20} fill="currentColor" /> DROP
                        </button>
                    )}

                    <button
                        onClick={handleReset}
                        className="px-4 bg-white border border-zinc-200 rounded-xl hover:bg-zinc-50 transition-colors"
                    >
                        <RotateCcw size={20} className="text-zinc-400" />
                    </button>
                </div>
            </div>
        </div>
    );
}

function ControlKnob({ label, icon, value }: { label: string, icon: any, value: number }) {
    return (
        <div className="bg-white rounded-xl p-4 border border-zinc-200 shadow-sm flex flex-col items-center justify-center gap-3">
            <div className="text-[10px] font-bold text-zinc-400 tracking-wider flex items-center gap-1">
                {icon} {label}
            </div>
            <div className="relative w-24 h-24 rounded-full border-4 border-zinc-100 flex items-center justify-center">
                <div className="absolute inset-0 rounded-full border-4 border-latte-500" style={{ clipPath: `polygon(0 0, 100% 0, 100% ${value}%, 0 ${value}%)` }} />
                <span className="text-xl font-bold text-zinc-700">{value}</span>
            </div>
        </div>
    );
}
