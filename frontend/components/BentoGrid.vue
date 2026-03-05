<template>
  <div class="grid w-full grid-cols-3 gap-4" :class="className">
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{ className?: string }>()
</script>
