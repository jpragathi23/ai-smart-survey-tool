// frontend/src/services/api.js

export async function generateSurveyFromPrompt({ prompt, numQuestions, surveyTitle, surveyDescription }) {
  const queryParams = new URLSearchParams({
    prompt,
    num_questions: numQuestions,
    survey_title: surveyTitle,
    survey_description: surveyDescription
  });

  const response = await fetch(`http://localhost:8000/api/surveys/generate-from-prompt?${queryParams}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({})
  });

  if (!response.ok) {
    throw new Error("Failed to generate survey");
  }

  return await response.json();
}
