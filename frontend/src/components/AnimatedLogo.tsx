import React from "react";
import { motion } from "framer-motion";

const AnimatedLogo: React.FC = () => (
  <motion.div
    initial={{ scale: 0.9, opacity: 0 }}
    animate={{ scale: 1, opacity: 1 }}
    transition={{ type: "spring", stiffness: 200, damping: 20 }}
    className="inline-flex items-center gap-2"
  >
    <motion.img
      src="/logo-animated.svg"
      alt="Logo"
      className="w-12 h-12"
      whileHover={{ scale: 1.1, rotate: 3 }}
      transition={{ duration: 0.3 }}
    />
    <div className="flex flex-col">
      <div className="text-lg font-bold text-primary">AI Smart Survey</div>
      <motion.div
        className="text-sm font-medium text-gray-700"
        initial={{ x: -5, opacity: 0.6 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ repeat: Infinity, repeatType: "reverse", duration: 3 }}
      >
        From Questions to Clarity
      </motion.div>
    </div>
  </motion.div>
);

export default AnimatedLogo;
