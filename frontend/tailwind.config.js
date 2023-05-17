/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
    colors: {
      'main': {
        100: '#EDEDFC',
        500: '#605CA8',
        700: '#4B4793',
      },
      'success': '#50C878',
      'danger': '#FF0000',
      'white': '#ffffff',
    },
  
  },
  plugins: [],
}

