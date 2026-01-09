'use client'

/**
 * Email verification page
 */

import { useEffect, useState } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { api } from '@/lib/api-client'
import Link from 'next/link'

export default function VerifyEmailPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading')
  const [message, setMessage] = useState('')

  useEffect(() => {
    const token = searchParams.get('token')
    
    if (!token) {
      setStatus('error')
      setMessage('No verification token provided')
      return
    }

    const verifyEmail = async () => {
      try {
        await api.auth.verifyEmail(token)
        setStatus('success')
        setMessage('Email verified successfully! You can now log in.')
      } catch (error: any) {
        setStatus('error')
        setMessage(
          error.message || 'Verification failed. The token may be invalid or expired.'
        )
      }
    }

    verifyEmail()
  }, [searchParams])

  return (
    <div className="min-h-screen flex items-center justify-center bg-black py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full bg-white rounded-lg shadow-xl p-8 space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Email Verification
          </h2>
        </div>

        <div className="mt-8">
          {status === 'loading' && (
            <div className="rounded-md bg-blue-50 p-4 border border-blue-200">
              <div className="text-sm text-blue-800">Verifying your email...</div>
            </div>
          )}

          {status === 'success' && (
            <div className="rounded-md bg-green-50 p-4 border border-green-200">
              <h3 className="text-lg font-semibold text-green-800 mb-2">
                Success!
              </h3>
              <p className="text-sm text-green-700 mb-4">{message}</p>
              <Link
                href="/login"
                className="inline-block px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 text-sm font-medium"
              >
                Go to Login
              </Link>
            </div>
          )}

          {status === 'error' && (
            <div className="rounded-md bg-red-50 p-4 border border-red-200">
              <h3 className="text-lg font-semibold text-red-800 mb-2">
                Verification Failed
              </h3>
              <p className="text-sm text-red-700 mb-4">{message}</p>
              <div className="space-y-2">
                <Link
                  href="/register"
                  className="block text-sm font-medium text-red-600 hover:text-red-500"
                >
                  Register again →
                </Link>
                <Link
                  href="/login"
                  className="block text-sm font-medium text-red-600 hover:text-red-500"
                >
                  Go to Login →
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
