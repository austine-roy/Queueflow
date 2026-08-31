import axios from "axios";
import type { Alert, LoginResult, Measurement, Queue, QueueAnalytics } from "../types/api";

const savedApiUrlKey = "queueflow.apiBaseUrl";
let accessToken: string | null = null;

export function setAccessToken(token: string | null): void { accessToken = token; }

export function getApiBaseUrl(): string {
  return localStorage.getItem(savedApiUrlKey) ?? import.meta.env.VITE_API_BASE_URL ?? "";
}

export function saveApiBaseUrl(value: string): void {
  localStorage.setItem(savedApiUrlKey, value.replace(/\/$/, ""));
}

function apiClient() {
  return axios.create({ baseURL: getApiBaseUrl(), timeout: 8_000, headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined });
}

export async function login(email: string, password: string): Promise<LoginResult> {
  return (await apiClient().post<LoginResult>("/api/auth/login", { email, password })).data;
}

export async function logout(): Promise<void> { await apiClient().post("/api/auth/logout"); }

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

export async function getQueueAnalytics(): Promise<QueueAnalytics[]> {
  return (await apiClient().get<QueueAnalytics[]>("/api/analytics/queues")).data;
}
