export function buildMeetingQuery({
  query,
  participant,
  dateFrom,
  dateTo,
  sort,
  page,
}: {
  query: string;
  participant: string;
  dateFrom: string;
  dateTo: string;
  sort: string;
  page: number;
}) {
  const params = new URLSearchParams({ q: query, participant, sort, page: String(page), page_size: "6" });
  if (dateFrom) params.set("date_from", dateFrom);
  if (dateTo) params.set("date_to", dateTo);
  return params;
}
