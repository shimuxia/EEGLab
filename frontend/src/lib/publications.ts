import { completeCatalog, parsePublicationsResponse } from "./publication-contract";

export interface Researcher {
  id: number;
  slug: string;
  name: string;
  nameEn?: string | null;
  orcid?: string | null;
  openalexAuthorId?: string | null;
  googleScholarId?: string | null;
  googleScholarUrl?: string | null;
  affiliation?: string | null;
  avatarUrl?: string | null;
  paperCount: number;
  currentPaperCount: number;
  scholarMetrics?: {
    totalCitations?: number | null;
    hIndex?: number | null;
    i10Index?: number | null;
    updatedAt?: string | null;
    status: "success" | "warning" | "pending";
  };
}

export interface PaperResearcher {
  id: number;
  slug: string;
  name: string;
  nameEn?: string | null;
  avatarUrl?: string | null;
  authorPosition?: number | null;
  isCorresponding: boolean;
  representative: boolean;
  missingSince?: string | null;
  scholarCitationId?: string | null;
  scholarCitedByCount?: number | null;
  scholarLastSeenAt?: string | null;
  scholarMissingSince?: string | null;
  sourceMatchStatus?: "confirmed" | "openalex_only";
  sourceMatchScore?: number | null;
}

export interface Publication {
  id: string;
  num: string;
  doi?: string | null;
  year: number;
  publicationDate?: string | null;
  title: string;
  authors: string;
  journal: string;
  type: "journal" | "conference";
  citedByCount: number;
  citationSource?: "openalex" | "googleScholar";
  citationSources?: {
    openalex?: number | null;
    googleScholar?: number | null;
  };
  sourceStatus?: "confirmed" | "openalex_only" | "scholar_only";
  field: string;
  tags: string[];
  quartile?: string | null;
  impactFactor?: number | null;
  isTop: boolean;
  lead: boolean;
  representative: boolean;
  researchers: PaperResearcher[];
}

export interface PublicationsResponse {
  version: string;
  updatedAt: string;
  total: number;
  typeCounts?: {
    journal: number;
    conference: number;
  };
  offset: number;
  limit: number;
  filterTags: string[];
  fields: string[];
  years: number[];
  researchers: Researcher[];
  papers: Publication[];
}

const catalogListeners = new Set<(data: PublicationsResponse) => void>();

export function onCatalogLoaded(listener: (data: PublicationsResponse) => void): () => void {
  catalogListeners.add(listener);
  return () => { catalogListeners.delete(listener); };
}

const responseCache = new Map<string, Promise<PublicationsResponse>>();

function apiBase(): string {
  const base = (import.meta.env.PUBLIC_PAPERS_API_URL || "/api/group").replace(/\/+$/, "");
  return base.endsWith("/group") ? base : `${base}/group`;
}

export function publicationsUrl(params?: URLSearchParams): string {
  const query = params?.toString();
  return `${apiBase()}/papers${query ? `?${query}` : ""}`;
}

export function fetchPublications(
  params?: URLSearchParams,
  options: { refresh?: boolean } = {},
): Promise<PublicationsResponse> {
  const url = publicationsUrl(params);
  if (options.refresh) responseCache.delete(url);
  let pending = responseCache.get(url);
  if (!pending) {
    const signal = AbortSignal.timeout(8000);
    const read = async (target: string) => {
      const response = await fetch(target, { signal, headers: { Accept: "application/json" } });
      if (!response.ok) throw new Error("论文服务暂时不可用，请稍后重试");
      return parsePublicationsResponse(await response.json());
    };
    pending = read(url).then(first => {
      if (params?.has("limit") || params?.has("offset")) return first;
      return completeCatalog(first, offset => {
        const next = new URLSearchParams(params);
        next.set("offset", String(offset));
        next.set("limit", String(first.limit));
        return read(publicationsUrl(next));
      });
    }).then(data => {
      if (!params?.size && responseCache.get(url) === pending) {
        catalogListeners.forEach(listener => listener(data));
      }
      return data;
    })
      .catch((error) => {
        if (responseCache.get(url) === pending) responseCache.delete(url);
        throw error;
      });
    responseCache.set(url, pending);
  }
  return pending;
}

export function formatUpdatedAt(value?: string): string {
  if (!value) return "尚未同步";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).format(date);
}
