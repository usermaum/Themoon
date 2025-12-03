"use client";

import React from 'react';
import { useLanguage } from '@/lib/i18n/LanguageContext';
import { Button } from '@/components/ui/Button';

export function LanguageSwitcher() {
    const { language, setLanguage } = useLanguage();

    return (
        <div className="flex items-center gap-2">
            <Button
                variant={language === 'ko' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setLanguage('ko')}
                className={`w-12 h-8 text-xs font-bold ${language === 'ko' ? 'bg-amber-600 hover:bg-amber-700' : 'text-stone-500'}`}
            >
                KO
            </Button>
            <Button
                variant={language === 'en' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setLanguage('en')}
                className={`w-12 h-8 text-xs font-bold ${language === 'en' ? 'bg-amber-600 hover:bg-amber-700' : 'text-stone-500'}`}
            >
                EN
            </Button>
        </div>
    );
}
