'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Sparkles, ArrowRight, Check, Coffee, RefreshCw, Zap, Bell, Heart, ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export function DemoAnimation() {
    return (
        <div className="min-h-screen bg-[#FFF8F0] p-8 md:p-12 font-sans relative">
            {/* Back Navigation */}
            <div className="absolute top-4 left-4 z-50">
                <Button
                    asChild
                    variant="ghost"
                    className="text-latte-600 hover:text-latte-900 hover:bg-latte-100/50 transition-colors"
                >
                    <Link href="/design-showcase?tab=samples">
                        <ArrowLeft className="mr-2 h-4 w-4" /> Back to Gallery
                    </Link>
                </Button>
            </div>

            <div className="max-w-5xl mx-auto space-y-12">
                {/* Header */}
                <motion.header
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    className="text-center space-y-4"
                >
                    <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-violet-100 text-violet-600 mb-4 shadow-sm">
                        <Sparkles size={32} />
                    </div>
                    <h1 className="font-serif text-4xl md:text-5xl font-bold text-latte-900">
                        Animation Gallery
                    </h1>
                    <p className="text-lg text-latte-600 max-w-2xl mx-auto">
                        Motion principles and interactive states for TheMoon project.
                        <br />
                        <span className="text-sm opacity-70">Powered by Framer Motion</span>
                    </p>
                </motion.header>

                <Tabs defaultValue="entry" className="w-full">
                    <div className="flex justify-center mb-8">
                        <TabsList className="bg-white border border-latte-200 p-1">
                            <TabsTrigger value="entry">Entry & Exit</TabsTrigger>
                            <TabsTrigger value="interactive">Micro-Interactions</TabsTrigger>
                            <TabsTrigger value="layout">Layout & List</TabsTrigger>
                        </TabsList>
                    </div>

                    {/* ENTRY ANIMATIONS */}
                    <TabsContent value="entry" className="space-y-8">
                        <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <FadeCard />
                            <SlideCard />
                            <ScaleCard />
                        </section>

                        <section>
                            <h3 className="text-xl font-serif text-latte-800 mb-4">Text Revelations</h3>
                            <Card className="p-8 bg-white border-latte-200">
                                <TypingEffect text="The perfect roast requires patience and precision..." />
                            </Card>
                        </section>
                    </TabsContent>

                    {/* INTERACTIVE ANIMATIONS */}
                    <TabsContent value="interactive" className="space-y-8">
                        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                            <ButtonInteract />
                            <LikeButton />
                            <NotificationBell />
                            <SubmitButton />
                        </section>

                        <section>
                            <h3 className="text-xl font-serif text-latte-800 mb-4">Hover cards</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <HoverCard3D />
                                <GlowCard />
                            </div>
                        </section>
                    </TabsContent>

                    {/* LAYOUT ANIMATIONS */}
                    <TabsContent value="layout" className="space-y-8">
                        <StaggeredList />
                    </TabsContent>
                </Tabs>
            </div>
        </div>
    );
}

// --- Components ---

function FadeCard() {
    const [visible, setVisible] = useState(true);
    return (
        <Card className="overflow-hidden border-latte-200">
            <CardHeader>
                <CardTitle>Fade In/Out</CardTitle>
                <CardDescription>Opacity transition</CardDescription>
            </CardHeader>
            <CardContent className="h-40 flex items-center justify-center bg-latte-50/50">
                <AnimatePresence>
                    {visible && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="w-24 h-24 bg-latte-400 rounded-xl flex items-center justify-center text-white"
                        >
                            <Coffee />
                        </motion.div>
                    )}
                </AnimatePresence>
            </CardContent>
            <CardFooter>
                <Button variant="outline" size="sm" onClick={() => setVisible(!visible)} className="w-full">
                    Toggle <RefreshCw size={14} className="ml-2" />
                </Button>
            </CardFooter>
        </Card>
    );
}

function SlideCard() {
    const [visible, setVisible] = useState(true);
    return (
        <Card className="overflow-hidden border-latte-200">
            <CardHeader>
                <CardTitle>Slide Up</CardTitle>
                <CardDescription>Y-axis translation</CardDescription>
            </CardHeader>
            <CardContent className="h-40 flex items-center justify-center bg-latte-50/50">
                <AnimatePresence>
                    {visible && (
                        <motion.div
                            initial={{ y: 50, opacity: 0 }}
                            animate={{ y: 0, opacity: 1 }}
                            exit={{ y: 50, opacity: 0 }}
                            className="w-24 h-24 bg-emerald-500 rounded-xl flex items-center justify-center text-white"
                        >
                            <ArrowRight />
                        </motion.div>
                    )}
                </AnimatePresence>
            </CardContent>
            <CardFooter>
                <Button variant="outline" size="sm" onClick={() => setVisible(!visible)} className="w-full">
                    Toggle <RefreshCw size={14} className="ml-2" />
                </Button>
            </CardFooter>
        </Card>
    );
}

function ScaleCard() {
    const [visible, setVisible] = useState(true);
    return (
        <Card className="overflow-hidden border-latte-200">
            <CardHeader>
                <CardTitle>Scale & Pop</CardTitle>
                <CardDescription>Spring physics</CardDescription>
            </CardHeader>
            <CardContent className="h-40 flex items-center justify-center bg-latte-50/50">
                <AnimatePresence>
                    {visible && (
                        <motion.div
                            initial={{ scale: 0 }}
                            animate={{ scale: 1, rotate: 0 }}
                            exit={{ scale: 0, rotate: -180 }}
                            transition={{ type: 'spring', stiffness: 260, damping: 20 }}
                            className="w-24 h-24 bg-orange-400 rounded-xl flex items-center justify-center text-white"
                        >
                            <Zap />
                        </motion.div>
                    )}
                </AnimatePresence>
            </CardContent>
            <CardFooter>
                <Button variant="outline" size="sm" onClick={() => setVisible(!visible)} className="w-full">
                    Toggle <RefreshCw size={14} className="ml-2" />
                </Button>
            </CardFooter>
        </Card>
    );
}

function TypingEffect({ text }: { text: string }) {
    return (
        <motion.div
            initial={{ opacity: 1 }}
            animate={{ opacity: 1 }}
            className="text-2xl md:text-3xl font-serif text-latte-900 leading-tight"
        >
            {text.split('').map((char, index) => (
                <motion.span
                    key={index}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{
                        duration: 0.1,
                        delay: index * 0.05,
                    }}
                >
                    {char}
                </motion.span>
            ))}
        </motion.div>
    );
}

function ButtonInteract() {
    return (
        <Card className="flex flex-col items-center justify-center p-6 border-latte-200">
            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-latte-900 text-white px-6 py-3 rounded-lg font-medium shadow-lg shadow-latte-200/50"
            >
                Press Me
            </motion.button>
            <span className="text-xs text-latte-400 mt-4">Scale on Hover/Tap</span>
        </Card>
    );
}

function LikeButton() {
    const [liked, setLiked] = useState(false);
    return (
        <Card className="flex flex-col items-center justify-center p-6 border-latte-200">
            <motion.button
                onClick={() => setLiked(!liked)}
                whileTap={{ scale: 0.8 }}
                className={`p-4 rounded-full transition-colors ${liked ? 'bg-rose-100 text-rose-500' : 'bg-latte-100 text-latte-400'}`}
            >
                <motion.div
                    animate={liked ? { scale: [1, 1.5, 1], rotate: [0, 15, -15, 0] } : {}}
                    transition={{ duration: 0.4 }}
                >
                    <Heart fill={liked ? 'currentColor' : 'none'} />
                </motion.div>
            </motion.button>
            <span className="text-xs text-latte-400 mt-4">Keyframe Animation</span>
        </Card>
    );
}

function NotificationBell() {
    return (
        <Card className="flex flex-col items-center justify-center p-6 border-latte-200">
            <motion.div
                whileHover={{ rotate: [0, -10, 10, -10, 10, 0] }}
                transition={{ duration: 0.5 }}
                className="relative p-3 bg-white border border-latte-200 rounded-full cursor-pointer hover:border-amber-400 transition-colors"
            >
                <Bell className="text-latte-700" />
                <span className="absolute top-0 right-0 w-3 h-3 bg-red-500 rounded-full border-2 border-white"></span>
            </motion.div>
            <span className="text-xs text-latte-400 mt-4">Shake on Hover</span>
        </Card>
    );
}

function SubmitButton() {
    const [status, setStatus] = useState<'idle' | 'loading' | 'success'>('idle');

    const handleClick = () => {
        if (status !== 'idle') return;
        setStatus('loading');
        setTimeout(() => {
            setStatus('success');
            setTimeout(() => setStatus('idle'), 2000);
        }, 1500);
    };

    return (
        <Card className="flex flex-col items-center justify-center p-6 border-latte-200">
            <motion.button
                onClick={handleClick}
                animate={{
                    width: status === 'idle' ? 120 : status === 'loading' ? 50 : 120,
                    backgroundColor: status === 'success' ? '#10B981' : '#1e1b4b', // latte-900 equivalent logic or hex
                }}
                className={`h-12 rounded-full flex items-center justify-center text-white overflow-hidden relative bg-latte-900`}
            >
                <AnimatePresence mode="wait">
                    {status === 'idle' && (
                        <motion.span
                            key="text"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                        >
                            Submit
                        </motion.span>
                    )}
                    {status === 'loading' && (
                        <motion.div
                            key="loader"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1, rotate: 360 }}
                            exit={{ opacity: 0 }}
                            transition={{
                                opacity: { duration: 0.2 },
                                rotate: { repeat: Infinity, duration: 1, ease: 'linear' },
                            }}
                        >
                            <RefreshCw size={20} />
                        </motion.div>
                    )}
                    {status === 'success' && (
                        <motion.div
                            key="success"
                            initial={{ opacity: 0, scale: 0.5 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="flex items-center gap-2"
                        >
                            <Check size={20} /> <span>Done</span>
                        </motion.div>
                    )}
                </AnimatePresence>
            </motion.button>
            <span className="text-xs text-latte-400 mt-4">Morphing State</span>
        </Card>
    );
}

function HoverCard3D() {
    return (
        <motion.div whileHover={{ y: -5 }} className="h-full">
            <Card className="h-full border-latte-200 shadow-md hover:shadow-xl transition-shadow duration-300">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Coffee className="text-latte-500" /> Coffee Card
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-latte-600">
                        A subtle lift effect that adds a premium feel to your UI components. Best used for
                        clickable cards or important content blocks.
                    </p>
                </CardContent>
            </Card>
        </motion.div>
    );
}

function GlowCard() {
    return (
        <div className="relative group h-full">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-pink-600 to-purple-600 rounded-lg blur opacity-25 group-hover:opacity-75 transition duration-1000 group-hover:duration-200"></div>
            <Card className="relative h-full bg-white border-none">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Sparkles className="text-purple-500" /> Glow Effect
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-latte-600">
                        A beautiful gradient glow effect using absolute positioning and blur. Great for
                        highlighting premium features or active states.
                    </p>
                </CardContent>
            </Card>
        </div>
    );
}

const listItems = [
    { id: 1, title: 'Ethiopia Yirgacheffe', desc: 'Floral & Bright' },
    { id: 2, title: 'Colombia Supremo', desc: 'Nutty & Caramel' },
    { id: 3, title: 'Sumatra Mandheling', desc: 'Earthy & Full Body' },
    { id: 4, title: 'Kenya AA', desc: 'Fruity & Winey' },
];

function StaggeredList() {
    const [key, setKey] = useState(0);

    return (
        <section>
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-serif text-latte-800">Staggered Entrance</h3>
                <Button variant="ghost" size="sm" onClick={() => setKey((k) => k + 1)}>
                    Replay <RefreshCw size={14} className="ml-2" />
                </Button>
            </div>

            <motion.div
                key={key}
                initial="hidden"
                animate="show"
                variants={{
                    hidden: { opacity: 0 },
                    show: {
                        opacity: 1,
                        transition: {
                            staggerChildren: 0.1,
                        },
                    },
                }}
                className="grid gap-3"
            >
                {listItems.map((item) => (
                    <motion.div
                        key={item.id}
                        variants={{
                            hidden: { opacity: 0, x: -20 },
                            show: { opacity: 1, x: 0 },
                        }}
                    >
                        <div className="bg-white p-4 rounded-lg border border-latte-200 shadow-sm flex items-center justify-between">
                            <div>
                                <div className="font-medium text-latte-900">{item.title}</div>
                                <div className="text-sm text-latte-500">{item.desc}</div>
                            </div>
                            <Button variant="ghost" size="icon" className="text-latte-400">
                                <ArrowRight size={16} />
                            </Button>
                        </div>
                    </motion.div>
                ))}
            </motion.div>
        </section>
    );
}
