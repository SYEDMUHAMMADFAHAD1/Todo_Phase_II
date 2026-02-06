import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/auth';

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Define public routes that don't require authentication
  // Note: /signin and /signup are served from (auth) route group but accessible at /<path>
  const publicRoutes = ['/', '/signin', '/signup', '/health'];
  const isPublicRoute = publicRoutes.some(route => pathname === route);

  // Skip middleware for public routes
  if (isPublicRoute) {
    return NextResponse.next();
  }

  // Protected routes - require authentication
  try {
    const session = await getSession();

    if (!session || !session.user) {
      // Redirect to signin page if not authenticated
      const redirectUrl = new URL('/signin', request.url);
      redirectUrl.searchParams.set('redirect', pathname);
      return NextResponse.redirect(redirectUrl);
    }

    // Add user info to headers for backend API calls
    const requestHeaders = new Headers(request.headers);
    if (session.user) {
      requestHeaders.set('x-user-id', session.user.id);
      requestHeaders.set('x-user-email', session.user.email || '');
    }

    return NextResponse.next({
      request: {
        headers: requestHeaders,
      },
    });
  } catch (error) {
    // Auth check failed, redirect to signin
    const redirectUrl = new URL('/signin', request.url);
    redirectUrl.searchParams.set('error', 'session_expired');
    return NextResponse.redirect(redirectUrl);
  }
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!api|_next/static|_next/image|favicon.ico|public).*)',
  ],
};