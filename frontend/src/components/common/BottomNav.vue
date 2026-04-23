<template>
  <nav class="fixed inset-x-0 bottom-0 z-10 flex justify-center pt-3">
    <div
      class="grid w-full max-w-3xl grid-cols-3 gap-3 rounded-t-[28px] rounded-b-none border border-line/70 bg-panel/90 p-3 shadow-soft backdrop-blur-md"
    >
      <RouterLink
        v-for="item in items"
        :key="item.to"
        :to="item.to"
        class="btn-ghost flex-col gap-1 px-3 text-center text-sm"
        active-class="!border-accent/30 !bg-accent !text-white"
      >
        <img
          :alt="`${item.label} 图标`"
          class="h-7 w-7 rounded-full border border-current/10 bg-white/70 p-1"
          :src="item.icon"
        />
        <span>{{ item.label }}</span>
      </RouterLink>
    </div>
  </nav>
</template>

<script setup lang="ts">
const items = [
  { label: '首页', to: '/daily', icon: '/panda-badge.svg' },
  { label: '成长档案', to: '/growth/archive', icon: '/panda-badge.svg' },
  { label: '我的', to: '/me', icon: '/panda-badge.svg' }
]
</script>
