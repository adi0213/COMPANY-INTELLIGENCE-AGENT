import React, { useState, useEffect } from 'react';

interface LoadingIndicatorProps {
  message?: string;
}

export default function LoadingIndicator({ message = "PROCESSING" }: LoadingIndicatorProps) {
  const [dots, setDots] = useState('');
  const [phraseIndex, setPhraseIndex] = useState(0);

  const phrases = [
    "INITIALIZING AI AGENTS...",
    "ANALYZING REQUIREMENTS...",
    "GENERATING ALGORITHMS...",
    "COMPILING LOGIC PUZZLES...",
    "VERIFYING QUALITY...",
    "ALMOST THERE..."
  ];

  useEffect(() => {
    const dotInterval = setInterval(() => {
      setDots(d => d.length >= 3 ? '' : d + '.');
    }, 500);

    const phraseInterval = setInterval(() => {
      setPhraseIndex(i => (i + 1) % phrases.length);
    }, 3000);

    return () => {
      clearInterval(dotInterval);
      clearInterval(phraseInterval);
    };
  }, [phrases.length]);

  return (
    <div className="b-card flex-center" style={{ flexDirection: 'column', padding: '100px 20px', border: '5px solid var(--info)' }}>
      <h1 style={{ marginBottom: 20 }}>{message}{dots}</h1>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: 15,
        marginTop: 20,
        fontFamily: 'var(--font-mono)'
      }}>
        <div style={{
          width: 40,
          height: 40,
          background: 'var(--accent)',
          border: '3px solid var(--primary)',
          animation: 'spin 2s linear infinite'
        }} />
        <p className="text-muted" style={{ fontSize: '1.2rem', fontWeight: 700, margin: 0 }}>
          {phrases[phraseIndex]}
        </p>
      </div>
      <style>{`
        @keyframes spin { 
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
