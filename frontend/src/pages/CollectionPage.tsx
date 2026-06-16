import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import PageLayout from '../components/layout/PageLayout';

const collectors = [
  { name: 'Company Collector', icon: '🏢', data: { name: 'Google LLC', founded: '1998', ceo: 'Sundar Pichai', hq: 'Mountain View, CA' } },
  { name: 'News Collector', icon: '📰', data: { title: 'Google launches Gemini 2.0', source: 'TechCrunch', date: '2024-12-01' } },
  { name: 'Hiring Collector', icon: '💼', data: { roles_found: 142, top_role: 'Senior ML Engineer', locations: ['Remote', 'NYC', 'London'] } },
  { name: 'Salary Collector', icon: '💰', data: { avg_salary: '$185,000', range: '$120K - $350K', equity: 'RSUs Included' } },
];

export default function CollectionPage() {
  const [company, setCompany] = useState('');
  const [isCollecting, setIsCollecting] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const [results, setResults] = useState<typeof collectors>([]);

  const runCollection = () => {
    if (!company.trim()) return;
    setIsCollecting(true);
    setResults([]);
    setActiveIndex(0);

    collectors.forEach((_, i) => {
      setTimeout(() => {
        setActiveIndex(i);
        setResults(prev => [...prev, collectors[i]]);
        if (i === collectors.length - 1) {
          setTimeout(() => setIsCollecting(false), 600);
        }
      }, (i + 1) * 800);
    });
  };

  return (
    <PageLayout
      label="Phase 2"
      title="DATA COLLECTION"
      subtitle="Multiple specialized collectors scrape public APIs and websites in parallel, extracting structured company data."
    >
      {/* Concept Blocks */}
      <div className="grid-2" style={{ marginBottom: 48 }}>
        <div className="learn-block">
          <div className="learn-block__question">What is it?</div>
          <div className="learn-block__answer">
            Data collection is the process of gathering raw, unstructured information from multiple public sources — APIs, news websites, job boards, and salary databases.
          </div>
        </div>
        <div className="learn-block">
          <div className="learn-block__question">Why is it needed?</div>
          <div className="learn-block__answer">
            AI models cannot browse the internet themselves. We must build specialized "collectors" that fetch, parse, and structure web data into a JSON format the pipeline can process.
          </div>
        </div>
      </div>

      {/* Interactive Demo */}
      <div className="b-panel" style={{ marginBottom: 48 }}>
        <div className="b-panel__header">Interactive Demo — Enter a Company Name</div>
        <div className="b-panel__body">
          <div style={{ display: 'flex', gap: 12, marginBottom: 24 }}>
            <input
              className="b-input"
              placeholder="e.g. Google, Microsoft, Apple..."
              value={company}
              onChange={e => setCompany(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && runCollection()}
              style={{ maxWidth: 400 }}
            />
            <button
              className="b-btn b-btn--accent"
              onClick={runCollection}
              disabled={isCollecting}
            >
              {isCollecting ? 'Collecting...' : '▶ Collect'}
            </button>
          </div>

          {/* Collector Cards */}
          <div className="grid-4">
            {collectors.map((c, i) => (
              <motion.div
                key={c.name}
                className="b-card"
                animate={{
                  borderColor: activeIndex === i ? '#FFD400' : '#000',
                  scale: activeIndex === i ? 1.03 : 1,
                }}
                transition={{ duration: 0.3 }}
              >
                <div style={{ fontSize: '2rem', marginBottom: 8 }}>{c.icon}</div>
                <h4 className="mono" style={{ fontSize: '0.8rem', marginBottom: 8 }}>
                  {c.name}
                </h4>
                <span className={`b-badge ${i <= activeIndex && isCollecting ? 'b-badge--success' : ''}`}>
                  {i < results.length ? 'Done' : i === activeIndex && isCollecting ? 'Fetching...' : 'Idle'}
                </span>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Results */}
      <AnimatePresence>
        {results.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            <h3 style={{ marginBottom: 16 }}>Raw Collected Data</h3>
            <div className="grid-2">
              {results.map(r => (
                <div key={r.name} className="b-panel">
                  <div className="b-panel__header">{r.icon} {r.name}</div>
                  <div className="b-panel__body">
                    <pre className="b-code">{JSON.stringify(r.data, null, 2)}</pre>
                  </div>
                </div>
              ))}
            </div>

            {/* Metrics */}
            <div className="grid-4" style={{ marginTop: 32 }}>
              <div className="metric-card">
                <div className="metric-card__value metric-card__value--accent">4</div>
                <div className="metric-card__label">Sources</div>
              </div>
              <div className="metric-card">
                <div className="metric-card__value metric-card__value--success">12</div>
                <div className="metric-card__label">Records</div>
              </div>
              <div className="metric-card">
                <div className="metric-card__value metric-card__value--info">3.2s</div>
                <div className="metric-card__label">Latency</div>
              </div>
              <div className="metric-card">
                <div className="metric-card__value metric-card__value--secondary">JSON</div>
                <div className="metric-card__label">Format</div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </PageLayout>
  );
}
