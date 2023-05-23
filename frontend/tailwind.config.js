/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
        colors: {
          ...colors,
          'red': {...colors.red},
          'main': {
            100: '#EDEDFC',
            500: '#605CA8',
            700: '#4B4793',
          },
          'success': '#50C878',
          'white': '#ffffff',
        }
    },
  
  },
  plugins: []
}

