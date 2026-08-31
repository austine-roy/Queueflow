export function formatWait(minutes: number): string {
  if (minutes < 1) return "< 1 min";
  return `${Math.round(minutes)} min`;
}

export function formatPercentage(value: number): string {
  return `${Math.round(value * 100)}%`;
}

export function formatDate(value: string): string {
  return new Intl.DateTimeFormat(undefined, { dateStyle: "medium", timeStyle: "short" }).format(new Date(value));
}

export function locationLabel(locationId: number): string {
  return `Location #${locationId}`;
}
