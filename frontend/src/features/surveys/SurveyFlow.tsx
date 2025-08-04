// src/features/surveys/SurveyFlow.tsx
import React, { useState } from "react";
import SurveyCard, { type Question } from "../../components/SurveyCard";

const questions: Question[] = [
  { id: "q1", text: "How satisfied are you with our service?", type: "rating" },
  { id: "q2", text: "What could we improve?", type: "text" },
  { id: "q3", text: "Would you recommend us?", type: "multiple", options: ["Yes", "No"] },
];

const SurveyFlow: React.FC = () => {
  const [index, setIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string | number>>({});

  const current = questions[index];
  const progress = ((index + 1) / questions.length) * 100;

  const handleAnswer = (id: string, answer: string | number) => {
    setAnswers((prev) => {
      const updated = { ...prev, [id]: answer };
      console.log("Updated answers:", updated); // uses `answers` so it's read
      return updated;
    });
    setTimeout(() => {
      if (index + 1 < questions.length) setIndex(index + 1);
    }, 300);
  };

  return (
    <div className="py-12 px-4">
      <SurveyCard question={current} progress={progress} onAnswer={handleAnswer} />
      <div className="mt-6 text-center text-sm text-gray-500">
        {index + 1} of {questions.length} completed
      </div>
    </div>
  );
};

export default SurveyFlow;
