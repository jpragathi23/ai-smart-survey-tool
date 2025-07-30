# backend/app/services/llm_service.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# ------------------------
# LLM Prompt Generator
# ------------------------
def generate_questions(prompt: str, num_questions: int = 5):
    try:
        system_prompt = (
            "You are a survey expert. Generate well-structured, diverse, and clear survey questions based on the prompt."
        )

        user_prompt = (
            f"Prompt: {prompt}\n\nGenerate {num_questions} concise survey questions in JSON list format. Each question should include:"
            " 'text', 'type' (text, radio, checkbox), and optional 'options' list if applicable."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        # Try to safely parse content as JSON
        import json
        from ast import literal_eval

        content = response['choices'][0]['message']['content'].strip()

        try:
            questions = json.loads(content)
        except:
            questions = literal_eval(content)

        # Fallback safety check
        if not isinstance(questions, list):
            raise Exception("Invalid response format from LLM.")

        return questions

    except Exception as e:
        print(f"Error generating questions from LLM: {e}")
        return [
            {"text": "Default Question 1", "type": "text"},
            {"text": "Default Question 2", "type": "radio", "options": ["Yes", "No"]}
        ]
