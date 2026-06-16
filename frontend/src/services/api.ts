const API_BASE = 'https://company-intelligence-agent-6hca.onrender.com/api/v1';

export async function analyzeCompany(company: string) {
  // Use AbortController for timeout — real pipeline takes 30-90 seconds
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 120_000); // 2 minute timeout

  try {
    const res = await fetch(`${API_BASE}/company/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ company }),
      signal: controller.signal,
    });
    clearTimeout(timeout);

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
      throw new Error(errorData.detail || `API error: ${res.status}`);
    }
    return res.json();
  } catch (err: unknown) {
    clearTimeout(timeout);
    if (err instanceof DOMException && err.name === 'AbortError') {
      throw new Error('Request timed out. The AI pipeline may be overloaded. Please try again.');
    }
    throw err;
  }
}

export async function askQuestion(company: string, question: string) {
  const res = await fetch(`${API_BASE}/agent-ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ company, question }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function generateReport(company: string) {
  const res = await fetch(`${API_BASE}/generate-report`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ company }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getMetrics() {
  const res = await fetch(`${API_BASE}/metrics`);
  return res.json();
}

export async function healthCheck() {
  try {
    const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(5000) });
    return res.json();
  } catch {
    throw new Error('Backend is not reachable. Start it with: uvicorn app.main:app --reload');
  }
}
