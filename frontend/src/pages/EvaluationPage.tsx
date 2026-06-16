import { useState, useEffect } from 'react';
import PageLayout from '../components/layout/PageLayout';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, CartesianGrid } from 'recharts';
import { getMetrics } from '../services/api';

const COLORS = ['#FFD400', '#FF5A36', '#3366FF', '#00C853', '#000', '#888'];

export default function EvaluationPage() {
  const [latencyData, setLatencyData] = useState<any[]>([]);
  const [agentUsage, setAgentUsage] = useState<any[]>([]);
  const [hallucination, setHallucination] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getMetrics();
        
        // Process Telemetry for Latency
        const latencyMap: Record<string, { total: number, count: number }> = {};
        data.telemetry.forEach((row: any) => {
          // row = [id, timestamp, company, endpoint, latency_ms, token_count, estimated_cost]
          const endpoint = row[3];
          const latency = row[4];
          if (!latencyMap[endpoint]) latencyMap[endpoint] = { total: 0, count: 0 };
          latencyMap[endpoint].total += latency;
          latencyMap[endpoint].count += 1;
        });
        
        const newLatencyData = Object.keys(latencyMap).map(endpoint => ({
          name: endpoint,
          latency: Math.round(latencyMap[endpoint].total / latencyMap[endpoint].count)
        }));
        setLatencyData(newLatencyData);

        // Process Evaluations for Hallucination and Agent Usage
        const usageMap: Record<string, number> = {};
        const newHallucinationData: any[] = [];
        
        // data.evaluations is already ordered DESC, so we take top 15 and reverse for chart
        const recentEvals = data.evaluations.slice(0, 15).reverse();
        
        data.evaluations.forEach((row: any) => {
          const agent = row[3];
          if (!usageMap[agent]) usageMap[agent] = 0;
          usageMap[agent] += 1;
        });

        recentEvals.forEach((row: any, index: number) => {
          const score = row[5];
          newHallucinationData.push({
            query: `Q${index + 1}`,
            score: score || 0
          });
        });

        const newAgentUsage = Object.keys(usageMap).map(agent => ({
          name: agent,
          value: usageMap[agent]
        }));
        
        setAgentUsage(newAgentUsage);
        setHallucination(newHallucinationData);
      } catch (err) {
        console.error("Failed to fetch metrics", err);
      } finally {
        setLoading(false);
      }
    }
    
    fetchData();
  }, []);

  if (loading) {
    return (
      <PageLayout label="Phase 9" title="EVALUATION & MONITORING" subtitle="Loading real-time telemetry...">
        <div style={{ textAlign: 'center', padding: '100px', fontSize: '1.2rem', fontFamily: 'JetBrains Mono' }}>
          Loading live metrics from backend...
        </div>
      </PageLayout>
    );
  }

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
                <Pie data={agentUsage} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100} strokeWidth={3} stroke="#000" label={({ name, percent }) => percent !== undefined ? `${name} ${(percent * 100).toFixed(0)}%` : name}>
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
