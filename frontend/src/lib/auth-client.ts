import { createAuthClient } from 'better-auth/client';

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3000',
  fetchOptions: {
    // This will ensure that the authorization header is included in requests
    credentials: 'include'
  }
});

// Export common auth functions
export const { signIn, signOut, useSession } = authClient;