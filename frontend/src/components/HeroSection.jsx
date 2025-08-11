import React from 'react';
import { ReactComponent as Logo } from '../assets/logo.svg'; // ensure logo.svg is in src/assets/

const HeroSection = () => {
  return (
    <section className="bg-gradient-to-br from-blue-100 via-white to-blue-50 py-20 px-6" id="hero">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between">
        {/* Text Content */}
        <div className="text-center md:text-left md:w-1/2">
          <h1 className="text-5xl font-extrabold text-blue-900 mb-6 leading-tight">
            Smart Survey Tool
          </h1>
          <p className="text-lg text-gray-700 mb-8">
            AI-powered, multilingual, voice-enabled, and field-ready survey system built for inclusivity and efficiency.
          </p>
          <a
            href="#features"
            className="inline-block px-8 py-3 bg-blue-700 text-white text-lg font-semibold rounded-xl shadow-md hover:bg-blue-800 transition"
          >
            Explore Features
          </a>
        </div>

        {/* Logo */}
        <div className="mt-10 md:mt-0 md:w-1/2 flex justify-center">
          <Logo className="w-64 h-64 md:w-80 md:h-80" />
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
