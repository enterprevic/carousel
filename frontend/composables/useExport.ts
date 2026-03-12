import type { Export } from "~/types"

export const useExport = () => {
  const config = useRuntimeConfig()
  const base = config.public.apiBase
  const { authHeaders, getToken } = useAuth()

  const getLatestExport = async (carouselId: string): Promise<Export | null> => {
    try {
      return await $fetch<Export | null>(`${base}/exports?carousel_id=${carouselId}`, { headers: authHeaders() })
    } catch {
      return null
    }
  }

  const startExport = async (carouselId: string): Promise<Export> => {
    return await $fetch<Export>(`${base}/exports`, {
      method: "POST",
      body: { carousel_id: carouselId },
      headers: authHeaders(),
    })
  }

  const getExport = async (id: string): Promise<Export> => {
    return await $fetch<Export>(`${base}/exports/${id}`, { headers: authHeaders() })
  }

  /**
   * Watch an export via SSE, with polling fallback.
   * Returns a stop() function.
   */
  const watchExport = (
    id: string,
    onDone: (exp: Export) => void,
    onFail: (exp?: Export) => void,
    { maxMs = 10 * 60 * 1000 } = {},
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
          const exp = await getExport(id)
          if (exp.status === "done") { stop(); onDone(exp); return }
          if (exp.status === "failed") { stop(); onFail(exp); return }
        } catch { /* retry */ }
        elapsed += delay
        if (elapsed >= maxMs) { stop(); onFail(); return }
        delay = Math.min(delay * 2, 10_000)
        fallbackTimer = setTimeout(tick, delay)
      }
      fallbackTimer = setTimeout(tick, 1000)
    }

    // SSE — auth via ?token= query param since EventSource doesn't support custom headers
    const token = getToken()
    const sseUrl = `${base}/exports/${id}/stream${token ? `?token=${encodeURIComponent(token)}` : ""}`
    try {
      es = new EventSource(sseUrl)
      const connectTimeout = setTimeout(() => { es?.close(); if (!stopped) startPolling() }, 4000)

      es.addEventListener("status", (e: MessageEvent) => {
        clearTimeout(connectTimeout)
        try {
          const data = JSON.parse(e.data) as { status: string }
          if (data.status === "done" || data.status === "failed") {
            getExport(id).then((exp) => {
              stop()
              data.status === "done" ? onDone(exp) : onFail(exp)
            }).catch(() => { stop(); onFail() })
          }
        } catch { /* ignore */ }
      })

      es.onerror = () => { clearTimeout(connectTimeout); es?.close(); if (!stopped) startPolling() }
    } catch {
      startPolling()
    }

    return stop
  }

  const pollExport = watchExport

  return { getLatestExport, startExport, getExport, watchExport, pollExport }
}
