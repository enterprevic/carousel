import type { Export } from "~/types"

export const useExport = () => {
  const config = useRuntimeConfig()
  const base = config.public.apiBase

  const startExport = async (carouselId: string): Promise<Export> => {
    return await $fetch<Export>(`${base}/exports`, {
      method: "POST",
      body: { carousel_id: carouselId },
    })
  }

  const getExport = async (id: string): Promise<Export> => {
    return await $fetch<Export>(`${base}/exports/${id}`)
  }

  const pollExport = (
    id: string,
    onDone: (exp: Export) => void,
    onFail: (exp?: Export) => void,
    { maxMs = 10 * 60 * 1000 } = {},
  ) => {
    let delay = 1000
    let elapsed = 0
    let timer: ReturnType<typeof setTimeout> | null = null
    let stopped = false

    const stop = () => {
      stopped = true
      if (timer) clearTimeout(timer)
    }

    const tick = async () => {
      if (stopped) return
      try {
        const exp = await getExport(id)
        if (exp.status === "done") { stop(); onDone(exp); return }
        if (exp.status === "failed") { stop(); onFail(exp); return }
      } catch {
        // network error — keep retrying with backoff
      }

      elapsed += delay
      if (elapsed >= maxMs) { stop(); onFail(); return } // timed out

      // exponential backoff: 1s → 2s → 4s → 8s → cap at 10s
      delay = Math.min(delay * 2, 10_000)
      timer = setTimeout(tick, delay)
    }

    timer = setTimeout(tick, delay)
    return stop
  }

  return { startExport, getExport, pollExport }
}
