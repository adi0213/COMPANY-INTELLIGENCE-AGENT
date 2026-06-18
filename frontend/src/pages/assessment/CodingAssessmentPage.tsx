import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { assessmentApi } from '../../services/assessmentApi';
import LoadingIndicator from '../../components/common/LoadingIndicator';

export default function CodingAssessmentPage() {
  const navigate = useNavigate();
  const [level, setLevel] = useState('beginner');
  const [questions, setQuestions] = useState<any[]>([]);
  const [answers, setAnswers] = useState<string[]>([]);
  const [languages, setLanguages] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const data = await assessmentApi.generate('coding', level, 5);
      setQuestions(data.questions);
      setAnswers(new Array(data.questions.length).fill(''));
      setLanguages(new Array(data.questions.length).fill('Python'));
    } catch (error) {
      console.error(error);
      alert('Failed to generate questions. Please make sure the backend is running with LLM keys.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      const formattedAnswers = answers.map((ans, i) => `[LANGUAGE: ${languages[i]}]\n${ans}`);
      const data = await assessmentApi.submit('coding', questions, formattedAnswers);
      navigate('/assessment/results', { state: { result: data } });
    } catch (error) {
      console.error(error);
      alert('Failed to submit assessment.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="container section">
        <LoadingIndicator message="GENERATING CODING CHALLENGES" />
      </div>
    );
  }

  if (submitting) {
    return (
      <div className="container section">
        <LoadingIndicator message="EVALUATING SOLUTIONS" />
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="container section">
        <div className="b-card" style={{ maxWidth: 600, margin: '0 auto', textAlign: 'center' }}>
          <h1 className="page__hero-title">CODING ASSESSMENT</h1>
          <p className="page__hero-subtitle" style={{ marginBottom: 30, margin: '0 auto' }}>
            Test your algorithmic problem-solving skills with 5 AI-generated questions.
          </p>
          
          <div style={{ marginBottom: 30 }}>
            <label style={{ display: 'block', marginBottom: 10, fontWeight: 700, fontFamily: 'var(--font-mono)' }}>SELECT TARGET ROLE LEVEL:</label>
            <select className="b-input" value={level} onChange={(e) => setLevel(e.target.value)} style={{ maxWidth: 300 }}>
              <option value="beginner">Beginner (Intern / Junior)</option>
              <option value="learner">Learner (Mid-Level)</option>
              <option value="expert">Expert (Senior / Staff)</option>
            </select>
          </div>

          <button 
            onClick={handleGenerate} 
            className="b-btn b-btn--accent"
          >
            START ASSESSMENT
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container section">
      <div style={{ maxWidth: 800, margin: '0 auto' }}>
        <h1 style={{ borderBottom: '5px solid var(--primary)', paddingBottom: 20, marginBottom: 40 }}>
          CODING ASSESSMENT
        </h1>
        
        {questions.map((q, index) => (
          <div key={index} className="b-card" style={{ marginBottom: 40 }}>
            <h2 style={{ borderBottom: '3px solid var(--primary)', paddingBottom: 10, marginBottom: 20 }}>
              QUESTION {index + 1}: {q.title}
            </h2>
            
            <div style={{ marginBottom: 20 }}>
              <span className="b-badge b-badge--info" style={{ marginRight: 10 }}>{q.difficulty}</span>
              <span className="b-badge b-badge--secondary">{q.topic}</span>
            </div>

            <p style={{ whiteSpace: 'pre-wrap', marginBottom: 20 }}>{q.problem_statement}</p>
            
            <div className="b-code" style={{ marginBottom: 20 }}>
              <p><strong>Input:</strong> {q.example_input}</p>
              <p><strong>Output:</strong> {q.example_output}</p>
              <p className="text-muted" style={{ marginTop: 10 }}>Time: {q.expected_time_complexity} | Space: {q.expected_space_complexity}</p>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
              <label style={{ fontWeight: 700, fontFamily: 'var(--font-mono)' }}>LANGUAGE:</label>
              <select
                className="b-input"
                value={languages[index] || 'Python'}
                onChange={(e) => {
                  const newLangs = [...languages];
                  newLangs[index] = e.target.value;
                  setLanguages(newLangs);
                }}
                style={{ width: '200px', padding: '10px', marginBottom: 0 }}
              >
                <option value="Python">Python</option>
                <option value="Java">Java</option>
                <option value="C++">C++</option>
                <option value="C">C</option>
              </select>
            </div>

            <textarea
              className="b-input"
              value={answers[index]}
              onChange={(e) => {
                const newAnswers = [...answers];
                newAnswers[index] = e.target.value;
                setAnswers(newAnswers);
              }}
              placeholder="// WRITE YOUR CODE HERE..."
              style={{ height: '200px' }}
            />
          </div>
        ))}

        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 40 }}>
          <button 
            onClick={handleSubmit} 
            disabled={submitting}
            className="b-btn b-btn--primary"
          >
            {submitting ? 'EVALUATING...' : 'SUBMIT ANSWERS'}
          </button>
        </div>
      </div>
    </div>
  );
}
