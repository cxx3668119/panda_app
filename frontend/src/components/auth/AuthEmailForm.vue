<template>
  <div class="surface-card panda-panel space-y-5">
    <div class="flex items-start justify-between gap-3">
      <div class="space-y-2">
        <div class="eyebrow">
          {{ mode === "login" ? "Welcome back" : "Create account" }}
        </div>
        <h3 class="section-title">
          {{ mode === "login" ? "账号密码登录" : "注册账号" }}
        </h3>
      </div>
      <img
        alt="熊猫徽章"
        class="h-12 w-12 rounded-2xl border border-line/70 bg-white/85 p-2 shadow-soft"
        src="/panda-badge.png"
      />
    </div>

    <div class="grid gap-4">
      <div v-if="mode === 'register'" class="grid gap-2">
        <label class="field-label">昵称</label>
        <input
          class="field-input"
          :value="nickname"
          placeholder="请输入昵称"
          @input="
            $emit('update:nickname', ($event.target as HTMLInputElement).value)
          "
        />
      </div>
      <div class="grid gap-2">
        <label class="field-label">邮箱</label>
        <input
          class="field-input"
          :value="email"
          type="email"
          placeholder="请输入邮箱"
          @input="
            $emit('update:email', ($event.target as HTMLInputElement).value)
          "
        />
      </div>
      <div v-if="mode === 'register'" class="grid gap-2">
        <label class="field-label">手机号</label>
        <input
          class="field-input"
          :value="mobile"
          placeholder="请输入手机号（可选）"
          @input="
            $emit('update:mobile', ($event.target as HTMLInputElement).value)
          "
        />
      </div>
      <div class="grid gap-2">
        <label class="field-label">密码</label>
        <input
          class="field-input"
          :value="password"
          type="password"
          placeholder="请输入密码"
          @input="
            $emit('update:password', ($event.target as HTMLInputElement).value)
          "
        />
      </div>
      <div v-if="mode === 'register'" class="grid gap-2">
        <label class="field-label">确认密码</label>
        <input
          class="field-input"
          :value="confirmPassword"
          type="password"
          placeholder="请再次输入密码"
          @input="
            $emit(
              'update:confirmPassword',
              ($event.target as HTMLInputElement).value,
            )
          "
        />
      </div>
      <div v-if="mode === 'register'" class="grid gap-2">
        <label class="field-label">时区</label>
        <input
          class="field-input"
          :value="timezone"
          placeholder="如 Asia/Shanghai"
          @input="
            $emit('update:timezone', ($event.target as HTMLInputElement).value)
          "
        />
      </div>
    </div>

    <div
      v-if="mode === 'login' && currentEnv === 'development'"
      class="rounded-2xl border border-line/70 bg-white/70 px-4 py-3 text-sm leading-6 text-muted"
    >
      演示账号：demo@example.com / 123456
    </div>

    <div class="flex flex-wrap gap-3">
      <button class="btn-primary" @click="$emit('submit')">
        {{ mode === "login" ? "登录" : "注册并进入" }}
      </button>
      <button class="btn-ghost" type="button" @click="$emit('toggle-mode')">
        {{ mode === "login" ? "去注册" : "返回登录" }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
const currentEnv = import.meta.env.MODE

defineProps<{
  mode: "login" | "register";
  nickname: string;
  email: string;
  mobile: string;
  password: string;
  confirmPassword: string;
  timezone: string;
}>();

defineEmits<{
  (e: "update:nickname", value: string): void;
  (e: "update:email", value: string): void;
  (e: "update:mobile", value: string): void;
  (e: "update:password", value: string): void;
  (e: "update:confirmPassword", value: string): void;
  (e: "update:timezone", value: string): void;
  (e: "submit"): void;
  (e: "toggle-mode"): void;
}>();
</script>
