/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{jsx,js}'],
  theme: {
    extend: {
      colors: {
        bg: '#FAF7F2',
        ink: '#2C2C2C',
        terracotta: '#A0522D',
        navy: '#16213E',
        gold: '#C4A265',
        'warm-gray': '#9B8E82',
        'light-gray': '#E8E3DC',
        'card-bg': '#FFFFFF',
      },
      fontFamily: {
        serif: ['"Instrument Serif"', 'serif'],
        sans: ['Inter', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
}
