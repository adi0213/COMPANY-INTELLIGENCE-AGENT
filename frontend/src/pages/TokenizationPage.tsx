import { useState } from 'react';
import { motion } from 'framer-motion';
import PageLayout from '../components/layout/PageLayout';

function simpleTokenize(text: string) {
  // Mimics BPE-style subword tokenization for demonstration
  const words = text.split(/(\s+|[.,!?;:'"])/g).filter(t => t.trim().length > 0);
  let id = 1000;
  return words.map((w, i) => ({ token: w, id: id + i * 7, index: i }));
}

export default function TokenizationPage() {
  const [text, setText] = useState('Google develops AI systems for search and cloud.');
  const tokens = simpleTokenize(text);
  const [hoveredIdx, setHoveredIdx] = useState<number | null>(null);

  return (
    <PageLayout
      label="Phase 4b"
      title="TOKENIZATION"
      subtitle="Convert human-readable text into numerical token IDs that transformer models can process."
    >
      <div className="grid-2" style={{ marginBottom: 48 }}>
        <div className="learn-block">
          <div className="learn-block__question">What is it?</div>
          <div className="learn-block__answer">Tokenization breaks text into subword units called "tokens." Each token maps to a unique integer ID. The model never sees raw text — it only sees sequences of numbers.</div>
        </div>
        <div className="learn-block">
          <div className="learn-block__question">Why subwords?</div>
          <div className="learn-block__answer">Whole-word tokenization can't handle unseen words. BPE (Byte-Pair Encoding) splits rare words into common subwords. "unfamiliar" → ["un", "familiar"]. This gives models a finite vocabulary that handles any text.</div>
        </div>
      </div>

      {/* Input */}
      <div className="b-panel" style={{ marginBottom: 32 }}>
        <div className="b-panel__header">Input Text</div>
        <div className="b-panel__body">
          <input
            className="b-input"
            value={text}
            onChange={e => setText(e.target.value)}
            placeholder="Type anything..."
          />
        </div>
      </div>

      {/* Token Display */}
      <div className="b-panel" style={{ marginBottom: 32 }}>
        <div className="b-panel__header">Tokens</div>
        <div className="b-panel__body" style={{ lineHeight: 2.5 }}>
          {tokens.map((t, i) => (
            <motion.span
              key={i}
              className={`token ${hoveredIdx === i ? 'token--highlight' : ''}`}
              onMouseEnter={() => setHoveredIdx(i)}
              onMouseLeave={() => setHoveredIdx(null)}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.03 }}
            >
              {t.token}
            </motion.span>
          ))}
        </div>
      </div>

      {/* Token IDs */}
      <div className="b-panel" style={{ marginBottom: 32 }}>
        <div className="b-panel__header">Token IDs</div>
        <div className="b-panel__body">
          <pre className="b-code">
            [{tokens.map(t => t.id).join(', ')}]
          </pre>
        </div>
      </div>

      {/* Hover Detail */}
      {hoveredIdx !== null && (
        <motion.div
          className="b-card b-card--accent"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          style={{ maxWidth: 400 }}
        >
          <div className="mono" style={{ fontSize: '0.75rem', color: '#888' }}>Hovered Token</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, margin: '4px 0' }}>"{tokens[hoveredIdx].token}"</div>
          <div className="mono" style={{ fontSize: '0.85rem' }}>ID: {tokens[hoveredIdx].id} | Index: {tokens[hoveredIdx].index}</div>
        </motion.div>
      )}

      {/* Metrics */}
      <div className="grid-4" style={{ marginTop: 32 }}>
        <div className="metric-card">
          <div className="metric-card__value metric-card__value--accent">{tokens.length}</div>
          <div className="metric-card__label">Token Count</div>
        </div>
        <div className="metric-card">
          <div className="metric-card__value metric-card__value--info">{text.length}</div>
          <div className="metric-card__label">Characters</div>
        </div>
        <div className="metric-card">
          <div className="metric-card__value metric-card__value--success">{(tokens.length / Math.max(text.split(' ').length, 1)).toFixed(1)}</div>
          <div className="metric-card__label">Tokens/Word</div>
        </div>
        <div className="metric-card">
          <div className="metric-card__value metric-card__value--secondary">{((tokens.length / 8192) * 100).toFixed(1)}%</div>
          <div className="metric-card__label">Context Used</div>
        </div>
      </div>
    </PageLayout>
  );
}
