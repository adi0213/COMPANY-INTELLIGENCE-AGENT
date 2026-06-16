import { NavLink } from 'react-router-dom';
import { useState } from 'react';

const productLinks = [
  { to: '/', label: 'Search' },
];

const learnLinks = [
  { to: '/learn', label: 'Overview' },
  { to: '/architecture', label: 'Architecture' },
  { to: '/collection', label: 'Collection' },
  { to: '/cleaning', label: 'Cleaning' },
  { to: '/chunking', label: 'Chunking' },
  { to: '/tokenization', label: 'Tokens' },
  { to: '/embeddings', label: 'Embeddings' },
  { to: '/vectordb', label: 'VectorDB' },
  { to: '/rag', label: 'RAG' },
  { to: '/agents', label: 'Agents' },
  { to: '/reports', label: 'Reports' },
  { to: '/evaluation', label: 'Eval' },
  { to: '/demo', label: 'Live Demo' },
];

export default function Header() {
  const [showLearn, setShowLearn] = useState(false);

  return (
    <nav className="nav">
      <div className="nav__inner">
        <NavLink to="/" className="nav__logo">
          <span className="nav__logo-dot" />
          CIA_
        </NavLink>

        <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
          {productLinks.map(l => (
            <NavLink
              key={l.to}
              to={l.to}
              className={({ isActive }) => `nav__link${isActive ? ' nav__link--active' : ''}`}
              end
            >
              {l.label}
            </NavLink>
          ))}

          {/* Learn dropdown toggle */}
          <div style={{ position: 'relative' }}>
            <button
              className={`nav__link ${showLearn ? 'nav__link--active' : ''}`}
              onClick={() => setShowLearn(!showLearn)}
              style={{ background: 'none', cursor: 'pointer', fontFamily: 'inherit' }}
            >
              Learn {showLearn ? '▲' : '▼'}
            </button>

            {showLearn && (
              <div style={{
                position: 'absolute',
                top: '100%',
                right: 0,
                marginTop: 4,
                background: '#F8F6F0',
                border: '3px solid #000',
                boxShadow: '4px 4px 0px #000',
                padding: '8px 0',
                zIndex: 200,
                minWidth: 160,
              }}>
                {learnLinks.map(l => (
                  <NavLink
                    key={l.to}
                    to={l.to}
                    onClick={() => setShowLearn(false)}
                    className={({ isActive }) => `nav__link${isActive ? ' nav__link--active' : ''}`}
                    style={{ display: 'block', padding: '6px 16px', width: '100%' }}
                  >
                    {l.label}
                  </NavLink>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
