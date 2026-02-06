import { redirect } from 'next/navigation';
import { cookies } from 'next/headers';

export default async function Home() {
  // Check for session token on the server side
  const allCookies = await cookies();
  const token = allCookies.get('todo_app_token');

  if (token && token.value) {
    redirect('/authenticated/dashboard');
  } else {
    redirect('/signin');
  }
}
