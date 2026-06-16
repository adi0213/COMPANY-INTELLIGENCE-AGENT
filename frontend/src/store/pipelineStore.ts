import { create } from 'zustand';
import type { PipelineStage } from '../types';

const STAGES: PipelineStage[] = [
  { id: 'collection', label: 'Collection', status: 'idle', description: 'Scrape data from multiple public sources.', route: '/collection' },
  { id: 'cleaning', label: 'Cleaning', status: 'idle', description: 'Remove HTML, normalize dates, deduplicate.', route: '/cleaning' },
  { id: 'chunking', label: 'Chunking', status: 'idle', description: 'Split documents into semantic chunks.', route: '/chunking' },
  { id: 'tokenization', label: 'Tokenization', status: 'idle', description: 'Convert text into numerical tokens.', route: '/tokenization' },
  { id: 'embeddings', label: 'Embeddings', status: 'idle', description: 'Generate dense vector representations.', route: '/embeddings' },
  { id: 'vectordb', label: 'Vector DB', status: 'idle', description: 'Store and index vectors for search.', route: '/vectordb' },
  { id: 'rag', label: 'RAG', status: 'idle', description: 'Retrieve context and generate answers.', route: '/rag' },
  { id: 'agents', label: 'Agents', status: 'idle', description: 'Route to specialized domain experts.', route: '/agents' },
  { id: 'reports', label: 'Reports', status: 'idle', description: 'Generate structured intelligence report.', route: '/reports' },
  { id: 'evaluation', label: 'Evaluation', status: 'idle', description: 'Grade quality and detect hallucinations.', route: '/evaluation' },
];

interface PipelineState {
  stages: PipelineStage[];
  activeStageIndex: number;
  company: string;
  isRunning: boolean;
  setCompany: (name: string) => void;
  startPipeline: () => void;
  advanceStage: () => void;
  resetPipeline: () => void;
  setStageStatus: (index: number, status: PipelineStage['status']) => void;
}

export const usePipelineStore = create<PipelineState>((set, get) => ({
  stages: STAGES.map(s => ({ ...s })),
  activeStageIndex: -1,
  company: '',
  isRunning: false,

  setCompany: (name) => set({ company: name }),

  startPipeline: () => {
    const freshStages: PipelineStage[] = STAGES.map(s => ({ ...s, status: 'idle' }));
    freshStages[0].status = 'processing';
    set({ stages: freshStages, activeStageIndex: 0, isRunning: true });
  },

  advanceStage: () => {
    const { stages, activeStageIndex } = get();
    const updated = [...stages];
    if (activeStageIndex >= 0 && activeStageIndex < updated.length) {
      updated[activeStageIndex].status = 'done';
    }
    const next = activeStageIndex + 1;
    if (next < updated.length) {
      updated[next].status = 'processing';
      set({ stages: updated, activeStageIndex: next });
    } else {
      set({ stages: updated, isRunning: false });
    }
  },

  resetPipeline: () => {
    set({
      stages: STAGES.map(s => ({ ...s, status: 'idle' as const })),
      activeStageIndex: -1,
      isRunning: false,
    });
  },

  setStageStatus: (index, status) => {
    const { stages } = get();
    const updated = [...stages];
    if (index >= 0 && index < updated.length) {
      updated[index] = { ...updated[index], status };
      set({ stages: updated });
    }
  },
}));
