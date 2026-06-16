import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import PageLayout from '../components/layout/PageLayout';

const pipelineSteps = [
  { label: 'Collection', icon: '📥', duration: 1200, detail: 'Fetching data from 4 sources...', output: '{"company": "Google", "founded": "1998"}' },
  { label: 'Cleaning', icon: '🧹', duration: 600, detail: 'Removing HTML, normalizing dates...', output: '"Google LLC, founded 1998, HQ Mountain View"' },
  { label: 'Chunking', icon: '✂️', duration: 400, detail: 'Splitting into 12 chunks (size=200, overlap=30)...', output: '[Chunk_01, Chunk_02, ... Chunk_12]' },
  { label: 'Tokenization', icon: '🔤', duration: 300, detail: 'Converting to 2,847 tokens...', output: '[1045, 2398, 887, 1123, ...]' },
  { label: 'Embeddings', icon: '🧮', duration: 900, detail: 'Generating 384-dim vectors via SBERT...', output: '[[0.023, -0.145, 0.891, ...], ...]' },
  { label: 'Vector DB', icon: '🗄️', duration: 200, detail: 'Indexing in ChromaDB...', output: 'Stored 12 vectors. Index updated.' },
  { label: 'Retrieval', icon: '🔍', duration: 150, detail: 'Top-5 chunks retrieved (cosine sim > 0.82)', output: '[chunk_001 (0.94), chunk_002 (0.88), ...]' },
  { label: 'RAG', icon: '🧠', duration: 2000, detail: 'Constructing prompt and querying Llama 3.1...', output: 'Google invests in Gemini, TPUs, and Cloud AI...' },
  { label: 'Agents', icon: '🤖', duration: 1500, detail: 'Coordinator → TechAgent + HiringAgent', output: 'Agent reports synthesized.' },
  { label: 'Report', icon: '📊', duration: 800, detail: 'Building executive summary, risks, opportunities...', output: '# Company Intelligence Report: Google\n...' },
];

export default function LiveDemoPage() {
  const [company, setCompany] = useState('Google');
  const [currentStep, setCurrentStep] = useState(-1);
  const [isRunning, setIsRunning] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const runPipeline = () => {
    if (!company.trim()) return;
    setIsRunning(true);
    setCurrentStep(0);
  };

  useEffect(() => {
    if (currentStep < 0 || currentStep >= pipelineSteps.length) return;

    timerRef.current = setTimeout(() => {
      if (currentStep < pipelineSteps.length - 1) {
        setCurrentStep(prev => prev + 1);
      } else {
        setIsRunning(false);
      }
    }, pipelineSteps[currentStep].duration);

    return () => { if (timerRef.current) clearTimeout(timerRef.current); };
  }, [currentStep]);

  const reset = () => {
    setCurrentStep(-1);
    setIsRunning(false);
  };

  return (
    <PageLayout
      label="Live Demo"
      title="END-TO-END PIPELINE"
      subtitle="Watch data flow through every stage of the Company Intelligence Agent in real time."
    >
      {/* Input */}
      <div className="b-panel" style={{ marginBottom: 32 }}>
        <div className="b-panel__header">Enter a Company</div>
        <div className="b-panel__body">
          <div style={{ display: 'flex', gap: 12 }}>
            <input className="b-input" value={company} onChange={e => setCompany(e.target.value)} disabled={isRunning} style={{ maxWidth: 400 }} />
            <button className="b-btn b-btn--accent" onClick={runPipeline} disabled={isRunning}>
              {isRunning ? '⏳ Running...' : '▶ Run Pipeline'}
            </button>
            <button className="b-btn" onClick={reset} disabled={isRunning}>Reset</button>
          </div>
        </div>
      </div>

      {/* Pipeline Steps */}
      {pipelineSteps.map((step, i) => {
        const isDone = currentStep > i;
        const isActive = currentStep === i;
        const isIdle = currentStep < i;

        return (
          <div key={step.label}>
            {i > 0 && (
              <div style={{ textAlign: 'center' }}>
                <motion.div
                  className="mono"
                  style={{ fontWeight: 800, fontSize: '1.2rem', color: isDone ? '#00C853' : '#ddd' }}
                  animate={{ color: isDone ? '#00C853' : isActive ? '#3366FF' : '#ddd' }}
                >
                  ↓
                </motion.div>
              </div>
            )}
            <motion.div
              animate={{
                borderColor: isDone ? '#00C853' : isActive ? '#3366FF' : '#ddd',
                opacity: isIdle && currentStep >= 0 ? 0.4 : 1,
              }}
              style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: 16,
                padding: 16,
                border: '3px solid #ddd',
                background: isActive ? '#EEF2FF' : '#fff',
                marginBottom: 4,
              }}
            >
              {/* Status icon */}
              <div style={{
                width: 40, height: 40, display: 'flex', alignItems: 'center', justifyContent: 'center',
                border: '3px solid #000', fontWeight: 800, fontSize: '1.2rem', flexShrink: 0,
                background: isDone ? '#00C853' : isActive ? '#3366FF' : '#fff',
                color: isDone || isActive ? '#fff' : '#000',
              }}>
                {isDone ? '✓' : step.icon}
              </div>

              {/* Content */}
              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span className="mono" style={{ fontWeight: 700, fontSize: '0.85rem', textTransform: 'uppercase' }}>
                    {step.label}
                  </span>
                  <span className={`b-badge ${isDone ? 'b-badge--success' : isActive ? 'b-badge--info' : ''}`}>
                    {isDone ? 'Complete' : isActive ? 'Processing...' : 'Pending'}
                  </span>
                </div>

                {(isActive || isDone) && (
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                    <div className="text-muted" style={{ fontSize: '0.85rem', margin: '8px 0' }}>{step.detail}</div>
                    {isDone && (
                      <pre className="b-code" style={{ fontSize: '0.75rem', padding: 8 }}>{step.output}</pre>
                    )}
                  </motion.div>
                )}
              </div>

              {/* Latency */}
              <div className="mono" style={{ fontSize: '0.75rem', color: '#888', flexShrink: 0, minWidth: 60, textAlign: 'right' }}>
                {isDone ? `${step.duration}ms` : ''}
              </div>
            </motion.div>
          </div>
        );
      })}

      {/* Final Result */}
      {currentStep >= pipelineSteps.length - 1 && !isRunning && currentStep >= 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          style={{ marginTop: 32, textAlign: 'center' }}
        >
          <div className="b-card b-card--dark" style={{ display: 'inline-block', padding: '24px 48px' }}>
            <div style={{ fontSize: '2rem', marginBottom: 8 }}>✅</div>
            <h3 style={{ color: '#00C853' }}>Pipeline Complete</h3>
            <p style={{ color: '#aaa', marginTop: 8 }}>
              Total time: {pipelineSteps.reduce((s, p) => s + p.duration, 0).toLocaleString()}ms
            </p>
          </div>
        </motion.div>
      )}
    </PageLayout>
  );
}
