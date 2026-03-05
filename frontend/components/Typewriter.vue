<template>
  <span class="inline whitespace-pre-wrap tracking-tight" :class="className">
    <span>{{ displayText }}</span>
    <span
      v-if="showCursor"
      class="cursor"
      :class="[cursorClassName, hideCursorOnType && isTypingActive ? 'opacity-0' : '']"
    >{{ cursorChar }}</span>
  </span>
</template>

<script setup lang="ts">
interface Props {
  text: string | string[]
  speed?: number
  initialDelay?: number
  waitTime?: number
  deleteSpeed?: number
  loop?: boolean
  className?: string
  showCursor?: boolean
  hideCursorOnType?: boolean
  cursorChar?: string
  cursorClassName?: string
}

const props = withDefaults(defineProps<Props>(), {
  speed: 50,
  initialDelay: 0,
  waitTime: 2000,
  deleteSpeed: 30,
  loop: true,
  showCursor: true,
  hideCursorOnType: false,
  cursorChar: '|',
  cursorClassName: 'ml-0.5',
})

const displayText = ref('')
const currentIndex = ref(0)
const isDeleting = ref(false)
const currentTextIndex = ref(0)

const texts = computed(() => Array.isArray(props.text) ? props.text : [props.text])
const isTypingActive = computed(() =>
  currentIndex.value < texts.value[currentTextIndex.value].length || isDeleting.value
)

let timeout: ReturnType<typeof setTimeout> | null = null

const tick = () => {
  const currentText = texts.value[currentTextIndex.value]

  if (isDeleting.value) {
    if (displayText.value === '') {
      isDeleting.value = false
      if (currentTextIndex.value === texts.value.length - 1 && !props.loop) return
      currentTextIndex.value = (currentTextIndex.value + 1) % texts.value.length
      currentIndex.value = 0
      timeout = setTimeout(tick, props.waitTime)
    } else {
      displayText.value = displayText.value.slice(0, -1)
      timeout = setTimeout(tick, props.deleteSpeed)
    }
  } else {
    if (currentIndex.value < currentText.length) {
      displayText.value += currentText[currentIndex.value]
      currentIndex.value++
      timeout = setTimeout(tick, props.speed)
    } else if (texts.value.length > 1) {
      timeout = setTimeout(() => {
        isDeleting.value = true
        tick()
      }, props.waitTime)
    }
  }
}

onMounted(() => {
  timeout = setTimeout(tick, props.initialDelay)
})

onUnmounted(() => {
  if (timeout) clearTimeout(timeout)
})
</script>

<style scoped>
.cursor {
  animation: blink 0.85s step-start infinite;
}
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
</style>
