import React, { useState } from 'react';
import axios from 'axios';

const SurveyBuilder = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [prompt, setPrompt] = useState('');
  const [numQuestions, setNumQuestions] = useState(5);
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleGenerateSurvey = async () => {
    if (!title || !description || !prompt) {
      alert('Please fill in all fields');
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(
        'http://localhost:8000/api/surveys/generate-from-prompt',
        {
          prompt,
          num_questions: numQuestions,
          survey_title: title,
          survey_description: description,
        }
      );
      setQuestions(response.data.questions || []);
    } catch (error) {
      console.error('Error generating survey:', error);
      alert('Survey generation failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-3xl mx-auto bg-white shadow-lg rounded-xl mt-6">
      <h2 className="text-2xl font-bold mb-4 text-center">🧠 AI Survey Builder</h2>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Survey Title</label>
        <input
          className="w-full px-4 py-2 border rounded-lg"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="e.g. Customer Satisfaction Survey"
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Survey Description</label>
        <textarea
          className="w-full px-4 py-2 border rounded-lg"
          rows={3}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Brief description of your survey"
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">AI Prompt</label>
        <input
          className="w-full px-4 py-2 border rounded-lg"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="e.g. Generate questions for an employee engagement survey"
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Number of Questions</label>
        <input
          type="number"
          className="w-full px-4 py-2 border rounded-lg"
          value={numQuestions}
          onChange={(e) => setNumQuestions(Number(e.target.value))}
          min={1}
          max={20}
        />
      </div>

      <button
        onClick={handleGenerateSurvey}
        className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
        disabled={loading}
      >
        {loading ? 'Generating...' : 'Generate Survey'}
      </button>

      {questions.length > 0 && (
        <div className="mt-6">
          <h3 className="text-xl font-semibold mb-2">📝 Generated Questions:</h3>
          <ul className="list-disc pl-5">
            {questions.map((q, idx) => (
              <li key={idx} className="mb-1">{q}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default SurveyBuilder;

