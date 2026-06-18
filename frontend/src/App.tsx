import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';

// Product pages
import HomePage from './pages/HomePage';
import CompanyResultPage from './pages/CompanyResultPage';

// Educational pages
import LandingPage from './pages/LandingPage';
import ArchitecturePage from './pages/ArchitecturePage';
import CollectionPage from './pages/CollectionPage';
import CleaningPage from './pages/CleaningPage';
import ChunkingPage from './pages/ChunkingPage';
import TokenizationPage from './pages/TokenizationPage';
import EmbeddingsPage from './pages/EmbeddingsPage';
import VectorDBPage from './pages/VectorDBPage';
import RAGPage from './pages/RAGPage';
import AgentsPage from './pages/AgentsPage';
import ReportsPage from './pages/ReportsPage';
import EvaluationPage from './pages/EvaluationPage';
import LiveDemoPage from './pages/LiveDemoPage';

// Assessment pages
import CodingAssessmentPage from './pages/assessment/CodingAssessmentPage';
import AptitudeAssessmentPage from './pages/assessment/AptitudeAssessmentPage';
import FullAssessmentPage from './pages/assessment/FullAssessmentPage';
import ResultsDashboardPage from './pages/assessment/ResultsDashboardPage';

export default function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        {/* Product Routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/company/:companyName" element={<CompanyResultPage />} />

        {/* Educational Routes */}
        <Route path="/learn" element={<LandingPage />} />
        <Route path="/architecture" element={<ArchitecturePage />} />
        <Route path="/collection" element={<CollectionPage />} />
        <Route path="/cleaning" element={<CleaningPage />} />
        <Route path="/chunking" element={<ChunkingPage />} />
        <Route path="/tokenization" element={<TokenizationPage />} />
        <Route path="/embeddings" element={<EmbeddingsPage />} />
        <Route path="/vectordb" element={<VectorDBPage />} />
        <Route path="/rag" element={<RAGPage />} />
        <Route path="/agents" element={<AgentsPage />} />
        <Route path="/reports" element={<ReportsPage />} />
        <Route path="/evaluation" element={<EvaluationPage />} />
        <Route path="/demo" element={<LiveDemoPage />} />
        
        {/* Assessment Routes */}
        <Route path="/assessment/full" element={<FullAssessmentPage />} />
        <Route path="/assessment/coding" element={<CodingAssessmentPage />} />
        <Route path="/assessment/aptitude" element={<AptitudeAssessmentPage />} />
        <Route path="/assessment/results" element={<ResultsDashboardPage />} />
      </Routes>
      <Footer />
    </BrowserRouter>
  );
}
