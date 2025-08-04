import React from "react";

const HomePage: React.FC = () => (
  <div className="px-6 py-12 max-w-6xl mx-auto flex flex-col md:flex-row gap-10 items-center">
    <div className="flex-1">
      <div className="flex items-center gap-4 mb-4">
        <div className="w-12 h-12 bg-gradient-to-br from-primary to-accent rounded flex items-center justify-center text-white font-bold">
          {/* replace with logo SVG later */}
          AI
        </div>
        <div className="text-lg font-medium">From Questions to Clarity</div>
      </div>
      <h1 className="text-4xl font-extrabold text-primary mb-4">
        Smarter Surveys. Deeper Insights.
      </h1>
      <p className="text-gray-700 mb-6">
        Launch adaptive, multilingual, AI-powered surveys with smooth UX and actionable dashboards.
      </p>
      <a
        href="/survey"
        className="inline-block px-6 py-3 bg-accent text-white rounded-full font-semibold shadow hover:scale-105 transition"
      >
        Start Survey
      </a>
    </div>
    <div className="flex-1">
      <div className="w-full h-64 bg-gradient-to-r from-primary to-growth rounded-xl shadow-lg flex items-center justify-center text-white">
        Hero Illustration
      </div>
    </div>
  </div>
);

export default HomePage;
