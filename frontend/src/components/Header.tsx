import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

const AnimatedLogo: React.FC = () => (
  <motion.div
    initial={{ scale: 0.85, opacity: 0 }}
    animate={{ scale: 1, opacity: 1 }}
    transition={{ type: "spring", stiffness: 220, damping: 18 }}
    className="inline-flex items-center gap-2"
  >
    <motion.img
      src="/logo-animated.svg"
      alt="AI Smart Survey Tool logo"
      className="w-12 h-12"
      whileHover={{ scale: 1.1, rotate: 3 }}
      transition={{ duration: 0.3 }}
    />
    <div className="flex flex-col leading-tight">
      <div className="text-lg font-bold text-primary">AI Smart Survey</div>
      <motion.div
        className="text-sm font-medium text-gray-700"
        initial={{ x: -4, opacity: 0.7 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ repeat: Infinity, repeatType: "reverse", duration: 4 }}
      >
        <span className="shimmer">From Questions to Clarity</span>
      </motion.div>
    </div>
  </motion.div>
);

const Header: React.FC = () => (
  <header className="w-full py-4 px-6 flex items-center justify-between bg-white shadow-md sticky top-0 z-20">
    <Link to="/" className="flex items-center gap-4">
      <AnimatedLogo />
    </Link>
    <nav>
      <Link
        to="/survey"
        className="px-5 py-2 bg-accent text-white rounded-full font-medium shadow-lg hover:scale-105 transition-transform duration-200"
      >
        Start Survey
      </Link>
    </nav>
  </header>
);

export default Header;

