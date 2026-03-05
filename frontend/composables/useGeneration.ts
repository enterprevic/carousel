import type { Generation } from "~/types"

export const useGeneration = () => {
  const config = useRuntimeConfig()
  const base = config.public.apiBase
  const { authHeaders, getToken } = useAuth()

  const startGeneration = async (carouselId: string): Promise<Generation> => {
    return await $fetch<Generation>(`${base}/generations`, {
      method: "POST",
      body: { carousel_id: carouselId },
      headers: authHeaders(),
    })
  }

  const getGeneration = async (id: string): Promise<Generation> => {
    return await $fetch<Generation>(`${base}/generations/${id}`, { headers: authHeaders() })
  }

  /**
   * Watch a generation via SSE, with polling fallback.
   * Returns a stop() function.
   */
  const watchGeneration = (
    id: string,
    onDone: (gen: Generation) => void,
    onFail: (gen: Generation) => void,
    { maxMs = 5 * 60 * 1000 } = {},
  ): (() => void) => {
    let stopped = false
    let es: EventSource | null = null
    let fallbackTimer: ReturnType<typeof setTimeout> | null = null

    const stop = () => {
      stopped = true
      es?.close()
      if (fallbackTimer) clearTimeout(fallbackTimer)
    }

    const startPolling = () => {
      let delay = 1000
      let elapsed = 0
      const tick = async () => {
        if (stopped) return
        try {
          const gen = await getGeneration(id)
          if (gen.status === "done") { stop(); onDone(gen); return }
          if (gen.status === "failed") { stop(); onFail(gen); return }
        } catch { /* retry */ }
        elapsed += delay
        if (elapsed >= maxMs) { stop(); onFail({ status: "failed" } as Generation); return }
        delay = Math.min(delay * 2, 10_000)
        fallbackTimer = setTimeout(tick, delay)
      }
      fallbackTimer = setTimeout(tick, 1000)
    }

    // SSE — auth via ?token= query param since EventSource doesn't support custom headers
    const token = getToken()
    const sseUrl = `${base}/generations/${id}/stream${token ? `?token=${encodeURIComponent(token)}` : ""}`
    try {
      es = new EventSource(sseUrl)
      const connectTimeout = setTimeout(() => { es?.close(); if (!stopped) startPolling() }, 4000)

      es.addEventListener("status", (e: MessageEvent) => {
        clearTimeout(connectTimeout)
        try {
          const data = JSON.parse(e.data) as { status: string }
          if (data.status === "done" || data.status === "failed") {
            getGeneration(id).then((gen) => {
              stop()
              data.status === "done" ? onDone(gen) : onFail(gen)
            }).catch(() => { stop(); onFail({ status: data.status } as Generation) })
          }
        } catch { /* ignore */ }
      })

      es.onerror = () => { clearTimeout(connectTimeout); es?.close(); if (!stopped) startPolling() }
    } catch {
      startPolling()
    }

    return stop
  }

  const pollGeneration = watchGeneration

  return { startGeneration, getGeneration, watchGeneration, pollGeneration }
}
