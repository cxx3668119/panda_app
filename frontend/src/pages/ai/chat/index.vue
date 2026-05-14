<template>
  <main class="chat-page">
    <section
      class="chat-shell"
      :style="{ '--chat-footer-space': `${footerHeight}px` }"
    >
      <header class="chat-header">
        <button class="chat-back" type="button" @click="handleBack">
          <span class="chat-back__icon"><</span>
          <span>返回</span>
        </button>

        <div class="chat-header__title">
          <div class="eyebrow">Panda guide</div>
          <h1 class="chat-title">AI 问答</h1>
        </div>
      </header>

      <section ref="messagesRef" class="chat-stream">
        <article
          v-if="messages.length === 0"
          class="message-row message-row-assistant"
        >
          <div class="assistant-avatar">
            <img
              alt="熊猫助手"
              class="assistant-avatar__image"
              src="/panda-badge.png"
            />
          </div>

          <!-- <div
            class="message-bubble message-bubble-assistant message-bubble-intro"
          >
            <div class="message-meta">
              <span class="message-name">Panda guide</span>
              <span class="message-chip">褰撴棩涓婁笅鏂?/span>
            </div>
            <div class="message-content">
              鎴戜細缁撳悎浣犱粖澶╃殑妗ｆ銆佹棩杩愬拰杩炵画鎻愰棶鏉ュ洖绛斻€備綘鍙互鐩存帴杈撳叆鏈€鍏冲績鐨勯棶棰橈紝鎴戜滑灏变粠閭ｉ噷寮€濮嬨€?            </div>
          </div> -->
        </article>

        <article
          v-for="message in messages"
          :key="message.id"
          class="message-row"
          :class="
            message.role === 'user'
              ? 'message-row-user'
              : 'message-row-assistant'
          "
        >
          <div v-if="message.role !== 'user'" class="assistant-avatar">
            <img
              alt="熊猫助手"
              class="assistant-avatar__image"
              src="/panda-badge.png"
            />
          </div>

          <div
            class="message-bubble"
            :class="
              message.role === 'user'
                ? 'message-bubble-user'
                : 'message-bubble-assistant'
            "
          >
            <div v-if="message.role !== 'user'" class="message-meta">
              <span class="message-name">Panda guide</span>
            </div>
            <div
              v-if="
                message.role === 'assistant' &&
                chatStore.loading &&
                !message.content
              "
              class="typing-dots"
              aria-label="正在生成回答"
            >
              <span />
              <span />
              <span />
            </div>
            <div v-else class="message-content">{{ message.content }}</div>
            <div
              v-if="message.disclaimer"
              class="message-disclaimer"
              :class="
                message.role === 'user'
                  ? 'message-disclaimer-user'
                  : 'message-disclaimer-assistant'
              "
            >
              {{ message.disclaimer }}
            </div>
          </div>
        </article>
      </section>
    </section>

    <section ref="footerRef" class="chat-footer">
      <div class="composer-card">
        <div class="composer-main">
          <textarea
            v-model="question"
            class="composer-input"
            rows="1"
            placeholder="给 Panda guide 发送消息"
            @keydown.enter.exact.prevent="handleSend"
          />
          <button
            class="composer-send"
            type="button"
            :disabled="chatStore.loading || !question.trim()"
            @click="handleSend"
          >
            ↑
          </button>
        </div>
      </div>

      <div class="chat-footer__disclaimer">内容由 AI 生成，请仔细甄别</div>
    </section>
  </main>

  <!-- <main v-else class="page-shell">
    <LoadingState text="姝ｅ湪鍔犺浇褰撴棩闂瓟涓婁笅鏂?.." />
  </main> -->
</template>

<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useChatStore } from "@/stores/chat";

const router = useRouter();
const chatStore = useChatStore();
const question = ref("");
// const booting = ref(true);
const messagesRef = ref<HTMLElement | null>(null);
const footerRef = ref<HTMLElement | null>(null);
const footerHeight = ref(172);
let footerResizeObserver: ResizeObserver | null = null;

const messages = computed(() => chatStore.messages);

onMounted(async () => {
  lockPageScroll();
  measureFooterHeight();
  if (typeof ResizeObserver !== "undefined" && footerRef.value) {
    footerResizeObserver = new ResizeObserver(() => {
      measureFooterHeight();
    });
    footerResizeObserver.observe(footerRef.value);
  }
  window.addEventListener("resize", measureFooterHeight);

  try {
    await chatStore.loadSession();
    await chatStore.streamIntroIfNeeded();
  } finally {
    // booting.value = false;
    await scrollToBottom("auto");
  }
});

watch(
  () =>
    messages.value.map((message) => ({
      id: message.id,
      contentLength: message.content.length,
      disclaimer: message.disclaimer ?? "",
    })),
  async () => {
    await scrollToBottom();
  },
  { deep: true, flush: "post" },
);

onBeforeUnmount(() => {
  footerResizeObserver?.disconnect();
  footerResizeObserver = null;
  window.removeEventListener("resize", measureFooterHeight);
  unlockPageScroll();
});

async function handleSend() {
  if (!question.value.trim()) return;
  if (chatStore.loading) return;

  const currentQuestion = question.value.trim();
  question.value = "";
  await scrollToBottom("smooth");
  await chatStore.sendQuestion(currentQuestion);
}

function handleBack() {
  router.back();
}

function measureFooterHeight() {
  const footer = footerRef.value;
  if (!footer) return;
  footerHeight.value = Math.ceil(footer.getBoundingClientRect().height) + 24;
}

async function scrollToBottom(behavior: ScrollBehavior = "smooth") {
  await nextTick();
  measureFooterHeight();

  const container = messagesRef.value;
  if (!container) return;

  container.scrollTo({
    top: container.scrollHeight,
    behavior,
  });
}

function lockPageScroll() {
  document.documentElement.style.overflow = "hidden";
  document.body.style.overflow = "hidden";
}

function unlockPageScroll() {
  document.documentElement.style.overflow = "";
  document.body.style.overflow = "";
}
</script>

<style scoped>
.chat-page {
  position: fixed;
  inset: 0;
  height: 100dvh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background:
    radial-gradient(
      ellipse 70% 45% at 12% 4%,
      rgba(95, 127, 98, 0.1) 0%,
      transparent 62%
    ),
    linear-gradient(
      180deg,
      rgba(255, 255, 255, 0.42) 0%,
      rgba(243, 241, 234, 0.1) 28%,
      rgba(243, 241, 234, 0.92) 100%
    );
}

.chat-shell {
  flex: 1;
  min-height: 0;
  width: min(100%, 860px);
  margin: 0 auto;
  padding: 18px 16px 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  position: sticky;
  top: 0;
  z-index: 5;
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 6px 0 18px;
  background: linear-gradient(
    180deg,
    rgba(243, 241, 234, 0.98) 0%,
    rgba(243, 241, 234, 0.84) 72%,
    rgba(243, 241, 234, 0) 100%
  );
  backdrop-filter: blur(10px);
}

.chat-back {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 40px;
  border: 1px solid rgba(215, 219, 210, 0.9);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.76);
  color: #161715;
  font-size: 14px;
  font-weight: 700;
  padding: 0 14px;
  transition:
    transform 0.2s ease,
    border-color 0.2s ease,
    background-color 0.2s ease;
}

.chat-back:hover {
  transform: translateY(-1px);
  border-color: rgba(95, 127, 98, 0.35);
  background: rgba(255, 255, 255, 0.92);
}

.chat-back__icon {
  font-size: 16px;
  line-height: 1;
}

.chat-header__title {
  min-width: 0;
}

.chat-title {
  margin: 6px 0 0;
  font-family: "Noto Serif SC", "Source Han Serif SC", serif;
  font-size: clamp(1.9rem, 3vw, 2.8rem);
  line-height: 1.1;
  color: #161715;
}

.chat-stream {
  flex: 1;
  min-height: 0;
  display: grid;
  gap: 18px;
  padding-top: 8px;
  overflow-y: auto;
  overscroll-behavior: contain;
}

.chat-stream::after {
  content: "";
  display: block;
  height: 4px;
}

.message-row {
  display: flex;
  align-items: flex-end;
  gap: 12px;
}

.message-row-user {
  justify-content: flex-end;
}

.assistant-avatar {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  border-radius: 16px;
  border: 1px solid rgba(215, 219, 210, 0.9);
  background: rgba(255, 255, 255, 0.82);
  box-shadow: 0 10px 24px rgba(22, 23, 21, 0.06);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.assistant-avatar__image {
  width: 28px;
  height: 28px;
}

.message-bubble {
  max-width: min(100%, 680px);
  border-radius: 28px;
  padding: 16px 18px;
}

.message-bubble-intro {
  max-width: min(100%, 620px);
}

.message-bubble-assistant {
  border: 1px solid rgba(215, 219, 210, 0.92);
  background: rgba(253, 252, 248, 0.92);
  box-shadow: 0 16px 34px rgba(22, 23, 21, 0.06);
}

.message-bubble-user {
  background: linear-gradient(
    135deg,
    rgba(95, 127, 98, 0.96),
    rgba(70, 96, 75, 0.96)
  );
  color: #fff;
  box-shadow: 0 16px 32px rgba(95, 127, 98, 0.18);
}

.message-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.message-name {
  color: #38513a;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.message-chip {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  background: rgba(223, 233, 220, 0.7);
  color: #46604b;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 8px;
}

.message-content {
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 16px;
  line-height: 1.85;
}

.message-disclaimer {
  margin-top: 12px;
  font-size: 12px;
  line-height: 1.6;
}

.message-disclaimer-assistant {
  color: #667067;
}

.message-disclaimer-user {
  color: rgba(255, 255, 255, 0.82);
}

.typing-bubble {
  min-width: 180px;
}

.typing-dots {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 0;
}

.typing-dots span {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: rgba(95, 127, 98, 0.45);
  animation: typingPulse 1.2s ease-in-out infinite;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.15s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.3s;
}

.chat-footer {
  position: relative;
  left: auto;
  right: auto;
  bottom: auto;
  z-index: 12;
  width: min(calc(100% - 20px), 860px);
  margin: 0 auto;
  margin-top: -8px;
  padding: 0 0 16px;
  flex-shrink: 0;
}

.composer-card {
  border: 1px solid rgba(215, 219, 210, 0.95);
  border-radius: 28px;
  background: rgba(253, 252, 248, 0.96);
  box-shadow: 0 22px 48px rgba(22, 23, 21, 0.1);
  backdrop-filter: blur(16px);
  padding: 10px 12px;
}

.composer-main {
  display: flex;
  align-items: flex-end;
  gap: 10px;
}

.composer-input {
  min-height: 52px;
  max-height: 160px;
  width: 100%;
  resize: none;
  border: 0;
  background: transparent;
  color: #161715;
  font-size: 15px;
  line-height: 1.8;
  outline: none;
  padding: 10px 6px 6px;
}

.composer-input::placeholder {
  color: #9aa196;
}

.composer-send {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  border: 0;
  border-radius: 999px;
  background: #5f7f62;
  color: #fff;
  font-size: 24px;
  line-height: 1;
  box-shadow: 0 12px 26px rgba(95, 127, 98, 0.25);
  transition:
    transform 0.2s ease,
    opacity 0.2s ease,
    background-color 0.2s ease;
}

.composer-send:not(:disabled):hover {
  transform: translateY(-1px);
  background: #46604b;
}

.composer-send:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.chat-footer__disclaimer {
  text-align: center;
  margin-top: 10px;
  color: #667067;
  font-size: 12px;
  line-height: 1.5;
}

@keyframes typingPulse {
  0%,
  80%,
  100% {
    transform: translateY(0);
    opacity: 0.35;
  }

  40% {
    transform: translateY(-4px);
    opacity: 1;
  }
}

@media (max-width: 640px) {
  .chat-shell {
    padding: 14px 10px 0;
  }

  .chat-header {
    align-items: flex-start;
    padding-bottom: 14px;
  }

  .message-bubble,
  .message-bubble-intro {
    max-width: calc(100vw - 76px);
  }

  .chat-footer {
    width: 100%;
    padding: 0 10px;
    padding-bottom: max(10px, env(safe-area-inset-bottom));
    z-index: 1000;
  }

  .composer-card {
    border-radius: 24px;
    padding: 8px 10px;
  }

  .chat-back {
    padding: 0 12px;
  }
}
</style>
