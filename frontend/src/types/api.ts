export type QueueStatus = "NORMAL" | "BUSY" | "CROWDED" | "CRITICAL" | "CLOSED";
export type UserRole = "admin" | "operator" | "viewer";

export interface AuthUser {
  id: number;
  email: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface LoginResult {
  access_token: string;
  token_type: "bearer";
  user: AuthUser;
}

export interface Queue {
  id: number;
  name: string;
  location_id: number;
  capacity: number;
  status: QueueStatus;
  current_count: number;
  estimated_wait_time: number;
  density: number;
  created_at: string;
  updated_at: string;
}

export interface Measurement {
  id: number;
  queue_id: number;
  person_count: number;
  density: number;
  estimated_wait_time: number;
  status: QueueStatus;
  recorded_at: string;
}

export interface Alert {
  id: number;
  queue_id: number;
  type: string;
  message: string;
  severity: "INFO" | "WARNING" | "CRITICAL";
  is_active: boolean;
  created_at: string;
  resolved_at: string | null;
}

export interface QueueAnalytics {
  queue_id: number;
  queue_name: string;
  measurement_count: number;
  average_wait_time: number;
  peak_person_count: number;
  latest_measurement_at: string | null;
  measurements: Measurement[];
}
