import { useState } from 'react';
import { motion } from 'framer-motion';
import PageLayout from '../components/layout/PageLayout';

const sections = [
  { title: 'Executive Summary', icon: '📋', content: 'Google is a global technology leader investing aggressively in AI through Gemini, TPU hardware, and cloud services, while maintaining strong hiring and compensation in the AI/ML domain.' },
  { title: 'Company Overview', icon: '🏢', content: 'Founded in 1998 by Larry Page and Sergey Brin. Headquartered in Mountain View, CA. Subsidiary of Alphabet Inc. Revenue: $307B (2023).' },
  { title: 'Products & Services', icon: '📦', content: 'Search, YouTube, Google Cloud, Android, Pixel devices, Workspace, Ads, Maps, and Gemini AI.' },
  { title: 'Recent News', icon: '📰', content: 'Launched Gemini 2.0 in December 2024. Expanded AI features in Google Workspace. Invested in AI safety research via DeepMind.' },
  { title: 'Technology Stack', icon: '⚙️', content: 'Python, Go, Java, C++, TensorFlow, JAX, Kubernetes, TPUs, GCP, BigQuery, Spanner.' },
  { title: 'Hiring Trends', icon: '💼', content: '142 open AI/ML roles. Key positions: Senior ML Engineer, Research Scientist, AI Infrastructure.' },
  { title: 'Salary Insights', icon: '💰', content: 'Senior AI Engineer: $185K-$350K base. Total comp at L6+ exceeds $500K including RSUs.' },
  { title: 'Risks', icon: '⚠️', content: 'Antitrust regulations, AI safety concerns, competition from OpenAI/Microsoft, talent retention challenges.' },
  { title: 'Opportunities', icon: '🚀', content: 'Enterprise AI adoption, Gemini ecosystem expansion, healthcare AI, autonomous vehicles via Waymo.' },
];

export default function ReportsPage() {
  const [generated, setGenerated] = useState(false);
  const [visibleSections, setVisibleSections] = useState<number[]>([]);

  const generate = () => {
    setGenerated(true);
    setVisibleSections([]);
    sections.forEach((_, i) => {
      setTimeout(() => setVisibleSections(prev => [...prev, i]), (i + 1) * 400);
    });
  };

  return (
    <PageLayout
      label="Phase 8"
      title="REPORT GENERATION"
      subtitle="All specialized agents contribute their findings to build a comprehensive, structured intelligence report."
    >
      <div className="grid-2" style={{ marginBottom: 48 }}>
        <div className="learn-block">
          <div className="learn-block__question">How is the report built?</div>
          <div className="learn-block__answer">The Report Builder wakes up all 6 agents. Each agent queries the vector database for its specific domain. Their outputs are combined into a draft, then 3 additional LLM calls generate the Executive Summary, Risk Analysis, and Opportunity Analysis.</div>
        </div>
        <div className="learn-block">
          <div className="learn-block__question">Output formats</div>
          <div className="learn-block__answer">Reports are exported as Markdown (for web rendering), JSON (for API consumption), and PDF (for executive distribution). The PDF uses styled HTML converted via pdfkit.</div>
        </div>
      </div>

      <div style={{ textAlign: 'center', marginBottom: 32 }}>
        <button className="b-btn b-btn--primary" onClick={generate}>
          📊 Generate Report for "Google"
        </button>
      </div>

      {generated && (
        <div>
          {sections.map((s, i) => (
            visibleSections.includes(i) && (
              <motion.div
                key={s.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="b-panel"
                style={{ marginBottom: 16 }}
              >
                <div className="b-panel__header">{s.icon} {s.title}</div>
                <div className="b-panel__body" style={{ lineHeight: 1.7 }}>{s.content}</div>
              </motion.div>
            )
          ))}

          {visibleSections.length === sections.length && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={{ textAlign: 'center', marginTop: 32 }}>
              <div className="grid-3" style={{ maxWidth: 500, margin: '0 auto' }}>
                <button className="b-btn b-btn--sm b-btn--accent">⬇ Markdown</button>
                <button className="b-btn b-btn--sm b-btn--primary">⬇ JSON</button>
                <button className="b-btn b-btn--sm b-btn--secondary">⬇ PDF</button>
              </div>
            </motion.div>
          )}
        </div>
      )}
    </PageLayout>
  );
}
