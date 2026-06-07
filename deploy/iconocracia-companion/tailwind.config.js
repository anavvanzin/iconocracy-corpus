/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}"
  ],
  theme: {
    extend: {
      colors: {
        'vintage-cream': '#E8DCC4',
        'vintage-bordeaux': '#6B1E3A',
        'vintage-green': '#2D4A3E',
        'vintage-gold': '#C9A961',
        'vintage-brown': '#3D2817',
        'vintage-light': '#F5ECD6',
      },
      fontFamily: {
        'serif': ['"Instrument Serif"', 'serif'],
        'sans': ['"Inter"', 'sans-serif'],
        'mono': ['"JetBrains Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
}
