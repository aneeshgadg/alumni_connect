/**
 * Authentication types
 */

export type UserRole = 'student' | 'alumni'

export interface User {
  id: string
  email: string
  role: UserRole
  email_verified: boolean
  created_at: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface LoginResponse extends AuthTokens {
  user: User
}

export interface RegisterData {
  email: string
  password: string
  role: UserRole
  university_id: string
}

export interface LoginData {
  email: string
  password: string
}
