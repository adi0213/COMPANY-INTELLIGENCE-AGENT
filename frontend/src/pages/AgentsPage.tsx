import { useState } from 'react';
import { motion } from 'framer-motion';
import PageLayout from '../components/layout/PageLayout';

const agents = [
  { name: 'Company Agent', icon: '🏢', domain: 'Overview, history, leadership', output: 'Google LLC was founded in 1998 by Larry Page and Sergey Brin as a search engine company. Today it is a subsidiary of Alphabet Inc.' },
  { name: 'News Agent', icon: '📰', domain: 'Recent events, launches', output: 'Google launched Gemini 2.0 in December 2024, marking its most advanced multimodal AI system to date.' },
  { name: 'Hiring Agent', icon: '💼', domain: 'Job trends, roles', output: 'Google currently has 142 open ML/AI positions across Mountain View, NYC, and London. Remote roles available.' },
  { name: 'Salary Agent', icon: '💰', domain: 'Compensation, equity', output: 'Senior AI Engineers at Google earn $185K-$350K base + RSUs. Total comp can exceed $500K at L6+.' },
  { name: 'Tech Agent', icon: '⚙️', domain: 'Stack, infrastructure', output: 'Google uses TensorFlow, JAX, TPUs, Kubernetes, Go, Python, and GCP internally for AI workloads.' },
  { name: 'Interview Agent', icon: '🎯', domain: 'Prep, questions', output: 'Google interviews focus on system design, ML fundamentals, and LeetCode medium/hard. 5-6 rounds typical.' },
];

export default function AgentsPage() {
  const [active, setActive] = useState<number[]>([]);
  const [isRunning, setIsRunning] = useState(false);

  const runAgents = () => {
    setIsRunning(true);
    setActive([]);
    agents.forEach((_, i) => {
      setTimeout(() => {
        setActive(prev => [...prev, i]);
        if (i === agents.length - 1) setTimeout(() => setIsRunning(false), 500);
      }, (i + 1) * 600);
    });
  };

  return (
    <PageLayout
      label="Phase 7"
      title="MULTI-AGENT SYSTEM"
      subtitle="A Coordinator Agent analyzes user intent and routes queries to specialized domain experts who work in parallel."
    >
      <div className="grid-2" style={{ marginBottom: 48 }}>
        <div className="learn-block">
          <div className="learn-block__question">What is an agent?</div>
          <div className="learn-block__answer">An Agent is an LLM equipped with a specific persona, tools, and autonomy. Instead of one generic AI answering everything, we create specialists — a Salary Expert, a Tech Expert, a News Expert — each querying only their domain.</div>
        </div>
        <div className="learn-block">
          <div className="learn-block__question">What is the Coordinator?</div>
          <div className="learn-block__answer">The Coordinator is a semantic router. It reads the user's question, detects intents (salary? hiring? tech?), and wakes up only the relevant agents. This reduces hallucinations and improves answer depth.</div>
        </div>
      </div>

      {/* Coordinator */}
      <div style={{ textAlign: 'center', marginBottom: 32 }}>
        <motion.div
          className="agent-node agent-node--coordinator"
          style={{ display: 'inline-block', padding: '16px 48px' }}
          whileHover={{ scale: 1.05 }}
        >
          <div className="agent-node__name">🎯 Coordinator Agent</div>
          <div className="agent-node__status">Semantic Router</div>
        </motion.div>
        <div className="mono" style={{ fontSize: '2rem', fontWeight: 800, margin: '8px 0' }}>↓</div>
        <button className="b-btn b-btn--primary" onClick={runAgents} disabled={isRunning}>
          {isRunning ? 'Routing...' : '▶ Run All Agents'}
        </button>
      </div>

      {/* Agent Grid */}
      <div className="grid-3">
        {agents.map((a, i) => (
          <motion.div
            key={a.name}
            className={`agent-node ${active.includes(i) ? 'agent-node--active' : ''}`}
            animate={{
              borderColor: active.includes(i) ? '#3366FF' : '#000',
              scale: active.includes(i) ? 1.02 : 1,
            }}
            style={{ textAlign: 'left', padding: 20 }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
              <span className="agent-node__name">{a.icon} {a.name}</span>
              <span className={`b-badge ${active.includes(i) ? 'b-badge--success' : ''}`} style={{ fontSize: '0.6rem' }}>
                {active.includes(i) ? 'Done' : 'Idle'}
              </span>
            </div>
            <div className="mono" style={{ fontSize: '0.7rem', color: active.includes(i) ? '#ccc' : '#888', marginBottom: 8 }}>
              Domain: {a.domain}
            </div>
            {active.includes(i) && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                style={{ fontSize: '0.85rem', lineHeight: 1.6, paddingTop: 8, borderTop: '2px solid currentColor' }}
              >
                {a.output}
              </motion.div>
            )}
          </motion.div>
        ))}
      </div>
    </PageLayout>
  );
}
