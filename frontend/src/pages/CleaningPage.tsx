import { useState } from 'react';
import { motion } from 'framer-motion';
import PageLayout from '../components/layout/PageLayout';
import type { RawCleanPair } from '../types';

const examples: RawCleanPair[] = [
  { raw: '<p>Google LLC was founded in <b>September 1998</b></p>', clean: 'Google LLC was founded in September 1998', operation: 'HTML Tag Removal' },
  { raw: '2024/12/01', clean: '2024-12-01T00:00:00Z', operation: 'Date Normalization' },
  { raw: 'salary: $185,000 USD per year', clean: '185000', operation: 'Numeric Extraction' },
  { raw: 'Google Google Google AI AI', clean: 'Google AI', operation: 'Deduplication' },
  { raw: '   Leading   spaces   everywhere   ', clean: 'Leading spaces everywhere', operation: 'Whitespace Normalization' },
  { raw: 'N/A', clean: '', operation: 'Null Value Handling' },
];

export default function CleaningPage() {
  const [activeIdx, setActiveIdx] = useState(0);

  return (
    <PageLayout
      label="Phase 3"
      title="DATA CLEANING"
      subtitle="Transform messy, inconsistent web data into structured, normalized records ready for AI processing."
    >
      <div className="grid-2" style={{ marginBottom: 48 }}>
        <div className="learn-block">
          <div className="learn-block__question">What is it?</div>
          <div className="learn-block__answer">Data cleaning is the process of detecting and correcting inaccurate, incomplete, or irrelevant parts of raw data. It includes removing HTML, normalizing formats, handling nulls, and deduplicating records.</div>
        </div>
        <div className="learn-block">
          <div className="learn-block__question">Why is it needed?</div>
          <div className="learn-block__answer">Garbage in, garbage out. If you feed an embedding model raw HTML tags or duplicate text, the resulting vectors will be polluted, leading to poor retrieval and hallucinated outputs.</div>
        </div>
      </div>

      {/* Operation Selector */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24, flexWrap: 'wrap' }}>
        {examples.map((ex, i) => (
          <button
            key={i}
            className={`b-btn b-btn--sm ${activeIdx === i ? 'b-btn--accent' : ''}`}
            onClick={() => setActiveIdx(i)}
          >
            {ex.operation}
          </button>
        ))}
      </div>

      {/* Split View */}
      <motion.div
        key={activeIdx}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
        className="split-view"
      >
        <div>
          <div className="split-view__label">🔴 Raw Data (Before)</div>
          <div className="split-view__pane">
            <pre className="b-code" style={{ background: '#2C0000', color: '#FF5A36' }}>{examples[activeIdx].raw}</pre>
          </div>
        </div>
        <div className="split-view__divider" />
        <div>
          <div className="split-view__label" style={{ background: '#00C853' }}>🟢 Clean Data (After)</div>
          <div className="split-view__pane">
            <pre className="b-code" style={{ background: '#002C00', color: '#00C853' }}>{examples[activeIdx].clean || '(empty — removed)'}</pre>
          </div>
        </div>
      </motion.div>

      <div style={{ textAlign: 'center', marginTop: 16 }}>
        <span className="b-badge">{examples[activeIdx].operation}</span>
      </div>
    </PageLayout>
  );
}
