import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useCompanyStore } from '../store/companyStore';
import { analyzeCompany } from '../services/api';

const popularCompanies = ['Google', 'Microsoft', 'Amazon', 'Apple', 'Netflix', 'OpenAI', 'NVIDIA', 'Tesla', 'Meta', 'Spotify'];

const loadingStages = [
  'Collecting company data from sources...',
  'Cleaning & normalizing data...',
  'Generating embeddings & indexing in ChromaDB...',
  'Running Company Overview Agent...',
  'Running News Agent...',
  'Running Technology Agent...',
  'Running Hiring & Salary Agents...',
  'Running Interview Agent...',
  'Generating executive summary...',
  'Compiling intelligence report...',
];

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

const stagger = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08 } },
};

export default function HomePage() {
  const [input, setInput] = useState('');
  const { loading, loadingStage, setLoading, setLoadingStage, setResult, setError, setQuery, error } = useCompanyStore();
  const navigate = useNavigate();

  const handleSearch = async (companyName?: string) => {
    const name = (companyName || input).trim();
    if (!name || loading) return;

    setQuery(name);
    setLoading(true);
    setError(null);
    setResult(null);

    // Animate through loading stages — real pipeline takes 30-90 seconds
    let stageIdx = 0;
    setLoadingStage(loadingStages[0]);
    const interval = setInterval(() => {
      stageIdx++;
      if (stageIdx < loadingStages.length) {
        setLoadingStage(loadingStages[stageIdx]);
      }
    }, 8000); // ~8 seconds per stage for real pipeline

    try {
      const result = await analyzeCompany(name);
      clearInterval(interval);
      setResult(result);
      setLoading(false);
      navigate(`/company/${encodeURIComponent(name)}`);
    } catch (err: unknown) {
      clearInterval(interval);
      setLoading(false);
      const message = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(message);
    }
  };

  return (
    <div className="page">
      {/* ── Hero Search ─────────────────────────────────── */}
      <section style={{
        minHeight: 'calc(100vh - 60px)',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '64px 24px',
        borderBottom: '5px solid #000',
      }}>
        <motion.div
          initial="hidden"
          animate="show"
          variants={stagger}
          style={{ textAlign: 'center', maxWidth: 800, width: '100%' }}
        >
          <motion.p
            variants={fadeUp}
            className="mono"
            style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.2em', color: '#888', marginBottom: 16 }}
          >
            AI-Powered Company Research
          </motion.p>

          <motion.h1 variants={fadeUp} style={{ fontSize: 'clamp(2.5rem, 6vw, 4.5rem)', marginBottom: 16 }}>
            COMPANY
            <br />
            <span style={{ color: '#FFD400', WebkitTextStroke: '2px #000' }}>INTELLIGENCE_</span>
          </motion.h1>

          <motion.p variants={fadeUp} style={{ fontSize: '1.1rem', color: '#888', maxWidth: 500, margin: '0 auto 40px', lineHeight: 1.7 }}>
            Search any company and receive AI-powered insights on technology, hiring, salary, interviews, and strategy.
          </motion.p>

          {/* Search Bar */}
          <motion.div variants={fadeUp} style={{ display: 'flex', gap: 0, maxWidth: 600, margin: '0 auto', width: '100%' }}>
            <input
              className="b-input"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSearch()}
              placeholder="Enter company name..."
              disabled={loading}
              style={{
                fontSize: '1.1rem',
                padding: '18px 24px',
                borderRight: 'none',
                flex: 1,
              }}
            />
            <button
              className="b-btn b-btn--primary"
              onClick={() => handleSearch()}
              disabled={loading}
              style={{ padding: '18px 32px', fontSize: '0.9rem', whiteSpace: 'nowrap' }}
            >
              {loading ? '⏳ Analyzing...' : '→ ANALYZE'}
            </button>
          </motion.div>

          {/* Loading Pipeline Animation */}
          {loading && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              style={{ marginTop: 32, maxWidth: 500, margin: '32px auto 0' }}
            >
              <div style={{
                padding: '16px 24px',
                border: '3px solid #3366FF',
                background: '#EEF2FF',
                fontFamily: 'JetBrains Mono, monospace',
                fontWeight: 700,
                fontSize: '0.85rem',
                textAlign: 'left',
              }}>
                <motion.div
                  key={loadingStage}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  style={{ display: 'flex', alignItems: 'center', gap: 8 }}
                >
                  <motion.span
                    animate={{ rotate: 360 }}
                    transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}
                    style={{ display: 'inline-block' }}
                  >
                    ⚙️
                  </motion.span>
                  {loadingStage}
                </motion.div>
              </div>
              <p className="mono text-muted" style={{ fontSize: '0.7rem', marginTop: 8, textAlign: 'center' }}>
                Full AI pipeline running — this may take 30-90 seconds.
              </p>
            </motion.div>
          )}

          {/* Error Display */}
          {error && !loading && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              style={{ marginTop: 24, maxWidth: 600, margin: '24px auto 0' }}
            >
              <div style={{
                padding: '16px 24px',
                border: '3px solid #FF5A36',
                background: '#FFF5F5',
                textAlign: 'left',
              }}>
                <div className="mono" style={{ fontWeight: 700, fontSize: '0.8rem', color: '#FF5A36', marginBottom: 8 }}>
                  ⚠ Connection Error
                </div>
                <p style={{ fontSize: '0.9rem', marginBottom: 12 }}>{error}</p>
                <div className="mono" style={{ fontSize: '0.75rem', color: '#888' }}>
                  Make sure the backend is running:
                </div>
                <pre className="b-code" style={{ fontSize: '0.75rem', padding: 8, marginTop: 8 }}>
                  {`cd "d:/LLM/Company Intelligent agents"\nuvicorn app.main:app --reload`}
                </pre>
                <div className="mono" style={{ fontSize: '0.75rem', color: '#888', marginTop: 8 }}>
                  Also ensure Ollama is running with llama3.1:
                </div>
                <pre className="b-code" style={{ fontSize: '0.75rem', padding: 8, marginTop: 8 }}>
                  {`ollama run llama3.1`}
                </pre>
              </div>
            </motion.div>
          )}

          {/* Popular Companies */}
          {!loading && (
            <motion.div variants={fadeUp} style={{ marginTop: 48 }}>
              <p className="mono" style={{ fontSize: '0.7rem', textTransform: 'uppercase', letterSpacing: '0.15em', color: '#888', marginBottom: 12 }}>
                Try Searching
              </p>
              <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', justifyContent: 'center' }}>
                {popularCompanies.map(c => (
                  <button
                    key={c}
                    className="b-btn b-btn--sm"
                    onClick={() => { setInput(c); handleSearch(c); }}
                    disabled={loading}
                    style={{ fontSize: '0.75rem' }}
                  >
                    {c}
                  </button>
                ))}
              </div>
            </motion.div>
          )}
        </motion.div>
      </section>

      {/* ── Features Grid ────────────────────────────────── */}
      <section style={{ padding: '64px 24px', borderBottom: '5px solid #000' }}>
        <div className="container">
          <h2 style={{ marginBottom: 48, textAlign: 'center' }}>INTELLIGENCE SECTIONS</h2>
          <div className="grid-4">
            {[
              { icon: '🏢', title: 'Company Overview', desc: 'Industry, leadership, and operations' },
              { icon: '📰', title: 'Latest Developments', desc: 'News, launches, and announcements' },
              { icon: '⚙️', title: 'Key Technologies', desc: 'Tech stack, platforms, and tools' },
              { icon: '📊', title: 'Business Areas', desc: 'Revenue drivers and growth areas' },
              { icon: '🎯', title: 'Interview Focus', desc: 'Technical and behavioral topics' },
              { icon: '💼', title: 'Hiring Trends', desc: 'Open roles and skill demands' },
              { icon: '💰', title: 'Salary Insights', desc: 'Compensation across roles' },
              { icon: '📋', title: 'Executive Summary', desc: 'AI-generated strategic analysis' },
            ].map(f => (
              <motion.div
                key={f.title}
                className="b-card"
                whileHover={{ y: -4, boxShadow: '6px 6px 0px #000' }}
              >
                <div style={{ fontSize: '1.8rem', marginBottom: 8 }}>{f.icon}</div>
                <h4 className="mono" style={{ fontSize: '0.85rem', marginBottom: 4 }}>{f.title}</h4>
                <p className="text-muted" style={{ fontSize: '0.8rem' }}>{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Learn More ────────────────────────────────── */}
      <section style={{ padding: '32px 24px', background: '#000', color: '#fff' }}>
        <div className="container" style={{ textAlign: 'center' }}>
          <p className="mono" style={{ fontSize: '0.8rem', color: '#aaa', marginBottom: 12 }}>
            Want to understand how this AI system works internally?
          </p>
          <button className="b-btn b-btn--accent" onClick={() => navigate('/architecture')}>
            Explore the Architecture →
          </button>
        </div>
      </section>
    </div>
  );
}
