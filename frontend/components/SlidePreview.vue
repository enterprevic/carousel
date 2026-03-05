<template>
  <div class="relative overflow-hidden rounded-2xl w-full" :style="[containerStyle, aspectStyle]">
    <!-- Darkening overlay -->
    <div v-if="effectiveBgImage && effectiveDarkening > 0"
      class="absolute inset-0 z-10" :style="{ background: `rgba(0,0,0,${effectiveDarkening})` }" />

    <!-- Pattern overlay -->
    <div v-if="patternStyle.backgroundImage"
      class="absolute inset-0 z-10 pointer-events-none"
      :style="patternStyle" />

    <!-- Header -->
    <div v-if="effectiveShowHeader && effectiveHeaderText"
      class="absolute top-0 left-0 right-0 z-20 px-4 pt-3"
      :style="{ textAlign: effectiveAlignH }">
      <span class="text-[9px] font-medium opacity-60" :style="{ color: tpl.body }">
        {{ effectiveHeaderText }}
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
      <div class="w-full" :style="{ textAlign: effectiveAlignH }">
        <div class="font-bold leading-tight mb-2"
          data-field="title"
          :style="titleStyle"
          v-html="renderInlineMarkup(slide?.title || 'Slide Title', effectiveAccent)" />
        <div class="leading-relaxed"
          data-field="body"
          :style="{ color: tpl.body, fontSize: bodySize, fontFamily: bodyFont }"
          v-html="renderInlineMarkup(slide?.body || 'Slide body content.', effectiveAccent)" />
        <div v-if="slide?.footer_cta" class="font-semibold mt-2"
          :style="{ color: effectiveAccent, fontSize: bodySize }">
          {{ slide.footer_cta }}
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div v-if="effectiveShowFooter && effectiveFooterText"
      class="absolute bottom-0 left-0 right-0 z-20 px-4 pb-3"
      :style="{ textAlign: effectiveAlignH }">
      <span class="text-[9px] font-medium opacity-60" :style="{ color: tpl.body }">
        {{ effectiveFooterText }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Slide, CarouselDesign } from "~/types"
import { FONT_FAMILIES } from "~/types"

const props = defineProps<{
  slide?: Slide | null
  design: CarouselDesign
  slideNumber?: number
  totalSlides?: number
  showCounter?: boolean
}>()

const TEMPLATES = {
  bright:   { bg: "#fff7ed", title: "#1c1917", body: "#44403c", accent: "#f97316", font: "'Roboto Condensed', Arial, sans-serif" },
  classic:  { bg: "#ffffff", title: "#1a1a1a", body: "#444444", accent: "#2563eb", font: "'Times New Roman', Times, serif" },
  comic:    { bg: "#fef08a", title: "#18181b", body: "#3f3f46", accent: "#7c3aed", font: "'Fredoka', 'Arial Rounded MT Bold', sans-serif" },
  elegant:  { bg: "#0f172a", title: "#f8fafc", body: "#cbd5e1", accent: "#d4af37", font: "'Times New Roman', Times, serif" },
  minimal:  { bg: "#f8f8f6", title: "#222222", body: "#555555", accent: "#10b981", font: "'Jost', 'Helvetica Neue', sans-serif" },
  notes:    { bg: "#fefce8", title: "#422006", body: "#78350f", accent: "#d97706", font: "'Caveat', cursive" },
  powerful: { bg: "#09090b", title: "#fafafa", body: "#a1a1aa", accent: "#ef4444", font: "'Space Mono', 'Courier New', monospace" },
} as const

// Merge per-slide overrides over carousel design
const ov = computed(() => props.slide?.overrides ?? {})

// Template: slide override > carousel design
const effectiveTemplate = computed(() => (ov.value.template ?? null) || props.design.template)
const tpl = computed(() => TEMPLATES[effectiveTemplate.value as keyof typeof TEMPLATES] || TEMPLATES.classic)

const effectiveBgColor        = computed(() => (ov.value.bg_color ?? null) || props.design.bg_color || tpl.value.bg)
const effectiveBgImage        = computed(() => (ov.value.bg_image_url ?? null) || props.design.bg_image_url || null)
const effectiveDarkening      = computed(() => ov.value.darkening != null ? ov.value.darkening : props.design.darkening)
const effectiveAccent         = computed(() => ov.value.accent_color ?? props.design.accent_color ?? tpl.value.accent)
const effectiveTitleHighlight = computed(() => "title_highlight" in ov.value ? (ov.value.title_highlight ?? null) : (props.design.title_highlight ?? null))
const effectiveAlignH         = computed(() => ov.value.align_h ?? props.design.align_h)
const effectiveAlignV         = computed(() => ov.value.align_v ?? props.design.align_v)
const effectivePadding        = computed(() => ov.value.padding != null ? ov.value.padding : props.design.padding)
const effectiveShowHeader     = computed(() => ov.value.show_header != null ? ov.value.show_header : props.design.show_header)
const effectiveHeaderText     = computed(() => ov.value.header_text != null ? ov.value.header_text : props.design.header_text)
const effectiveShowFooter     = computed(() => ov.value.show_footer != null ? ov.value.show_footer : props.design.show_footer)
const effectiveFooterText     = computed(() => ov.value.footer_text != null ? ov.value.footer_text : props.design.footer_text)

const titleFont = computed(() => {
  const key = props.design.title_font ?? "system"
  return key === "system" ? tpl.value.font : (FONT_FAMILIES[key] ?? tpl.value.font)
})
const bodyFont = computed(() => {
  const key = props.design.body_font ?? "system"
  return key === "system" ? tpl.value.font : (FONT_FAMILIES[key] ?? tpl.value.font)
})

const ASPECT_RATIOS: Record<string, string> = { "4:5": "4/5", "9:16": "9/16", "1:1": "1/1" }

const aspectStyle = computed(() => ({
  aspectRatio: ASPECT_RATIOS[props.design.aspect_ratio ?? "4:5"] ?? "4/5",
}))

const containerStyle = computed(() => {
  const style: Record<string, string> = {
    backgroundColor: effectiveBgColor.value,
    fontFamily: tpl.value.font,
  }
  if (effectiveBgImage.value) {
    style.backgroundImage = `url('${effectiveBgImage.value}')`
    style.backgroundSize = "cover"
    style.backgroundPosition = "center"
  }
  return style
})

// Pattern SVG backgrounds
function buildPatternSvg(pattern: string, color: string, opacity: number): string {
  const c = encodeURIComponent(color)
  const o = opacity
  switch (pattern) {
    case "dots1":
      return `url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='2' cy='2' r='1.5' fill='${c}' fill-opacity='${o}'/%3E%3C/svg%3E")`
    case "dots2":
      return `url("data:image/svg+xml,%3Csvg width='16' height='16' viewBox='0 0 16 16' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='2' cy='2' r='2' fill='${c}' fill-opacity='${o}'/%3E%3C/svg%3E")`
    case "dots3":
      return `url("data:image/svg+xml,%3Csvg width='30' height='30' viewBox='0 0 30 30' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='3' cy='3' r='3' fill='${c}' fill-opacity='${o}'/%3E%3C/svg%3E")`
    case "grid":
      return `url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M24 0H0v1h24V0zm0 23H0v1h24v-1zM1 0v24h1V0H1zm22 0v24h1V0h-1z' fill='${c}' fill-opacity='${o}'/%3E%3C/svg%3E")`
    case "lines":
      return `url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'%3E%3Cline x1='0' y1='10' x2='20' y2='10' stroke='${c}' stroke-opacity='${o}' stroke-width='1'/%3E%3C/svg%3E")`
    case "cells":
      return `url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 20h40M20 0v40' stroke='${c}' stroke-opacity='${o}' stroke-width='0.8'/%3E%3Cpath d='M0 0h40v40H0z' fill='none'/%3E%3C/svg%3E")`
    case "blobs":
      return `url("data:image/svg+xml,%3Csvg width='120' height='120' viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M28 14c7 -3 16 1 18 8s-3 16 -10 19s-16 -1 -18 -9s3 -15 10 -18z' fill='${c}' fill-opacity='${o}'/%3E%3Cpath d='M85 52c8 2 14 10 12 18s-11 13 -19 11s-13 -11 -11 -19s10 -12 18 -10z' fill='${c}' fill-opacity='${o}'/%3E%3Cpath d='M22 82c6 -4 15 -2 19 5s1 16 -6 20s-15 1 -19 -6s0 -15 6 -19z' fill='${c}' fill-opacity='${o}'/%3E%3Cpath d='M95 10c5 3 7 10 4 16s-10 9 -16 6s-7 -10 -4 -16s10 -9 16 -6z' fill='${c}' fill-opacity='${o}'/%3E%3Cpath d='M58 90c6 -2 12 3 13 9s-3 12 -9 13s-12 -3 -13 -10s3 -10 9 -12z' fill='${c}' fill-opacity='${o}'/%3E%3C/svg%3E")`
    default:
      return ""
  }
}

const patternStyle = computed(() => {
  const p = ov.value.pattern ?? props.design.pattern ?? "none"
  if (p === "none") return {}
  const color   = ov.value.pattern_color   ?? props.design.pattern_color   ?? "#000000"
  const opacity = ov.value.pattern_opacity ?? props.design.pattern_opacity ?? 0.06
  return {
    backgroundImage: buildPatternSvg(p, color, opacity),
    backgroundRepeat: "repeat",
  }
})

const titleStyle = computed(() => {
  const s: Record<string, string> = {
    color: tpl.value.title,
    fontSize: titleSize.value,
    fontFamily: titleFont.value,
  }
  if (effectiveTitleHighlight.value) {
    s.backgroundColor = effectiveTitleHighlight.value
    s.padding = "0 6px"
    s.borderRadius = "3px"
    s.display = "inline"
    s.boxDecorationBreak = "clone"
  }
  return s
})

const justifyMap: Record<string, string> = { left: "flex-start", center: "center", right: "flex-end" }
const alignMap: Record<string, string>   = { top: "flex-start", center: "center", bottom: "flex-end" }

const contentWrapStyle = computed(() => ({
  padding: `${effectivePadding.value}px`,
  justifyContent: alignMap[effectiveAlignV.value] || "center",
  alignItems: justifyMap[effectiveAlignH.value] || "center",
}))

const titleSize = computed(() => "1.05rem")
const bodySize  = computed(() => "0.8rem")

function renderInlineMarkup(text: string, accentColor: string): string {
  if (!text) return ''
  const escaped = text
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  return escaped
    .replace(/==(#[0-9a-fA-F]{3,8})\|(#[0-9a-fA-F]{3,8})\|(.+?)==/g, (_, bg, fg, m) =>
      `<span style="background-color:${bg};color:${fg};border-radius:3px;padding:0 3px;box-decoration-break:clone;-webkit-box-decoration-break:clone;">${m}</span>`)
    .replace(/==(.+?)==/g, (_, m) =>
      `<span style="background-color:${accentColor};color:#fff;border-radius:3px;padding:0 3px;box-decoration-break:clone;-webkit-box-decoration-break:clone;">${m}</span>`)
    .replace(/\*\*(.+?)\*\*/g, (_, m) => `<span style="font-weight:700">${m}</span>`)
}
</script>
