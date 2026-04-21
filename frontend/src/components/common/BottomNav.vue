<template>
  <nav class="fixed inset-x-0 bottom-0 z-10 flex justify-center px-4 pb-5 pt-3">
    <div class="grid w-full max-w-3xl grid-cols-3 gap-3 rounded-[28px] border border-line/70 bg-panel/90 p-3 shadow-soft backdrop-blur-md">
      <RouterLink
        v-for="item in items"
        :key="item.to"
        :to="item.to"
        class="btn-ghost px-3 text-center text-sm"
        active-class="!border-accent/30 !bg-accent !text-white"
      >
        {{ item.label }}
      </RouterLink>
    </div>
  </nav>
</template>

<script setup lang="ts">
const items = [
  { label: '首页', to: '/daily' },
  { label: '成长档案', to: '/growth/archive' },
  { label: '设置', to: '/settings/reminder' }
]
</script>
