import PageLayout from '../components/layout/PageLayout';

// Mock 2D PCA projections of embedding vectors
const points = [
  { x: 120, y: 80, label: 'Google AI', cluster: 'AI' },
  { x: 150, y: 100, label: 'DeepMind', cluster: 'AI' },
  { x: 140, y: 60, label: 'OpenAI', cluster: 'AI' },
  { x: 130, y: 110, label: 'Gemini', cluster: 'AI' },
  { x: 400, y: 300, label: 'AWS Cloud', cluster: 'Cloud' },
  { x: 420, y: 280, label: 'GCP', cluster: 'Cloud' },
  { x: 380, y: 320, label: 'Azure', cluster: 'Cloud' },
  { x: 410, y: 340, label: 'Cloudflare', cluster: 'Cloud' },
  { x: 250, y: 400, label: 'React', cluster: 'Frontend' },
  { x: 270, y: 420, label: 'Vue', cluster: 'Frontend' },
  { x: 230, y: 380, label: 'Angular', cluster: 'Frontend' },
  { x: 260, y: 440, label: 'Svelte', cluster: 'Frontend' },
];

const clusterColors: Record<string, string> = {
  AI: '#FF5A36',
  Cloud: '#3366FF',
  Frontend: '#00C853',
};

const mockVector = [0.0234, -0.1458, 0.8912, 0.0045, -0.3321, 0.5567, 0.1123, -0.7789];

export default function EmbeddingsPage() {
  return (
    <PageLayout
      label="Phase 4c"
      title="EMBEDDINGS"
      subtitle="Transform text into dense numerical vectors that capture semantic meaning. Similar concepts cluster together in vector space."
    >
      <div className="grid-2" style={{ marginBottom: 48 }}>
        <div className="learn-block">
          <div className="learn-block__question">What is it?</div>
          <div className="learn-block__answer">An embedding is a list of floating-point numbers (a vector) that represents the "meaning" of text. Models like Sentence-BERT compress entire sentences into 384-dimensional vectors. Similar meanings produce similar vectors.</div>
        </div>
        <div className="learn-block">
          <div className="learn-block__question">How does it work?</div>
          <div className="learn-block__answer">A pre-trained transformer model reads the text, processes it through attention layers, and outputs a fixed-size vector. "Google AI" and "DeepMind" will be close in vector space because they share semantic meaning.</div>
        </div>
      </div>

      {/* Vector Display */}
      <div className="b-panel" style={{ marginBottom: 32 }}>
        <div className="b-panel__header">Example: "Google develops AI" → Vector[384]</div>
        <div className="b-panel__body">
          <pre className="b-code">[{mockVector.join(', ')}, ... 376 more dimensions]</pre>
          <div className="grid-4" style={{ marginTop: 16 }}>
            <div className="metric-card">
              <div className="metric-card__value metric-card__value--accent">384</div>
              <div className="metric-card__label">Dimensions</div>
            </div>
            <div className="metric-card">
              <div className="metric-card__value metric-card__value--info">float32</div>
              <div className="metric-card__label">Data Type</div>
            </div>
            <div className="metric-card">
              <div className="metric-card__value metric-card__value--success">1.5KB</div>
              <div className="metric-card__label">Size / Vector</div>
            </div>
            <div className="metric-card">
              <div className="metric-card__value metric-card__value--secondary">SBERT</div>
              <div className="metric-card__label">Model</div>
            </div>
          </div>
        </div>
      </div>

      {/* 2D PCA Visualization (SVG) */}
      <div className="b-panel">
        <div className="b-panel__header">2D PCA Projection — Semantic Clusters</div>
        <div className="b-panel__body" style={{ display: 'flex', justifyContent: 'center' }}>
          <svg width={550} height={500} style={{ border: '1px solid #ddd' }}>
            {/* Grid lines */}
            {[...Array(11)].map((_, i) => (
              <line key={`h${i}`} x1={0} y1={i * 50} x2={550} y2={i * 50} stroke="#eee" strokeWidth={1} />
            ))}
            {[...Array(12)].map((_, i) => (
              <line key={`v${i}`} x1={i * 50} y1={0} x2={i * 50} y2={500} stroke="#eee" strokeWidth={1} />
            ))}

            {/* Points */}
            {points.map((p, i) => (
              <g key={i}>
                <circle
                  cx={p.x}
                  cy={p.y}
                  r={8}
                  fill={clusterColors[p.cluster]}
                  stroke="#000"
                  strokeWidth={2}
                />
                <text
                  x={p.x + 14}
                  y={p.y + 4}
                  fontFamily="JetBrains Mono, monospace"
                  fontSize="11"
                  fontWeight={600}
                  fill="#000"
                >
                  {p.label}
                </text>
              </g>
            ))}

            {/* Legend */}
            {Object.entries(clusterColors).map(([label, color], i) => (
              <g key={label} transform={`translate(420, ${20 + i * 25})`}>
                <rect width={12} height={12} fill={color} stroke="#000" strokeWidth={2} />
                <text x={18} y={11} fontFamily="JetBrains Mono" fontSize="11" fontWeight={600}>{label}</text>
              </g>
            ))}
          </svg>
        </div>
      </div>
    </PageLayout>
  );
}
