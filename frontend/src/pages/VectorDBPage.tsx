import { useState } from 'react';
import { motion } from 'framer-motion';
import PageLayout from '../components/layout/PageLayout';

const mockDB = [
  { id: 'chunk_001', text: 'Google is investing heavily in Gemini AI models and TPU hardware.', similarity: 0.94 },
  { id: 'chunk_002', text: 'Google Cloud Platform (GCP) offers AI and ML services for enterprises.', similarity: 0.88 },
  { id: 'chunk_003', text: 'DeepMind is a subsidiary of Alphabet focused on AI safety research.', similarity: 0.82 },
  { id: 'chunk_004', text: 'Google Maps uses machine learning for real-time traffic predictions.', similarity: 0.71 },
  { id: 'chunk_005', text: 'The company was founded in 1998 by Larry Page and Sergey Brin.', similarity: 0.45 },
  { id: 'chunk_006', text: 'Google Pixel phones feature advanced camera AI processing.', similarity: 0.39 },
  { id: 'chunk_007', text: 'Alphabet reported $307 billion in revenue for fiscal year 2023.', similarity: 0.22 },
];

export default function VectorDBPage() {
  const [query, setQuery] = useState('What AI technologies is Google building?');
  const [topK, setTopK] = useState(5);
  const [searched, setSearched] = useState(false);

  const results = mockDB.slice(0, topK);

  return (
    <PageLayout
      label="Phase 5"
      title="VECTOR DATABASE"
      subtitle="Store embedding vectors and retrieve the most semantically similar chunks using cosine similarity search."
    >
      <div className="grid-2" style={{ marginBottom: 48 }}>
        <div className="learn-block">
          <div className="learn-block__question">What is it?</div>
          <div className="learn-block__answer">A vector database stores high-dimensional embedding vectors and provides ultra-fast similarity search. When a user asks a question, we embed the question, then find the stored chunks whose vectors are closest to the query vector.</div>
        </div>
        <div className="learn-block">
          <div className="learn-block__question">What is cosine similarity?</div>
          <div className="learn-block__answer">It measures the angle between two vectors. A score of 1.0 means identical direction (same meaning). A score of 0.0 means orthogonal (unrelated). We rank results by similarity and return the Top-K.</div>
        </div>
      </div>

      {/* Search */}
      <div className="b-panel" style={{ marginBottom: 32 }}>
        <div className="b-panel__header">Semantic Search Explorer</div>
        <div className="b-panel__body">
          <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
            <input className="b-input" value={query} onChange={e => setQuery(e.target.value)} style={{ flex: 1 }} />
            <button className="b-btn b-btn--accent" onClick={() => setSearched(true)}>🔍 Search</button>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <label className="mono" style={{ fontSize: '0.8rem', fontWeight: 700 }}>Top-K: {topK}</label>
            <input type="range" className="b-slider" min={1} max={7} value={topK} onChange={e => setTopK(Number(e.target.value))} style={{ maxWidth: 200 }} />
          </div>
        </div>
      </div>

      {/* Results */}
      {searched && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <h3 style={{ marginBottom: 16 }}>Top-{topK} Results</h3>
          {results.map((r, i) => (
            <motion.div
              key={r.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 }}
              style={{
                display: 'flex',
                gap: 16,
                alignItems: 'center',
                marginBottom: 12,
                border: '3px solid #000',
                padding: 16,
                background: '#fff',
              }}
            >
              <div style={{
                fontFamily: 'JetBrains Mono',
                fontWeight: 800,
                fontSize: '1.5rem',
                minWidth: 40,
                color: r.similarity > 0.8 ? '#00C853' : r.similarity > 0.5 ? '#FFD400' : '#FF5A36',
              }}>
                #{i + 1}
              </div>
              <div style={{ flex: 1 }}>
                <div className="mono" style={{ fontSize: '0.7rem', color: '#888' }}>{r.id}</div>
                <div style={{ marginTop: 4 }}>{r.text}</div>
              </div>
              {/* Similarity Bar */}
              <div style={{ minWidth: 120, textAlign: 'right' }}>
                <div className="mono" style={{ fontWeight: 800, fontSize: '1.1rem' }}>
                  {(r.similarity * 100).toFixed(0)}%
                </div>
                <div style={{ height: 6, background: '#eee', border: '1px solid #000', marginTop: 4 }}>
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${r.similarity * 100}%` }}
                    transition={{ delay: i * 0.1 + 0.3, duration: 0.5 }}
                    style={{
                      height: '100%',
                      background: r.similarity > 0.8 ? '#00C853' : r.similarity > 0.5 ? '#FFD400' : '#FF5A36',
                    }}
                  />
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}
    </PageLayout>
  );
}
