import PageLayout from '../components/layout/PageLayout';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, CartesianGrid } from 'recharts';

const latencyData = [
  { name: 'Collection', latency: 3200 },
  { name: 'Cleaning', latency: 120 },
  { name: 'Chunking', latency: 45 },
  { name: 'Embedding', latency: 890 },
  { name: 'Vector Search', latency: 32 },
  { name: 'RAG', latency: 4500 },
  { name: 'Agents', latency: 8200 },
];

const agentUsage = [
  { name: 'Tech', value: 34 },
  { name: 'News', value: 22 },
  { name: 'Hiring', value: 18 },
  { name: 'Salary', value: 12 },
  { name: 'Company', value: 9 },
  { name: 'Interview', value: 5 },
];

const hallucination = [
  { query: 'Q1', score: 0.95 },
  { query: 'Q2', score: 0.88 },
  { query: 'Q3', score: 0.92 },
  { query: 'Q4', score: 0.78 },
  { query: 'Q5', score: 0.96 },
  { query: 'Q6', score: 0.84 },
  { query: 'Q7', score: 0.91 },
  { query: 'Q8', score: 0.87 },
];

const COLORS = ['#FFD400', '#FF5A36', '#3366FF', '#00C853', '#000', '#888'];

export default function EvaluationPage() {
  return (
    <PageLayout
      label="Phase 9"
      title="EVALUATION & MONITORING"
      subtitle="Track retrieval quality, hallucination rates, agent performance, latency, and cost across every pipeline stage."
    >
      <div className="grid-2" style={{ marginBottom: 48 }}>
        <div className="learn-block">
          <div className="learn-block__question">Why evaluate AI?</div>
          <div className="learn-block__answer">Unlike traditional software, AI systems are non-deterministic. A prompt change can silently break your entire pipeline. Automated evaluation catches regressions before users do.</div>
        </div>
        <div className="learn-block">
          <div className="learn-block__question">LLM-as-a-Judge</div>
          <div className="learn-block__answer">We use a second LLM to grade the first LLM's output. It reads the source context and the generated answer, then scores how "grounded" the answer is. A score below 0.8 triggers a hallucination alert.</div>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid-4" style={{ marginBottom: 48 }}>
        <div className="metric-card">
          <div className="metric-card__value metric-card__value--success">Healthy</div>
          <div className="metric-card__label">System Status</div>
        </div>
        <div className="metric-card">
          <div className="metric-card__value metric-card__value--accent">247</div>
          <div className="metric-card__label">Total Queries</div>
        </div>
        <div className="metric-card">
          <div className="metric-card__value metric-card__value--info">89%</div>
          <div className="metric-card__label">Avg Groundedness</div>
        </div>
        <div className="metric-card">
          <div className="metric-card__value metric-card__value--secondary">4.5s</div>
          <div className="metric-card__label">Avg Latency</div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid-2" style={{ marginBottom: 48 }}>
        <div className="b-panel">
          <div className="b-panel__header">Pipeline Latency (ms)</div>
          <div className="b-panel__body">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={latencyData}>
                <XAxis dataKey="name" tick={{ fontFamily: 'JetBrains Mono', fontSize: 10 }} />
                <YAxis tick={{ fontFamily: 'JetBrains Mono', fontSize: 10 }} />
                <Tooltip />
                <Bar dataKey="latency" fill="#FFD400" stroke="#000" strokeWidth={2} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="b-panel">
          <div className="b-panel__header">Agent Usage Distribution</div>
          <div className="b-panel__body">
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie data={agentUsage} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100} strokeWidth={3} stroke="#000" label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}>
                  {agentUsage.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="b-panel">
        <div className="b-panel__header">Hallucination Scores Over Queries (1.0 = Fully Grounded)</div>
        <div className="b-panel__body">
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={hallucination}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="query" tick={{ fontFamily: 'JetBrains Mono', fontSize: 10 }} />
              <YAxis domain={[0, 1]} tick={{ fontFamily: 'JetBrains Mono', fontSize: 10 }} />
              <Tooltip />
              <Line type="monotone" dataKey="score" stroke="#00C853" strokeWidth={3} dot={{ fill: '#000', r: 5 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </PageLayout>
  );
}
