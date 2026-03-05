const PUBLIC_PATHS = ["/", "/login", "/register"]

export default defineNuxtRouteMiddleware(async (to) => {
  if (PUBLIC_PATHS.includes(to.path)) return
  if (!import.meta.client) return // skip during SSR

  const config = useRuntimeConfig()
  const base = config.public.apiBase
  const token = localStorage.getItem("auth_token")

  if (!token) return navigateTo("/")

  try {
    await $fetch(`${base}/auth/verify?token=${encodeURIComponent(token)}`)
    // ok — proceed
  } catch {
    return navigateTo("/")
  }
})
