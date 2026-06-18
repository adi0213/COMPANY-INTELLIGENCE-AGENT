
import { useLocation, Navigate, Link } from 'react-router-dom';

export default function ResultsDashboardPage() {
  const location = useLocation();
  const result = location.state?.result;

  if (!result || !result.report) {
    return <Navigate to="/" />;
  }

  const { report } = result;
  const isGoodScore = report.overall_score >= 70;

  return (
    <div className="container section">
      <div style={{ maxWidth: 900, margin: '0 auto' }}>
        
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '5px solid var(--primary)', paddingBottom: 20, marginBottom: 40 }}>
          <h1 style={{ margin: 0 }}>ASSESSMENT RESULTS</h1>
          <Link to="/" className="b-btn b-btn--sm">RETURN HOME</Link>
        </div>

        {/* Score Header */}
        <div className="b-card" style={{ marginBottom: 40, textAlign: 'center', background: isGoodScore ? 'var(--success)' : 'var(--secondary)', color: 'var(--white)' }}>
          <h2 style={{ fontSize: '5rem', margin: 0, textShadow: '4px 4px 0px var(--primary)', fontFamily: 'var(--font-mono)' }}>
            {report.overall_score}%
          </h2>
          <div className="b-badge" style={{ marginTop: 20, background: 'var(--primary)', color: 'var(--white)', fontSize: '1rem', padding: '10px 20px' }}>
            ESTIMATED LEVEL: {report.estimated_level}
          </div>
        </div>

        {/* Summary Box */}
        <div className="b-panel" style={{ marginBottom: 40 }}>
          <div className="b-panel__header" style={{ background: 'var(--accent)', color: 'var(--primary)' }}>
            AI SUMMARY REPORT
          </div>
          <div className="b-panel__body">
            <p style={{ fontSize: '1.1rem', fontWeight: 500 }}>{report.human_readable_summary}</p>
          </div>
        </div>

        {/* Strengths & Weaknesses */}
        <div className="grid-2" style={{ marginBottom: 40 }}>
          <div className="b-panel" style={{ border: '3px solid var(--success)' }}>
            <div className="b-panel__header" style={{ background: 'var(--success)', borderBottom: '3px solid var(--success)' }}>
              TOP STRENGTHS [++]
            </div>
            <div className="b-panel__body">
              <ul style={{ paddingLeft: 20, fontWeight: 500 }}>
                {report.strengths.map((s: string, i: number) => <li key={i} style={{ marginBottom: 10 }}>{s}</li>)}
              </ul>
            </div>
          </div>
          
          <div className="b-panel" style={{ border: '3px solid var(--secondary)' }}>
            <div className="b-panel__header" style={{ background: 'var(--secondary)', borderBottom: '3px solid var(--secondary)' }}>
              AREAS TO IMPROVE [--]
            </div>
            <div className="b-panel__body">
              <ul style={{ paddingLeft: 20, fontWeight: 500 }}>
                {report.weaknesses.map((w: string, i: number) => <li key={i} style={{ marginBottom: 10 }}>{w}</li>)}
              </ul>
            </div>
          </div>
        </div>

        {/* Roadmap */}
        <h2 style={{ borderBottom: '3px solid var(--primary)', paddingBottom: 10, marginBottom: 20 }}>
          PERSONALIZED ROADMAP
        </h2>
        
        <div className="grid-2">
          {[1, 2, 3, 4].map((week) => {
            const weekKey = `week_${week}` as keyof typeof report.roadmap;
            return (
              <div key={week} className="chunk chunk--overlap">
                <div className="chunk__id">PHASE: WEEK {week}</div>
                <ul style={{ paddingLeft: 20, margin: 0, fontWeight: 500 }}>
                  {report.roadmap[weekKey]?.map((item: string, i: number) => <li key={i} style={{ marginBottom: 5 }}>{item}</li>)}
                </ul>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
