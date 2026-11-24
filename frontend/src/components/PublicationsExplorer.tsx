import { representativePapers } from '../data/group';
import { useEffect, useMemo, useState } from 'react';
import {
  fetchPublications,
  formatUpdatedAt,
  type Publication,
  type PublicationsResponse,
  type Researcher,
} from '../lib/publications';

type ActiveFilter = '代表作' | '全部' | string;

export default function PublicationsExplorer() {
  const [data, setData] = useState<PublicationsResponse | null>(null);
  const [error, setError] = useState('');
  const [activeResearcher, setActiveResearcher] = useState('all');
  const [activeFilter, setActiveFilter] = useState<ActiveFilter>('代表作');
  const [query, setQuery] = useState('');

  const load = (refresh = false) => {
    setError('');
    fetchPublications(undefined, { refresh })
      .then(result => {
        setData(result);
        if (result.papers.length && !result.papers.some(paper => paper.representative)) {
          setActiveFilter('全部');
        }
      })
      .catch(reason => setError(reason instanceof Error ? reason.message : '论文服务暂时不可用'));
  };

  useEffect(() => { load(); }, []);

  const visible = useMemo(() => {
    if (!data) return [];
    const normalizedQuery = query.trim().toLocaleLowerCase();
    return data.papers.filter(paper => {
      const researcherMatch = activeResearcher === 'all'
        || paper.researchers.some(researcher => researcher.slug === activeResearcher);
      const filterMatch = activeFilter === '全部'
        || (activeFilter === '代表作' ? paper.representative : paper.tags.includes(activeFilter));
      const queryMatch = !normalizedQuery
        || `${paper.title} ${paper.authors} ${paper.journal}`.toLocaleLowerCase().includes(normalizedQuery);
      return researcherMatch && filterMatch && queryMatch;
    });
  }, [data, activeResearcher, activeFilter, query]);

  const selectedResearcher = data?.researchers.find(item => item.slug === activeResearcher);
  const years = [...new Set(visible.map(paper => paper.year))].sort((a, b) => b - a);

  if (error) {
    return (
      <div className="publication-error" role="alert">
        <strong>暂时无法连接论文服务</strong>
        <p>已保留静态代表论文，完整目录可稍后重试。</p>
        <StaticSelection />
        <button onClick={() => load(true)}>重新加载</button>
        <style>{errorStyles}</style>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="publication-loading" aria-label="正在加载论文">
        <span /><span /><span />
        <style>{loadingStyles}</style>
      </div>
    );
  }

  return (
    <div className="publications-explorer">
      {import.meta.env.PUBLIC_LOCAL_PREVIEW === 'true' && <p className="local-catalog-note">本地预览 · 当前目录使用随仓数据，完整论文库待接入。</p>}
      {data.total === 0 && <section className="catalog-empty"><h3>课题组选登的代表论文</h3><p>当前目录暂无已核验条目。以下选自课题组公开介绍。</p><StaticSelection /></section>}
      <div className="researcher-switcher" aria-label="按研究者筛选">
        <button
          className={activeResearcher === 'all' ? 'active' : ''}
          onClick={() => setActiveResearcher('all')}
        >
          <span className="researcher-avatar all">ALL</span>
          <span><strong>全部成员</strong><small>{data.total} 篇</small></span>
        </button>
        {data.researchers.map(researcher => (
          <button
            key={researcher.slug}
            className={activeResearcher === researcher.slug ? 'active' : ''}
            onClick={() => setActiveResearcher(researcher.slug)}
          >
            {researcher.avatarUrl
              ? <img className="researcher-avatar" src={researcher.avatarUrl} alt="" />
              : <span className="researcher-avatar">{researcher.name.slice(0, 1)}</span>}
            <span><strong>{researcher.name}</strong><small>{researcher.paperCount} 篇</small></span>
          </button>
        ))}
      </div>

      <div className="publication-toolbar">
        <div className="filter-bar">
          {['代表作', ...data.filterTags, '全部'].map(filter => (
            <button
              key={filter}
              className={activeFilter === filter ? 'active' : ''}
              onClick={() => setActiveFilter(filter)}
            >{filter}</button>
          ))}
        </div>
        <label className="paper-search">
          <span className="sr-only">搜索论文</span>
          <svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="4.5" /><path d="m10.5 10.5 3 3" /></svg>
          <input value={query} onChange={event => setQuery(event.target.value)} placeholder="搜索标题、作者或期刊" />
        </label>
      </div>

      <div className="publication-meta">
        <span>显示 {visible.length} / {data.total} 篇</span>
        <span>更新于 {formatUpdatedAt(data.updatedAt)}</span>
        {selectedResearcher?.googleScholarUrl && (
          <a href={selectedResearcher.googleScholarUrl} target="_blank" rel="noopener noreferrer">
            {selectedResearcher.name}的 Google Scholar ↗
          </a>
        )}
        {selectedResearcher?.scholarMetrics?.totalCitations != null && (
          <span>
            Scholar 总引用 {selectedResearcher.scholarMetrics.totalCitations}
            {selectedResearcher.scholarMetrics.hIndex != null
              ? ` · h-index ${selectedResearcher.scholarMetrics.hIndex}` : ''}
          </span>
        )}
      </div>

      <div className="paper-list">
        {years.map(year => (
          <section key={year} className="paper-year-group">
            <div className="year-divider"><span>{year}</span></div>
            {visible.filter(paper => paper.year === year).map(paper => (
              <PaperRow paper={paper} key={paper.id} />
            ))}
          </section>
        ))}
        {!visible.length && <p className="no-results">当前条件下暂无论文</p>}
      </div>
      <style>{explorerStyles}</style>
    </div>
  );
}

function StaticSelection() {
  return <ul className="static-selection">{representativePapers.map(paper => (
    <li key={paper.title}>
      <small>{paper.year} · {paper.venue}</small>
      <a href={paper.link} target="_blank" rel="noopener noreferrer">{paper.title}</a>
    </li>
  ))}</ul>;
}

function PaperRow({ paper }: { paper: Publication }) {
  return (
    <article className="paper-row">
      <div className="pr-num">{paper.num}</div>
      <div className="pr-body">
        {paper.doi
          ? <a className="pr-title" href={`https://doi.org/${paper.doi}`} target="_blank" rel="noopener noreferrer">{paper.title}</a>
          : <div className="pr-title">{paper.title}</div>}
        <div className="pr-authors">{paper.authors}</div>
        <div className="paper-researchers">
          {paper.researchers.map(researcher => (
            <span key={researcher.slug} title={researcher.isCorresponding ? '通讯作者' : undefined}>
              {researcher.name}{researcher.isCorresponding ? ' *' : ''}
            </span>
          ))}
        </div>
        <div className="pr-tags">
          {paper.journal && <span className="pr-tag venue">{paper.journal}</span>}
          {paper.impactFactor && <span className={`pr-tag if ${paper.impactFactor >= 7 ? 'gold' : paper.impactFactor >= 5 ? 'blue' : ''}`}>IF {paper.impactFactor}</span>}
          {paper.quartile && <span className={`pr-tag rank ${paper.isTop ? 'top' : ''}`}>{paper.quartile}{paper.isTop ? ' Top' : ''}</span>}
          {paper.tags.filter(tag => !['一区', '二区', '会议', '其他'].includes(tag)).map(tag => (
            <span className="pr-tag topic" key={tag}>{tag}</span>
          ))}
          <span className={`pr-tag source ${paper.sourceStatus === 'confirmed' ? 'confirmed' : ''}`}>
            {paper.sourceStatus === 'confirmed'
              ? 'OpenAlex + Scholar 已核验'
              : paper.sourceStatus === 'scholar_only' ? 'Scholar 已确认' : 'OpenAlex'}
          </span>
          {paper.citationSources?.googleScholar != null && (
            <span className="pr-tag citation">Scholar 引用 {paper.citationSources.googleScholar}</span>
          )}
          {paper.citationSources?.openalex != null && (
            <span className="pr-tag citation">OpenAlex 引用 {paper.citationSources.openalex}</span>
          )}
        </div>
      </div>
      <div className="pr-year">{paper.year}</div>
    </article>
  );
}

const loadingStyles = `
  .publication-loading{display:grid;gap:10px}.publication-loading span{height:96px;border-radius:var(--radius);background:linear-gradient(90deg,var(--bg-surface) 0%,var(--bg-elevated) 40%,var(--bg-surface) 80%);background-size:200% 100%;animation:publication-loading 1.4s linear infinite}@keyframes publication-loading{to{background-position:-200% 0}}
  @media(prefers-reduced-motion:reduce){.publication-loading span{animation:none}}
`;

const errorStyles = `
  .publication-error{padding:clamp(1.25rem,3vw,2rem);border-radius:var(--radius);background:var(--canvas);color:var(--text-2)}
  .publication-error strong{display:block;font-size:var(--fs-lg);color:var(--text)}
  .publication-error p{margin-top:.3rem;font-size:var(--fs-sm);color:var(--text-2)}
  .publication-error .static-selection{margin:1.25rem 0}
  .publication-error button{min-height:44px;padding:.55rem 1.3rem;border:1px solid var(--text);border-radius:999px;background:var(--text);color:#fff;font-weight:600;font-size:var(--fs-sm);cursor:pointer}
  .publication-error button:hover{background:#000}
`;

const explorerStyles = `
  .publications-explorer{min-width:0}
  .researcher-switcher{display:flex;gap:.5rem;overflow-x:auto;padding:0 0 1.25rem;margin-bottom:1.25rem;border-bottom:1px solid var(--border);scrollbar-width:thin}
  .researcher-switcher button{display:flex;align-items:center;gap:.65rem;flex:0 0 auto;min-height:48px;padding:.45rem .9rem .45rem .5rem;border:1px solid var(--border);border-radius:999px;background:var(--canvas);color:var(--text-2);cursor:pointer;text-align:left;transition:border-color var(--dur-fast),background-color var(--dur-fast)}
  .researcher-switcher button:hover{border-color:var(--border-md)}
  .researcher-switcher button.active{border-color:var(--text);background:var(--text);color:#fff}
  .researcher-switcher button.active small{color:#c9ccd1}
  .researcher-switcher button>span:last-child{display:grid;gap:0;line-height:1.35}
  .researcher-switcher strong{font-size:var(--fs-sm);font-weight:600}
  .researcher-switcher small{font-size:.75rem;color:var(--text-3);font-variant-numeric:tabular-nums}
  .researcher-avatar{width:34px;height:34px;border-radius:50%;object-fit:cover;background:var(--bg-surface);display:grid;place-items:center;font-size:.75rem;font-weight:700;color:var(--text-2)}
  .researcher-avatar.all{font-size:.6875rem;letter-spacing:.04em}
  .publication-toolbar{display:flex;align-items:center;justify-content:space-between;gap:1rem 1.5rem;margin-bottom:1rem;flex-wrap:wrap}
  .filter-bar{display:flex;flex-wrap:wrap;gap:.25rem;padding:.3rem;background:var(--canvas);border-radius:999px}
  .filter-bar button{min-height:36px;padding:.3rem .9rem;font-size:var(--fs-sm);font-weight:500;border-radius:999px;border:0;background:transparent;color:var(--text-2);cursor:pointer;transition:background-color var(--dur-fast),color var(--dur-fast)}
  .filter-bar button:hover{color:var(--text)}
  .filter-bar button.active{background:var(--text);color:#fff;font-weight:600}
  .paper-search{display:flex;align-items:center;gap:.5rem;min-width:260px;min-height:44px;padding:0 1rem;border:1px solid var(--border-md);border-radius:999px;background:var(--bg);transition:border-color var(--dur-fast)}
  .paper-search:focus-within{border-color:var(--text);outline:2px solid var(--focus);outline-offset:2px}
  .paper-search svg{width:16px;height:16px;fill:none;stroke:var(--text-3);stroke-width:1.4}
  .paper-search input{width:100%;border:0;outline:0;font-size:var(--fs-sm);background:transparent;color:var(--text)}
  .paper-search input::placeholder{color:var(--text-3)}
  .sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
  .publication-meta{display:flex;gap:.5rem 1.5rem;align-items:center;flex-wrap:wrap;margin-bottom:1.5rem;color:var(--text-3);font-size:var(--fs-xs);font-variant-numeric:tabular-nums}
  .publication-meta a{margin-left:auto;color:var(--accent);font-weight:600}
  .paper-list{display:flex;flex-direction:column}
  .year-divider{display:flex;align-items:center;gap:1rem;padding:1.75rem 0 .5rem;font-size:var(--fs-sm);font-weight:650;color:var(--text);font-variant-numeric:tabular-nums}
  .year-divider:after{content:'';flex:1;height:1px;background:var(--border-md)}
  .paper-row{display:grid;grid-template-columns:3rem minmax(0,1fr) auto;gap:1.25rem;align-items:start;padding:1.25rem 0;border-bottom:1px solid var(--border);transition:background-color var(--dur-fast)}
  .pr-num{font-size:var(--fs-xs);color:var(--text-3);padding-top:.3rem;font-variant-numeric:tabular-nums}
  .pr-title{display:block;font-size:var(--fs-lg);font-weight:600;line-height:1.5;margin-bottom:.35rem;color:var(--text);text-decoration:none;transition:color var(--dur-fast)}
  a.pr-title:hover{color:var(--accent)}
  .pr-authors{font-size:var(--fs-sm);color:var(--text-2);line-height:1.6}
  .paper-researchers{display:flex;gap:.35rem .9rem;flex-wrap:wrap;margin:.4rem 0 .6rem;font-size:var(--fs-xs);color:var(--accent);font-weight:600}
  .pr-tags{display:flex;flex-wrap:wrap;gap:.35rem}
  .pr-tag{font-size:.75rem;line-height:1.5;padding:.1rem .55rem;border-radius:999px;background:var(--canvas);color:var(--text-2)}
  .pr-tag.venue{background:transparent;padding-left:0;color:var(--text);font-weight:600}
  .pr-tag.if.gold,.pr-tag.rank.top{background:var(--accent-dim);color:var(--accent)}
  .pr-tag.topic{background:transparent;border:1px solid var(--border)}
  .pr-tag.source.confirmed{background:#e8f1ec;color:var(--success)}
  .pr-tag.citation{background:transparent;color:var(--text-3)}
  .pr-year{font-size:var(--fs-xs);color:var(--text-3);padding-top:.3rem;font-variant-numeric:tabular-nums}
  .no-results{color:var(--text-3);font-size:var(--fs-sm);padding:3rem 0;border-bottom:1px solid var(--border)}
  .pr-body{min-width:0;overflow-wrap:anywhere}
  .pr-tags,.pr-tags>span,.paper-researchers>span{min-width:0;max-width:100%;overflow-wrap:anywhere}
  @media(max-width:760px){.publication-toolbar{display:grid}.paper-search{min-width:0}.publication-meta a{margin-left:0}.paper-row{grid-template-columns:1fr;gap:.5rem}.pr-num,.pr-year{display:none}}
`;
