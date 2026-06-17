import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useCompanyStore } from '../store/companyStore';
import ReactMarkdown from 'react-markdown';

const fadeIn = {
  hidden: { opacity: 0, y: 20 },
  show: (delay: number) => ({ opacity: 1, y: 0, transition: { duration: 0.4, delay } }),
};

function Section({ icon, title, data, delay = 0 }: { icon: string; title: string; data: any; delay?: number }) {
  if (!data || !data.content) return null;
  
  return (
    <motion.div
      className="b-panel"
      style={{ marginBottom: 24, position: 'relative' }}
      initial="hidden"
      animate="show"
      custom={delay}
      variants={fadeIn}
    >
      <div className="b-panel__header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>{icon} {title}</span>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', fontSize: '0.7rem' }}>
          {data.sources > 0 && (
            <span style={{ border: '1px solid #000', padding: '2px 6px', borderRadius: 4 }}>
              Sources: {data.sources}
            </span>
          )}
        </div>
      </div>
      <div className="b-panel__body react-markdown-container" style={{ lineHeight: 1.8, fontSize: '0.95rem' }}>
        <ReactMarkdown>{data.content}</ReactMarkdown>
      </div>
    </motion.div>
  );
}

export default function CompanyResultPage() {
  const { companyName } = useParams<{ companyName: string }>();
  const { result, loading, error } = useCompanyStore();
  const navigate = useNavigate();

  // Loading state
  if (loading) {
    return (
      <div className="page flex-center" style={{ minHeight: '60vh' }}>
        <div style={{ textAlign: 'center' }}>
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ repeat: Infinity, duration: 2, ease: 'linear' }}
            style={{ fontSize: '3rem', display: 'inline-block' }}
          >
            ⚙️
          </motion.div>
          <h3 style={{ marginTop: 16 }}>Analyzing {companyName}...</h3>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="page" style={{ padding: 64 }}>
        <div className="container">
          <div className="b-card" style={{ borderColor: '#FF5A36', maxWidth: 600 }}>
            <h3 style={{ color: '#FF5A36', marginBottom: 8 }}>Analysis Failed</h3>
            <p style={{ marginBottom: 16 }}>{error}</p>
            <button className="b-btn b-btn--secondary" onClick={() => navigate('/')}>
              ← Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  // No result — prompt user to search
  if (!result) {
    return (
      <div className="page" style={{ padding: 64 }}>
        <div className="container" style={{ textAlign: 'center' }}>
          <h2 style={{ marginBottom: 16 }}>No Data Loaded</h2>
          <p className="text-muted" style={{ marginBottom: 24 }}>
            Search for a company from the homepage to see intelligence results.
          </p>
          <button className="b-btn b-btn--primary" onClick={() => navigate('/')}>
            ← Go to Search
          </button>
        </div>
      </div>
    );
  }

  // ── Success: Display the full report ──────────────────
  return (
    <div className="page">
      {/* ── Company Header ────────────────────────────── */}
      <section style={{ padding: '48px 0 32px', borderBottom: '5px solid #000' }}>
        <div className="container">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 16, flexWrap: 'wrap' }}>
              <button className="b-btn b-btn--sm" onClick={() => navigate('/')}>← Back to Search</button>
              <span className="b-badge">Company Intelligence Report</span>
            </div>
            <h1 style={{ fontSize: 'clamp(2rem, 5vw, 4rem)' }}>
              {result.company.toUpperCase()}
              <span style={{ color: '#FFD400' }}>_</span>
            </h1>
          </motion.div>
        </div>
      </section>

      {/* ── Report Content ────────────────────────────── */}
      <section style={{ padding: '48px 0' }}>
        <div className="container">
          {/* Executive Summary - Hero Card */}
          {result.executive_summary && result.executive_summary.content && (
            <motion.div
              className="b-card b-card--dark"
              style={{ marginBottom: 32, padding: 32 }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <span className="b-badge" style={{ marginBottom: 12, display: 'inline-block' }}>📋 AI-Generated Executive Summary</span>
              </div>
              <p style={{ fontSize: '1.1rem', lineHeight: 1.8, color: '#ccc' }}>
                {result.executive_summary.content}
              </p>
            </motion.div>
          )}

          <div className="grid-2">
            {/* Left Column */}
            <div>
              <Section icon="🏢" title="Company Overview" data={result.overview} delay={0.1} />
              <Section icon="⚙️" title="Key Technologies" data={result.key_technologies} delay={0.3} />
              <Section icon="🎯" title="Interview Focus Areas" data={result.interview_focus} delay={0.5} />
              <Section icon="💰" title="Salary Insights" data={result.salary_insights} delay={0.7} />
            </div>

            {/* Right Column */}
            <div>
              <Section icon="📰" title="Latest Developments" data={result.latest_developments} delay={0.2} />
              <Section icon="📊" title="Important Business Areas" data={result.business_areas} delay={0.4} />
              <Section icon="💼" title="Hiring Trends" data={result.hiring_trends} delay={0.6} />
            </div>
          </div>

          {/* Actions */}
          <motion.div
            style={{ marginTop: 32, display: 'flex', gap: 12, flexWrap: 'wrap' }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
          >
            <button className="b-btn b-btn--accent" onClick={() => navigate('/')}>
              🔍 Search Another Company
            </button>
            <button className="b-btn" onClick={() => navigate('/architecture')}>
              🏗️ How This System Works
            </button>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
