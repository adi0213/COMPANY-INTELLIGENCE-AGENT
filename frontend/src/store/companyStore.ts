import { create } from 'zustand';

export interface CompanyResult {
  company: string;
  overview: string;
  latest_developments: string;
  key_technologies: string;
  business_areas: string;
  interview_focus: string;
  hiring_trends: string;
  salary_insights: string;
  executive_summary: string;
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
