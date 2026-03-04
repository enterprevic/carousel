<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="dismiss" />

        <!-- Modal -->
        <Transition
          enter-active-class="transition-all duration-300 ease-out"
          enter-from-class="opacity-0 scale-95 translate-y-4"
          enter-to-class="opacity-100 scale-100 translate-y-0"
        >
          <div v-if="visible"
            class="relative bg-white rounded-3xl shadow-[0_24px_80px_rgba(0,0,0,0.2)] w-full max-w-md overflow-hidden">

            <!-- Step content -->
            <div class="relative overflow-hidden">
              <div class="flex transition-transform duration-400 ease-out"
                :style="{ transform: `translateX(-${step * 100}%)` }">
                <!-- Step 1 -->
                <div class="w-full shrink-0 px-8 pt-10 pb-6 text-center">
                  <div class="w-20 h-20 bg-[#0071e3]/10 rounded-[24px] flex items-center justify-center mx-auto mb-6">
                    <svg class="w-10 h-10 text-[#0071e3]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                        d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <h2 class="text-[22px] font-bold text-[#1c1c1e] tracking-tight mb-3">Welcome to CarouselGen</h2>
                  <p class="text-[15px] text-[#3a3a3c] leading-relaxed">
                    Turn any article, video, or link into beautiful Instagram carousel slides — in seconds, powered by AI.
                  </p>
                </div>

                <!-- Step 2 -->
                <div class="w-full shrink-0 px-8 pt-10 pb-6 text-center">
                  <div class="w-20 h-20 bg-emerald-50 rounded-[24px] flex items-center justify-center mx-auto mb-6">
                    <svg class="w-10 h-10 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                        d="M4 6h16M4 10h16M4 14h10M4 18h6" />
                    </svg>
                  </div>
                  <h2 class="text-[22px] font-bold text-[#1c1c1e] tracking-tight mb-3">Create &amp; Generate</h2>
                  <p class="text-[15px] text-[#3a3a3c] leading-relaxed mb-5">
                    Pick your source — paste text, drop a video link, or add URLs. Choose the number of slides, language, and writing style.
                  </p>
                  <div class="space-y-2.5 text-left">
                    <div v-for="tip in step2Tips" :key="tip.label"
                      class="flex items-start gap-3 bg-[#f2f2f7] rounded-2xl px-4 py-3">
                      <span class="text-lg mt-0.5">{{ tip.icon }}</span>
                      <div>
                        <p class="text-[13px] font-semibold text-[#1c1c1e]">{{ tip.label }}</p>
                        <p class="text-[12px] text-[#3a3a3c] mt-0.5">{{ tip.desc }}</p>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Step 3 -->
                <div class="w-full shrink-0 px-8 pt-10 pb-6 text-center">
                  <div class="w-20 h-20 bg-purple-50 rounded-[24px] flex items-center justify-center mx-auto mb-6">
                    <svg class="w-10 h-10 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <h2 class="text-[22px] font-bold text-[#1c1c1e] tracking-tight mb-3">Design &amp; Export</h2>
                  <p class="text-[15px] text-[#3a3a3c] leading-relaxed mb-5">
                    Edit each slide's text, pick a template, set your background — even upload a custom photo per slide. Then export as a ZIP of 1080×1350 PNGs.
                  </p>
                  <div class="space-y-2.5 text-left">
                    <div v-for="tip in step3Tips" :key="tip.label"
                      class="flex items-start gap-3 bg-[#f2f2f7] rounded-2xl px-4 py-3">
                      <span class="text-lg mt-0.5">{{ tip.icon }}</span>
                      <div>
                        <p class="text-[13px] font-semibold text-[#1c1c1e]">{{ tip.label }}</p>
                        <p class="text-[12px] text-[#3a3a3c] mt-0.5">{{ tip.desc }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Dots -->
            <div class="flex justify-center gap-1.5 pb-1">
              <button v-for="i in 3" :key="i"
                class="rounded-full transition-all duration-200"
                :class="step === i - 1
                  ? 'w-5 h-2 bg-[#0071e3]'
                  : 'w-2 h-2 bg-[#d1d1d6] hover:bg-[#8e8e93]'"
                @click="step = i - 1" />
            </div>

            <!-- Actions -->
            <div class="px-8 pb-8 pt-4 flex gap-3">
              <button v-if="step > 0"
                class="btn-secondary flex-1"
                @click="step--">
                Back
              </button>
              <button v-if="step < 2"
                class="btn-primary flex-1"
                @click="step++">
                Next
              </button>
              <button v-else
                class="btn-primary flex-1"
                @click="dismiss">
                Get started →
              </button>
            </div>

            <!-- Close -->
            <button class="absolute top-4 right-4 w-8 h-8 flex items-center justify-center rounded-full
              text-[#8e8e93] hover:text-[#3a3a3c] hover:bg-black/5 transition-colors text-lg"
              @click="dismiss">
              ×
            </button>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
const STORAGE_KEY = "carouselgen_onboarded"

const visible = ref(false)
const step = ref(0)

const step2Tips = [
  { icon: "✍️", label: "From Text", desc: "Paste an article, post, or any draft text." },
  { icon: "🎬", label: "From Video", desc: "Add a YouTube or other video URL with optional notes." },
  { icon: "🔗", label: "From Links", desc: "Curate a list of URLs with bullet-point context." },
]

const step3Tips = [
  { icon: "🎨", label: "Per-slide design", desc: "Each slide can have its own background color or photo." },
  { icon: "📐", label: "3 templates", desc: "Classic, Bold, or Minimal — applied globally or per slide." },
  { icon: "📦", label: "Export as ZIP", desc: "Download all slides as 1080×1350 px PNG images." },
]

const dismiss = () => {
  visible.value = false
  if (typeof localStorage !== "undefined") {
    localStorage.setItem(STORAGE_KEY, "1")
  }
}

onMounted(() => {
  if (typeof localStorage !== "undefined" && !localStorage.getItem(STORAGE_KEY)) {
    visible.value = true
  }
})
</script>
