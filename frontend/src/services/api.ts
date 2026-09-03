import axios from "axios";
import type { Alert, Camera, CameraAnalysis, Location, LoginResult, Measurement, Queue, QueueAnalytics, QueueCreate, QueuePrediction } from "../types/api";

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

export async function getLocations(): Promise<Location[]> {
  return (await apiClient().get<Location[]>("/api/locations")).data;
}

export async function createQueue(payload: QueueCreate): Promise<Queue> {
  return (await apiClient().post<Queue>("/api/queues", payload)).data;
}

export async function deleteQueue(queueId: number): Promise<void> {
  await apiClient().delete(`/api/queues/${queueId}`);
}

export async function createCamera(payload: { name: string; location_id: number; queue_id: number; source_type: "WEBCAM" }): Promise<Camera> {
  return (await apiClient().post<Camera>("/api/cameras", payload)).data;
}

export async function submitCameraObservation(cameraId: number, payload: { person_count: number; density: number }): Promise<Camera> {
  return (await apiClient().post<Camera>(`/api/cameras/${cameraId}/observations`, payload)).data;
}

export async function analyzeCameraFrame(cameraId: number, frameData: string): Promise<CameraAnalysis> {
  return (await apiClient().post<CameraAnalysis>(`/api/cameras/${cameraId}/analyze-frame`, { frame_data: frameData })).data;
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

export async function getQueuePrediction(queueId: number): Promise<QueuePrediction> {
  return (await apiClient().get<QueuePrediction>(`/api/analytics/queues/${queueId}/prediction`)).data;
}
