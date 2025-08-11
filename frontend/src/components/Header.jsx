import React from "react";
import Logo from "./Logo";

const Header = () => {
  return (
    <header className="flex items-center justify-between px-6 py-4 shadow-md bg-white">
      <Logo />
      <nav className="flex space-x-4">
        <a href="/" className="text-gray-700 hover:text-blue-600">Home</a>
        <a href="/builder" className="text-gray-700 hover:text-blue-600">Survey Builder</a>
        <a href="/dashboard" className="text-gray-700 hover:text-blue-600">Dashboard</a>
      </nav>
    </header>
  );
};

export default Header;
