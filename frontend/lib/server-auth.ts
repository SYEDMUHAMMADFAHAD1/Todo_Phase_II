import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

// Server-side session checker
export async function getServerSession() {
  const cookieStore = await cookies();
  const token = cookieStore.get('todo_app_token')?.value;

  if (!token) {
    return null;
  }

  // Optionally verify token with backend
  try {
    // Using the global fetch available in Next.js server components
    const response = await fetch(`${process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:8000'}/api/auth/session`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      cache: 'no-store' // Prevent caching of session data
    });

    if (response.ok) {
      return await response.json();
    }
    return null;
  } catch (error) {
    console.error('Session verification failed:', error);
    return null;
  }
}

export async function requireAuth(redirectPath = '/signin') {
  const session = await getServerSession();
  if (!session) {
    redirect(redirectPath);
  }
  return session;
}