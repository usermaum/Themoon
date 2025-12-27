/** @type {import('tailwindcss').Config} */
// Force rebuild for demo page
module.exports = {
  darkMode: ['class'],
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        serif: ['var(--font-playfair)'],
        sans: ['var(--font-inter)'],
      },
      colors: {
        latte: {
          50: '#FFF8F0',
          100: '#F5EBE0',
          200: '#E6D5C3',
          300: '#D7BF9D',
          400: '#C8AA77',
          500: '#B0A69D',
          600: '#8D7B68',
          700: '#6B5D4D',
          800: '#4A403A',
          900: '#2C1810',
        },
        coffee: {
          50: '#fdf8f6',
          100: '#f2e8e5',
          200: '#eaddd7',
          300: '#e0cec7',
          400: '#d2bab0',
          500: '#a18072',
          600: '#977669',
          700: '#846358',
          800: '#43302b',
          900: '#1c1311',
        },
        blob: {
          orange: '#FFD6BA',
          green: '#C3E2DD',
        },
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))',
        },
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        chart: {
          1: 'hsl(var(--chart-1))',
          2: 'hsl(var(--chart-2))',
          3: 'hsl(var(--chart-3))',
          4: 'hsl(var(--chart-4))',
          5: 'hsl(var(--chart-5))',
        },
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      keyframes: {
        'accordion-down': {
          from: {
            height: '0',
          },
          to: {
            height: 'var(--radix-accordion-content-height)',
          },
        },
        'accordion-up': {
          from: {
            height: 'var(--radix-accordion-content-height)',
          },
          to: {
            height: '0',
          },
        },
        'float-slow': {
          '0%, 100%': {
            transform: 'translate(0, 0) rotate(0deg)',
          },
          '25%': {
            transform: 'translate(10px, -15px) rotate(5deg)',
          },
          '50%': {
            transform: 'translate(-5px, -25px) rotate(-3deg)',
          },
          '75%': {
            transform: 'translate(-15px, -10px) rotate(8deg)',
          },
        },
        'float-medium': {
          '0%, 100%': {
            transform: 'translate(0, 0) rotate(0deg) scale(1)',
          },
          '33%': {
            transform: 'translate(15px, -20px) rotate(-10deg) scale(1.05)',
          },
          '66%': {
            transform: 'translate(-10px, -30px) rotate(12deg) scale(0.95)',
          },
        },
        'float-fast': {
          '0%, 100%': {
            transform: 'translate(0, 0) rotate(0deg)',
          },
          '20%': {
            transform: 'translate(8px, -12px) rotate(15deg)',
          },
          '40%': {
            transform: 'translate(-8px, -20px) rotate(-10deg)',
          },
          '60%': {
            transform: 'translate(12px, -28px) rotate(20deg)',
          },
          '80%': {
            transform: 'translate(-5px, -15px) rotate(-15deg)',
          },
        },
        'float-reverse': {
          '0%, 100%': {
            transform: 'translate(0, 0) rotate(0deg)',
          },
          '25%': {
            transform: 'translate(-12px, 18px) rotate(-8deg)',
          },
          '50%': {
            transform: 'translate(8px, 30px) rotate(5deg)',
          },
          '75%': {
            transform: 'translate(15px, 12px) rotate(-12deg)',
          },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
        'float-slow': 'float-slow 8s ease-in-out infinite',
        'float-medium': 'float-medium 6s ease-in-out infinite',
        'float-fast': 'float-fast 4s ease-in-out infinite',
        'float-reverse': 'float-reverse 7s ease-in-out infinite',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};
