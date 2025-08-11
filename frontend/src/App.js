import React from 'react';

import SurveyBuilder from './components/SurveyBuilder';
import Dashboard from './components/Dashboard';
import VoiceRecorder from './components/VoiceRecorder';
import TranslationSelector from './components/TranslationSelector';

import Navbar from './components/Navbar';
import Logo from './components/Logo';
import HeroSection from './components/HeroSection';
import FeaturesSection from './components/FeaturesSection';
import Footer from './components/Footer';

function App() {
  return (
    <div className="App">
      <Navbar />
      <Logo />
      <HeroSection />
      <FeaturesSection /> {/* ✅ Correct placement */}
      <Footer />
    </div>
  );
}

export default App;
