const express = require('express');
const router = express.Router();
const { OpenAI } = require('openai');

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

router.post('/diagnose', async (req, res) => {
  const { age, symptoms, healthConditions } = req.body;

  const prompt = `
A patient aged ${age} reports the following symptoms: ${symptoms}.
Health conditions: ${healthConditions || "none"}.
Based on WHO/CDC guidelines, provide:
1. Likely disease/illness
2. Suggested treatment or cure
3. Specialist type to consult (e.g., Dermatologist)
`;

  try {
    const chatCompletion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        { role: 'system', content: 'You are a healthcare assistant AI trained on CDC and WHO data.' },
        { role: 'user', content: prompt }
      ],
      temperature: 0.5,
    });

    const response = chatCompletion.choices[0].message.content;
    res.status(200).json({ diagnosis: response });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Error generating response from GPT" });
  }
});
const axios = require('axios');

const getDoctorRecommendations = async (speciality) => {
  const res = await axios.get(`http://localhost:5000/api/doctors/${speciality}`);
  return res.data;
};

module.exports = router;
