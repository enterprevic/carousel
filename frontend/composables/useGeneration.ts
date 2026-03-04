import type { Generation } from "~/types"

export const useGeneration = () => {
  const config = useRuntimeConfig()
  const base = config.public.apiBase

  const startGeneration = async (carouselId: string): Promise<Generation> => {
    return await $fetch<Generation>(`${base}/generations`, {
      method: "POST",
      body: { carousel_id: carouselId },
    })
  }

  const getGeneration = async (id: string): Promise<Generation> => {
    return await $fetch<Generation>(`${base}/generations/${id}`)
  }

  const pollGeneration = (
    id: string,
    onDone: (gen: Generation) => void,
    onFail: (gen: Generation) => void,
    { maxMs = 5 * 60 * 1000 } = {},
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
        const gen = await getGeneration(id)
        if (gen.status === "done") { stop(); onDone(gen); return }
        if (gen.status === "failed") { stop(); onFail(gen); return }
      } catch {
        // network error — keep retrying with backoff
      }

      elapsed += delay
      if (elapsed >= maxMs) { stop(); onFail({ status: "failed" } as Generation); return }

      // exponential backoff: 1s → 2s → 4s → 8s → cap at 10s
      delay = Math.min(delay * 2, 10_000)
      timer = setTimeout(tick, delay)
    }

    timer = setTimeout(tick, delay)
    return stop
  }

  return { startGeneration, getGeneration, pollGeneration }
}
