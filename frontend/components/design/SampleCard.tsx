'use client';

import Link from 'next/link';
import { LucideIcon, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardHeader,
    CardTitle,
    CardDescription,
    CardContent,
    CardFooter,
} from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export interface Sample {
    title: string;
    desc: string;
    href: string;
    icon: LucideIcon;
    preview: string;
    color: string;
}

interface SampleCardProps {
    sample: Sample;
}

export function SampleCard({ sample }: SampleCardProps) {
    return (
        <Link href={sample.href} className="group">
            <Card className="h-full border-latte-200 hover:border-latte-400 hover:shadow-xl transition-all duration-300 bg-white overflow-hidden relative rounded-[1.5rem]">
                <div
                    className={`absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity ${sample.color} rounded-bl-[2rem]`}
                >
                    <sample.icon size={64} />
                </div>
                <CardHeader>
                    <div
                        className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${sample.color}`}
                    >
                        <sample.icon size={24} />
                    </div>
                    <CardTitle className="font-serif text-2xl text-latte-900 group-hover:text-latte-700 transition-colors">
                        {sample.title}
                    </CardTitle>
                    <CardDescription className="text-latte-500 text-sm min-h-[40px]">
                        {sample.desc}
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="flex flex-wrap gap-2">
                        {sample.preview.split(', ').map((tag: string) => (
                            <Badge
                                key={tag}
                                variant="secondary"
                                className="bg-latte-50 text-latte-600 font-normal border border-latte-100"
                            >
                                {tag}
                            </Badge>
                        ))}
                    </div>
                </CardContent>
                <CardFooter className="pt-2">
                    <Button
                        variant="ghost"
                        className="p-0 text-latte-600 hover:text-latte-900 hover:bg-transparent group-hover:translate-x-2 transition-all"
                    >
                        Go to Sample <ArrowRight className="ml-2 w-4 h-4" />
                    </Button>
                </CardFooter>
            </Card>
        </Link>
    );
}
