<template>
  <div class="surface-card space-y-5">
    <div class="space-y-2">
      <div class="eyebrow">Birth profile</div>
      <h3 class="section-title">八字建档</h3>
    </div>

    <div class="grid gap-4 sm:grid-cols-2">
      <div class="grid gap-2">
        <label class="field-label">出生日期</label>
        <input class="field-input" :value="modelValue.birthDate" type="date" @input="update('birthDate', ($event.target as HTMLInputElement).value)" />
      </div>
      <div class="grid gap-2">
        <label class="field-label">出生时间</label>
        <input class="field-input" :value="modelValue.birthTime ?? ''" :disabled="modelValue.birthTimeUnknown" type="time" @input="update('birthTime', ($event.target as HTMLInputElement).value)" />
      </div>
      <div class="grid gap-2">
        <label class="field-label">性别</label>
        <select class="field-input" :value="modelValue.gender" @change="update('gender', ($event.target as HTMLSelectElement).value)">
          <option value="FEMALE">女</option>
          <option value="MALE">男</option>
        </select>
      </div>
      <div class="grid gap-2">
        <label class="field-label">历法</label>
        <select class="field-input" :value="modelValue.calendarType" @change="update('calendarType', ($event.target as HTMLSelectElement).value)">
          <option value="SOLAR">公历</option>
          <option value="LUNAR">农历</option>
        </select>
      </div>
      <div class="grid gap-2">
        <label class="field-label">出生地</label>
        <input class="field-input" :value="modelValue.birthPlace" placeholder="例如：杭州" @input="update('birthPlace', ($event.target as HTMLInputElement).value)" />
      </div>
      <div class="grid gap-2">
        <label class="field-label">时区</label>
        <input class="field-input" :value="modelValue.timezone" placeholder="Asia/Shanghai" @input="update('timezone', ($event.target as HTMLInputElement).value)" />
      </div>
    </div>

    <div class="flex items-center justify-between gap-3 rounded-2xl bg-cream px-4 py-3">
      <span class="text-sm font-semibold text-ink/85">未知时辰</span>
      <input class="h-5 w-5 accent-accent" :checked="modelValue.birthTimeUnknown" type="checkbox" @change="toggleUnknown(($event.target as HTMLInputElement).checked)" />
    </div>

    <p class="text-sm leading-6 text-muted">未知时辰可继续建档和查看日运/解读，但不可使用 AI 提问。</p>

    <div class="flex flex-wrap gap-3">
      <button class="btn-primary" @click="$emit('submit')">保存并生成解读</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { UserProfile } from '@/types'

const props = defineProps<{
  modelValue: UserProfile
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: UserProfile): void
  (e: 'submit'): void
}>()

function update<K extends keyof UserProfile>(key: K, value: UserProfile[K] | string) {
  emit('update:modelValue', {
    ...props.modelValue,
    [key]: value
  })
}

function toggleUnknown(value: boolean) {
  emit('update:modelValue', {
    ...props.modelValue,
    birthTimeUnknown: value,
    birthTime: value ? null : props.modelValue.birthTime ?? '09:00'
  })
}
</script>
