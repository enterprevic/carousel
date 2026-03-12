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
  if (!import.meta.client) return // skip during SSR

  const token = localStorage.getItem("auth_token")
  const loggedIn = !!(token && !isTokenExpired(token))

  // Redirect logged-in users away from auth/landing pages to dashboard
  if (loggedIn && (to.path === "/" || to.path === "/login" || to.path === "/register")) {
    return navigateTo("/dashboard")
  }

  // Redirect unauthenticated users away from protected pages
  if (!loggedIn && !PUBLIC_PATHS.includes(to.path)) {
    return navigateTo("/")
  }
})
