import { useEffect, useState } from 'react';
import { fetchPublications, onCatalogLoaded, type PublicationsResponse } from '../lib/publications';

interface Props {
  type?: 'all' | 'journal' | 'conference';
  suffix?: string;
}

export default function PublicationCount({ type = 'all', suffix = '' }: Props) {
  const [count, setCount] = useState<number | null>(null);
  useEffect(() => {
    const update = (data: PublicationsResponse) => {
      setCount(
        type === 'all'
          ? data.total
          : data.typeCounts?.[type] ?? data.papers.filter(paper => paper.type === type).length,
      );
    };
    const unsubscribe = onCatalogLoaded(update);
    let mounted = true;
    fetchPublications().then(data => { if (mounted) update(data); }).catch(() => {});
    return () => { mounted = false; unsubscribe(); };
  }, [type]);
  return <>{count === null ? '—' : `${count}${suffix}`}</>;
}
