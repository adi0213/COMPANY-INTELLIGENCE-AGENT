import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { usePipelineStore } from '../store/pipelineStore';

const stagger = {
  hidden: {},
  show: { transition: { staggerChildren: 0.1 } },
};

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export default function LandingPage() {
  const { stages } = usePipelineStore();
  const navigate = useNavigate();

  return (
    <div className="page">
      {/* ── Hero ─────────────────────────────────────────── */}
      <section style={{ padding: '96px 0 64px', borderBottom: '5px solid #000' }}>
        <div className="container">
          <motion.div initial="hidden" animate="show" variants={stagger}>
            <motion.p
              variants={fadeUp}
              className="mono"
              style={{
                fontSize: '0.8rem',
                fontWeight: 700,
                textTransform: 'uppercase',
                letterSpacing: '0.15em',
                color: '#888',
                marginBottom: 16,
              }}
            >
              Phase 1–10 Complete
            </motion.p>

            <motion.h1 variants={fadeUp} style={{ marginBottom: 16 }}>
              COMPANY
              <br />
              INTELLIGENCE
              <br />
              <span style={{ color: '#FFD400', WebkitTextStroke: '2px #000' }}>
                AGENT_
              </span>
            </motion.h1>

            <motion.p
              variants={fadeUp}
              style={{
                fontSize: '1.15rem',
                maxWidth: 600,
                color: '#888',
                lineHeight: 1.7,
                marginBottom: 32,
              }}
            >
              An interactive platform to learn how modern AI systems work
              internally — from raw data collection to multi-agent report
              generation. Every stage visualized. Every concept explained.
            </motion.p>

            <motion.div variants={fadeUp} style={{ display: 'flex', gap: 12 }}>
              <button
                className="b-btn b-btn--primary"
                onClick={() => navigate('/demo')}
              >
                ▶ Live Demo
              </button>
              <button
                className="b-btn b-btn--accent"
                onClick={() => navigate('/architecture')}
              >
                View Architecture
              </button>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* ── Animated Pipeline ────────────────────────────── */}
      <section style={{ padding: '64px 0' }}>
        <div className="container">
          <h2 style={{ marginBottom: 8 }}>THE PIPELINE</h2>
          <p className="text-muted" style={{ marginBottom: 48 }}>
            Click any stage to explore how it works.
          </p>

          <motion.div
            className="pipeline"
            initial="hidden"
            animate="show"
            variants={stagger}
          >
            {stages.map((stage, i) => (
              <motion.div key={stage.id} variants={fadeUp}>
                {i > 0 && <div className="pipeline__arrow">↓</div>}
                <div
                  className="pipeline__stage"
                  onClick={() => navigate(stage.route)}
                  style={{ cursor: 'pointer' }}
                >
                  <span className="pipeline__number">{String(i + 1).padStart(2, '0')}</span>
                  <div className={`pipeline__node pipeline__node--${stage.status}`}>
                    {stage.label}
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ── Feature Grid ─────────────────────────────────── */}
      <section
        style={{
          padding: '64px 0',
          borderTop: '5px solid #000',
        }}
      >
        <div className="container">
          <h2 style={{ marginBottom: 48 }}>WHAT YOU'LL LEARN</h2>
          <div className="grid-3">
            {[
              {
                title: 'Data Engineering',
                desc: 'Collection, cleaning, deduplication, and normalization of unstructured web data.',
                badge: 'Phase 2-3',
              },
              {
                title: 'NLP & Embeddings',
                desc: 'Chunking, tokenization, and dense vector representations using transformer models.',
                badge: 'Phase 4',
              },
              {
                title: 'Vector Databases',
                desc: 'Indexing, cosine similarity, and approximate nearest neighbor search with ChromaDB.',
                badge: 'Phase 5',
              },
              {
                title: 'RAG Architecture',
                desc: 'Retrieval-Augmented Generation with context building, prompt engineering, and LLM synthesis.',
                badge: 'Phase 6',
              },
              {
                title: 'Multi-Agent Systems',
                desc: 'Coordinator routing, specialized domain agents, and output aggregation.',
                badge: 'Phase 7',
              },
              {
                title: 'LLMOps & Evaluation',
                desc: 'Hallucination detection, latency tracking, cost monitoring, and production observability.',
                badge: 'Phase 9',
              },
            ].map((item) => (
              <motion.div
                key={item.title}
                className="b-card"
                whileHover={{ y: -4, boxShadow: '6px 6px 0px #000' }}
              >
                <span className="b-badge">{item.badge}</span>
                <h3 style={{ margin: '12px 0 8px', fontSize: '1.1rem' }}>
                  {item.title}
                </h3>
                <p className="text-muted" style={{ fontSize: '0.9rem' }}>
                  {item.desc}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Stats Bar ────────────────────────────────────── */}
      <section
        style={{
          borderTop: '5px solid #000',
          padding: '32px 0',
          background: '#000',
          color: '#fff',
        }}
      >
        <div className="container">
          <div className="grid-4" style={{ textAlign: 'center' }}>
            {[
              { value: '10', label: 'Phases Built' },
              { value: '9', label: 'AI Agents' },
              { value: '13', label: 'Interactive Pages' },
              { value: '100%', label: 'From Scratch' },
            ].map((s) => (
              <div key={s.label}>
                <div
                  className="mono"
                  style={{ fontSize: '2.5rem', fontWeight: 800, color: '#FFD400' }}
                >
                  {s.value}
                </div>
                <div
                  className="mono"
                  style={{
                    fontSize: '0.7rem',
                    textTransform: 'uppercase',
                    letterSpacing: '0.1em',
                    marginTop: 4,
                    color: '#aaa',
                  }}
                >
                  {s.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
