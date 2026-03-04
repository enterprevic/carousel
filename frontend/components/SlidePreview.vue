<template>
  <div class="relative overflow-hidden rounded-2xl slide-aspect w-full" :style="containerStyle">
    <!-- Darkening overlay -->
    <div v-if="design.bg_image_url && design.darkening > 0"
      class="absolute inset-0 z-10" :style="{ background: `rgba(0,0,0,${design.darkening})` }" />

    <!-- Header -->
    <div v-if="design.show_header && design.header_text"
      class="absolute top-0 left-0 right-0 z-20 px-4 pt-3"
      :style="{ textAlign: design.align_h }">
      <span class="text-[9px] font-medium opacity-60" :style="{ color: tpl.body }">
        {{ design.header_text }}
      </span>
    </div>

    <!-- Slide counter -->
    <div v-if="showCounter && totalSlides"
      class="absolute top-3 right-3 z-20 text-[9px] font-medium opacity-50"
      :style="{ color: tpl.body }">
      {{ slideNumber }}/{{ totalSlides }}
    </div>

    <!-- Content -->
    <div class="absolute inset-0 z-10 flex flex-col" :style="contentWrapStyle">
      <div class="w-full" :style="{ textAlign: design.align_h }">
        <div class="font-bold leading-tight mb-2"
          :style="{ color: tpl.title, fontSize: titleSize }">
          {{ slide?.title || 'Slide Title' }}
        </div>
        <div class="leading-relaxed"
          :style="{ color: tpl.body, fontSize: bodySize }">
          {{ slide?.body || 'Slide body content.' }}
        </div>
        <div v-if="slide?.footer_cta" class="font-semibold mt-2"
          :style="{ color: tpl.accent, fontSize: bodySize }">
          {{ slide.footer_cta }}
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div v-if="design.show_footer && design.footer_text"
      class="absolute bottom-0 left-0 right-0 z-20 px-4 pb-3"
      :style="{ textAlign: design.align_h }">
      <span class="text-[9px] font-medium opacity-60" :style="{ color: tpl.body }">
        {{ design.footer_text }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Slide, CarouselDesign } from "~/types"

const props = defineProps<{
  slide?: Slide | null
  design: CarouselDesign
  slideNumber?: number
  totalSlides?: number
  showCounter?: boolean
  small?: boolean
}>()

const TEMPLATES = {
  classic: { bg: "#ffffff", title: "#1a1a1a", body: "#444444", accent: "#2563eb", font: "Georgia, serif" },
  bold:    { bg: "#0f0f0f", title: "#ffffff", body: "#d0d0d0", accent: "#f59e0b", font: "'Arial Black', sans-serif" },
  minimal: { bg: "#f8f8f6", title: "#222222", body: "#555555", accent: "#10b981", font: "'Helvetica Neue', Helvetica, sans-serif" },
} as const

const tpl = computed(() => TEMPLATES[props.design.template as keyof typeof TEMPLATES] || TEMPLATES.classic)

const containerStyle = computed(() => {
  const d = props.design
  const style: Record<string, string> = {
    backgroundColor: d.bg_color || tpl.value.bg,
    fontFamily: tpl.value.font,
  }
  if (d.bg_image_url) {
    style.backgroundImage = `url('${d.bg_image_url}')`
    style.backgroundSize = "cover"
    style.backgroundPosition = "center"
  }
  return style
})

const justifyMap: Record<string, string> = { left: "flex-start", center: "center", right: "flex-end" }
const alignMap: Record<string, string>   = { top: "flex-start", center: "center", bottom: "flex-end" }

const contentWrapStyle = computed(() => ({
  padding: props.small ? "8px" : `${props.design.padding}px`,
  justifyContent: alignMap[props.design.align_v] || "center",
  alignItems: justifyMap[props.design.align_h] || "center",
}))

const titleSize = computed(() => props.small ? "0.55rem" : "1.05rem")
const bodySize  = computed(() => props.small ? "0.45rem" : "0.8rem")
</script>
