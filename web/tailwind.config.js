/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        saffron: {
          50: '#fff7ed',
          100: '#ffedd5',
          400: '#fb923c',
          500: '#ff9933',
          600: '#ea580c',
        },
        navy: {
          800: '#111827',
          900: '#0b132b',
          950: '#070b19',
        }
      }
    },
  },
  plugins: [],
}
