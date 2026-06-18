export default function Footer() {
  return (
    <footer className="footer" style={{ padding: '32px 24px', display: 'flex', flexDirection: 'column', gap: 12, alignItems: 'center' }}>
      <p className="footer__text">
        <strong>COMPANY INTELLIGENCE AGENT</strong> — Built from scratch to learn how AI systems work internally. Phase 1–10.
      </p>
      <p className="footer__text" style={{ fontSize: '0.85rem', fontWeight: 600 }}>
        © {new Date().getFullYear()} Developed by <a href="https://github.com/adi0213" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--accent)', background: 'var(--primary)', padding: '2px 8px', marginLeft: 4, textDecoration: 'none' }}>Adith S</a>
      </p>
    </footer>
  );
}
