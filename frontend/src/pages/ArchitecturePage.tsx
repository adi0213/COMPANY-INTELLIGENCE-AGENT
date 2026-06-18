import { useCallback } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  type Node,
  type Edge,
  useNodesState,
  useEdgesState,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { useNavigate } from 'react-router-dom';
import PageLayout from '../components/layout/PageLayout';

const nodeStyle = (bg: string, color = '#000') => ({
  padding: '14px 28px',
  border: '3px solid #000',
  fontFamily: 'JetBrains Mono, monospace',
  fontWeight: 700,
  fontSize: '0.8rem',
  textTransform: 'uppercase' as const,
  letterSpacing: '0.05em',
  background: bg,
  color,
  cursor: 'pointer',
  boxShadow: '4px 4px 0px #000',
  minWidth: 180,
  textAlign: 'center' as const,
});

const initialNodes: Node[] = [
  // Top Row (Data Pipeline)
  { id: '1', position: { x: 50, y: 50 }, data: { label: '🌐 Internet' }, style: nodeStyle('#F8F6F0') },
  { id: '2', position: { x: 300, y: 50 }, data: { label: '📥 Collection' }, style: nodeStyle('#FFD400') },
  { id: '3', position: { x: 550, y: 50 }, data: { label: '🧹 Cleaning' }, style: nodeStyle('#FFD400') },
  { id: '4', position: { x: 800, y: 50 }, data: { label: '✂️ Chunking' }, style: nodeStyle('#FFD400') },
  { id: '5', position: { x: 1050, y: 50 }, data: { label: '🔤 Tokenization' }, style: nodeStyle('#FFD400') },
  
  // Middle Row (Vector DB -> RAG -> Agents)
  { id: '6', position: { x: 1050, y: 200 }, data: { label: '🧮 Embeddings' }, style: nodeStyle('#3366FF', '#fff') },
  { id: '7', position: { x: 800, y: 200 }, data: { label: '🗄️ Vector DB' }, style: nodeStyle('#3366FF', '#fff') },
  { id: '8', position: { x: 550, y: 200 }, data: { label: '🔍 RAG' }, style: nodeStyle('#FF5A36', '#fff') },
  { id: '9', position: { x: 300, y: 200 }, data: { label: '🤖 Agents' }, style: nodeStyle('#FF5A36', '#fff') },
  { id: '10', position: { x: 50, y: 200 }, data: { label: '📊 Reports' }, style: nodeStyle('#00C853', '#fff') },
  
  // Bottom Row (Evaluation)
  { id: '11', position: { x: 50, y: 350 }, data: { label: '📈 Evaluation' }, style: nodeStyle('#00C853', '#fff') },
];

const initialEdges: Edge[] = [
  { id: 'e1-2', source: '1', target: '2', type: 'smoothstep', animated: true, style: { strokeWidth: 3 } },
  { id: 'e2-3', source: '2', target: '3', type: 'smoothstep', animated: true, style: { strokeWidth: 3 } },
  { id: 'e3-4', source: '3', target: '4', type: 'smoothstep', animated: true, style: { strokeWidth: 3 } },
  { id: 'e4-5', source: '4', target: '5', type: 'smoothstep', animated: true, style: { strokeWidth: 3 } },
  { id: 'e5-6', source: '5', target: '6', type: 'smoothstep', animated: true, style: { strokeWidth: 3 } },
  { id: 'e6-7', source: '6', target: '7', type: 'smoothstep', animated: true, style: { strokeWidth: 3 } },
  { id: 'e7-8', source: '7', target: '8', type: 'smoothstep', animated: true, style: { strokeWidth: 3 } },
  { id: 'e8-9', source: '8', target: '9', type: 'smoothstep', animated: true, style: { strokeWidth: 3 } },
  { id: 'e9-10', source: '9', target: '10', type: 'smoothstep', animated: true, style: { strokeWidth: 3 } },
  { id: 'e10-11', source: '10', target: '11', type: 'smoothstep', animated: true, style: { strokeWidth: 3 } },
];

const routeMap: Record<string, string> = {
  '2': '/collection', '3': '/cleaning', '4': '/chunking', '5': '/tokenization',
  '6': '/embeddings', '7': '/vectordb', '8': '/rag', '9': '/agents',
  '10': '/reports', '11': '/evaluation',
};

export default function ArchitecturePage() {
  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, , onEdgesChange] = useEdgesState(initialEdges);
  const navigate = useNavigate();

  const onNodeClick = useCallback((_: React.MouseEvent, node: Node) => {
    const route = routeMap[node.id];
    if (route) navigate(route);
  }, [navigate]);

  return (
    <PageLayout
      label="Phase 1–10"
      title="SYSTEM ARCHITECTURE"
      subtitle="Click any node to explore that stage of the pipeline. Zoom and pan to navigate."
    >
      <div style={{ height: 500, border: '3px solid #000', background: '#fff' }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={onNodeClick}
          fitView
          minZoom={0.3}
          maxZoom={2}
        >
          <Background gap={20} size={1} />
          <Controls />
        </ReactFlow>
      </div>

      <div style={{ marginTop: 48 }}>
        <h3 style={{ marginBottom: 16 }}>How to Read This Diagram</h3>
        <div className="grid-3">
          <div className="learn-block">
            <div className="learn-block__question">🟡 Yellow = Data Engineering</div>
            <div className="learn-block__answer">Collection, cleaning, chunking, and tokenization transform raw internet data into structured, model-ready inputs.</div>
          </div>
          <div className="learn-block">
            <div className="learn-block__question">🔵 Blue = AI / ML</div>
            <div className="learn-block__answer">Embeddings and Vector DB handle the mathematical transformation and storage of semantic meaning.</div>
          </div>
          <div className="learn-block">
            <div className="learn-block__question">🔴 Red = Intelligence</div>
            <div className="learn-block__answer">RAG and Agents use retrieval and LLMs to generate grounded, specialized answers.</div>
          </div>
        </div>
      </div>
    </PageLayout>
  );
}
