// backend/index.js

const express = require('express');
const cors = require('cors');
require('dotenv').config(); // To use .env variables

const OpenAI = require('openai');

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

const app = express();
app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.send('Smart Survey Backend Running ✅');
});

// Health check endpoint for Render
app.get('/healthz', (req, res) => {
  res.status(200).send('OK');
});

app.post('/api/survey', async (req, res) => {
  const { topic, language } = req.body;

  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: [
        {
          role: 'user',
          content: `Generate 5 survey questions on the topic "${topic}" in ${language}.`
        }
      ]
    });

    const questions = response.choices[0].message.content
      .trim()
      .split('\n')
      .filter(q => q.trim() !== '');
    res.json({ questions });
  } catch (error) {
    console.error('OpenAI API Error:', error);
    res.status(500).json({ error: 'Survey generation failed' });
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Backend server is running on http://localhost:${PORT}`);
});
