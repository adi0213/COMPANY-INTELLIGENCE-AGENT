import type { ReactNode } from 'react';

interface Props {
  label: string;
  title: string;
  subtitle?: string;
  children: ReactNode;
}

export default function PageLayout({ label, title, subtitle, children }: Props) {
  return (
    <div className="page">
      <section className="page__hero">
        <div className="container">
          <p className="page__hero-label">{label}</p>
          <h1 className="page__hero-title">{title}</h1>
          {subtitle && <p className="page__hero-subtitle">{subtitle}</p>}
        </div>
      </section>
      <section className="page__content">
        <div className="container">{children}</div>
      </section>
    </div>
  );
}
