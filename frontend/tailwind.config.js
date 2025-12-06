/** @type {import('tailwindcss').Config} */
module.exports = {
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
        blob: {
          orange: '#FFD6BA',
          green: '#C3E2DD',
        }
      }
    },
  },
  plugins: [],
}
