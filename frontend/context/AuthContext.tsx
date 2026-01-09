'use client'

/**
 * Authentication context for managing user auth state
 */

import React, { createContext, useContext, useEffect, useState } from 'react'
import { User, LoginData, RegisterData } from '@/types/auth'
import { api } from '@/lib/api-client'

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (data: LoginData) => Promise<void>
  register: (data: RegisterData) => Promise<void>
  logout: () => void
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  // Check if user is logged in on mount
  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (token) {
        const userData = await api.auth.getCurrentUser()
        setUser(userData)
      }
    } catch (error) {
      // Not authenticated or token expired
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    } finally {
      setLoading(false)
    }
  }

  const login = async (data: LoginData) => {
    const response = await api.auth.login(data)
    setUser(response.user)
  }

  const register = async (data: RegisterData) => {
    await api.auth.register(data)
    // After registration, user needs to verify email before logging in
  }

  const logout = async () => {
    await api.auth.logout()
    setUser(null)
  }

  const refreshUser = async () => {
    try {
      const userData = await api.auth.getCurrentUser()
      setUser(userData)
    } catch (error) {
      setUser(null)
    }
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
