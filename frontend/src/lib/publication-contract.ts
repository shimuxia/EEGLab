import type { PublicationsResponse } from "./publications";

type RecordValue = Record<string, unknown>;
const record = (value: unknown): value is RecordValue =>
  typeof value === "object" && value !== null && !Array.isArray(value);
const text = (value: unknown): value is string => typeof value === "string";
const number = (value: unknown): value is number =>
  typeof value === "number" && Number.isFinite(value);
const count = (value: unknown): boolean =>
  number(value) && Number.isInteger(value) && value >= 0;
const texts = (value: unknown): boolean =>
  Array.isArray(value) && value.every(text);
const optionalText = (value: unknown): boolean => value == null || text(value);
const optionalNumber = (value: unknown): boolean =>
  value == null || number(value);

function safeUrl(value: unknown, image = false): boolean {
  if (value == null || value === "") return true;
  if (!text(value)) return false;
  if (image && /^\/(?!\/)/.test(value) && !value.includes("\\")) return true;
  try {
    const url = new URL(value);
    return url.protocol === "https:" && !url.username && !url.password;
  } catch {
    return false;
  }
}

function researcher(value: unknown): value is RecordValue {
  return (
    record(value) &&
    count(value.id) &&
    text(value.slug) &&
    !!value.slug.trim() &&
    text(value.name) &&
    safeUrl(value.avatarUrl, true) &&
    optionalText(value.nameEn)
  );
}

function paper(value: unknown): boolean {
  if (!record(value)) return false;
  return (
    text(value.id) &&
    text(value.num) &&
    text(value.title) &&
    text(value.authors) &&
    text(value.journal) &&
    text(value.field) &&
    number(value.year) &&
    count(value.citedByCount) &&
    (value.type === "journal" || value.type === "conference") &&
    texts(value.tags) &&
    optionalText(value.doi) &&
    optionalText(value.quartile) &&
    optionalNumber(value.impactFactor) &&
    typeof value.representative === "boolean" &&
    typeof value.isTop === "boolean" &&
    typeof value.lead === "boolean" &&
    Array.isArray(value.researchers) &&
    value.researchers.every(researcher)
  );
}

/** Fail closed at the API boundary; React must never receive unsafe nested records. */
export function parsePublicationsResponse(
  value: unknown,
): PublicationsResponse {
  const valid =
    record(value) &&
    text(value.version) &&
    text(value.updatedAt) &&
    count(value.total) &&
    count(value.offset) &&
    count(value.limit) &&
    texts(value.filterTags) &&
    texts(value.fields) &&
    Array.isArray(value.years) &&
    value.years.every(number) &&
    Array.isArray(value.papers) &&
    value.papers.every(paper) &&
    Array.isArray(value.researchers) &&
    value.researchers.every(
      (item) =>
        researcher(item) &&
        count(item.paperCount) &&
        count(item.currentPaperCount) &&
        safeUrl(item.googleScholarUrl) &&
        (item.scholarMetrics == null ||
          (record(item.scholarMetrics) &&
            optionalNumber(item.scholarMetrics.totalCitations) &&
            optionalNumber(item.scholarMetrics.hIndex) &&
            optionalNumber(item.scholarMetrics.i10Index))),
    ) &&
    (value.typeCounts == null ||
      (record(value.typeCounts) &&
        count(value.typeCounts.journal) &&
        count(value.typeCounts.conference)));
  if (!valid) throw new Error("论文数据格式暂时不可用");
  return value as unknown as PublicationsResponse;
}
