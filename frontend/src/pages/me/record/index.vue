<template>
  <main class="page-shell">
    <section class="page-hero">
      <div class="eyebrow">record</div>
      <h1 class="page-title">个人档案</h1>
      <p class="page-subtitle">维护用于预测的个人信息。</p>
    </section>

    <section class="surface-card space-y-6">
      <ErrorRetryBox v-if="error">{{ error }}</ErrorRetryBox>
      <div v-else-if="success" class="info-box">{{ success }}</div>

      <div class="grid gap-4">
        <div
          class="grid gap-2"
          v-for="value in userStore.$state.userRecords"
          :key="value.id"
        >
          <div class="flex justify-between">
            <div>
              <div>
                <span>{{ value.name }}</span> <span>{{ value.gender }}</span>
              </div>
              <div>{{ value.birthday }}</div>
            </div>
            <div>
              <div>{{ value.horoscope }}</div>
              <div>{{ value.zodiac }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- <div class="flex flex-wrap gap-3">
        <button class="btn-primary" :disabled="saving" @click="handleSubmit">
          {{ saving ? "提交中..." : "确认修改" }}
        </button>
        <RouterLink class="btn-ghost" to="/me">返回我的主页</RouterLink>
      </div> -->
    </section>
  </main>
</template>

<script setup>
import { ref } from "vue";
import ErrorRetryBox from "@/components/common/ErrorRetryBox.vue";
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();

console.log(userStore.$state);
</script>
