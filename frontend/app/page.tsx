'use client'

import { useAuth } from '@/context/AuthContext'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import Link from 'next/link'

export default function Home() {
  const { user, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && user) {
      router.push('/dashboard')
    }
  }, [user, loading, router])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    )
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-black">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <div className="bg-white rounded-lg shadow-xl p-12">
          <h1 className="text-4xl font-bold text-center mb-8 text-gray-900">
            Alumni Connect
          </h1>
          <p className="text-center text-gray-600 mb-8">
            Career navigation and warm-introduction platform
          </p>
          <div className="flex justify-center space-x-4">
            <Link
              href="/login"
              className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium"
            >
              Sign In
            </Link>
            <Link
              href="/register"
              className="px-6 py-3 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 font-medium"
            >
              Sign Up
            </Link>
          </div>
        </div>
      </div>
    </main>
  )
}
