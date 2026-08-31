import axios from "axios";
import type { Alert, Measurement, Queue } from "../types/api";

const savedApiUrlKey = "queueflow.apiBaseUrl";

export function getApiBaseUrl(): string {
  return localStorage.getItem(savedApiUrlKey) ?? import.meta.env.VITE_API_BASE_URL ?? "";
}

export function saveApiBaseUrl(value: string): void {
  localStorage.setItem(savedApiUrlKey, value.replace(/\/$/, ""));
}

function apiClient() {
  return axios.create({ baseURL: getApiBaseUrl(), timeout: 8_000 });
}

export async function getQueues(): Promise<Queue[]> {
  return (await apiClient().get<Queue[]>("/api/queues")).data;
}

export async function getQueue(id: number): Promise<Queue> {
  return (await apiClient().get<Queue>(`/api/queues/${id}`)).data;
}

export async function getMeasurements(queueId: number): Promise<Measurement[]> {
  return (await apiClient().get<Measurement[]>(`/api/queues/${queueId}/measurements`)).data;
}

export async function getAlerts(): Promise<Alert[]> {
  return (await apiClient().get<Alert[]>("/api/alerts")).data;
}
