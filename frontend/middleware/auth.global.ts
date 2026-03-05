const PUBLIC_PATHS = ["/", "/login", "/register"]

function isTokenExpired(token: string): boolean {
  try {
    const payload = JSON.parse(atob(token.split(".")[1]))
    return typeof payload.exp === "number" && payload.exp * 1000 < Date.now()
  } catch {
    return true
  }
}

export default defineNuxtRouteMiddleware((to) => {
  if (PUBLIC_PATHS.includes(to.path)) return
  if (!import.meta.client) return // skip during SSR

  const token = localStorage.getItem("auth_token")
  if (!token || isTokenExpired(token)) return navigateTo("/")
})
