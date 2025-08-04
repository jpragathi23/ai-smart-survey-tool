// src/components/SurveyCard.tsx
import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

export type Question = {
  id: string;
  text: string;
  type: "multiple" | "text" | "rating";
  options?: string[];
};

type Props = {
  question: Question;
  progress: number; // 0..100
  onAnswer: (qId: string, answer: string | number) => void;
};

const SurveyCard: React.FC<Props> = ({ question, progress, onAnswer }) => {
  const [selected, setSelected] = useState<string | number>("");

  useEffect(() => {
    setSelected("");
  }, [question]);

  const handleSelect = (val: string | number) => {
    setSelected(val);
    onAnswer(question.id, val);
  };

  return (
    <div className="max-w-xl mx-auto p-6 bg-white rounded-2xl shadow-lg relative overflow-hidden">
      {/* Progress bar */}
      <div className="h-2 w-full rounded-full overflow-hidden mb-4">
        <div
          className="h-full rounded-full"
          style={{
            width: `${progress}%`,
            background: "linear-gradient(90deg,#0D3B66,#2A9D8F)",
            transition: "width 0.6s ease",
          }}
          aria-label={`Progress: ${progress}%`}
        />
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={question.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.4 }}
        >
          <div className="flex items-start gap-4">
            <div className="flex-shrink-0">
              <div className="w-10 h-10 flex items-center justify-center rounded-full bg-gradient-to-br from-[#0D3B66] to-[#F4A261] text-white font-semibold">
                {Math.round(progress)}%
              </div>
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-semibold text-[#0D3B66] mb-2">
                {question.text}
              </h2>

              {question.type === "multiple" && question.options && (
                <div className="grid gap-3 mt-2">
                  {question.options.map((opt) => (
                    <button
                      key={opt}
                      onClick={() => handleSelect(opt)}
                      className={`
                        relative flex items-center justify-center px-4 py-2 rounded-full font-medium
                        transition
                        ${
                          selected === opt
                            ? "bg-gradient-to-r from-[#2A9D8F] to-[#F4A261] text-white shadow-md"
                            : "bg-gray-100 text-gray-700 hover:scale-[1.02]"
                        }
                      `}
                      aria-pressed={selected === opt}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              )}

              {question.type === "text" && (
                <textarea
                  value={selected as string}
                  onChange={(e) => handleSelect(e.target.value)}
                  placeholder="Type your answer..."
                  className="w-full mt-2 p-3 border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-[#2A9D8F]"
                  rows={4}
                />
              )}

              {question.type === "rating" && (
                <div className="flex gap-2 mt-2">
                  {[1, 2, 3, 4, 5].map((n) => (
                    <motion.div
                      key={n}
                      onClick={() => handleSelect(n)}
                      whileTap={{ scale: 0.9 }}
                      className={`
                        cursor-pointer flex items-center justify-center w-10 h-10 rounded-full border-2
                        ${
                          selected === n
                            ? "bg-[#F4A261] text-white border-transparent"
                            : "bg-white text-gray-600 border-[#0D3B66]"
                        }
                        transition
                      `}
                      aria-label={`${n} stars`}
                    >
                      {n}
                    </motion.div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </motion.div>
      </AnimatePresence>

      <div className="mt-6 flex justify-between items-center text-sm text-gray-500">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-[#2A9D8F]" />
          <span>AI suggests related follow-up based on your answer.</span>
        </div>
        <div className="font-medium text-[#0D3B66]">Need help?</div>
      </div>
    </div>
  );
};

export default SurveyCard;
