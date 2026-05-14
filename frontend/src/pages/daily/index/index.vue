<template>
  <main class="page-shell">
    <section class="page-hero">
      <div class="eyebrow">Daily Reading</div>
      <h1 class="page-title">今日运势</h1>
      <p class="page-subtitle">
        你的每日状态会按当天上下文生成，适合反复查看与回顾。
      </p>
    </section>

    <template v-if="today">
      <section class="relative">
        <div
          class="space-y-6 transition-opacity duration-300"
          :class="{ 'opacity-55': isRefreshingToday }"
        >
          <DailyFortuneCard :data="today" />
          <DailyFortuneDetail :data="today" />
        </div>

        <transition name="fortune-overlay">
          <div v-if="isRefreshingToday" class="fortune-refresh-overlay">
            <div class="fortune-refresh-panel">
              <div class="fortune-refresh-badge">
                <span class="fortune-refresh-badge__dot" />
                正在重新生成
              </div>
              <h3 class="fortune-refresh-title">
                已切换档案，正在刷新今日运势
              </h3>
              <p class="fortune-refresh-text">
                接口已经发出，当前内容会在生成完成后自动更新。
              </p>
              <div class="fortune-refresh-steps">
                <span
                  v-for="step in loadingSteps"
                  :key="step"
                  class="fortune-refresh-step"
                >
                  {{ step }}
                </span>
              </div>
            </div>
          </div>
        </transition>
      </section>

      <div class="mt-6 flex flex-wrap gap-3">
        <button
          class="btn-ghost"
          type="button"
          :disabled="isLoadingToday"
          @click="handleClick('pickRecord')"
        >
          {{ userStore.user?.boundRecordId ? "切换" : "选择" }}档案
        </button>
        <RouterLink class="btn-primary" to="/ai/chat">发起 AI 提问</RouterLink>
        <RouterLink class="btn-secondary" to="/daily/history">
          查看历史日运
        </RouterLink>
      </div>
    </template>

    <template v-else-if="isLoadingToday">
      <LoadingState
        title="今日运势生成中"
        text="接口已经发出，AI 正在结合你的档案与当天状态生成更完整的解读。"
        :steps="loadingSteps"
      />

      <div class="mt-6 flex flex-wrap gap-3">
        <button
          class="btn-ghost"
          type="button"
          :disabled="isLoadingToday"
          @click="handleClick('pickRecord')"
        >
          {{ userStore.user?.boundRecordId ? "切换" : "选择" }}档案
        </button>
      </div>
    </template>

    <template v-else>
      <section class="error-box">
        今日运势还没有加载出来，请稍后再试一次。
      </section>

      <div class="mt-6 flex flex-wrap gap-3">
        <button class="btn-primary" type="button" @click="loadTodayFortune">
          重新获取
        </button>
        <button
          class="btn-ghost"
          type="button"
          :disabled="isLoadingToday"
          @click="handleClick('pickRecord')"
        >
          {{ userStore.user?.boundRecordId ? "切换" : "选择" }}档案
        </button>
      </div>
    </template>

    <BottomNav />

    <van-dialog
      v-model:show="pickModalVisible"
      title="选择档案"
      class-name="record-picker-dialog"
      show-cancel-button
      :confirm-button-loading="isSubmittingRecord"
      @confirm="handleClick('modalConfirm')"
    >
      <div class="max-h-[400px] overflow-y-auto">
        <van-radio-group v-model="pickRecordId" class="record-picker-list">
          <van-radio
            v-for="item in userRecords"
            :key="item.id"
            :name="item.id"
            class="record-picker-option"
          >
            <div class="min-w-0">
              <div class="record-picker-name">{{ item.name }}</div>
              <div class="record-picker-meta">
                {{ formatBirthday(item.birthday) }}
              </div>
            </div>
          </van-radio>
        </van-radio-group>
      </div>
    </van-dialog>
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import BottomNav from "@/components/common/BottomNav.vue";
import LoadingState from "@/components/common/LoadingState.vue";
import DailyFortuneCard from "@/components/daily/DailyFortuneCard.vue";
import DailyFortuneDetail from "@/components/daily/DailyFortuneDetail.vue";
import { useDailyFortuneStore } from "@/stores/dailyFortune";
import { useUserStore } from "@/stores/user";
import { showToast, showSuccessToast, showFailToast } from "vant";
import { useRouter } from "vue-router";
const router = useRouter();

const userStore = useUserStore();
const dailyFortuneStore = useDailyFortuneStore();

const today = computed(() => dailyFortuneStore.today);
const isLoadingToday = computed(() => dailyFortuneStore.loadingToday);
const isRefreshingToday = computed(
  () => Boolean(today.value) && isLoadingToday.value,
);
const pickModalVisible = ref(false);
const pickRecordId = ref<number | string>(0);
const isSubmittingRecord = ref(false);
const userRecords = computed(() => userStore.userRecords);
const loadingSteps = ["读取当前档案", "整理今日状态线索", "生成适合今天的建议"];

onMounted(async () => {
  if (!dailyFortuneStore.today) {
    await loadTodayFortune();
  }

  if (!userStore.user?.boundRecordId) {
    pickModalVisible.value = true;
  }
});

async function loadTodayFortune() {
  try {
    await dailyFortuneStore.loadToday();
  } catch (err) {
    showToast(
      err instanceof Error ? err.message : "今日运势获取失败，请稍后重试",
    );
  }
}

async function handleClick(action: string) {
  if (action === "pickRecord") {
    pickRecordId.value = Number(userStore.user?.boundRecordId || "");
    console.log(pickRecordId.value);

    await userStore.getUserRecords();
    pickModalVisible.value = true;
  }

  if (action === "modalConfirm") {
    const nextRecordId = Number(pickRecordId.value);
    const currentRecordId = Number(userStore.user?.boundRecordId || "");
    if (!userRecords.value.length) {
      router.push("/me/record");
    }
    
    if (!nextRecordId) {
      showFailToast("请先选择一个档案");
      return;
    }

    if (nextRecordId === currentRecordId) {
      pickModalVisible.value = false;
      return;
    }

    isSubmittingRecord.value = true;

    try {
      pickModalVisible.value = false;
      await userStore.setCurrentRecord(nextRecordId);
      showSuccessToast("档案已切换，今日运势已更新");
    } catch (err) {
      showFailToast(err instanceof Error ? err.message : "档案切换失败");
    } finally {
      isSubmittingRecord.value = false;
    }
  }
}

function formatBirthday(value: string) {
  return value.replace("T", " ").slice(0, 19);
}
</script>

<style scoped>
:deep(.record-picker-dialog) {
  width: min(320px, calc(100vw - 48px));
  overflow: hidden;
  border-radius: 18px;
  background: #fdfcf8;
}

:deep(.record-picker-dialog .van-dialog__header) {
  padding-top: 22px;
  color: #161715;
  font-size: 16px;
  font-weight: 700;
}

:deep(.record-picker-dialog .van-dialog__content) {
  padding: 12px 16px 16px;
}

:deep(.record-picker-dialog .van-dialog__footer) {
  border-top: 1px solid rgba(215, 219, 210, 0.85);
}

:deep(.record-picker-dialog .van-dialog__cancel) {
  color: #667067;
}

:deep(.record-picker-dialog .van-dialog__confirm) {
  color: #5f7f62;
  font-weight: 700;
}

.record-picker-list {
  display: grid;
  gap: 10px;
}

.record-picker-option {
  margin: 0;
  align-items: center;
  border: 1px solid rgba(215, 219, 210, 0.9);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.72);
  padding: 10px 12px;
  transition:
    border-color 0.2s ease,
    background-color 0.2s ease,
    box-shadow 0.2s ease;
}

.record-picker-option:has(.van-radio__icon--checked) {
  border-color: rgba(95, 127, 98, 0.55);
  background: rgba(223, 233, 220, 0.45);
  box-shadow: 0 10px 24px rgba(95, 127, 98, 0.12);
}

:deep(.record-picker-option .van-radio__label) {
  min-width: 0;
  flex: 1;
  margin-left: 10px;
}

.record-picker-name {
  overflow: hidden;
  color: #161715;
  font-size: 14px;
  font-weight: 700;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.record-picker-meta {
  margin-top: 2px;
  color: #667067;
  font-size: 12px;
  line-height: 1.5;
}

.fortune-refresh-overlay {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 35vh 20px 20px;
  z-index: 40;
  pointer-events: none;
}

.fortune-refresh-panel {
  width: min(100%, 420px);
  border: 1px solid rgba(215, 219, 210, 0.92);
  border-radius: 28px;
  background: rgba(253, 252, 248, 0.92);
  backdrop-filter: blur(12px);
  box-shadow: 0 20px 40px rgba(95, 127, 98, 0.14);
  padding: 18px 18px 16px;
  text-align: left;
}

.fortune-refresh-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border-radius: 999px;
  background: rgba(223, 233, 220, 0.78);
  color: #38513a;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.06em;
  padding: 6px 12px;
}

.fortune-refresh-badge__dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #5f7f62;
  animation: softPulse 1.5s ease-in-out infinite;
}

.fortune-refresh-title {
  margin: 14px 0 0;
  color: #161715;
  font-size: 18px;
  font-weight: 700;
  line-height: 1.4;
}

.fortune-refresh-text {
  margin: 8px 0 0;
  color: #667067;
  font-size: 14px;
  line-height: 1.7;
}

.fortune-refresh-steps {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
}

.fortune-refresh-step {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.86);
  border: 1px solid rgba(215, 219, 210, 0.9);
  color: #516352;
  font-size: 12px;
  font-weight: 600;
  padding: 7px 10px;
}

.fortune-overlay-enter-active,
.fortune-overlay-leave-active {
  transition:
    opacity 0.25s ease,
    transform 0.25s ease;
}

.fortune-overlay-enter-from,
.fortune-overlay-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@keyframes softPulse {
  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0.42;
  }
}
</style>
