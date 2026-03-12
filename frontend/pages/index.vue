<template>
  <div class="text-[#1c1c1e] overflow-x-hidden bg-white">
    <!-- ── NAV ── -->
    <nav class="fixed top-0 inset-x-0 z-50 px-4 py-3">
      <div
        class="max-w-5xl mx-auto bg-white border border-black/[0.08] rounded-2xl shadow-sm px-4 h-12 flex items-center justify-between"
      >
        <div class="flex items-center gap-2.5">
          <img src="/visible.png" alt="trendsee" class="w-7 h-7 object-contain shrink-0" />
          <span class="font-semibold text-[#1B1A25] tracking-tight" style="font-family:'Unbounded',sans-serif;font-size:15px;line-height:1.2;">trendsee</span>
        </div>
        <div class="flex items-center gap-2">
          <NuxtLink
            to="/login"
            class="text-sm font-medium text-[#6e6e73] hover:text-[#1c1c1e] transition-colors hidden sm:block px-3 py-1.5"
          >
            Sign in
          </NuxtLink>
          <NuxtLink
            to="/register"
            class="text-sm font-semibold bg-[#1c1c1e] text-white px-4 py-1.5 rounded-xl hover:bg-[#3a3a3c] transition-colors"
          >
            Get started free
          </NuxtLink>
        </div>
      </div>
    </nav>

    <!-- ── HERO ── -->
    <section class="relative bg-white pt-20 overflow-hidden">
      <!-- Radial glow -->
      <div
        class="absolute top-0 left-1/2 -translate-x-1/2 w-[900px] h-[600px] rounded-full bg-[#0071e3]/10 blur-[120px] pointer-events-none"
        style="will-change:transform;transform:translateZ(0)"
      />
      <div
        class="absolute top-40 left-1/4 w-[400px] h-[400px] rounded-full bg-[#5856d6]/8 blur-[100px] pointer-events-none"
        style="will-change:transform;transform:translateZ(0)"
      />
      <div
        class="absolute top-20 right-1/4 w-[300px] h-[300px] rounded-full bg-[#0071e3]/6 blur-[80px] pointer-events-none"
        style="will-change:transform;transform:translateZ(0)"
      />

      <div
        class="relative max-w-4xl mx-auto px-5 sm:px-8 pt-16 sm:pt-20 pb-24 sm:pb-32 text-center"
      >
        <h1
          class="text-[36px] sm:text-[60px] lg:text-[72px] font-bold tracking-[-0.03em] leading-[1.06] text-[#1c1c1e] mb-6"
        >
          Turn any content<br />
          into&nbsp;<span class="text-[#0071e3]"
            ><Typewriter
              :text="[
                'carousels.',
                'slides.',
                'LinkedIn posts.',
                'viral content.',
              ]"
              :speed="60"
              :wait-time="2000"
              :delete-speed="35"
              cursor-char="_"
              cursor-class-name="ml-0.5"
          /></span>
        </h1>

        <p
          class="text-[15px] sm:text-[20px] text-[#6e6e73] leading-relaxed max-w-lg mx-auto mb-10 sm:mb-12 font-normal"
        >
          Paste text, a YouTube link, or a URL. AI writes the slides. You style
          and export in one click.
        </p>

        <div
          class="flex flex-col sm:flex-row items-center justify-center gap-3 mb-10"
        >
          <NuxtLink
            to="/register"
            class="bg-[#0071e3] hover:bg-[#0077ed] active:scale-[0.97] text-white font-semibold text-[15px] px-8 py-3.5 rounded-xl transition-all shadow-xl shadow-[#0071e3]/20 w-full sm:w-auto justify-center inline-flex items-center"
          >
            Start for free
            <svg
              class="w-4 h-4 ml-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 7l5 5m0 0l-5 5m5-5H6"
              />
            </svg>
          </NuxtLink>
          <NuxtLink
            to="/login"
            class="bg-[#f5f5f7] hover:bg-[#ebebeb] border border-black/[0.06] text-[#1c1c1e] font-semibold text-[15px] px-8 py-3.5 rounded-xl transition-all w-full sm:w-auto justify-center inline-flex items-center"
          >
            Sign in
          </NuxtLink>
        </div>

        <p class="text-[12px] text-[#aeaeb2] tracking-wide">
          Free · No credit card · No design skills required
        </p>

        <!-- Floating slide mock-ups -->
        <div
          class="mt-16 sm:mt-20 relative h-[260px] sm:h-[400px] select-none pointer-events-none"
        >
          <!-- Centre card -->
          <div
            class="absolute left-1/2 -translate-x-1/2 bottom-0 w-[150px] sm:w-[220px] z-20"
          >
            <div
              class="slide-mock bg-gradient-to-br from-[#0071e3] to-[#5856d6] rounded-2xl shadow-2xl shadow-[#0071e3]/25 p-4 sm:p-5 flex flex-col justify-between"
              style="aspect-ratio: 4/5"
            >
              <div>
                <div class="w-16 h-1.5 bg-white/40 rounded-full mb-3" />
                <div class="w-full h-3 bg-white rounded-lg mb-2 opacity-90" />
                <div class="w-4/5 h-3 bg-white rounded-lg mb-5 opacity-90" />
                <div class="w-full h-2 bg-white/50 rounded-full mb-1.5" />
                <div class="w-full h-2 bg-white/50 rounded-full mb-1.5" />
                <div class="w-3/4 h-2 bg-white/50 rounded-full" />
              </div>
              <div class="w-20 h-2 bg-white/30 rounded-full" />
            </div>
          </div>
          <!-- Left card -->
          <div
            class="absolute left-1/2 -translate-x-[calc(50%+90px)] sm:-translate-x-[calc(50%+140px)] bottom-8 w-[120px] sm:w-[185px] z-10 rotate-[-8deg]"
          >
            <div
              class="slide-mock bg-white border border-black/[0.08] rounded-2xl shadow-xl p-3 sm:p-4 flex flex-col justify-between"
              style="aspect-ratio: 4/5"
            >
              <div>
                <div class="w-12 h-1.5 bg-[#aeaeb2]/50 rounded-full mb-3" />
                <div class="w-full h-2.5 bg-[#1c1c1e]/70 rounded-lg mb-2" />
                <div class="w-3/4 h-2.5 bg-[#1c1c1e]/70 rounded-lg mb-4" />
                <div class="w-full h-1.5 bg-[#aeaeb2]/40 rounded-full mb-1.5" />
                <div class="w-5/6 h-1.5 bg-[#aeaeb2]/40 rounded-full" />
              </div>
              <div class="w-16 h-1.5 bg-[#aeaeb2]/30 rounded-full" />
            </div>
          </div>
          <!-- Right card -->
          <div
            class="absolute left-1/2 translate-x-[calc(-50%+90px)] sm:translate-x-[calc(-50%+140px)] bottom-8 w-[120px] sm:w-[185px] z-10 rotate-[8deg]"
          >
            <div
              class="slide-mock bg-gradient-to-br from-[#ff9500] to-[#ff6b00] rounded-2xl shadow-xl p-3 sm:p-4 flex flex-col justify-between"
              style="aspect-ratio: 4/5"
            >
              <div>
                <div class="w-12 h-1.5 bg-white/40 rounded-full mb-3" />
                <div class="w-full h-2.5 bg-white/90 rounded-lg mb-2" />
                <div class="w-4/5 h-2.5 bg-white/90 rounded-lg mb-4" />
                <div class="w-full h-1.5 bg-white/40 rounded-full mb-1.5" />
                <div class="w-2/3 h-1.5 bg-white/40 rounded-full" />
              </div>
              <div class="w-16 h-1.5 bg-white/30 rounded-full" />
            </div>
          </div>
          <!-- Far left -->
          <div
            class="hidden sm:block absolute left-1/2 -translate-x-[calc(50%+280px)] bottom-16 w-[140px] z-0 rotate-[-14deg] opacity-60"
          >
            <div
              class="slide-mock bg-gradient-to-br from-[#34c759] to-[#248a3d] rounded-2xl shadow-lg p-4 flex flex-col justify-between"
              style="aspect-ratio: 4/5"
            >
              <div>
                <div class="w-10 h-1.5 bg-white/40 rounded-full mb-2" />
                <div class="w-full h-2 bg-white/80 rounded-lg mb-2" />
                <div class="w-3/4 h-2 bg-white/80 rounded-lg mb-3" />
                <div class="w-full h-1.5 bg-white/30 rounded-full mb-1" />
                <div class="w-5/6 h-1.5 bg-white/30 rounded-full" />
              </div>
            </div>
          </div>
          <!-- Far right -->
          <div
            class="hidden sm:block absolute left-1/2 translate-x-[calc(-50%+280px)] bottom-16 w-[140px] z-0 rotate-[14deg] opacity-60"
          >
            <div
              class="slide-mock bg-gradient-to-br from-[#ff3b30] to-[#c0392b] rounded-2xl shadow-lg p-4 flex flex-col justify-between"
              style="aspect-ratio: 4/5"
            >
              <div>
                <div class="w-10 h-1.5 bg-white/40 rounded-full mb-2" />
                <div class="w-full h-2 bg-white/90 rounded-lg mb-2" />
                <div class="w-2/3 h-2 bg-white/90 rounded-lg mb-3" />
                <div class="w-full h-1.5 bg-white/30 rounded-full mb-1" />
                <div class="w-4/5 h-1.5 bg-white/30 rounded-full" />
              </div>
            </div>
          </div>
          <!-- Ground fade -->
          <div
            class="absolute bottom-0 inset-x-0 h-24 bg-gradient-to-t from-white to-transparent"
          />
        </div>
      </div>
    </section>

    <!-- ── STATS BAR ── -->
    <section class="bg-[#f5f5f7] border-y border-[#e5e5ea] py-8 px-5 sm:px-8">
      <div class="max-w-4xl mx-auto grid grid-cols-3 gap-6 text-center">
        <div v-for="stat in stats" :key="stat.label">
          <p
            class="text-[28px] sm:text-[36px] font-bold text-[#1c1c1e] tracking-tight"
          >
            {{ stat.value }}
          </p>
          <p class="text-[12px] text-[#8e8e93] mt-1 tracking-wide">
            {{ stat.label }}
          </p>
        </div>
      </div>
    </section>

    <!-- ── HOW IT WORKS ── -->
    <section class="bg-[#f5f5f7] py-24 px-5 sm:px-8">
      <div class="max-w-5xl mx-auto">
        <div class="text-center mb-14">
          <p class="text-[#0071e3] text-[11px] font-bold uppercase tracking-[0.2em] mb-3">
            How it works
          </p>
          <h2 class="text-[28px] sm:text-[40px] font-bold tracking-tight text-[#1c1c1e]">
            From idea to carousel in minutes
          </h2>
        </div>

        <!-- 2×2 bento grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div
            v-for="(step, i) in steps"
            :key="i"
            class="group relative flex flex-col overflow-hidden rounded-2xl bg-white border border-black/[0.06] shadow-[0_0_0_1px_rgba(0,0,0,.03),0_2px_4px_rgba(0,0,0,.05),0_12px_24px_rgba(0,0,0,.05)] p-7 transition-shadow duration-300 hover:shadow-[0_0_0_1px_rgba(0,0,0,.06),0_8px_24px_rgba(0,0,0,.09),0_24px_48px_rgba(0,0,0,.10)]"
          >
            <!-- Top: step number + icon -->
            <div class="flex items-start justify-between mb-6">
              <!-- Icon -->
              <div
                class="w-12 h-12 rounded-2xl flex items-center justify-center transition-transform duration-300 group-hover:scale-105"
                :style="{ background: step.color + '14', border: `1px solid ${step.color}28` }"
              >
                <svg
                  class="w-5.5 h-5.5"
                  :style="{ color: step.color }"
                  width="22" height="22"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" :d="step.icon" />
                </svg>
              </div>
              <!-- Step number -->
              <span
                class="text-[64px] font-black leading-none tracking-tighter select-none transition-transform duration-300 group-hover:-translate-y-1"
                :style="{ color: step.color + '18' }"
              >{{ i + 1 }}</span>
            </div>

            <!-- Content -->
            <div class="mt-auto">
              <h3 class="font-bold text-[18px] text-[#1c1c1e] tracking-tight mb-2">
                {{ step.title }}
              </h3>
              <p class="text-[14px] text-[#6e6e73] leading-relaxed mb-4">
                {{ step.desc }}
              </p>
              <!-- Tags -->
              <div class="flex flex-wrap gap-1.5">
                <span
                  v-for="tag in step.tags"
                  :key="tag"
                  class="text-[11px] font-semibold px-2.5 py-1 rounded-full"
                  :style="{ color: step.color, background: step.color + '12', border: `1px solid ${step.color}25` }"
                >{{ tag }}</span>
              </div>
            </div>

            <!-- Accent strip at bottom -->
            <div
              class="absolute bottom-0 inset-x-0 h-0.5 rounded-b-2xl transition-all duration-300 opacity-0 group-hover:opacity-100"
              :style="{ background: `linear-gradient(90deg, transparent, ${step.color}60, transparent)` }"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- ── FEATURES (BENTO) ── -->
    <section class="bg-[#f5f5f7] py-24 px-5 sm:px-8">
      <div class="max-w-5xl mx-auto">
        <div class="text-center mb-16">
          <p
            class="text-[#0071e3] text-[11px] font-bold uppercase tracking-[0.2em] mb-3"
          >
            Features
          </p>
          <h2
            class="text-[28px] sm:text-[40px] font-bold tracking-tight text-[#1c1c1e]"
          >
            Everything you need to grow
          </h2>
        </div>

        <!-- Bento grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <!-- Large card: AI Generation (spans 2 rows on lg) -->
          <BentoCard
            name="AI generation"
            description="State-of-the-art LLM turns your raw content into punchy, scroll-stopping slide copy — in seconds."
            href="/register"
            cta="Try it free"
            class-name="sm:col-span-2 lg:col-span-1 lg:row-span-2"
            style="min-height: 36rem"
          >
            <template #background>
              <div
                class="absolute inset-0 bg-gradient-to-b from-[#0071e3]/5 to-transparent"
              />
              <div class="absolute top-6 left-6 right-6">
                <div class="space-y-2.5">
                  <div
                    class="bg-[#f2f2f7] rounded-2xl rounded-tl-sm px-3.5 py-2.5 text-[12px] text-[#3a3a3c] max-w-[80%] leading-relaxed"
                  >
                    Paste your blog post here…
                  </div>
                  <div
                    class="bg-[#0071e3] rounded-2xl rounded-tr-sm px-3.5 py-2.5 text-[12px] text-white max-w-[85%] ml-auto leading-relaxed"
                  >
                    ✦ Generating 8 slides…
                  </div>
                  <div
                    class="bg-[#f2f2f7] rounded-2xl rounded-tl-sm px-3.5 py-2.5 text-[12px] text-[#3a3a3c] max-w-[90%] leading-relaxed"
                  >
                    <span class="font-semibold">Slide 1:</span> "The one habit
                    that changed everything"
                  </div>
                  <div
                    class="bg-[#f2f2f7] rounded-2xl rounded-tl-sm px-3.5 py-2.5 text-[12px] text-[#3a3a3c] max-w-[75%] leading-relaxed opacity-60"
                  >
                    <span class="font-semibold">Slide 2:</span> "Why most people
                    fail at…"
                  </div>
                </div>
              </div>
            </template>
            <template #icon>
              <svg
                class="w-full h-full text-[#0071e3]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                />
              </svg>
            </template>
          </BentoCard>

          <!-- 7 Templates (wide, col 2-3) -->
          <BentoCard
            name="7 professional templates"
            description="Minimal, bold, elegant, comic and more — each with curated fonts and colour pairings."
            href="/register"
            cta="See templates"
            class-name="sm:col-span-2 lg:col-span-2"
          >
            <template #background>
              <div
                class="absolute top-5 left-6 right-6 flex gap-2.5 overflow-hidden"
              >
                <div
                  v-for="tmpl in templateCards.slice(0, 5)"
                  :key="tmpl.name"
                  class="shrink-0 w-[70px] rounded-xl overflow-hidden border border-black/[0.06] shadow-sm"
                  style="aspect-ratio: 4/5"
                  :style="{ background: tmpl.bg }"
                >
                  <div
                    class="h-full p-2 flex flex-col gap-1"
                    :style="{ color: tmpl.text }"
                  >
                    <div
                      class="w-5 h-0.5 rounded opacity-50"
                      :style="{ background: tmpl.accent }"
                    />
                    <div
                      class="w-full h-1.5 rounded opacity-70"
                      :style="{ background: tmpl.text }"
                    />
                    <div
                      class="w-4/5 h-1.5 rounded opacity-70"
                      :style="{ background: tmpl.text }"
                    />
                    <div
                      class="w-full h-1 rounded opacity-30 mt-1"
                      :style="{ background: tmpl.text }"
                    />
                    <div
                      class="w-full h-1 rounded opacity-30"
                      :style="{ background: tmpl.text }"
                    />
                  </div>
                </div>
              </div>
            </template>
            <template #icon>
              <svg
                class="w-full h-full text-[#5856d6]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"
                />
              </svg>
            </template>
          </BentoCard>

          <!-- Per-slide overrides -->
          <BentoCard
            name="Per-slide overrides"
            description="Customise background, accent, layout and fonts on any individual slide."
            href="/register"
            cta="Learn more"
            class-name=""
          >
            <template #background>
              <div class="absolute top-5 left-6 right-6 flex flex-col gap-2">
                <div class="flex items-center gap-2">
                  <div class="w-4 h-4 rounded-full bg-[#0071e3]" />
                  <div
                    class="h-2 flex-1 bg-[#e5e5ea] rounded-full overflow-hidden"
                  >
                    <div class="h-full w-3/4 bg-[#0071e3]/40 rounded-full" />
                  </div>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-4 h-4 rounded-full bg-[#ff9500]" />
                  <div
                    class="h-2 flex-1 bg-[#e5e5ea] rounded-full overflow-hidden"
                  >
                    <div class="h-full w-1/2 bg-[#ff9500]/40 rounded-full" />
                  </div>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-4 h-4 rounded-full bg-[#34c759]" />
                  <div
                    class="h-2 flex-1 bg-[#e5e5ea] rounded-full overflow-hidden"
                  >
                    <div class="h-full w-5/6 bg-[#34c759]/40 rounded-full" />
                  </div>
                </div>
              </div>
            </template>
            <template #icon>
              <svg
                class="w-full h-full text-[#ff9500]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
                />
              </svg>
            </template>
          </BentoCard>

          <!-- ZIP Export -->
          <BentoCard
            name="One-click ZIP export"
            description="High-res PNGs for all slides, packaged and ready to post instantly."
            href="/register"
            cta="Try exporting"
            class-name=""
          >
            <template #background>
              <div class="absolute top-5 left-1/2 -translate-x-1/2">
                <div class="relative w-16 h-20">
                  <div
                    class="absolute inset-0 bg-[#34c759]/10 border border-[#34c759]/20 rounded-xl flex items-center justify-center"
                  >
                    <svg
                      class="w-7 h-7 text-[#34c759]"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="1.75"
                        d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                      />
                    </svg>
                  </div>
                  <div
                    class="absolute -bottom-1 -right-2 text-[10px] font-bold bg-[#34c759] text-white px-1.5 py-0.5 rounded-md"
                  >
                    .ZIP
                  </div>
                </div>
              </div>
            </template>
            <template #icon>
              <svg
                class="w-full h-full text-[#34c759]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                />
              </svg>
            </template>
          </BentoCard>
        </div>
      </div>
    </section>

    <!-- ── TEMPLATE SHOWCASE ── -->
    <section class="bg-[#f2f2f7] py-24 px-5 sm:px-8">
      <div class="max-w-5xl mx-auto">
        <div class="text-center mb-16">
          <p
            class="text-[#0071e3] text-[11px] font-bold uppercase tracking-[0.2em] mb-3"
          >
            Templates
          </p>
          <h2
            class="text-[28px] sm:text-[40px] font-bold tracking-tight text-[#1c1c1e]"
          >
            7 professional styles
          </h2>
          <p class="text-[#8e8e93] mt-3 max-w-md mx-auto text-[15px]">
            Customise colours, fonts and backgrounds — globally or per slide.
          </p>
        </div>

        <!-- Scrollable template cards -->
        <div
          class="flex gap-4 overflow-x-auto pb-4 snap-x snap-mandatory -mx-5 px-5 sm:-mx-8 sm:px-8 scrollbar-hide"
        >
          <div
            v-for="tmpl in templateCards"
            :key="tmpl.name"
            class="shrink-0 snap-start w-[160px] sm:w-[185px]"
          >
            <div
              class="rounded-2xl overflow-hidden shadow-md border border-black/[0.07]"
              style="aspect-ratio: 4/5"
              :style="{ background: tmpl.bg }"
            >
              <div
                class="h-full p-5 flex flex-col justify-between"
                :style="{ color: tmpl.text }"
              >
                <div>
                  <div
                    class="w-10 h-1 rounded-full mb-3 opacity-60"
                    :style="{ background: tmpl.accent }"
                  />
                  <div
                    class="text-[11px] font-bold mb-3 opacity-70"
                    :style="{ color: tmpl.accent }"
                  >
                    {{ tmpl.name }}
                  </div>
                  <div
                    class="w-full h-2.5 rounded mb-1.5 opacity-80"
                    :style="{ background: tmpl.text }"
                  />
                  <div
                    class="w-4/5 h-2.5 rounded mb-4 opacity-80"
                    :style="{ background: tmpl.text }"
                  />
                  <div
                    class="w-full h-1.5 rounded mb-1 opacity-35"
                    :style="{ background: tmpl.text }"
                  />
                  <div
                    class="w-full h-1.5 rounded mb-1 opacity-35"
                    :style="{ background: tmpl.text }"
                  />
                  <div
                    class="w-2/3 h-1.5 rounded opacity-35"
                    :style="{ background: tmpl.text }"
                  />
                </div>
                <div
                  class="w-14 h-1.5 rounded opacity-30"
                  :style="{ background: tmpl.accent }"
                />
              </div>
            </div>
            <p class="text-[12px] font-semibold text-[#3a3a3c] mt-2.5 ml-0.5">
              {{ tmpl.name }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── SOURCE TYPES ── -->
    <section class="bg-white py-24 px-5 sm:px-8">
      <div class="max-w-5xl mx-auto">
        <div class="text-center mb-14">
          <p class="text-[#0071e3] text-[11px] font-bold uppercase tracking-[0.2em] mb-3">Input sources</p>
          <h2 class="text-[28px] sm:text-[40px] font-bold tracking-tight text-[#1c1c1e]">
            Works with any content
          </h2>
          <p class="text-[#6e6e73] mt-3 max-w-sm mx-auto text-[15px]">Paste it, link it, or drop it — we handle the rest.</p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div
            v-for="src in sources"
            :key="src.title"
            class="group relative flex flex-col rounded-2xl bg-white border border-black/[0.06] shadow-[0_0_0_1px_rgba(0,0,0,.03),0_2px_4px_rgba(0,0,0,.05),0_12px_24px_rgba(0,0,0,.05)] p-7 transition-shadow duration-300 hover:shadow-[0_0_0_1px_rgba(0,0,0,.06),0_8px_24px_rgba(0,0,0,.09)]"
          >
            <div
              class="w-12 h-12 rounded-2xl mb-5 flex items-center justify-center transition-transform duration-300 group-hover:scale-105"
              :class="src.bg"
            >
              <svg class="w-6 h-6" :class="src.color" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" :d="src.icon" />
              </svg>
            </div>
            <h3 class="font-bold text-[16px] mb-2 text-[#1c1c1e]">{{ src.title }}</h3>
            <p class="text-[13px] text-[#6e6e73] leading-relaxed">{{ src.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── TESTIMONIALS ── -->
    <section class="bg-[#f5f5f7] py-24 px-5 sm:px-8">
      <div class="max-w-6xl mx-auto">

        <!-- Heading -->
        <div class="text-center mb-12">
          <h2 class="text-[28px] sm:text-[40px] font-bold tracking-tight text-[#1c1c1e]">
            Loved by creators
          </h2>
          <div class="flex items-center justify-center gap-1.5 mt-3">
            <svg v-for="i in 5" :key="i" class="w-4 h-4 text-[#ff9500]" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
            <span class="text-[13px] font-semibold text-[#1c1c1e]">4.9</span>
            <span class="text-[13px] text-[#8e8e93]">· 200+ creators</span>
          </div>
        </div>

        <!-- Asymmetric grid: left tall dark hero + right column of 3 -->
        <div class="grid grid-cols-1 lg:grid-cols-5 gap-4">

          <!-- Hero quote — dark card, spans 2 rows on lg -->
          <div class="lg:col-span-2 relative flex flex-col rounded-2xl overflow-hidden p-8" style="background: #1c1c1e; min-height: 28rem">
            <!-- Decorative large quote -->
            <div class="text-[120px] leading-[0.8] font-serif text-white/[0.07] select-none pointer-events-none mb-4">"</div>
            <p class="text-[17px] font-semibold text-white leading-relaxed flex-1 mb-8">
              I used to spend 3 hours making carousels in Canva. Now it takes 5 minutes — the AI nails the structure every time. My engagement went up 40%.
            </p>
            <!-- Stars -->
            <div class="flex gap-1 mb-5">
              <svg v-for="i in 5" :key="i" class="w-4 h-4 text-[#ff9500]" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
            </div>
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-[#0071e3] flex items-center justify-center text-white font-bold text-sm shrink-0">S</div>
              <div>
                <p class="text-[14px] font-bold text-white">Sarah M.</p>
                <p class="text-[12px] text-white/50">Content creator · 42k followers</p>
              </div>
            </div>
          </div>

          <!-- Right column: 3 cards stacked -->
          <div class="lg:col-span-3 flex flex-col gap-4">

            <!-- Quote 2 -->
            <div class="flex flex-col rounded-2xl bg-white border border-black/[0.06] shadow-[0_0_0_1px_rgba(0,0,0,.03),0_2px_4px_rgba(0,0,0,.05),0_12px_24px_rgba(0,0,0,.05)] p-6">
              <div class="flex items-start justify-between gap-4 mb-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-full bg-[#ff9500] flex items-center justify-center text-white font-bold text-sm shrink-0">M</div>
                  <div>
                    <p class="text-[13px] font-bold text-[#1c1c1e]">Marcus T.</p>
                    <p class="text-[11px] text-[#8e8e93]">Brand strategist</p>
                  </div>
                </div>
                <div class="flex gap-0.5 shrink-0 pt-0.5">
                  <svg v-for="i in 5" :key="i" class="w-3 h-3 text-[#ff9500]" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                  </svg>
                </div>
              </div>
              <p class="text-[14px] text-[#3a3a3c] leading-relaxed">
                "The per-slide design controls are incredible. I can make every slide feel on-brand without touching Figma."
              </p>
            </div>

            <!-- Quote 3 -->
            <div class="flex flex-col rounded-2xl bg-white border border-black/[0.06] shadow-[0_0_0_1px_rgba(0,0,0,.03),0_2px_4px_rgba(0,0,0,.05),0_12px_24px_rgba(0,0,0,.05)] p-6">
              <div class="flex items-start justify-between gap-4 mb-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-full bg-[#34c759] flex items-center justify-center text-white font-bold text-sm shrink-0">A</div>
                  <div>
                    <p class="text-[13px] font-bold text-[#1c1c1e]">Aisha K.</p>
                    <p class="text-[11px] text-[#8e8e93]">SaaS founder · LinkedIn Top Voice</p>
                  </div>
                </div>
                <div class="flex gap-0.5 shrink-0 pt-0.5">
                  <svg v-for="i in 5" :key="i" class="w-3 h-3 text-[#ff9500]" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                  </svg>
                </div>
              </div>
              <p class="text-[14px] text-[#3a3a3c] leading-relaxed">
                "Exported a 10-slide carousel as PNGs in under a minute. Pixel-perfect quality. My designer was shocked I made it myself."
              </p>
            </div>

            <!-- Quote 4 -->
            <div class="flex flex-col rounded-2xl bg-white border border-black/[0.06] shadow-[0_0_0_1px_rgba(0,0,0,.03),0_2px_4px_rgba(0,0,0,.05),0_12px_24px_rgba(0,0,0,.05)] p-6">
              <div class="flex items-start justify-between gap-4 mb-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-full bg-[#5856d6] flex items-center justify-center text-white font-bold text-sm shrink-0">J</div>
                  <div>
                    <p class="text-[13px] font-bold text-[#1c1c1e]">James R.</p>
                    <p class="text-[11px] text-[#8e8e93]">Developer advocate · 28k followers</p>
                  </div>
                </div>
                <div class="flex gap-0.5 shrink-0 pt-0.5">
                  <svg v-for="i in 5" :key="i" class="w-3 h-3 text-[#ff9500]" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                  </svg>
                </div>
              </div>
              <p class="text-[14px] text-[#3a3a3c] leading-relaxed">
                "I paste in my blog post URL and get a ready-to-post carousel in minutes. It's my go-to for repurposing content across platforms."
              </p>
            </div>
          </div>
        </div>

        <!-- Stats strip -->
        <div class="mt-4 grid grid-cols-3 divide-x divide-black/[0.06] rounded-2xl bg-white border border-black/[0.06] shadow-[0_0_0_1px_rgba(0,0,0,.03),0_2px_4px_rgba(0,0,0,.05)]">
          <div class="px-3 sm:px-8 py-5 sm:py-6 text-center">
            <p class="text-[24px] sm:text-[32px] font-black text-[#0071e3] tracking-tight leading-none">500+</p>
            <p class="text-[10px] sm:text-[12px] text-[#6e6e73] mt-2 font-medium">carousels created</p>
          </div>
          <div class="px-3 sm:px-8 py-5 sm:py-6 text-center">
            <p class="text-[24px] sm:text-[32px] font-black text-[#ff9500] tracking-tight leading-none">10×</p>
            <p class="text-[10px] sm:text-[12px] text-[#6e6e73] mt-2 font-medium">faster than Canva</p>
          </div>
          <div class="px-3 sm:px-8 py-5 sm:py-6 text-center">
            <p class="text-[24px] sm:text-[32px] font-black text-[#34c759] tracking-tight leading-none">40%</p>
            <p class="text-[10px] sm:text-[12px] text-[#6e6e73] mt-2 font-medium">avg engagement lift</p>
          </div>
        </div>

      </div>
    </section>

    <!-- ── CTA ── -->
    <section class="bg-white py-24 px-5 sm:px-8">
      <div class="max-w-4xl mx-auto">
        <div class="relative rounded-3xl overflow-hidden px-6 sm:px-16 py-12 sm:py-16 text-center" style="background: #0071e3">
          <!-- Subtle radial glow inside -->
          <div class="absolute inset-0 pointer-events-none" style="background: radial-gradient(ellipse at 50% -20%, rgba(255,255,255,0.15) 0%, transparent 70%)" />
          <h2 class="relative text-[26px] sm:text-[44px] font-bold text-white tracking-tight leading-tight mb-4">
            Start creating carousels<br class="hidden sm:block" /> in minutes
          </h2>
          <p class="relative text-[15px] sm:text-[16px] text-white/70 mb-8 sm:mb-10 max-w-md mx-auto">
            Free to use. No design skills required. Your first carousel is one paste away.
          </p>
          <NuxtLink
            to="/register"
            class="relative inline-flex items-center gap-2 bg-white text-[#0071e3] font-bold text-[15px] px-8 py-3.5 rounded-2xl hover:bg-white/90 active:scale-[0.97] transition-all shadow-xl shadow-black/10"
          >
            Get started free
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </NuxtLink>
          <p class="relative text-[12px] text-white/40 mt-4">No credit card required</p>
        </div>
      </div>
    </section>

    <!-- ── FOOTER ── -->
    <footer class="bg-[#f5f5f7] border-t border-black/[0.06] py-10 px-5 sm:px-8">
      <div class="max-w-6xl mx-auto">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6">
          <!-- Brand -->
          <div class="flex items-center gap-2.5">
            <img src="/visible.png" alt="trendsee" class="w-7 h-7 object-contain shrink-0" />
            <div>
              <span class="font-semibold text-[#1B1A25] text-[14px]" style="font-family:'Unbounded',sans-serif;">trendsee</span>
              <p class="text-[11px] text-[#aeaeb2] mt-0.5">© 2025 · Made for creators</p>
            </div>
          </div>

          <!-- Links -->
          <div class="flex items-center gap-6">
            <NuxtLink to="/register" class="text-[13px] text-[#6e6e73] hover:text-[#0071e3] transition-colors font-medium">Get started</NuxtLink>
            <NuxtLink to="/login" class="text-[13px] text-[#6e6e73] hover:text-[#0071e3] transition-colors font-medium">Sign in</NuxtLink>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false })
useHead({ title: "trendsee — AI-powered Instagram carousels" });

const stats = [
  { value: "10×", label: "faster than Canva" },
  { value: "7", label: "pro templates" },
  { value: "3", label: "aspect ratios" },
];

const steps = [
  {
    title: "Add your content",
    desc: "Paste raw text, drop a YouTube URL, or link to any article. No formatting needed — just dump it in.",
    color: "#0071e3",
    icon: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
    tags: ["Plain text", "YouTube URL", "Any link"],
  },
  {
    title: "AI writes the slides",
    desc: "Claude analyses your content and generates a structured set of slides with titles, body copy and a CTA — tuned to your chosen style and language.",
    color: "#5856d6",
    icon: "M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z",
    tags: ["EN / FR / RU", "Up to 12 slides", "Editable"],
  },
  {
    title: "Style it your way",
    desc: "Pick from 7 templates. Adjust colours, fonts, background images and layout — globally or slide by slide.",
    color: "#ff9500",
    icon: "M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z",
    tags: ["7 templates", "Live preview", "Per-slide overrides"],
  },
  {
    title: "Export & post",
    desc: "Hit Export. Get a ZIP of pixel-perfect PNGs ready to upload directly to Instagram, LinkedIn or X.",
    color: "#34c759",
    icon: "M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4",
    tags: ["4:5 · 9:16 · 1:1", "High-res PNG", "ZIP download"],
  },
];

const templateCards = [
  { name: "Minimal", bg: "#ffffff", text: "#1c1c1e", accent: "#1c1c1e" },
  { name: "Bright", bg: "#0071e3", text: "#ffffff", accent: "#ffffff" },
  { name: "Classic", bg: "#1c1c1e", text: "#ffffff", accent: "#5856d6" },
  { name: "Elegant", bg: "#faf7f2", text: "#2c2010", accent: "#c0a060" },
  { name: "Notes", bg: "#fefce8", text: "#1c1c1e", accent: "#d97706" },
  { name: "Comic", bg: "#fef2f2", text: "#1c1c1e", accent: "#ef4444" },
  { name: "Powerful", bg: "#111827", text: "#ffffff", accent: "#f9fafb" },
];

const sources = [
  {
    title: "Plain text",
    desc: "Paste a blog post, article, script or braindump. AI finds the key points.",
    icon: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
    bg: "bg-blue-50",
    color: "text-[#0071e3]",
  },
  {
    title: "YouTube video",
    desc: "Drop in a YouTube URL. We extract the transcript and build slides from it.",
    icon: "M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
    bg: "bg-red-50",
    color: "text-red-500",
  },
  {
    title: "Any URL",
    desc: "Link to any article or page — we scrape and summarise it for you.",
    icon: "M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1",
    bg: "bg-purple-50",
    color: "text-purple-500",
  },
];
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
