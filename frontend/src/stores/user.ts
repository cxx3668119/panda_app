import { defineStore } from "pinia";
import { computed, ref } from "vue";
import {
  clearAuthStorage,
  TOKEN_STORAGE_KEY,
  USER_STORAGE_KEY,
} from "@/api/client";
import {
  fetchMe,
  updateMe as updateMeRequest,
  uploadAvatar as uploadAvatarRequest,
} from "@/api/account";
import {
  setRecord,
  changePassword,
  login as loginRequest,
  register as registerRequest,
} from "@/api/auth";
import { fetchTodayFortune } from "@/api/daily";
import { useDailyFortuneStore } from "@/stores/dailyFortune";
import { getRecordList } from "@/api/record";
import type {
  AccountUpdatePayload,
  RegisterPayload,
  UserAccount,
  UserRecord,
} from "@/types";

function readStoredUser(): UserAccount | null {
  const raw = localStorage.getItem(USER_STORAGE_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as UserAccount;
  } catch {
    localStorage.removeItem(USER_STORAGE_KEY);
    return null;
  }
}

export const useUserStore = defineStore("user", () => {
  const dailyFortuneStore = useDailyFortuneStore();
  const storedUser = readStoredUser();
  const token = ref(localStorage.getItem(TOKEN_STORAGE_KEY) || "");
  const user = ref<UserAccount | null>(storedUser);
  const userRecords = ref<UserRecord[]>([]);
  const isLoggedIn = computed(() => !!token.value);

  async function login(email: string, password: string) {
    const result = await loginRequest({ email, password });
    token.value = result.token;
    user.value = result.user;
    persist(result.token, result.user);
    return result;
  }

  async function register(payload: RegisterPayload) {
    const result = await registerRequest(payload);
    token.value = result.token;
    user.value = result.user;
    persist(result.token, result.user);
    return result;
  }

  async function loadMe() {
    if (!token.value) return null;
    user.value = await fetchMe();
    persist(token.value, user.value);
    return user.value;
  }

  async function updateMe(payload: AccountUpdatePayload) {
    user.value = await updateMeRequest(payload);
    persist(token.value, user.value);
    return user.value;
  }

  async function uploadAvatar(file: File) {
    user.value = await uploadAvatarRequest(file);
    persist(token.value, user.value);
    return user.value;
  }

  async function updatePassword(currentPassword: string, newPassword: string) {
    await changePassword({ currentPassword, newPassword });
  }

  function logout() {
    token.value = "";
    user.value = null;
    clearAuthStorage();
  }

  function persist(nextToken: string, nextUser: UserAccount | null) {
    if (!nextToken || !nextUser) {
      clearAuthStorage();
      return;
    }
    localStorage.setItem(TOKEN_STORAGE_KEY, nextToken);
    localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(nextUser));
  }

  async function getUserRecords() {
    userRecords.value = await getRecordList();
    return userRecords.value;
  }

  async function setCurrentRecord(recordId: number | string) {
    if (user.value) {
      await setRecord({ recordId });
      user.value.boundRecordId = recordId;
      persist(token.value, user.value);
      await dailyFortuneStore.loadToday();
    }
  }

  return {
    token,
    user,
    userRecords,
    isLoggedIn,
    login,
    register,
    loadMe,
    updateMe,
    uploadAvatar,
    updatePassword,
    logout,
    getUserRecords,
    setCurrentRecord,
  };
});
