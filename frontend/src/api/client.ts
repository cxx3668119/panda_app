import axios, { AxiosError } from "axios";

const TOKEN_STORAGE_KEY = "panda-app-token";
const USER_STORAGE_KEY = "panda-app-user";

interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
}

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

function getApiBaseUrl() {
  return import.meta.env.VITE_API_BASE_URL || "/api/v1";
}

function getAuthToken() {
  return localStorage.getItem(TOKEN_STORAGE_KEY);
}

function clearAuthStorage() {
  localStorage.removeItem(TOKEN_STORAGE_KEY);
  localStorage.removeItem(USER_STORAGE_KEY);
}

const client = axios.create({
  baseURL: getApiBaseUrl(),
  headers: {
    "Content-Type": "application/json",
  },
});

client.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

client.interceptors.response.use(
  (response) => {
    const result = response.data as ApiResponse<unknown>;
    if (!result?.success) {
      throw new ApiError(
        result?.message || "请求失败，请稍后重试",
        response.status,
      );
    }
    return result.data;
  },
  (error: AxiosError<ApiResponse<unknown>>) => {
    const status = error.response?.status || 0;
    const message =
      error.response?.data?.message || error.message || "请求失败，请稍后重试";

    if (status === 401) {
      clearAuthStorage();
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }

    throw new ApiError(message, status);
  },
);

export function get<T>(path: string) {
  return client.get<any, T>(path);
}

export function post<T>(path: string, body?: unknown) {
  return client.post<any, T>(path, body);
}

export function patch<T>(path: string, body?: unknown) {
  return client.patch<any, T>(path, body);
}

export function postForm<T>(path: string, body: FormData) {
  return client.post<any, T>(path, body, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

export { TOKEN_STORAGE_KEY, USER_STORAGE_KEY, clearAuthStorage, getAuthToken };
