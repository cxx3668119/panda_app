<template>
  <main v-if="today" class="page-shell">
    <section class="page-hero">
      <div class="eyebrow">Daily reading</div>
      <h1 class="page-title">今日运势</h1>
      <p class="page-subtitle">
        你的每日状态会按当天上下文固定生成，适合反复查看与回顾。
      </p>
    </section>

    <DailyFortuneCard :data="today" />
    <DailyFortuneDetail class="mt-6" :data="today" />

    <div class="mt-6 flex flex-wrap gap-3">
      <button
        class="btn-ghost"
        type="button"
        @click="handleClick('pickRecord')"
      >
        {{ userStore.user?.boundRecordId ? "切换" : "选择" }}档案
      </button>
      <RouterLink class="btn-primary" to="/ai/chat">发起 AI 提问</RouterLink>
      <RouterLink class="btn-secondary" to="/daily/history"
        >查看历史日运</RouterLink
      >
    </div>

    <BottomNav />

    <van-dialog
      v-model:show="pickModalVisible"
      title="选择档案"
      class-name="record-picker-dialog"
      show-cancel-button
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

  <main v-else class="page-shell">
    <LoadingState text="正在生成今日日运..." />
    <div class="mt-6 flex flex-wrap gap-3">
      <button
        class="btn-ghost"
        type="button"
        @click="handleClick('pickRecord')"
      >
        {{ userStore.user?.boundRecordId ? "切换" : "选择" }}档案
      </button>
    </div>
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
const userStore = useUserStore();
const dailyFortuneStore = useDailyFortuneStore();
const today = computed(() => dailyFortuneStore.today);
const pickModalVisible = ref(false);
const pickRecordId = ref<number | string>(0);
const userRecords = computed(() => userStore.userRecords);

onMounted(async () => {
  if (!dailyFortuneStore.today) {
    try {
      await dailyFortuneStore.loadToday();
    } catch (err) {
      showToast(
        err instanceof Error ? err.message : "今日日运获取失败，请稍后重试",
      );
    }
  }
  if (!userStore.user?.boundRecordId) {
    pickModalVisible.value = true;
  }
});

async function handleClick(action: string) {
  if (action === "pickRecord") {
    pickRecordId.value = Number(userStore.user?.boundRecordId || "");
    await userStore.getUserRecords();
    pickModalVisible.value = true;
  }

  if (action === "modalConfirm") {
    pickRecordId.value = Number(pickRecordId.value);
    try {
      await userStore.setCurrentRecord(pickRecordId.value);
      showSuccessToast("档案选择成功");
    } catch (err) {
      showFailToast(err instanceof Error ? err.message : "档案选择失败");
    }
    pickModalVisible.value = false;
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
</style>
