import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-md px-6 py-4 flex justify-between items-center">
      {/* Logo */}
      <div className="flex items-center">
        <img src="/assets/logosvg.svg" alt="Smart Survey Logo" className="h-10 w-auto mr-2" />
        <span className="text-xl font-bold text-gray-800">Smart Survey</span>
      </div>

      {/* Navigation Links */}
      <div className="space-x-6 hidden md:flex">
        <Link to="/" className="text-gray-600 hover:text-blue-600 font-medium">Home</Link>
        <Link to="/features" className="text-gray-600 hover:text-blue-600 font-medium">Features</Link>
        <Link to="/dashboard" className="text-gray-600 hover:text-blue-600 font-medium">Dashboard</Link>
        <Link to="/create" className="text-gray-600 hover:text-blue-600 font-medium">Create Survey</Link>
      </div>

      {/* Login/Signup Buttons */}
      <div className="hidden md:flex items-center space-x-4">
        <Link to="/login" className="text-blue-600 font-medium hover:underline">Login</Link>
        <Link to="/signup" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 font-medium">
          Sign Up
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
