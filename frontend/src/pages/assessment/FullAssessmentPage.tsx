import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { assessmentApi } from '../../services/assessmentApi';
import LoadingIndicator from '../../components/common/LoadingIndicator';

export default function FullAssessmentPage() {
  const navigate = useNavigate();
  const [phase, setPhase] = useState<'setup' | 'generating' | 'coding' | 'aptitude' | 'submitting'>('setup');
  const [level, setLevel] = useState('learner');
  
  const [codingQuestions, setCodingQuestions] = useState<any[]>([]);
  const [codingAnswers, setCodingAnswers] = useState<string[]>([]);
  const [codingLanguages, setCodingLanguages] = useState<string[]>([]);
  const [currentCodingIndex, setCurrentCodingIndex] = useState(0);

  const [aptitudeQuestions, setAptitudeQuestions] = useState<any[]>([]);
  const [aptitudeAnswers, setAptitudeAnswers] = useState<string[]>([]);
  const [currentAptitudeIndex, setCurrentAptitudeIndex] = useState(0);

  // Sequential generation to prevent OOM
  const handleGenerate = async () => {
    setPhase('generating');
    try {
      // 1. Generate Coding
      const codingData = await assessmentApi.generate('coding', level, 5);
      setCodingQuestions(codingData.questions);
      setCodingAnswers(new Array(codingData.questions.length).fill(''));
      setCodingLanguages(new Array(codingData.questions.length).fill('Python'));
      
      // 2. Generate Aptitude
      const aptitudeData = await assessmentApi.generate('aptitude', level, 10);
      setAptitudeQuestions(aptitudeData.questions);
      setAptitudeAnswers(new Array(aptitudeData.questions.length).fill(''));
      
      setPhase('coding');
    } catch (error) {
      console.error(error);
      alert('Failed to generate the full assessment.');
      setPhase('setup');
    }
  };

  const handleNextCoding = () => {
    if (currentCodingIndex < codingQuestions.length - 1) {
      setCurrentCodingIndex(curr => curr + 1);
    } else {
      setPhase('aptitude');
    }
  };

  const handleNextAptitude = () => {
    if (currentAptitudeIndex < aptitudeQuestions.length - 1) {
      setCurrentAptitudeIndex(curr => curr + 1);
    } else {
      handleSubmit();
    }
  };

  const handleSubmit = async () => {
    setPhase('submitting');
    try {
      const formattedCodingAnswers = codingAnswers.map((ans, i) => `[LANGUAGE: ${codingLanguages[i]}]\n${ans}`);
      const data = await assessmentApi.submitFull(
        codingQuestions, formattedCodingAnswers, 
        aptitudeQuestions, aptitudeAnswers
      );
      navigate('/assessment/results', { state: { result: data } });
    } catch (error) {
      console.error(error);
      alert('Failed to submit full assessment.');
      setPhase('aptitude');
    }
  };

  const renderSetup = () => (
    <div className="b-card">
      <h1 className="page__hero-title">FULL ASSESSMENT</h1>
      <p className="page__hero-subtitle" style={{ marginBottom: 20 }}>
        A comprehensive evaluation comprising 5 LeetCode-style technical problems and 10 Aptitude logic puzzles.
      </p>
      
      <div style={{ marginBottom: 30 }}>
        <label style={{ display: 'block', marginBottom: 10, fontWeight: 700, fontFamily: 'var(--font-mono)' }}>SELECT TARGET ROLE LEVEL:</label>
        <select 
          className="b-input"
          value={level} 
          onChange={(e) => setLevel(e.target.value)} 
          style={{ maxWidth: 300 }}
        >
          <option value="beginner">Beginner (Intern / Junior)</option>
          <option value="learner">Learner (Mid-Level)</option>
          <option value="expert">Expert (Senior / Staff)</option>
        </select>
      </div>

      <button className="b-btn b-btn--accent" onClick={handleGenerate}>
        START COMPREHENSIVE ASSESSMENT
      </button>
    </div>
  );

  const renderGenerating = () => (
    <LoadingIndicator message="GENERATING ASSESSMENT" />
  );

  const renderSubmitting = () => (
    <LoadingIndicator message="EVALUATING ANSWERS" />
  );

  const renderCoding = () => {
    const q = codingQuestions[currentCodingIndex];
    if (!q) return null;
    return (
      <div className="b-card">
        <h2 style={{ borderBottom: '3px solid var(--primary)', paddingBottom: 10, marginBottom: 20 }}>
          CODING CHALLENGE [{currentCodingIndex + 1}/{codingQuestions.length}]
        </h2>
        
        <div style={{ marginBottom: 20 }}>
          <span className="b-badge b-badge--info" style={{ marginRight: 10 }}>{q.difficulty}</span>
          <span className="b-badge b-badge--secondary">{q.topic}</span>
        </div>

        <h3>{q.title}</h3>
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
            value={codingLanguages[currentCodingIndex] || 'Python'}
            onChange={(e) => {
              const newLangs = [...codingLanguages];
              newLangs[currentCodingIndex] = e.target.value;
              setCodingLanguages(newLangs);
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
          value={codingAnswers[currentCodingIndex] || ''}
          onChange={(e) => {
            const newAns = [...codingAnswers];
            newAns[currentCodingIndex] = e.target.value;
            setCodingAnswers(newAns);
          }}
          placeholder="// WRITE YOUR OPTIMAL SOLUTION HERE"
          style={{ height: '300px', marginBottom: 20 }}
        />

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button className="b-btn b-btn--primary" onClick={handleNextCoding}>
            {currentCodingIndex === codingQuestions.length - 1 ? 'PROCEED TO APTITUDE →' : 'NEXT QUESTION'}
          </button>
        </div>
      </div>
    );
  };

  const renderAptitude = () => {
    const q = aptitudeQuestions[currentAptitudeIndex];
    if (!q) return null;
    return (
      <div className="b-card">
        <h2 style={{ borderBottom: '3px solid var(--primary)', paddingBottom: 10, marginBottom: 20 }}>
          APTITUDE QUESTION [{currentAptitudeIndex + 1}/{aptitudeQuestions.length}]
        </h2>
        
        <div style={{ marginBottom: 20 }}>
          <span className="b-badge b-badge--accent">{q.topic}</span>
        </div>

        <p style={{ fontSize: '1.2rem', marginBottom: 30, fontWeight: 600 }}>{q.question}</p>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: 15, marginBottom: 30 }}>
          {q.options.map((opt: string, i: number) => {
            const isSelected = aptitudeAnswers[currentAptitudeIndex] === opt;
            return (
              <button
                key={i}
                onClick={() => {
                  const newAns = [...aptitudeAnswers];
                  newAns[currentAptitudeIndex] = opt;
                  setAptitudeAnswers(newAns);
                }}
                className={`b-btn ${isSelected ? 'b-btn--accent' : ''}`}
                style={{ justifyContent: 'flex-start', textTransform: 'none' }}
              >
                {opt}
              </button>
            );
          })}
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button 
            className={`b-btn ${aptitudeAnswers[currentAptitudeIndex] ? 'b-btn--primary' : ''}`}
            disabled={!aptitudeAnswers[currentAptitudeIndex]}
            onClick={handleNextAptitude}
          >
            {currentAptitudeIndex === aptitudeQuestions.length - 1 ? 'SUBMIT ASSESSMENT' : 'NEXT QUESTION'}
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="container section">
      <div style={{ maxWidth: 800, margin: '0 auto' }}>
        {/* Progress Display */}
        {(phase === 'coding' || phase === 'aptitude') && (
          <div className="b-panel" style={{ marginBottom: 20 }}>
            <div className="b-panel__header flex-between">
              <span>PROGRESS</span>
              <span>PHASE: {phase.toUpperCase()}</span>
            </div>
            <div style={{ height: 10, background: 'var(--primary)', width: `${((phase === 'coding' ? currentCodingIndex : 5 + currentAptitudeIndex) / 15) * 100}%` }} />
          </div>
        )}

        {phase === 'setup' && renderSetup()}
        {phase === 'generating' && renderGenerating()}
        {phase === 'coding' && renderCoding()}
        {phase === 'aptitude' && renderAptitude()}
        {phase === 'submitting' && renderSubmitting()}
      </div>
    </div>
  );
}
