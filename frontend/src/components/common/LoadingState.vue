<template>
  <section class="surface-card panda-panel loading-state">
    <div class="loading-state__header">
      <div class="loading-state__badge">
        <span class="loading-state__badge-dot" />
        AI 生成中
      </div>
      <div class="loading-state__elapsed">已等待 {{ elapsedLabel }}</div>
    </div>

    <div class="loading-state__body">
      <img
        alt="等待中的熊猫徽章"
        class="loading-state__avatar"
        src="/panda-badge.png"
      />

      <div class="min-w-0 flex-1">
        <h3 class="loading-state__title">{{ title }}</h3>
        <p class="loading-state__text">{{ text }}</p>

        <div class="loading-state__status">
          <span class="loading-state__pulse" />
          <span>{{ activeStep }}</span>
        </div>
      </div>
    </div>

    <div class="loading-state__steps">
      <div
        v-for="(step, index) in normalizedSteps"
        :key="step"
        class="loading-step"
        :class="{
          'loading-step-active': index === activeStepIndex,
          'loading-step-done': index < activeStepIndex
        }"
      >
        <span class="loading-step__index">{{ index + 1 }}</span>
        <span class="loading-step__text">{{ step }}</span>
      </div>
    </div>

    <div class="loading-state__preview">
      <div class="loading-state__score shimmer-block">
        <div class="loading-state__score-date shimmer-line shimmer-line-sm" />
        <div class="loading-state__score-main">
          <div class="shimmer-line shimmer-line-lg" />
          <div class="shimmer-circle" />
        </div>
        <div class="shimmer-line shimmer-line-md" />
      </div>

      <div class="loading-state__detail shimmer-block">
        <div class="shimmer-line shimmer-line-sm" />
        <div class="shimmer-line shimmer-line-full" />
        <div class="shimmer-line shimmer-line-full" />
        <div class="shimmer-line shimmer-line-md" />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

const props = withDefaults(
  defineProps<{
    title?: string
    text?: string
    steps?: string[]
  }>(),
  {
    title: '正在生成今日运势',
    text: '已发起接口调用，AI 正在结合当前档案与当天状态整理解读。',
    steps: () => ['读取当前档案', '整理今日线索', '生成建议与摘要']
  }
)

const elapsedSeconds = ref(0)
let timer: number | null = null

const normalizedSteps = computed(() =>
  props.steps.length ? props.steps : ['准备中']
)

const activeStepIndex = computed(() =>
  Math.min(Math.floor(elapsedSeconds.value / 4), normalizedSteps.value.length - 1)
)

const activeStep = computed(() => normalizedSteps.value[activeStepIndex.value])

const elapsedLabel = computed(() => {
  if (elapsedSeconds.value < 60) {
    return `${elapsedSeconds.value} 秒`
  }

  const minutes = Math.floor(elapsedSeconds.value / 60)
  const seconds = elapsedSeconds.value % 60
  return `${minutes} 分 ${seconds} 秒`
})

onMounted(() => {
  timer = window.setInterval(() => {
    elapsedSeconds.value += 1
  }, 1000)
})

onBeforeUnmount(() => {
  if (timer !== null) {
    window.clearInterval(timer)
  }
})
</script>

<style scoped>
.loading-state {
  display: grid;
  gap: 18px;
}

.loading-state__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.loading-state__badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border-radius: 999px;
  background: rgba(223, 233, 220, 0.72);
  padding: 6px 12px;
  color: #38513a;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.loading-state__badge-dot,
.loading-state__pulse {
  display: inline-flex;
  border-radius: 999px;
  background: #5f7f62;
}

.loading-state__badge-dot {
  width: 8px;
  height: 8px;
  animation: softPulse 1.5s ease-in-out infinite;
}

.loading-state__elapsed {
  color: #667067;
  font-size: 12px;
  font-weight: 600;
}

.loading-state__body {
  display: flex;
  align-items: center;
  gap: 16px;
}

.loading-state__avatar {
  width: 72px;
  height: 72px;
  flex-shrink: 0;
  border: 1px solid rgba(215, 219, 210, 0.9);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.88);
  padding: 10px;
  box-shadow: 0 16px 28px rgba(95, 127, 98, 0.1);
}

.loading-state__title {
  margin: 0;
  color: #161715;
  font-size: 20px;
  font-weight: 700;
  line-height: 1.3;
}

.loading-state__text {
  margin: 8px 0 0;
  color: #667067;
  font-size: 14px;
  line-height: 1.75;
}

.loading-state__status {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  margin-top: 12px;
  color: #38513a;
  font-size: 13px;
  font-weight: 600;
}

.loading-state__pulse {
  width: 10px;
  height: 10px;
  box-shadow: 0 0 0 0 rgba(95, 127, 98, 0.28);
  animation: ringPulse 1.8s ease-out infinite;
}

.loading-state__steps {
  display: grid;
  gap: 10px;
}

.loading-step {
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid rgba(215, 219, 210, 0.88);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.62);
  padding: 10px 12px;
  color: #667067;
  transition:
    border-color 0.25s ease,
    background-color 0.25s ease,
    transform 0.25s ease,
    box-shadow 0.25s ease;
}

.loading-step-active {
  border-color: rgba(95, 127, 98, 0.45);
  background: rgba(223, 233, 220, 0.56);
  color: #2f4431;
  transform: translateY(-1px);
  box-shadow: 0 12px 26px rgba(95, 127, 98, 0.1);
}

.loading-step-done {
  border-color: rgba(95, 127, 98, 0.2);
  color: #516352;
}

.loading-step__index {
  display: inline-flex;
  width: 24px;
  height: 24px;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: rgba(95, 127, 98, 0.12);
  color: #38513a;
  font-size: 12px;
  font-weight: 700;
}

.loading-step__text {
  font-size: 13px;
  font-weight: 600;
}

.loading-state__preview {
  display: grid;
  gap: 14px;
}

.loading-state__score,
.loading-state__detail {
  border: 1px solid rgba(215, 219, 210, 0.8);
  border-radius: 24px;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.7),
    rgba(246, 247, 241, 0.9)
  );
  padding: 18px;
}

.loading-state__score-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin: 14px 0 18px;
}

.shimmer-block,
.shimmer-line,
.shimmer-circle {
  position: relative;
  overflow: hidden;
}

.shimmer-line,
.shimmer-circle {
  background: rgba(95, 127, 98, 0.09);
}

.shimmer-line::after,
.shimmer-circle::after {
  content: '';
  position: absolute;
  inset: 0;
  transform: translateX(-100%);
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.65),
    transparent
  );
  animation: shimmer 1.8s ease-in-out infinite;
}

.shimmer-line {
  border-radius: 999px;
}

.shimmer-circle {
  width: 52px;
  height: 52px;
  border-radius: 999px;
}

.shimmer-line-sm {
  width: 96px;
  height: 10px;
}

.shimmer-line-md {
  width: 68%;
  height: 12px;
}

.shimmer-line-lg {
  width: 150px;
  height: 34px;
}

.shimmer-line-full {
  width: 100%;
  height: 12px;
}

.loading-state__detail {
  display: grid;
  gap: 12px;
}

@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}

@keyframes softPulse {
  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0.4;
  }
}

@keyframes ringPulse {
  0% {
    box-shadow: 0 0 0 0 rgba(95, 127, 98, 0.28);
  }

  70% {
    box-shadow: 0 0 0 9px rgba(95, 127, 98, 0);
  }

  100% {
    box-shadow: 0 0 0 0 rgba(95, 127, 98, 0);
  }
}

@media (max-width: 640px) {
  .loading-state__header,
  .loading-state__body,
  .loading-state__score-main {
    align-items: flex-start;
    flex-direction: column;
  }

  .loading-state__avatar {
    width: 64px;
    height: 64px;
  }

  .shimmer-line-lg {
    width: 120px;
  }
}
</style>
