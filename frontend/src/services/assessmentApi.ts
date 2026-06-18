const API_BASE_URL = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api/v1';

export const assessmentApi = {
  generate: async (type: string, level: string, count: number = 5) => {
    const response = await fetch(`${API_BASE_URL}/assessment/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ type, level, count }),
    });
    if (!response.ok) {
      throw new Error('Failed to generate assessment');
    }
    return response.json();
  },

  submit: async (assessmentType: string, questions: any[], answers: any[]) => {
    const response = await fetch(`${API_BASE_URL}/assessment/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ assessment_type: assessmentType, questions, answers }),
    });
    if (!response.ok) {
      throw new Error('Failed to submit assessment');
    }
    return response.json();
  },

  submitFull: async (codingQuestions: any[], codingAnswers: any[], aptitudeQuestions: any[], aptitudeAnswers: any[]) => {
    const response = await fetch(`${API_BASE_URL}/assessment/submit_full`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        coding_questions: codingQuestions, 
        coding_answers: codingAnswers,
        aptitude_questions: aptitudeQuestions,
        aptitude_answers: aptitudeAnswers
      }),
    });
    if (!response.ok) {
      throw new Error('Failed to submit full assessment');
    }
    return response.json();
  },

  analyze: async (results: any) => {
    const response = await fetch(`${API_BASE_URL}/assessment/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ results }),
    });
    if (!response.ok) {
      throw new Error('Failed to analyze assessment');
    }
    return response.json();
  }
};
