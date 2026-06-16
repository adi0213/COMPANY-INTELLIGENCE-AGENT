import { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import PageLayout from '../components/layout/PageLayout';

const sampleText = `Google LLC is an American multinational corporation and technology company focusing on online advertising, search engine technology, cloud computing, computer software, quantum computing, e-commerce, consumer electronics, and artificial intelligence. It has been referred to as the most powerful company in the world and is one of the world's most valuable brands due to its market dominance and AI advancements.`;

function chunkText(text: string, size: number, overlap: number) {
  const words = text.split(' ');
  const chunks: { id: number; text: string; isOverlap: boolean; words: string[] }[] = [];
  let i = 0;
  let id = 0;
  while (i < words.length) {
    const end = Math.min(i + size, words.length);
    const chunkWords = words.slice(i, end);
    chunks.push({ id: id++, text: chunkWords.join(' '), isOverlap: false, words: chunkWords });
    i += size - overlap;
    if (i >= words.length) break;
  }
  return chunks;
}

export default function ChunkingPage() {
  const [chunkSize, setChunkSize] = useState(15);
  const [overlap, setOverlap] = useState(3);

  const chunks = useMemo(() => chunkText(sampleText, chunkSize, overlap), [chunkSize, overlap]);

  return (
    <PageLayout
      label="Phase 4a"
      title="CHUNKING"
      subtitle="Split large documents into smaller, semantically meaningful pieces that fit inside an LLM's context window."
    >
      <div className="grid-2" style={{ marginBottom: 48 }}>
        <div className="learn-block">
          <div className="learn-block__question">What is it?</div>
          <div className="learn-block__answer">Chunking is the process of breaking large documents into smaller text segments. Each chunk becomes an independent unit that gets its own embedding vector and is stored separately in the vector database.</div>
        </div>
        <div className="learn-block">
          <div className="learn-block__question">Why use overlap?</div>
          <div className="learn-block__answer">Without overlap, a sentence split across two chunks loses context. Overlapping ensures that boundary information is preserved in both neighboring chunks, improving retrieval accuracy.</div>
        </div>
      </div>

      {/* Controls */}
      <div className="b-panel" style={{ marginBottom: 32 }}>
        <div className="b-panel__header">Chunk Configuration</div>
        <div className="b-panel__body">
          <div className="grid-2">
            <div>
              <label className="mono" style={{ fontSize: '0.8rem', fontWeight: 700 }}>
                Chunk Size: {chunkSize} words
              </label>
              <input
                type="range"
                className="b-slider"
                min={5}
                max={30}
                value={chunkSize}
                onChange={e => setChunkSize(Number(e.target.value))}
                style={{ marginTop: 8 }}
              />
            </div>
            <div>
              <label className="mono" style={{ fontSize: '0.8rem', fontWeight: 700 }}>
                Overlap: {overlap} words
              </label>
              <input
                type="range"
                className="b-slider"
                min={0}
                max={Math.min(10, chunkSize - 1)}
                value={overlap}
                onChange={e => setOverlap(Number(e.target.value))}
                style={{ marginTop: 8 }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Source Document */}
      <div className="b-panel" style={{ marginBottom: 32 }}>
        <div className="b-panel__header">Source Document</div>
        <div className="b-panel__body">
          <p style={{ lineHeight: 1.8, fontSize: '0.95rem' }}>{sampleText}</p>
        </div>
      </div>

      {/* Generated Chunks */}
      <h3 style={{ marginBottom: 16 }}>Generated Chunks ({chunks.length})</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
        {chunks.map((chunk, i) => (
          <motion.div
            key={`${chunkSize}-${overlap}-${i}`}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.08 }}
          >
            {i > 0 && <div className="pipeline__arrow" style={{ fontSize: '1rem' }}>↓</div>}
            <div className="chunk">
              <div className="chunk__id">Chunk #{chunk.id} — {chunk.words.length} words</div>
              {chunk.text}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Metrics */}
      <div className="grid-4" style={{ marginTop: 32 }}>
        <div className="metric-card">
          <div className="metric-card__value metric-card__value--accent">{chunks.length}</div>
          <div className="metric-card__label">Total Chunks</div>
        </div>
        <div className="metric-card">
          <div className="metric-card__value metric-card__value--info">{chunkSize}</div>
          <div className="metric-card__label">Words / Chunk</div>
        </div>
        <div className="metric-card">
          <div className="metric-card__value metric-card__value--secondary">{overlap}</div>
          <div className="metric-card__label">Overlap</div>
        </div>
        <div className="metric-card">
          <div className="metric-card__value metric-card__value--success">{sampleText.split(' ').length}</div>
          <div className="metric-card__label">Source Words</div>
        </div>
      </div>
    </PageLayout>
  );
}
