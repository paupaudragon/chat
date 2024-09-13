/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      maxHeight: {
        fitted: "calc(100vh - 48px)",
      },
      fontSize: {
        xxs: ["10px", "14px"], /* font size and line height */
      }
    }
  },
  plugins: [],
}

