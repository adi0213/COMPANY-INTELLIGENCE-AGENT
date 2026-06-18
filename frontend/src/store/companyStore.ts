import { create } from 'zustand';

export interface AgentResponse {
  content: string;
  confidence?: number;
  sources?: number;
  source_types?: string[];
}

export interface CompanyResult {
  company: string;
  overview: AgentResponse;
  latest_developments: AgentResponse;
  key_technologies: AgentResponse;
  business_areas: AgentResponse;
  interview_focus: AgentResponse;
  hiring_trends: AgentResponse;
  salary_insights: AgentResponse;
  executive_summary: AgentResponse;
}

interface CompanyState {
  query: string;
  loading: boolean;
  loadingStage: string;
  result: CompanyResult | null;
  error: string | null;
  setQuery: (q: string) => void;
  setLoading: (l: boolean) => void;
  setLoadingStage: (s: string) => void;
  setResult: (r: CompanyResult | null) => void;
  setError: (e: string | null) => void;
  reset: () => void;
}

export const useCompanyStore = create<CompanyState>((set) => ({
  query: '',
  loading: false,
  loadingStage: '',
  result: null,
  error: null,
  setQuery: (q) => set({ query: q }),
  setLoading: (l) => set({ loading: l }),
  setLoadingStage: (s) => set({ loadingStage: s }),
  setResult: (r) => set({ result: r }),
  setError: (e) => set({ error: e }),
  reset: () => set({ query: '', loading: false, loadingStage: '', result: null, error: null }),
}));
