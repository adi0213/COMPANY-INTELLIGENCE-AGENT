import { useState } from 'react';
import { motion } from 'framer-motion';
import PageLayout from '../components/layout/PageLayout';

const mockChunks = [
  'Google is investing heavily in Gemini AI models and TPU hardware.',
  'Google Cloud Platform offers AI and ML services for enterprises.',
  'DeepMind is a subsidiary of Alphabet focused on AI safety research.',
];

const mockPrompt = (q: string, ctx: string) =>
  `System: You are a Company Intelligence Analyst. Answer strictly based on the provided context.\n\nContext:\n${ctx}\n\nQuestion: ${q}\n\nAnswer:`;

const mockAnswer = `Based on the retrieved context, Google is investing heavily in several key AI technologies:

1. **Gemini AI Models** — Google's next-generation multimodal AI system
2. **TPU Hardware** — Custom tensor processing units for AI training
3. **Google Cloud AI/ML Services** — Enterprise AI platform on GCP
4. **DeepMind Research** — Fundamental AI safety and capabilities research

These investments span hardware, models, cloud services, and fundamental research.`;

export default function RAGPage() {
  const [question, setQuestion] = useState('What AI technologies is Google investing in?');
  const [step, setStep] = useState(0);

  const steps = [
    { label: 'Retrieve', icon: '🔍' },
    { label: 'Context', icon: '📄' },
    { label: 'Prompt', icon: '✍️' },
    { label: 'LLM', icon: '🧠' },
    { label: 'Answer', icon: '✅' },
  ];

  const run = () => {
    setStep(0);
    let i = 0;
    const interval = setInterval(() => {
      i++;
      setStep(i);
      if (i >= steps.length) clearInterval(interval);
    }, 700);
  };

  const contextStr = mockChunks.map((c, i) => `[${i + 1}] ${c}`).join('\n');

  return (
    <PageLayout
      label="Phase 6"
      title="RETRIEVAL-AUGMENTED GENERATION"
      subtitle="Combine vector search with LLM generation to produce grounded, factual answers backed by real data."
    >
      <div className="grid-2" style={{ marginBottom: 48 }}>
        <div className="learn-block">
          <div className="learn-block__question">What is RAG?</div>
          <div className="learn-block__answer">RAG (Retrieval-Augmented Generation) is a technique where we first retrieve relevant documents from a vector database, inject them as context into the LLM's prompt, and then generate an answer. The LLM can only use the provided context, dramatically reducing hallucinations.</div>
        </div>
        <div className="learn-block">
          <div className="learn-block__question">Why not just ask the LLM directly?</div>
          <div className="learn-block__answer">LLMs have a knowledge cutoff date and hallucinate freely. RAG grounds the LLM's output in your actual data — it can only cite what the retriever found. This is the industry standard for enterprise AI.</div>
        </div>
      </div>

      {/* Input */}
      <div className="b-panel" style={{ marginBottom: 32 }}>
        <div className="b-panel__header">Ask a Question</div>
        <div className="b-panel__body">
          <div style={{ display: 'flex', gap: 12 }}>
            <input className="b-input" value={question} onChange={e => setQuestion(e.target.value)} style={{ flex: 1 }} />
            <button className="b-btn b-btn--accent" onClick={run}>▶ Run RAG</button>
          </div>
        </div>
      </div>

      {/* Pipeline Steps */}
      <div style={{ display: 'flex', gap: 0, marginBottom: 32, flexWrap: 'wrap' }}>
        {steps.map((s, i) => (
          <div key={s.label} style={{ display: 'flex', alignItems: 'center' }}>
            <motion.div
              animate={{
                background: step > i ? '#00C853' : step === i ? '#3366FF' : '#fff',
                color: step >= i ? '#fff' : '#000',
                boxShadow: step === i ? '4px 4px 0px #000' : 'none',
              }}
              style={{
                padding: '12px 24px',
                border: '3px solid #000',
                fontFamily: 'JetBrains Mono',
                fontWeight: 700,
                fontSize: '0.8rem',
                textTransform: 'uppercase',
                textAlign: 'center',
              }}
            >
              {s.icon} {s.label}
            </motion.div>
            {i < steps.length - 1 && (
              <div className="mono" style={{ padding: '0 8px', fontWeight: 800, fontSize: '1.2rem' }}>→</div>
            )}
          </div>
        ))}
      </div>

      {/* Step Content */}
      {step >= 1 && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="b-panel" style={{ marginBottom: 16 }}>
          <div className="b-panel__header">🔍 Retrieved Chunks (Top-3)</div>
          <div className="b-panel__body">
            {mockChunks.map((c, i) => (
              <div key={i} className="chunk">{c}</div>
            ))}
          </div>
        </motion.div>
      )}

      {step >= 3 && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="b-panel" style={{ marginBottom: 16 }}>
          <div className="b-panel__header">✍️ Constructed Prompt</div>
          <div className="b-panel__body">
            <pre className="b-code" style={{ fontSize: '0.75rem' }}>{mockPrompt(question, contextStr)}</pre>
          </div>
        </motion.div>
      )}

      {step >= 5 && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="b-panel">
          <div className="b-panel__header" style={{ background: '#00C853' }}>✅ Generated Answer (Grounded)</div>
          <div className="b-panel__body">
            <div style={{ whiteSpace: 'pre-wrap', lineHeight: 1.8 }}>{mockAnswer}</div>
          </div>
        </motion.div>
      )}
    </PageLayout>
  );
}
