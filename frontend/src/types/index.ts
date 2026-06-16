export interface PipelineStage {
  id: string;
  label: string;
  status: 'idle' | 'processing' | 'done';
  description: string;
  route: string;
}

export interface ChunkData {
  id: number;
  text: string;
  isOverlap: boolean;
}

export interface TokenData {
  token: string;
  id: number;
  index: number;
}

export interface AgentInfo {
  name: string;
  role: string;
  status: 'idle' | 'active' | 'done';
  output?: string;
}

export interface MetricData {
  label: string;
  value: number | string;
  color: 'accent' | 'success' | 'info' | 'secondary';
}

export interface EmbeddingPoint {
  x: number;
  y: number;
  label: string;
  cluster: string;
}

export interface RawCleanPair {
  raw: string;
  clean: string;
  operation: string;
}

export interface LatencyEntry {
  name: string;
  latency: number;
}

export interface EvalEntry {
  name: string;
  score: number;
}
