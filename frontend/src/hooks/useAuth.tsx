/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useMemo, useState } from "react";
import { login as loginRequest, logout as logoutRequest, setAccessToken } from "../services/api";
import type { AuthUser } from "../types/api";

interface AuthState {
  user: AuthUser | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  hasRole: (...roles: AuthUser["role"][]) => boolean;
}

const Context = createContext<AuthState>({ user: null, token: null, login: async () => undefined, logout: async () => undefined, hasRole: () => false });

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const value = useMemo(() => ({
    user,
    token,
    login: async (email: string, password: string) => {
      const result = await loginRequest(email, password);
      setAccessToken(result.access_token);
      setToken(result.access_token);
      setUser(result.user);
    },
    logout: async () => {
      try { if (token) await logoutRequest(); } finally { setAccessToken(null); setToken(null); setUser(null); }
    },
    hasRole: (...roles: AuthUser["role"][]) => user !== null && roles.includes(user.role),
  }), [token, user]);
  return <Context.Provider value={value}>{children}</Context.Provider>;
}

export function useAuth(): AuthState { return useContext(Context); }
