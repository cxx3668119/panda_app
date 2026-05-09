<template>
  <main class="page-shell">
    <section class="grid gap-6 lg:grid-cols-[1.15fr_0.85fr] lg:items-start">
      <div
        class="page-hero panda-panel rounded-[32px] border border-line/70 bg-panel/75 p-6 pt-6 lg:pt-8"
      >
        <div class="flex items-center gap-3 text-sm text-muted">
          <img
            alt="熊猫徽章"
            class="h-12 w-12 rounded-2xl border border-line/70 bg-white/80 p-2 shadow-soft"
            src="/panda-badge.png"
          />
          <div>
            <div class="eyebrow">Panda companion</div>
            <div class="text-xs leading-6">
              从“我的”统一管理账号、提醒与命盘体验
            </div>
          </div>
        </div>
        <div class="mt-5 space-y-3">
          <h1 class="page-title">AI 运势助手</h1>
          <p class="page-subtitle">
            {{
              mode === "login"
                ? "使用账号密码登录，进入你的专属主页，管理账号信息、头像、密码与提醒设置。"
                : "先注册账号，再创建你的专属命盘档案与提醒体验。"
            }}
          </p>
        </div>
        <div
          class="mt-6 overflow-hidden rounded-[28px] border border-accent/15 bg-white/72 p-4 shadow-soft"
        >
          <img alt="熊猫主题插画" class="h-auto w-full" src="/panda-mark.gif" />
        </div>
      </div>

      <div class="space-y-4">
        <AuthEmailForm
          :mode="mode"
          :nickname="nickname"
          :email="email"
          :mobile="mobile"
          :password="password"
          :confirm-password="confirmPassword"
          :timezone="timezone"
          @update:nickname="nickname = $event"
          @update:email="email = $event"
          @update:mobile="mobile = $event"
          @update:password="password = $event"
          @update:confirmPassword="confirmPassword = $event"
          @update:timezone="timezone = $event"
          @submit="handleSubmit"
          @toggle-mode="toggleMode"
        />

        <ErrorRetryBox v-if="error">
          {{ error }}
        </ErrorRetryBox>
        <LoadingState
          v-else-if="loading"
          :text="mode === 'login' ? '正在登录...' : '正在注册... '"
        />

        <DisclaimerBlock
          text="本产品内容仅供娱乐陪伴和自我探索参考，不构成医疗、法律、投资等专业建议。"
        />
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import AuthEmailForm from "@/components/auth/AuthEmailForm.vue";
import DisclaimerBlock from "@/components/common/DisclaimerBlock.vue";
import ErrorRetryBox from "@/components/common/ErrorRetryBox.vue";
import LoadingState from "@/components/common/LoadingState.vue";
import { useUserStore } from "@/stores/user";

const router = useRouter();
const userStore = useUserStore();
const currentEnv = import.meta.env.MODE;
const mode = ref<"login" | "register">("login");
const nickname = ref("");
const email = ref(currentEnv === "development" ? "demo@example.com" : "");
const mobile = ref("");
const password = ref(currentEnv === "development" ? "123456" : "");
const confirmPassword = ref("");
const timezone = ref("Asia/Shanghai");
const loading = ref(false);
const error = ref("");

function toggleMode() {
  mode.value = mode.value === "login" ? "register" : "login";
  error.value = "";
  if (mode.value === "register") {
    nickname.value = "";
    email.value = "";
    mobile.value = "";
    password.value = "";
    confirmPassword.value = "";
    timezone.value = "Asia/Shanghai";
  } else {
    email.value = "demo@example.com";
    password.value = "123456";
    confirmPassword.value = "";
  }
}

async function handleSubmit() {
  error.value = "";
  if (!email.value.trim() || !/.+@.+\..+/.test(email.value)) {
    error.value = "请输入有效邮箱地址";
    return;
  }
  if (!password.value.trim()) {
    error.value = "请输入密码";
    return;
  }

  if (mode.value === "register") {
    if (!nickname.value.trim()) {
      error.value = "请输入昵称";
      return;
    }
    if (password.value.trim().length < 6) {
      error.value = "密码长度不能少于6位";
      return;
    }
    if (password.value !== confirmPassword.value) {
      error.value = "两次输入的密码不一致";
      return;
    }
    if (!timezone.value.trim()) {
      error.value = "请输入时区";
      return;
    }
  }

  try {
    loading.value = true;
    const result =
      mode.value === "login"
        ? await userStore.login(email.value.trim(), password.value)
        : await userStore.register({
            nickname: nickname.value.trim(),
            email: email.value.trim(),
            mobile: mobile.value.trim() || null,
            password: password.value,
            timezone: timezone.value.trim(),
          });
    router.push(result.hasProfile ? "/daily" : "/profile/create");
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : mode.value === "login"
          ? "登录失败，请检查邮箱和密码"
          : "注册失败，请稍后重试";
  } finally {
    loading.value = false;
  }
}
</script>
