/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'navy-primary': '#0B1F4B',
        'navy-dark': '#071633',
        'med-blue': '#1D4ED8',
        'med-lightblue': '#EFF6FF',
        'med-bg': '#F5F7FA',
      }
    },
  },
  plugins: [],
}