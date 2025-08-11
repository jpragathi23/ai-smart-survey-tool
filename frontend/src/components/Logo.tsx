// src/components/Logo.tsx

const Logo = () => (
  <svg
    width="120"
    height="120"
    viewBox="0 0 1024 1024"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <rect width="1024" height="1024" fill="#F7F9FC" />
    <g transform="translate(150,150)">
      <rect x="0" y="0" width="724" height="724" rx="50" fill="#FFFFFF" stroke="#000000" strokeWidth="8" />
      <text x="120" y="100" fontSize="64" fill="#000" fontFamily="Arial, sans-serif" fontWeight="bold">
        Smart Survey
      </text>
      <circle cx="230" cy="180" r="80" stroke="#2B50EC" strokeWidth="8" fill="#E8F0FE" />
      <path
        d="M200 180 L225 205 L270 150"
        stroke="#2B50EC"
        strokeWidth="10"
        fill="none"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <rect x="100" y="300" width="500" height="60" rx="15" fill="#FFBE0B" />
      <rect x="100" y="400" width="400" height="60" rx="15" fill="#FB5607" />
      <rect x="100" y="500" width="300" height="60" rx="15" fill="#3A86FF" />
      <rect x="100" y="600" width="200" height="60" rx="15" fill="#2B50EC" />
      <circle cx="650" cy="330" r="15" fill="#FFBE0B" />
      <circle cx="650" cy="430" r="15" fill="#FB5607" />
      <circle cx="650" cy="530" r="15" fill="#3A86FF" />
      <circle cx="650" cy="630" r="15" fill="#2B50EC" />
    </g>
  </svg>
);

export default Logo;
