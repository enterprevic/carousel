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

  const pollGeneration = (id: string, onDone: (gen: Generation) => void, onFail: (gen: Generation) => void) => {
    const interval = setInterval(async () => {
      try {
        const gen = await getGeneration(id)
        if (gen.status === "done") {
          clearInterval(interval)
          onDone(gen)
        } else if (gen.status === "failed") {
          clearInterval(interval)
          onFail(gen)
        }
      } catch {
        clearInterval(interval)
      }
    }, 2000)
    return () => clearInterval(interval)
  }

  return { startGeneration, getGeneration, pollGeneration }
}
