/**
 * Next.js API Route: /api/auth/logout
 * Handles logout (mainly client-side token removal)
 */

import { NextResponse } from 'next/server'

export async function POST() {
  // Logout is primarily client-side (removing tokens)
  // Could add server-side session invalidation here if needed
  return NextResponse.json({ message: 'Logged out successfully' })
}
