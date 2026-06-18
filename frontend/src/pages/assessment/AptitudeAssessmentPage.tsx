import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { assessmentApi } from '../../services/assessmentApi';
import LoadingIndicator from '../../components/common/LoadingIndicator';

export default function AptitudeAssessmentPage() {
  const navigate = useNavigate();
  const [level, setLevel] = useState('beginner');
  const [questions, setQuestions] = useState<any[]>([]);
  const [answers, setAnswers] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const data = await assessmentApi.generate('aptitude', level, 10);
      setQuestions(data.questions);
      setAnswers(new Array(data.questions.length).fill(''));
    } catch (error) {
      console.error(error);
      alert('Failed to generate questions.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      const data = await assessmentApi.submit('aptitude', questions, answers);
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
        <LoadingIndicator message="GENERATING APTITUDE PUZZLES" />
      </div>
    );
  }

  if (submitting) {
    return (
      <div className="container section">
        <LoadingIndicator message="EVALUATING RESPONSES" />
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="container section">
        <div className="b-card" style={{ maxWidth: 600, margin: '0 auto', textAlign: 'center' }}>
          <h1 className="page__hero-title">APTITUDE ASSESSMENT</h1>
          <p className="page__hero-subtitle" style={{ marginBottom: 30, margin: '0 auto' }}>
            Test your quantitative, logical, and verbal skills with 10 questions.
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
          APTITUDE ASSESSMENT
        </h1>
        
        {questions.map((q, index) => (
          <div key={index} className="b-card" style={{ marginBottom: 40 }}>
            <h2 style={{ borderBottom: '3px solid var(--primary)', paddingBottom: 10, marginBottom: 20 }}>
              QUESTION {index + 1}
            </h2>
            
            <div style={{ marginBottom: 20 }}>
              <span className="b-badge b-badge--accent">{q.topic}</span>
            </div>

            <p style={{ fontSize: '1.2rem', marginBottom: 30, fontWeight: 600 }}>{q.question}</p>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: 15 }}>
              {q.options.map((opt: string, optIndex: number) => {
                const isSelected = answers[index] === opt;
                return (
                  <button
                    key={optIndex}
                    onClick={() => {
                      const newAnswers = [...answers];
                      newAnswers[index] = opt;
                      setAnswers(newAnswers);
                    }}
                    className={`b-btn ${isSelected ? 'b-btn--accent' : ''}`}
                    style={{ justifyContent: 'flex-start', textTransform: 'none' }}
                  >
                    {opt}
                  </button>
                );
              })}
            </div>
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
