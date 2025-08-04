import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#0D3B66",
        accent: "#F4A261",
        growth: "#2A9D8F",
      },
    },
  },
  plugins: [],
};

export default config;
