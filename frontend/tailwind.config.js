/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brandRed: "#ff0000",
        brandOrange: "#ff9900",
        brandGreen: "#00cc66",
      },
      backgroundImage: {
        "gradient-brand": "linear-gradient(135deg, #ff0000, #ff9900, #00cc66)",
      },
    },
  },
  plugins: [],
};
