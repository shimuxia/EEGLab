import { parsePublicationsResponse } from "./publication-contract";

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

const responseCache = new Map<string, Promise<PublicationsResponse>>();

function apiBase(): string {
  return (import.meta.env.PUBLIC_PAPERS_API_URL || "/api/group").replace(
    /\/$/,
    "",
  );
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
    pending = fetch(url, {
      signal: AbortSignal.timeout(8000),
      headers: { Accept: "application/json" },
    })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error("论文服务暂时不可用，请稍后重试");
        }
        return parsePublicationsResponse(await response.json());
      })
      .catch((error) => {
        responseCache.delete(url);
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
