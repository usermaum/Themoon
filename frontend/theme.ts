'use client';

import { createTheme, rem, virtualColor } from '@mantine/core';

export const theme = createTheme({
    primaryColor: 'artistic-brown',
    colors: {
        'artistic-brown': [
            '#f5f0eb', // 0
            '#e6dbd3', // 1
            '#cfb8a6', // 2
            '#b89478', // 3
            '#a37550', // 4
            '#966136', // 5
            '#8a522a', // 6
            '#4a403a', // 7 (Primary Dark) - Matches design-lab text
            '#8d7b68', // 8 (Secondary) - Matches design-lab secondary
            '#2e2621', // 9
        ],
        'artistic-cream': [
            '#fffdfb',
            '#fff8f0', // Base BG
            '#ffe8d0',
            '#ffd6ba', // Accent 1
            '#ffc4a0',
            '#ffb286',
            '#ffa06c',
            '#ff8e52',
            '#ff7c38',
            '#ff6a1e',
        ],
        'artistic-mint': [
            '#f0fcf9',
            '#e2f7f3',
            '#c3e2dd', // Accent 2
            '#a4cdc7',
            '#85b9b1',
            '#66a49b',
            '#478f85',
            '#287a6f',
            '#096559',
            '#005043',
        ]
    },
    defaultRadius: 'xl',
    fontFamily: 'Inter, sans-serif',
    headings: {
        fontFamily: 'Playfair Display, serif',
        sizes: {
            h1: { fontSize: rem(42), fontWeight: '700' },
            h2: { fontSize: rem(32), fontWeight: '600' },
            h3: { fontSize: rem(26), fontWeight: '600' },
            h4: { fontSize: rem(22), fontWeight: '500' },
        },
    },
    radius: {
        md: '16px',
        lg: '24px',
        xl: '40px', // Matches the 2.5rem from design lab
    },
    shadows: {
        md: '0 4px 20px rgba(74, 64, 58, 0.08)',
        xl: '0 8px 30px rgba(74, 64, 58, 0.12)',
    },
    components: {
        Button: {
            defaultProps: {
                size: 'md',
                radius: 'xl',
            },
            styles: {
                root: {
                    fontWeight: 500,
                },
            },
        },
        TextInput: {
            defaultProps: {
                size: 'md',
                radius: 'xl',
            },
            styles: {
                input: {
                    backgroundColor: 'rgba(255, 255, 255, 0.6)',
                    borderColor: 'transparent',
                    '&:focus': {
                        backgroundColor: '#fff',
                        borderColor: '#E6D5C3',
                    },
                },
            },
        },
        Paper: {
            defaultProps: {
                shadow: 'sm',
                radius: 'xl',
                withBorder: false,
            },
            styles: {
                root: {
                    backgroundColor: 'rgba(255, 255, 255, 0.8)',
                    backdropFilter: 'blur(10px)',
                },
            },
        },
        Card: {
            defaultProps: {
                shadow: 'sm',
                radius: 'xl',
                withBorder: false,
                padding: 'xl',
            },
            styles: {
                root: {
                    backgroundColor: '#fff',
                },
            },
        },
        Badge: {
            defaultProps: {
                variant: 'light',
                radius: 'md',
            },
        }
    },
});
