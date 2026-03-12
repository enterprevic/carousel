<template>
  <span
    class="w-6 h-6 rounded-[6px] flex items-center justify-center shrink-0"
    :style="{ background: bg, color: color }"
  >
    <slot />
  </span>
</template>

<script setup lang="ts">
defineProps<{ color: string; bg: string }>()
</script>
