"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import ko from './locales/ko.json';
import en from './locales/en.json';

type Language = 'ko' | 'en';
type Translations = typeof ko;

interface LanguageContextType {
    language: Language;
    setLanguage: (lang: Language) => void;
    t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: ReactNode }) {
    const [language, setLanguage] = useState<Language>('ko');
    const [translations, setTranslations] = useState<Translations>(ko);

    useEffect(() => {
        const savedLang = localStorage.getItem('language') as Language;
        if (savedLang && (savedLang === 'ko' || savedLang === 'en')) {
            setLanguage(savedLang);
        }
    }, []);

    useEffect(() => {
        setTranslations(language === 'ko' ? ko : en);
        localStorage.setItem('language', language);
    }, [language]);

    const t = (key: string): string => {
        const keys = key.split('.');
        let value: any = translations;

        for (const k of keys) {
            if (value && typeof value === 'object' && k in value) {
                value = value[k as keyof typeof value];
            } else {
                return key; // Return key if translation not found
            }
        }

        return typeof value === 'string' ? value : key;
    };

    return (
        <LanguageContext.Provider value={{ language, setLanguage, t }}>
            {children}
        </LanguageContext.Provider>
    );
}

export function useLanguage() {
    const context = useContext(LanguageContext);
    if (context === undefined) {
        throw new Error('useLanguage must be used within a LanguageProvider');
    }
    return context;
}
