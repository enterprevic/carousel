<template>
  <button
    class="w-full flex items-center gap-4 px-3 py-3 transition-colors"
    :class="active ? 'bg-[#EEF0FF]' : 'hover:bg-[#F4F5F6]'"
    @click="$emit('click')"
  >
    <svg class="w-6 h-6 shrink-0" :class="active ? 'text-[#2B31B3]' : 'text-[#4E616B]'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="icon" />
    </svg>
    <span class="text-[16px] font-medium text-left" :class="active ? 'text-[#2B31B3]' : 'text-[#4E616B]'">{{ label }}</span>
  </button>
</template>

<script setup lang="ts">
defineProps<{ icon: string; label: string; active?: boolean }>()
defineEmits<{ click: [] }>()
</script>
