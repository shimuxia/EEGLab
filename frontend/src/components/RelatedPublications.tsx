import { useEffect, useState } from 'react';
import { fetchPublications, type Publication } from '../lib/publications';

interface Props {
  tags: string[];
  limit?: number;
  variant?: 'overview' | 'detail';
}

function matches(paper: Publication, researchTags: string[]) {
  return paper.tags.some(tag => researchTags.some(researchTag => (
    tag.includes(researchTag.slice(0, 3)) || researchTag.includes(tag.slice(0, 3))
  )));
}

export default function RelatedPublications({ tags, limit = 3, variant = 'detail' }: Props) {
  const [papers, setPapers] = useState<Publication[] | null>(null);
  useEffect(() => {
    fetchPublications().then(data => setPapers(data.papers.filter(paper => matches(paper, tags)).slice(0, limit)))
      .catch(() => setPapers([]));
  }, [tags.join('|'), limit]);

  if (papers === null) return <div className="related-paper-loading">正在加载相关论文…</div>;
  if (!papers.length) return null;
  return (
    <section className={`related-publications ${variant}`}>
      <h2>{variant === 'detail' ? '相关论文' : '相关论文'}</h2>
      <div>
        {papers.map(paper => (
          <a href="/achievements" key={paper.id}>
            <span className="related-year">{paper.year}</span>
            <span className="related-title">{paper.title}</span>
            <span className="related-journal">{paper.journal}</span>
          </a>
        ))}
      </div>
      {variant === 'detail' && <a className="related-all" href="/achievements">查看全部成果 →</a>}
      <style>{`
        .related-publications { margin-top:clamp(2.5rem,5vw,4rem); }
        .related-publications h2 { margin:0 0 1rem; font-size:var(--fs-xs); letter-spacing:.08em; color:var(--text-2); font-weight:650; }
        .related-publications > div { border-top:1px solid var(--text); }
        .related-publications a:not(.related-all) { display:grid; grid-template-columns:4rem minmax(0,1fr) minmax(8rem,14rem); gap:1rem; align-items:baseline; padding:1rem 0; border-bottom:1px solid var(--border); color:var(--text); text-decoration:none; }
        .related-publications a:not(.related-all):hover .related-title { color:var(--accent); }
        .related-year { color:var(--text-3); font-size:var(--fs-xs); font-variant-numeric:tabular-nums; }
        .related-title { font-size:var(--fs-md); font-weight:600; line-height:1.5; transition:color var(--dur-fast); }
        .related-journal { color:var(--text-3); font-size:var(--fs-xs); text-align:right; }
        .related-all { display:inline-flex; margin-top:1rem; font-size:var(--fs-sm); font-weight:600; color:var(--text); text-decoration:none; border-bottom:1px solid var(--signal); }
        .related-all:hover { color:var(--accent); }
        .related-paper-loading { margin-top:2rem; color:var(--text-3); font-size:var(--fs-sm); }
        @media(max-width:640px){.related-publications a:not(.related-all){grid-template-columns:3rem minmax(0,1fr)}.related-journal{display:none}}
      `}</style>
    </section>
  );
}
