import React, { useState, useEffect } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import Confetti from "react-confetti";
import { useWindowSize } from "react-use";

const GenerateSurvey: React.FC = () => {
  const [prompt, setPrompt] = useState("");
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [numQuestions, setNumQuestions] = useState(5);
  const [loading, setLoading] = useState(false);
  const [survey, setSurvey] = useState<any>(null);
  const [showConfetti, setShowConfetti] = useState(false);
  const { width, height } = useWindowSize();

  const handleGenerate = async () => {
    setSurvey(null);
    setShowConfetti(false);
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/api/surveys/generate-from-prompt", {
        prompt,
        num_questions: numQuestions,
        survey_title: title,
        survey_description: description,
      });
      setSurvey(res.data);
      setShowConfetti(true);
    } catch (error) {
      console.error(error);
      alert("Error generating survey");
    }
    setLoading(false);
  };

  // Auto-hide confetti after 5 seconds
  useEffect(() => {
    if (showConfetti) {
      const timer = setTimeout(() => setShowConfetti(false), 5000);
      return () => clearTimeout(timer);
    }
  }, [showConfetti]);

  return (
    <div className="max-w-3xl mx-auto p-6">
      {showConfetti && <Confetti width={width} height={height} recycle={false} />}

      <motion.h1
        className="text-3xl font-bold text-center mb-6 text-gradient"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        AI Smart Survey Generator
      </motion.h1>

      {/* Form */}
      <motion.div
        className="space-y-4 bg-white p-6 rounded-xl shadow-lg"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
      >
        <input
          type="text"
          placeholder="Survey Title"
          className="w-full p-3 border rounded-lg"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <textarea
          placeholder="Survey Description"
          className="w-full p-3 border rounded-lg"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <textarea
          placeholder="Enter your prompt here..."
          className="w-full p-3 border rounded-lg"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <input
          type="number"
          className="p-3 border rounded-lg"
          value={numQuestions}
          onChange={(e) => setNumQuestions(parseInt(e.target.value))}
        />

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="px-6 py-3 bg-gradient-to-r from-pink-500 via-purple-500 to-indigo-500 text-white rounded-lg font-semibold shadow-lg"
          onClick={handleGenerate}
          disabled={loading}
        >
          {loading ? "Generating..." : "Generate Survey"}
        </motion.button>
      </motion.div>

      {/* Loading Skeleton */}
      {loading && (
        <motion.div
          className="mt-8 space-y-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {[...Array(numQuestions)].map((_, i) => (
            <motion.div
              key={i}
              className="h-6 w-full rounded-lg bg-gradient-to-r from-pink-200 via-purple-200 to-indigo-200 animate-pulse"
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.15 }}
            />
          ))}
        </motion.div>
      )}

      {/* Survey Output */}
      {survey && (
        <motion.div
          className="mt-8 bg-gradient-to-r from-green-200 to-blue-200 p-6 rounded-xl shadow-lg"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <h2 className="text-2xl font-bold mb-2">{survey.title}</h2>
          <p className="mb-4">{survey.description}</p>
          <motion.ol
            className="list-decimal pl-6 space-y-2"
            initial="hidden"
            animate="visible"
            variants={{
              hidden: { opacity: 0 },
              visible: {
                opacity: 1,
                transition: { staggerChildren: 0.2 },
              },
            }}
          >
            {survey.questions.map((q: string, i: number) => (
              <motion.li
                key={i}
                className="p-2 bg-white rounded-lg shadow"
                variants={{
                  hidden: { opacity: 0, y: 10 },
                  visible: { opacity: 1, y: 0 },
                }}
                transition={{ duration: 0.4 }}
              >
                {q}
              </motion.li>
            ))}
          </motion.ol>
        </motion.div>
      )}
    </div>
  );
};

export default GenerateSurvey;
