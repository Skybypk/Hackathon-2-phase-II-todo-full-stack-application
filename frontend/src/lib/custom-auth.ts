// Remove unused import - Anybody is not a valid export from next/font/google
import { UserRegister, UserLogin, Token, UserResponse } from '../types/auth';

const API_BASE_URLS = [
  process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  'http://127.0.0.1:8000',
  'http://0.0.0.0:8000',
  'http://host.docker.internal:8000', // For Docker environments
];

class CustomAuthService {
  private apiBaseUrl: string | null = null;

  private async getApiUrl(): Promise<string> {
    if (this.apiBaseUrl) {
      return this.apiBaseUrl;
    }

    // Try each possible URL to find which one works
    for (const url of API_BASE_URLS) {
      try {
        // Increase timeout and add better error handling
        const controller = new AbortController();
        const timeoutId = setTimeout(() => {
          controller.abort(new Error('Health check request timeout'));
        }, 20000); // 20 second timeout (increased from 10 seconds)

        try {
          const response = await fetch(`${url}/`, {
            method: 'GET',
            cache: 'no-cache',
            signal: controller.signal,
            headers: {
              'Accept': 'application/json',
              'Cache-Control': 'no-cache'
            }
          });

          clearTimeout(timeoutId);

          if (response.ok) {
            this.apiBaseUrl = url;
            console.log(`Connected to backend at: ${url}`);
            return url;
          }
        } catch (error) {
          // Handle AbortError specifically with more context
          if (error instanceof Error && error.name === 'AbortError') {
            console.warn(`Health check to ${url} timed out or was aborted`);
          } else {
            console.warn(`Failed to connect to ${url}:`, error);
          }
          throw error; // Re-throw to continue to next URL
        }
      } catch (error) {
        // URL didn't work, try the next one
        continue;
      }
    }

    // If none worked, return the primary URL and let the actual API calls handle the error
    this.apiBaseUrl = API_BASE_URLS[0];
    return this.apiBaseUrl;
  }

  private async makeRequest(endpoint: string, options: RequestInit) {
    let lastError: Error | null = null;

    // Try the cached URL first, then try others if that fails
    const urlsToTry = this.apiBaseUrl
      ? [this.apiBaseUrl, ...API_BASE_URLS.filter(url => url !== this.apiBaseUrl)]
      : API_BASE_URLS;

    for (const baseUrl of urlsToTry) {
      try {
        // Retry mechanism for handling initial DB setup delays
        let attempts = 0;
        const maxAttempts = 3;
        let response: Response | null = null;
        let attemptError: Error | null = null;

        while (attempts < maxAttempts) {
          try {
            // Add timeout control for API requests with better error handling
            const controller = new AbortController();
            const timeoutId = setTimeout(() => {
              controller.abort(new Error('Request timeout exceeded'));
            }, 30000); // 30 second timeout (increased from 15 seconds)

            try {
              const enhancedOptions = {
                ...options,
                cache: 'no-cache',
                signal: controller.signal,
                headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json',
                  'Cache-Control': 'no-cache',
                  ...options.headers
                }
              };

              response = await fetch(`${baseUrl}${endpoint}`, enhancedOptions);
              clearTimeout(timeoutId);

              // If we get a response, break out of retry loop
              break;
            } catch (attemptErr) {
              clearTimeout(timeoutId);
              attempts++;
              attemptError = attemptErr as Error;

              // If this was an AbortError, it might be due to initial DB setup delay
              if (attemptErr instanceof Error && attemptErr.name === 'AbortError') {
                console.warn(`Attempt ${attempts} failed due to timeout, retrying in 2 seconds...`);
                await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2 seconds before retry
                continue;
              } else if (attemptErr instanceof Error) {
                // For other errors, check if it's a network issue
                if (attemptErr.message.includes('fetch') || attemptErr.message.includes('network')) {
                  console.warn(`Network error on attempt ${attempts}, retrying...`);
                  await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second before retry
                  continue;
                }
              }

              // If it's not a network/timeout error, don't retry
              break;
            }
          } catch (innerError) {
            attempts++;
            attemptError = innerError as Error;
            break;
          }
        }

        // If we have a response after retries, return it
        if (response) {
          // Update the cached URL if this one works
          if (response.ok) {
            this.apiBaseUrl = baseUrl;
          }

          return response;
        }

        // If we exhausted retries, throw the last error
        if (attemptError) {
          throw attemptError;
        }

      } catch (error) {
        // Handle AbortError specifically with more context
        if (error instanceof Error && error.name === 'AbortError') {
          lastError = new Error(`Request to ${baseUrl}${endpoint} timed out or was aborted`);
        } else {
          lastError = error as Error;
        }

        console.warn(`Failed to connect to ${baseUrl}, trying next URL...`, lastError);
        continue;
      }
    }

    // If all URLs failed, throw the last error
    if (lastError) {
      throw lastError;
    } else {
      throw new Error('No backend URLs available');
    }
  }

  async register(userData: UserRegister): Promise<UserResponse> {
    try {
      const response = await this.makeRequest('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      console.log('Register response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text().catch(() => `HTTP error ${response.status}`);
        let errorData;
        try {
          // Try to parse as JSON first
          errorData = JSON.parse(errorText);
        } catch {
          // If not JSON, use the raw text
          errorData = { detail: errorText };
        }

        console.error('Registration error response:', errorData);
        throw new Error(errorData.detail || `Registration failed: ${response.status} ${response.statusText}`);
      }

      const result = await response.json();
      console.log('Registration successful, received data:', result);
      return result;
    } catch (error) {
      console.error('Registration error caught:', error);
      if (error instanceof TypeError && (error.message.toLowerCase().includes('fetch') || error.message.toLowerCase().includes('network'))) {
        throw new Error('Failed to connect to the server. Please make sure the backend is running and accessible.');
      }
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          throw new Error('Request timeout exceeded. The server may be busy or not responding.');
        }
        throw error;
      }
      throw new Error('An unexpected error occurred during registration');
    }
  }

  async login(credentials: UserLogin): Promise<Token> {
    try {
      const response = await this.makeRequest('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      // Log the response for debugging
      console.log('Login response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text().catch(() => `HTTP error ${response.status}`);
        let errorData;
        try {
          // Try to parse as JSON first
          errorData = JSON.parse(errorText);
        } catch {
          // If not JSON, use the raw text
          errorData = { detail: errorText };
        }

        console.error('Login error response:', errorData);
        throw new Error(errorData.detail || `Login failed: ${response.status} ${response.statusText}`);
      }

      const result = await response.json();
      console.log('Login successful, received data:', result);
      return result;
    } catch (error) {
      console.error('Login error caught:', error);
      if (error instanceof TypeError && (error.message.toLowerCase().includes('fetch') || error.message.toLowerCase().includes('network'))) {
        throw new Error('Failed to connect to the server. Please make sure the backend is running and accessible.');
      }
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          throw new Error('Request timeout exceeded. The server may be busy or not responding.');
        }
        throw error;
      }
      throw new Error('An unexpected error occurred during login');
    }
  }

  async getCurrentUser(token: string): Promise<UserResponse> {
    try {
      const response = await this.makeRequest('/api/auth/me', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to get user: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Get user error:', error);
      if (error instanceof TypeError && (error.message.includes('fetch') || error.message.includes('network'))) {
        throw new Error('Failed to connect to the server. Please make sure the backend is running and accessible.');
      }
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('An unexpected error occurred while fetching user data');
    }
  }

  async testConnection(): Promise<boolean> {
    try {
      const apiUrl = await this.getApiUrl();
      const controller = new AbortController();
      let timeoutId: NodeJS.Timeout | null = null;

      try {
        timeoutId = setTimeout(() => controller.abort(new Error('Connection test timeout exceeded')), 10000); // 10 second timeout

        const response = await fetch(`${apiUrl}/health`, {
          method: 'GET',
          cache: 'no-cache',
          signal: controller.signal
        });

        clearTimeout(timeoutId);
        return response.ok;
      } catch (error) {
        if (timeoutId) clearTimeout(timeoutId);
        throw error;
      }
    } catch (error) {
      console.error('Connection test failed:', error);
      return false;
    }
  }
}

export const customAuth = new CustomAuthService(); 