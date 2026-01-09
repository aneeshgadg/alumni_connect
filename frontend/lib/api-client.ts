/**
 * Frontend API client - calls Next.js API routes (not FastAPI directly)
 * This keeps backend URL and credentials server-side
 */

// Client-side API functions that call Next.js API routes
export const api = {
  // Auth endpoints
  auth: {
    register: async (data: {
      email: string
      password: string
      role: 'student' | 'alumni'
      university_id: string
    }) => {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Registration failed')
      }
      return response.json()
    },

    login: async (data: { email: string; password: string }) => {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Login failed')
      }
      const result = await response.json()
      // Store tokens in localStorage (handled by Next.js API route)
      if (result.access_token) {
        localStorage.setItem('access_token', result.access_token)
        localStorage.setItem('refresh_token', result.refresh_token)
      }
      return result
    },

    logout: async () => {
      await fetch('/api/auth/logout', { method: 'POST' })
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },

    getCurrentUser: async () => {
      const response = await fetch('/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      })
      if (!response.ok) {
        throw new Error('Not authenticated')
      }
      return response.json()
    },

    verifyEmail: async (token: string) => {
      const response = await fetch(`/api/auth/verify-email?token=${token}`, {
        method: 'POST',
      })
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Verification failed')
      }
      return response.json()
    },
  },
}
